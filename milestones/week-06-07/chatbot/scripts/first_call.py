"""Save real-model evidence only when the backend confirms a successful live reply."""
import json
from datetime import datetime, timezone
from pathlib import Path
import httpx
ROOT=Path(__file__).resolve().parents[1]
if __name__=='__main__':
    payload={'message':'Check APA missing year: Earlier research supports this claim (Nadir).','style':'APA'}
    try:
        with httpx.Client(timeout=30) as c:
            health=c.get('http://127.0.0.1:8000/health'); health.raise_for_status()
            if health.json()['provider']=='local':
                raise SystemExit('NOT live evidence. Set LLM_PROVIDER=gemini or openai and your key in .env; restart the server.')
            r=c.post('http://127.0.0.1:8000/chat',json=payload);r.raise_for_status();result=r.json()
        if result['status']!='ok' or result.get('live_model_response') is not True:
            raise SystemExit('No successful live model response. Backend status: '+result['status']+'. Check the server configuration and try again.')
        capture={'captured_at':datetime.now(timezone.utc).isoformat(),'request':payload,'http_status':r.status_code,'response':result}
        folder=ROOT/'evidence';folder.mkdir(exist_ok=True)
        path=folder/('live-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'.json')
        path.write_text(json.dumps(capture,indent=2)+'\n')
        print(json.dumps(capture,indent=2));print('Saved:',path)
    except httpx.HTTPError:
        raise SystemExit('Backend unavailable. Start uvicorn and check /health first.')
