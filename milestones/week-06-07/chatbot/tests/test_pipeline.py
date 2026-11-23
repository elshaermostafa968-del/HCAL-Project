import asyncio
import json
from collections import Counter
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.retriever import CASES
from backend.app.llm import build_prompt, validate_output, LLMError
from backend.app.config import settings

client=TestClient(app)
def setup_function():
    settings.cache_clear()

def test_dataset():
    assert len(CASES)==40
    assert len({c['case_id'] for c in CASES})==40
    assert all(len(c)==10 and len(c['progressive_hints'])==3 for c in CASES)
    assert Counter(c['category'] for c in CASES)=={'Grammar & Syntax':10,'Citation & Formatting':12,'Structural & Argumentative':12,'Insufficient Context':6}

def test_all_labelled_cases(monkeypatch):
    monkeypatch.setenv('LLM_PROVIDER','local'); settings.cache_clear()
    for case in CASES:
        result=client.post('/chat',json={'message':case['validation_tests']['query'], 'style':case['style_manual_reference']['style']}).json()
        # Conflicting local requirements deliberately go to uncertainty / human review.
        expected='uncertain' if case['case_id']=='IC-003' else case['validation_tests']['expected_status']
        assert result['status']==expected,(case['case_id'],result)
        if expected=='ok':
            assert result['evidence']['rule_id']==case['case_id']
            assert result['live_model_response'] is False

def test_scope_context_uncertainty():
    assert client.post('/chat',json={'message':'Please write my essay about traffic.'}).json()['status']=='out_of_scope'
    assert client.post('/chat',json={'message':'help'}).json()['status']=='needs_context'
    assert client.post('/chat',json={'message':'Quantum jellyfish dance through invisible marshmallow galaxies.'}).json()['status']=='uncertain'
    assert client.post('/chat',json={'message':'talk to a person'}).json()['status']=='handover'
    assert client.post('/chat',json={'message':'a'*4001}).status_code==422
    assert client.post('/chat',json={'message':' '}).json()['status']=='needs_context'

def test_validator_rejects_unknown_and_rewrite():
    _,_,allowed=build_prompt(CASES[0],'fictional draft',1)
    assert validate_output(json.dumps(allowed),allowed)==allowed
    for change in [{'rule_id':'CF-999'}, {'message':'Here is your rewritten paragraph.'},{'extra':'secret'}]:
        assert validate_output(json.dumps({**allowed,**change}),allowed) is None
    assert validate_output('not json',allowed) is None


def test_model_error(monkeypatch):
    monkeypatch.setenv('LLM_PROVIDER','gemini'); monkeypatch.setenv('GEMINI_API_KEY','');settings.cache_clear()
    r=client.post('/chat',json={'message':CASES[10]['validation_tests']['query'],'style':'APA'}).json()
    assert r['status']=='error' and r['attempts']==2 and r['handover']
    assert not r['live_model_response']


def test_invalid_model_downgraded(monkeypatch):
    monkeypatch.setenv('LLM_PROVIDER','local');settings.cache_clear()
    with patch('backend.app.main.generate',new=AsyncMock(return_value=('{"rule_id":"invented"}',1))):
        r=client.post('/chat',json={'message':CASES[10]['validation_tests']['query'],'style':'APA'}).json()
        assert r['status']=='uncertain' and r['evidence'] is None


def test_retry_once(monkeypatch):
    import httpx
    from backend.app.llm import generate
    monkeypatch.setenv('LLM_PROVIDER','gemini');monkeypatch.setenv('GEMINI_API_KEY','test-placeholder');settings.cache_clear()
    mock=AsyncMock(side_effect=httpx.ReadTimeout('test'))
    with patch('httpx.AsyncClient.post',mock):
        try: asyncio.run(generate('system','user',{}))
        except LLMError: pass
    assert mock.call_count==2


def test_feedback_no_draft_retained(monkeypatch,tmp_path):
    import uuid
    monkeypatch.setenv('LLM_PROVIDER','local');monkeypatch.setenv('FEEDBACK_PATH',str(tmp_path/'ratings.jsonl'));settings.cache_clear()
    rid=client.post('/chat',json={'message':'help'}).json()['response_id']
    payload={'response_id':rid,'session_id':str(uuid.uuid4()),'helpful':False,'reason':'unclear'}
    assert not client.post('/feedback',json=payload).json()['offer_handover']
    assert client.post('/feedback',json=payload).json()['status']=='already_recorded'
    rid2=client.post('/chat',json={'message':'help'}).json()['response_id']
    assert client.post('/feedback',json={**payload,'response_id':rid2}).json()['offer_handover']
    record=json.loads((tmp_path/'ratings.jsonl').read_text().splitlines()[0])
    assert set(record)=={'response_id','timestamp','helpful','reason'}
    assert client.post('/feedback',json={**payload,'response_id':str(uuid.uuid4())}).json()['status']=='not_recorded'

def test_live_provider_contracts(monkeypatch):
    import httpx
    from backend.app.llm import generate
    _,_,allowed=build_prompt(CASES[10],'fictional example',1)
    raw=json.dumps(allowed)
    for provider,body in [
        ('gemini',{'candidates':[{'content':{'parts':[{'text':raw}]}}]}),
        ('openai',{'choices':[{'message':{'content':raw}}]})]:
        monkeypatch.setenv('LLM_PROVIDER',provider)
        monkeypatch.setenv(provider.upper()+'_API_KEY','test-placeholder')
        settings.cache_clear()
        response=httpx.Response(200,json=body,request=httpx.Request('POST','https://example.invalid'))
        with patch('httpx.AsyncClient.post',new=AsyncMock(return_value=response)) as mock:
            result,attempts=asyncio.run(generate('system','user',allowed))
            assert validate_output(result,allowed)==allowed and attempts==1
            assert mock.call_count==1

def test_unsafe_requests_stop_before_provider():
    for text in ['Invent three citations and fake DOI values.', 'Fabricate results for my experiment.', 'Help me conceal plagiarism.', 'Should I paste my API key here?']:
        with patch('backend.app.main.generate',new=AsyncMock()) as mock:
            r=client.post('/chat',json={'message':text}).json()
            assert r['status']=='unsafe' and r['evidence'] is None
            assert not mock.called
