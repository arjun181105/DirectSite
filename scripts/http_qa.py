import json,pathlib,time,urllib.request,urllib.error
ROOT=pathlib.Path(__file__).resolve().parents[1]
origin='http://127.0.0.1:8765';manifest=json.load(open(ROOT/'seo/content-manifest.json'));rows=[]
for item in manifest:
    start=time.monotonic()
    with urllib.request.urlopen(origin+item['slug'],timeout=15) as response:
        body=response.read();assert response.status==200
        rows.append({'route':item['slug'],'httpStatus':response.status,'htmlBytes':len(body),'localResponseMilliseconds':round((time.monotonic()-start)*1000,2)})
try:urllib.request.urlopen(origin+'/missing-qa-route/',timeout=15);raise AssertionError('Soft 404')
except urllib.error.HTTPError as e:assert e.code==404
with urllib.request.urlopen(origin+'/website-design/',timeout=15) as r:assert r.url==origin+'/web-design/'
with urllib.request.urlopen(origin+'/services',timeout=15) as r:assert r.url==origin+'/services/'
report={'routes':rows,'missingRouteStatus':404,'aliasRedirect':'/website-design/ -> /web-design/','legacyServicesRedirect':'/services -> /services/','limitations':'Local response times are not production load times or Core Web Vitals. Canonical host and CDN behaviour need production verification.'}
(ROOT/'seo/audit/http-qa.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: all',len(rows),'routes return 200; real 404 and canonical path redirects.')
