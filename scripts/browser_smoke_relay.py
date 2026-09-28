"""Optional developer test: requires Playwright and /usr/bin/chromium.
Uses an explicit Python HTTP relay; not a native browser network test.
"""
import json,sys,threading,time
from pathlib import Path
from playwright.sync_api import sync_playwright
from http.client import HTTPConnection
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from neuroweave.server import make_server
server=make_server(0);t=threading.Thread(target=server.serve_forever,daemon=True);t.start()
checks=[];errors=[]
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':1440,'height':1100},device_scale_factor=1)
  page.on('pageerror',lambda error:errors.append(str(error)))
  def relay(url, options=None):
   options=options or {}
   connection=HTTPConnection('127.0.0.1',server.server_port,timeout=10)
   connection.request(options.get('method','GET'),url,body=options.get('body'),headers=options.get('headers',{}))
   response=connection.getresponse(); result={'status':response.status,'body':response.read().decode()};connection.close();return result
  page.expose_function('nwRelay',relay)
  html=(root/'neuroweave/web/index.html').read_text().replace('<link rel="stylesheet" href="/style.css">','').replace('<script src="/app.js" defer></script>','')
  page.set_content(html)
  page.add_style_tag(content=(root/'neuroweave/web/style.css').read_text())
  page.add_script_tag(content="window.fetch=async (url,options)=>{const r=await window.nwRelay(url,options);return new Response(r.body,{status:r.status,headers:{'Content-Type':'application/json'}});};")
  page.add_script_tag(content=(root/'neuroweave/web/app.js').read_text())
  page.locator('#chapters button').first.wait_for()
  assert page.locator('#chapters button').count()==18
  checks.append('18 chapter navigation entries loaded')
  page.locator('#run').click();page.wait_for_function("document.querySelector('#status').textContent.startsWith('Complete.')")
  print('selected',page.locator('#title').text_content(),'json length',len(page.locator('#json').text_content()),'status',page.locator('#status').text_content())
  assert page.locator('#json').text_content().find('"replay_equal": true')>=0
  checks.append('memory experiment ran in Python and reported equal replay')
  page.locator('#chapters button').nth(6).click()
  page.locator('#params').fill('{"current_na":0.25,"dt_ms":0.5}')
  page.locator('#run').click();page.wait_for_function("document.querySelector('#status').textContent.startsWith('Complete.')")
  assert page.locator('#chartBox').is_visible()
  checks.append('LIF parameter change produced displayed time series')
  page.screenshot(path=str(root/'docs/assets/lab-desktop.png'),full_page=True)
  with page.expect_download() as info:page.locator('#export').click()
  download=info.value
  download.save_as(str(root/'validation/ui_export.json'))
  exported=json.load(open(root/'validation/ui_export.json'))
  assert exported['protocol']['parameters']['current_na']==.25
  checks.append('export button produced valid JSON for chosen parameters')
  page.locator('#params').fill('{"current_na": "invalid"}')
  page.locator('#run').click();page.wait_for_function("document.querySelector('#status').textContent.startsWith('Experiment rejected:')")
  assert not page.locator('#result').is_visible()
  checks.append('invalid parameter rejected with visible error')
  page.locator('#search').fill('confirmation')
  assert page.locator('#chapters button').count()==1
  checks.append('chapter filtering works')
  page.locator('#search').fill('');page.locator('#chapters button').nth(15).click()
  page.locator('#run').click();page.wait_for_function("document.querySelector('#status').textContent.startsWith('Complete.')")
  assert 'evidence_changed_after_planning' in page.locator('#json').text_content()
  checks.append('integrated runtime result includes stale-plan rejection')
  page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(root/'docs/assets/lab-mobile.png'),full_page=True)
  assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth')
  checks.append('390-pixel viewport has no horizontal overflow')
  version=browser.version
  browser.close()
 receipt={'status':'passed_with_python_http_relay' if not errors else 'failed','browser':'Chromium','browser_version':version,
          'checked_url_kind':'in-memory assets; real local HTTP API called through a Python test relay',
          'direct_browser_navigation':'blocked by container administrator policy; not verified',
          'relay_changes':'fetch is delegated to Python HTTPConnection for this test only; delivered app uses native browser fetch','checks':checks,'page_errors':errors,
          'screenshots':['docs/assets/lab-desktop.png','docs/assets/lab-mobile.png'],
          'scope':'browser smoke test; not an accessibility or production security certification'}
 (root/'validation/UI_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(receipt,indent=2))
finally:
 server.shutdown();server.server_close();t.join()
