"""Auditable public-site benchmark CLI. No public arbitrary-URL endpoint.

Uses an explicit sample file, honours robots, bounds response size and rejects
private/local addresses and cross-domain redirects. Manual observations stay null.
"""
import argparse,datetime,hashlib,http.client,ipaddress,json,pathlib,socket,ssl,time,urllib.parse,urllib.robotparser,statistics
from html.parser import HTMLParser
ROOT=pathlib.Path(__file__).resolve().parents[1]
UA='DirectSiteResearch/1.0 (public website usability research)'
LIMIT=2_000_000
class AuditHTML(HTMLParser):
    def __init__(self):super().__init__();self.title='';self.in_title=False;self.meta=None;self.tel=0;self.forms=0;self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='title':self.in_title=True
        if tag=='meta' and a.get('name','').lower()=='description':self.meta=a.get('content')
        if tag=='a':
            href=a.get('href','');self.tel+=href.startswith('tel:');self.links.append(href)
        if tag=='form':self.forms+=1
    def handle_endtag(self,tag):
        if tag=='title':self.in_title=False
    def handle_data(self,data):
        if self.in_title:self.title+=data
def public_url(url):
    u=urllib.parse.urlsplit(url)
    if u.scheme!='https' or not u.hostname or u.username or u.password or u.port not in {None,443}:raise ValueError('Only public HTTPS sites on port 443')
    addresses=sorted({x[4][0] for x in socket.getaddrinfo(u.hostname,443,type=socket.SOCK_STREAM)})
    if not addresses or any(not ipaddress.ip_address(a).is_global for a in addresses):raise ValueError('Non-public network destination')
    return u,addresses
class PinnedHTTPS(http.client.HTTPSConnection):
    def __init__(self,host,address):super().__init__(host,timeout=15,context=ssl.create_default_context());self.address=address
    def connect(self):
        sock=socket.create_connection((self.address,443),self.timeout)
        self.sock=self._context.wrap_socket(sock,server_hostname=self.host)
def fetch(url,allowed_host):
    for _ in range(4):
        u,addresses=public_url(url)
        if u.hostname!=allowed_host:raise ValueError('Redirect outside the explicitly sampled hostname')
        conn=PinnedHTTPS(u.hostname,addresses[0]);start=time.monotonic()
        conn.request('GET',urllib.parse.urlunsplit(('', '',u.path or '/',u.query,'')),headers={'User-Agent':UA,'Accept':'text/html,text/plain;q=0.9','Accept-Encoding':'identity'})
        response=conn.getresponse();status=response.status;headers=dict(response.getheaders());body=response.read(LIMIT+1);conn.close()
        if len(body)>LIMIT:raise ValueError('Response exceeds 2 MB cap')
        if status in {301,302,303,307,308}:
            target=response.getheader('Location')
            if not target:raise ValueError('Redirect without Location')
            url=urllib.parse.urljoin(url,target);continue
        return {'url':url,'status':status,'headers':headers,'seconds':round(time.monotonic()-start,4),'body':body}
    raise ValueError('Too many redirects')
def scan(sample,out):
    url=sample['url'];u,_=public_url(url)
    robot_url=urllib.parse.urlunsplit(('https',u.netloc,'/robots.txt','',''));robots=fetch(robot_url,u.hostname)
    if robots['status'] not in {200,404,410}:raise ValueError('Robots unavailable; fail closed')
    rp=urllib.robotparser.RobotFileParser();rp.parse(robots['body'].decode('utf-8','replace').splitlines() if robots['status']==200 else [])
    if robots['status']==200 and not rp.can_fetch(UA,url):raise ValueError('Robots disallows research crawl')
    delay=rp.crawl_delay(UA) or rp.crawl_delay('*') or 2
    if delay>30:raise ValueError('Long crawl delay; schedule manual review')
    time.sleep(max(2,delay));res=fetch(url,u.hostname)
    if res['status']!=200:raise ValueError('Page returned '+str(res['status']))
    content_type=next((v for k,v in res['headers'].items() if k.lower()=='content-type'),'')
    if 'text/html' not in content_type:raise ValueError('Not an HTML page')
    parser=AuditHTML();parser.feed(res['body'].decode('utf-8','replace'))
    digest=hashlib.sha256(res['body']).hexdigest();(out/(sample['id']+'.html')).write_bytes(res['body'])
    record={**sample,'observedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'observed','method':'single-page-static-html','finalUrl':res['url'],'sha256':digest,'responseHeaders':res['headers'],'responseSeconds':res['seconds'],'htmlBytes':len(res['body']),'https':True,'title':parser.title.strip(),'metaDescription':parser.meta,'tapToCallLinksInHTML':parser.tel,'formElementsInHTML':parser.forms,'mobilePageSpeed':None,'desktopPageSpeed':None,'fieldCoreWebVitals':None,'aboveFoldCTA':None,'visiblePhone':None,'reviewIntegration':None,'serviceAreaClear':None,'pageCount':None,'mobileUsability':None,'imageWeight':None,'notes':['HTML presence is not visibility or functionality. Response seconds are not page load time.']}
    (out/(sample['id']+'.json')).write_text(json.dumps(record,indent=2)+'\n');return record
def summarise(rows):
    valid=[r for r in rows if r.get('status')=='observed'];n=len(valid)
    def group(key):
        result={}
        for r in valid:result.setdefault(r.get(key,'unknown'),[]).append(r)
        return {k:{'n':len(v),'htmlTapToCallFraction':sum(x['tapToCallLinksInHTML']>0 for x in v)/len(v)} for k,v in result.items()}
    return {'n':n,'publishable':False,'publicationGate':'Representative sample, manual verification and methodology review required','medianHtmlBytes':statistics.median(r['htmlBytes'] for r in valid) if n else None,'htmlTapToCallFraction':sum(r['tapToCallLinksInHTML']>0 for r in valid)/n if n else None,'byIndustry':group('industry'),'byLocation':group('location'),'quotableFindings':[]}
def main():
    a=argparse.ArgumentParser();a.add_argument('--sample',default='seo/benchmark/sample.json');a.add_argument('--scan',action='store_true');args=a.parse_args()
    out=ROOT/'seo/benchmark/raw';out.mkdir(parents=True,exist_ok=True)
    samples=json.loads((ROOT/args.sample).read_text());rows=[]
    for sample in samples:
        if args.scan:
            if not sample.get('selectionReason') or not sample.get('sourceUrl'):raise ValueError('Sample selection provenance required')
            if not __import__('re').fullmatch('[a-z0-9-]+',sample['id']):raise ValueError('Invalid sample ID')
            try:rows.append(scan(sample,out))
            except Exception as e:
                record={**sample,'status':'unavailable','error':str(e),'observedAt':datetime.datetime.now(datetime.timezone.utc).isoformat()};rows.append(record);(out/(sample['id']+'.json')).write_text(json.dumps(record,indent=2)+'\n')
        elif (out/(sample['id']+'.json')).exists():rows.append(json.loads((out/(sample['id']+'.json')).read_text()))
    (ROOT/'seo/benchmark/cleaned.json').write_text(json.dumps(rows,indent=2)+'\n')
    (ROOT/'seo/benchmark/summary.json').write_text(json.dumps(summarise(rows),indent=2)+'\n')
    print(f'{len(rows)} records. Unmeasured values remain null; publication is gated.')
if __name__=='__main__':main()
