import json, pathlib, urllib.request, urllib.error, datetime
host='https://kowhaigoods.com'
dist=pathlib.Path('.')
key=(dist/'indexnow_key.txt').read_text().strip()
key_url=f'{host}/{key}.txt'
try:
    live=urllib.request.urlopen(key_url,timeout=15).read().strip()==key.encode()
except Exception:
    live=False
if not live:
    print('KEY NOT LIVE YET — GitHub Pages still propagating or key file missing. Do not probe again today. Exiting.'); raise SystemExit(0)
urls={host+'/'}
for p in sorted(dist.glob('*.html')):
    if p.name!='index.html': urls.add(f'{host}/{p.name}')
urls=sorted(urls)
payload={'host':'kowhaigoods.com','key':key,'keyLocation':key_url,'urlList':urls}
req=urllib.request.Request('https://api.indexnow.org/indexnow',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json; charset=utf-8'})
try:
    r=urllib.request.urlopen(req,timeout=30)
    print('IndexNow HTTP',r.status,'| submitted',len(urls),'URLs')
except Exception as e:
    print('IndexNow error:',e)