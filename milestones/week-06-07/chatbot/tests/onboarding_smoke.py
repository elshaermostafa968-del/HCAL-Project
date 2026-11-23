from pathlib import Path
import os,subprocess,sys,time,urllib.request,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'evidence';OUT.mkdir(exist_ok=True)
p=subprocess.Popen([sys.executable,'-m','uvicorn','backend.app.main:app','--port','8766'],cwd=ROOT,env={**os.environ,'LLM_PROVIDER':'local'},stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
try:
 for _ in range(50):
  try:urllib.request.urlopen('http://127.0.0.1:8766/health',timeout=1);break
  except Exception:time.sleep(.2)
 with sync_playwright() as w:
  b=w.chromium.launch();page=b.new_page(viewport={'width':1440,'height':1080});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8766');page.get_by_role('button',name='Show a worked example',exact=True).click()
  page.get_by_text('Mandatory rule',exact=True).wait_for();page.locator('#chat').evaluate('(e)=>e.scrollTop=e.scrollHeight');page.screenshot(path=str(OUT/'onboarding-stage-1.png'),full_page=True)
  page.get_by_role('button',name='Continue to co-pilot',exact=True).click();page.get_by_role('button',name='Load guided task',exact=True).click()
  page.get_by_role('button',name='Check my excerpt').click();page.get_by_role('button',name='Continue independently',exact=True).wait_for()
  page.screenshot(path=str(OUT/'onboarding-stage-2.png'),full_page=True)
  page.get_by_role('button',name='Continue independently',exact=True).click();page.get_by_role('heading',name='3 of 3 · The user does it').wait_for()
  page.screenshot(path=str(OUT/'onboarding-stage-3.png'),full_page=True)
  page.get_by_role('button',name='Restart guided onboarding',exact=True).first.click();page.get_by_role('heading',name='1 of 3 · The system does it').wait_for()
  page.set_viewport_size({'width':390,'height':844});page.evaluate('window.scrollTo(0,0)');page.screenshot(path=str(OUT/'onboarding-mobile.png'),full_page=True)
  assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
  assert not errors,errors
  b.close();print(json.dumps({'onboarding_smoke':'passed','stages':3,'mobile_overflow':False,'js_errors':errors}))
finally:
 p.terminate();p.wait(timeout=5)
