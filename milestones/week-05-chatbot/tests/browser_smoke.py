"""Browser smoke test with a temporary localhost server, no saved login or user account."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import urllib.request
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
if __name__=='__main__':
    out=ROOT/'evidence';out.mkdir(exist_ok=True)
    env={**os.environ,'LLM_PROVIDER':'local','FEEDBACK_PATH':str(out/'test-feedback.jsonl')}
    process=subprocess.Popen([sys.executable,'-m','uvicorn','backend.app.main:app','--port','8765'],cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    try:
        for i in range(60):
            try:
                urllib.request.urlopen('http://127.0.0.1:8765/health',timeout=1);break
            except Exception:time.sleep(.2)
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True)
            page=browser.new_page(viewport={'width':1440,'height':1080},device_scale_factor=1)
            errors=[];page.on('pageerror',lambda err:errors.append(str(err)))
            page.goto('http://127.0.0.1:8765')
            page.get_by_text('LOCAL DEMO · 40 teaching cases').wait_for()
            page.screenshot(path=str(out/'desktop-start.png'),full_page=True)
            page.get_by_role('button',name='Verify a citation',exact=True).click()
            page.get_by_role('button',name='Check my excerpt').click()
            page.get_by_text('Mandatory rule',exact=True).wait_for()
            page.get_by_text('Why this rule? · CF-001',exact=True).click()
            page.locator('#chat').evaluate('(e)=>{e.scrollTop=e.scrollHeight}')
            page.locator('#chat').evaluate('(e)=>{e.style.height="auto";e.style.maxHeight="none"}')
            page.screenshot(path=str(out/'desktop-feedback.png'),full_page=True)
            page.locator('#chat').evaluate('(e)=>{e.style.height="";e.style.maxHeight=""}')
            page.get_by_role('button',name='Next hint',exact=True).click()
            page.get_by_text('Hint 2 / 3',exact=False).wait_for()
            page.get_by_role('button',name='Previous hint',exact=True).click()
            page.get_by_role('button',name="I'm done",exact=True).click()
            page.get_by_text('Session summary:',exact=False).wait_for()
            page.get_by_role('button',name='Talk to a person',exact=True).first.click()
            page.get_by_role('dialog').wait_for()
            page.screenshot(path=str(out/'handover.png'),full_page=True)
            page.get_by_role('button',name='Back to my session').click()
            page.get_by_role('button',name='Clear chat',exact=True).first.click()
            assert page.get_by_text('A coach, not a ghostwriter.').count()==1
            page.set_viewport_size({'width':390,'height':844})
            page.screenshot(path=str(out/'mobile-start.png'),full_page=True)
            assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
            assert not errors,errors
            browser.close()
            print(json.dumps({'browser_smoke':'passed','page_errors':errors,'screenshots':4}))
    finally:
        process.terminate()
        try:process.wait(timeout=5)
        except subprocess.TimeoutExpired:process.kill()
        feedback=out/'test-feedback.jsonl'
        if feedback.exists():feedback.unlink()
