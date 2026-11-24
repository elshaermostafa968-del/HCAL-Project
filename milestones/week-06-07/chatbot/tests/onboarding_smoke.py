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
  kw={'executable_path':os.environ['CHROME_PATH']} if os.environ.get('CHROME_PATH') else {}
  b=w.chromium.launch(**kw,args=['--no-sandbox']);page=b.new_page(viewport={'width':1440,'height':1080});errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  btn=lambda n:page.get_by_role('button',name=n,exact=True)
  page.goto('http://127.0.0.1:8766')
  btn('See an example').click();page.get_by_text('Mandatory rule',exact=True).wait_for()
  page.screenshot(path=str(OUT/'onboarding-stage-1.png'))
  # Step navigation stays reachable in the one-line bar, also after hide/show guidance.
  btn('Hide guidance').click();btn('Show guidance').click()
  btn('Continue to co-pilot').click();btn('Hide guidance').click();btn('Show guidance').click()
  btn('Load guided task').click()
  page.locator('#composer button[type=submit]').click();btn('Continue independently').wait_for()
  page.screenshot(path=str(OUT/'onboarding-stage-2.png'))
  btn('Continue independently').click();page.get_by_text('Step 3 of 3').wait_for()
  page.screenshot(path=str(OUT/'onboarding-stage-3.png'))
  page.set_viewport_size({'width':390,'height':844})
  page.screenshot(path=str(OUT/'onboarding-mobile.png'))
  assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
  assert not errors,errors
  b.close();print(json.dumps({'onboarding_smoke':'passed','stages':3,'js_errors':errors}))
finally:
 p.terminate();p.wait(timeout=5)
