"""Small, transparent lexical retriever. Scores are similarity, NOT probability."""
import json
import math
import re
from collections import Counter
from .config import ROOT

CASES = json.loads((ROOT / 'academic_guidelines_dataset.json').read_text())
STOP = set('a an the is are was were in on at of to for and or my this that with it i please check can you'.split())

def tokens(text):
    return set(re.findall(r'[a-z0-9]+', text.lower())) - STOP

DOCUMENTS = [tokens(c['observed_issue'] + ' ' + c['student_draft_snippet']) for c in CASES]
DF = Counter(t for d in DOCUMENTS for t in d)
IDF = {t: math.log((len(CASES)+1)/(n+1))+1 for t,n in DF.items()}

def retrieve(message, style='General', category='Auto'):
    query = tokens(message)
    ranked = []
    for case, document in zip(CASES, DOCUMENTS):
        ref_style = case['style_manual_reference']['style']
        if ref_style not in {'General', style} and style != 'General':
            continue
        if category != 'Auto' and case['category'] != category and not case['case_id'].startswith('IC'):
            continue
        overlap = query & document
        numerator = sum(IDF.get(t, 1)**2 for t in overlap)
        denominator = math.sqrt(sum(IDF.get(t,1)**2 for t in query)*sum(IDF.get(t,1)**2 for t in document))
        score = numerator / denominator if denominator else 0
        # A full fixture match is strong evidence only of the fixture, never of general correctness.
        if case['student_draft_snippet'].lower() in message.lower():
            score = max(score, 0.85)
        ranked.append((round(min(score,1),3),case,sorted(overlap)))
    ranked.sort(key=lambda row: row[0], reverse=True)
    return ranked

THRESHOLD = 0.24
AMBIGUITY_MARGIN = 0.025
