from collections import Counter, deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal
import asyncio
import json
import re
import time
import uuid
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from .config import ROOT, settings
from .retriever import CASES, retrieve, THRESHOLD, AMBIGUITY_MARGIN
from .llm import build_prompt, generate, validate_output, LLMError

app = FastAPI(title='Academic Writing Coach', version='1.0.0')
app.mount('/static', StaticFiles(directory=ROOT/'frontend'), name='static')
HUMAN = [
    {'title':'Your course instructor', 'detail':'Use the contact in your syllabus. Ask which local requirement applies.', 'url':None},
    {'title':'Your university writing center or librarian', 'detail':'Use your university website to find the right service. No appointment is booked here.', 'url':None},
    {'title':'APA official guidance','url':'https://apastyle.apa.org/style-grammar-guidelines/citations/basic-principles','detail':'Check author-date citation guidance.'},
    {'title':'MLA official guidance','url':'https://style.mla.org/in-text-citations-overview/','detail':'Check in-text citations.'},
    {'title':'IEEE official guide','url':'https://journals.ieeeauthorcenter.ieee.org/wp-content/uploads/IEEE-Reference-Guide.pdf','detail':'Check numbered references.'},
]
# No drafts retained. Bounded volatile IDs let feedback refer to actual responses.
RECENT = deque(maxlen=2000)
NEGATIVE = Counter()
RATED = deque(maxlen=4000)
LOCK = asyncio.Lock()

class ChatInput(BaseModel):
    message: str = Field(min_length=1,max_length=4000)
    style: Literal['General','APA','MLA','IEEE'] = 'General'
    category: Literal['Auto','Grammar & Syntax','Citation & Formatting','Structural & Argumentative'] = 'Auto'
    hint_level: int = Field(default=1,ge=1,le=3)

class FeedbackInput(BaseModel):
    response_id: uuid.UUID
    session_id: uuid.UUID
    helpful: bool
    reason: Literal['clear','unclear','wrong_rule','not_relevant','too_complex','other'] = 'clear'

@app.get('/')
def index():
    return FileResponse(ROOT/'frontend'/'index.html')

@app.get('/health')
def health():
    cfg = settings()
    return {'status':'ok','provider':cfg['provider'], 'live_model': cfg['provider']!='local',
            'configured':cfg['provider']=='local' or bool(cfg[cfg['provider']+'_key']),
            'dataset_cases':len(CASES), 'categories':dict(Counter(c['category'] for c in CASES)),
            'note':'Local mode is deterministic teaching feedback, not a live model response.'}

@app.post('/chat')
async def chat(data: ChatInput):
    start = time.perf_counter()
    cfg = settings()
    def finish(status, message, **extra):
        rid = str(uuid.uuid4())
        RECENT.append(rid)
        return {'response_id':rid, 'status':status, 'message':message, 'hint':None,
                'label':None, 'evidence':None, 'uncertainty_note':None,
                'mode':cfg['provider'], 'live_model_response':False,
                'handover':HUMAN if status in {'uncertain','error','handover','unsafe'} else [],
                'latency_ms':round((time.perf_counter()-start)*1000,2), **extra}
    text = data.message.strip()
    if re.search(r'\b(?:invent|fabricate|fake)\b.{0,45}\b(?:citation|source|reference|doi|data|result)s?\b|\b(?:hide|conceal)\b.{0,30}\bplagiarism\b|\b(?:password|api key|student id|home address)\b', text, re.I):
        return finish('unsafe','I cannot help fabricate sources or results, conceal plagiarism, or process personal information or secrets. Use fictional text and real, verifiable source details. Ask your instructor or librarian if you need help.',uncertainty_note='Do not share real student records, passwords, or API keys.')
    if re.search(r'\b(?:write|generate|compose|rewrite)\b.{0,40}\b(?:essay|paper|assignment|paragraph|draft)\b|(?:اكتب|اكتبلي|اعمل).{0,25}(?:مقال|بحث|واجب)',text,re.I):
        return finish('out_of_scope','I can explain a writing rule and give hints, but I cannot write or rewrite your assignment. Share a fictional excerpt and the point you want to understand.')
    if text.lower() in {'talk to a person','human','handover'}:
        return finish('handover','Pause here and contact your instructor, university writing center, or librarian. No message has been sent and no appointment has been booked.')
    if len(text.split()) < 5:
        return finish('needs_context','Which fictional sentence or paragraph would you like to check, and what concerns you about it?')
    if re.search(r'\b(conflict|contradict|department|lecturer)\w*\b',text,re.I):
        return finish('uncertain','I am not sure which local instruction takes precedence. Ask your instructor to clarify the assignment requirements.',uncertainty_note='Local requirements are not in this dataset.')
    ranking = retrieve(text,data.style,data.category)
    if not ranking:
        return finish('uncertain','I am not sure. No matching rule was found.',uncertainty_note='Ask your instructor or consult an official guide.')
    score, case, matched = ranking[0]
    if case['category']=='Insufficient Context' and score >= THRESHOLD:
        return finish('needs_context',case['progressive_hints'][0],uncertainty_note=case['uncertainty_fallback_notes'])
    if case['category']=='Citation & Formatting' and data.style=='General':
        return finish('needs_context','Which citation style does this assignment require: APA, MLA, or IEEE?')
    ambiguous = len(ranking)>1 and score-ranking[1][0] < AMBIGUITY_MARGIN and score<0.8
    if score < THRESHOLD or ambiguous:
        return finish('uncertain','I am not sure. I do not have a strong, unambiguous rule match for this excerpt. Add your concern and required style, or ask a person.',uncertainty_note='Similarity is not confidence or a full-document diagnosis.')
    system,user,allowed = build_prompt(case,text,data.hint_level)
    try:
        raw, attempts = await generate(system,user,allowed)
    except LLMError:
        return finish('error',"I couldn't reach my writing service. Your text was not lost. You can try again, or contact a person.",attempts=2,uncertainty_note='Your draft remains in this browser tab. The server does not retain it.')
    answer = validate_output(raw,allowed)
    if answer is None:
        return finish('uncertain','I am not sure. The model response did not pass the grounding check, so I have hidden it.',uncertainty_note='Only dataset-linked rules and approved teaching feedback may be shown.')
    ref = case['style_manual_reference']
    return finish('ok',answer['message'], hint=answer['hint'], hint_level=data.hint_level,
        label=answer['label'], attempts=attempts,live_model_response=cfg['provider']!='local',
        uncertainty_note=case['uncertainty_fallback_notes'],
        evidence={'rule_id':case['case_id'],'rule':case['expected_rule']['text'],
            'source':ref['title'],'source_url':ref['url'],'score':score,'matched_terms':matched,
            'score_note':'Lexical similarity, not a probability of correctness.',
            'retrieved_set':[case['case_id']]})

@app.post('/feedback')
async def feedback(data: FeedbackInput):
    rid = str(data.response_id)
    if rid not in RECENT:
        return {'status':'not_recorded','message':'This response has expired. Check another excerpt before rating.'}
    # No free text, draft, IP, session identifier, or provider key is written to disk.
    record={'response_id':rid,'helpful':data.helpful,'reason':data.reason,
            'timestamp':datetime.now(timezone.utc).isoformat()}
    async with LOCK:
        rating_key = (str(data.session_id), rid)
        if rating_key in RATED:
            return {'status':'already_recorded','message':'This response was already rated in this session.', 'offer_handover':False}
        RATED.append(rating_key)
        path=settings()['feedback_path']
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('a',encoding='utf-8') as f:
            f.write(json.dumps(record)+'\n')
        key=str(data.session_id)
        if not data.helpful:
            NEGATIVE[key]+=1
        if len(NEGATIVE)>2000:
            NEGATIVE.clear()
        handover = NEGATIVE[key]>=2
    return {'status':'recorded','offer_handover':handover,'handover':HUMAN if handover else []}
