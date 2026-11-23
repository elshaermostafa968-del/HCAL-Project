"""40 labelled fixture checks. These are smoke tests, NOT measured human usability."""
import json
import sys
from collections import Counter
from pathlib import Path
from statistics import mean
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.retriever import CASES

def run():
    rows=[]
    with TestClient(app) as client:
        health=client.get('/health').json()
        if health['provider']!='local':
            raise SystemExit('Evaluation is offline by default. Set LLM_PROVIDER=local and restart this script. Avoid accidental paid API calls.')
        for case in CASES:
            expected='uncertain' if case['case_id']=='IC-003' else case['validation_tests']['expected_status']
            result=client.post('/chat',json={'message':case['validation_tests']['query'],'style':case['style_manual_reference']['style']}).json()
            passed=result['status']==expected and (expected!='ok' or result['evidence']['rule_id']==case['case_id'])
            rows.append({'case_id':case['case_id'],'expected_status':expected,'passed':passed,'response':result})
    summary={'mode':'local','cases':len(rows),'passed':sum(r['passed'] for r in rows),'fixture_pass_rate':sum(r['passed'] for r in rows)/len(rows),'mean_backend_latency_ms':round(mean(r['response']['latency_ms'] for r in rows),2),'limitations':'Labelled fixture reuse, not held-out accuracy, provider latency, real model evidence, or usability testing.'}
    dest=Path(__file__).parent/'results';dest.mkdir(exist_ok=True)
    (dest/'outputs.json').write_text(json.dumps(rows,indent=2)+'\n')
    (dest/'metrics.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
    return 0 if all(r['passed'] for r in rows) else 1
if __name__=='__main__':sys.exit(run())
