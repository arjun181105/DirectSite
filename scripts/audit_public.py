"""Read-only capture of a bounded set of already identified public pages."""
import json,pathlib,urllib.request,datetime
from html.parser import HTMLParser
ROOT=pathlib.Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self):super().__init__();self.title='';self.headings=[];self.active=None;self.links=[];self.parts=[];self.skip=0;self.in_head=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in {'script','style'}:self.skip+=1
        if tag=='head':self.in_head=True
        if tag=='title' and self.in_head:self.active='title'
        if tag in {'h1','h2','h3'}:self.active=tag;self.headings.append({'level':tag,'text':''})
        if tag=='a' and a.get('href'):self.links.append(a['href'])
    def handle_endtag(self,tag):
        if tag=='head':self.in_head=False
        if tag in {'script','style'}:self.skip=max(0,self.skip-1)
        if tag==self.active:self.active=None
    def handle_data(self,value):
        if self.active=='title':self.title+=value
        elif self.active:self.headings[-1]['text']+=value
        if not self.skip:self.parts.append(value)
urls=['https://visualweb.com.au/web-design-melbourne/','https://www.tradiewebguys.com.au/','https://www.chromatix.com.au/','https://www.boldagency.com.au/web-design/melbourne']
records=[]
for url in urls:
    try:
        request=urllib.request.Request(url,headers={'User-Agent':'DirectSite public website research'})
        with urllib.request.urlopen(request,timeout=20) as r:body=r.read(2_000_000);status=r.status;final=r.url
        p=Page();p.feed(body.decode('utf-8','replace'))
        record={'url':url,'finalUrl':final,'httpStatus':status,'title':p.title,'headings':p.headings,'approximateStaticTextWordsIncludingNavigation':len(' '.join(p.parts).split()),'observedLinkPatterns':list(dict.fromkeys(p.links)),'observedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'backlinks':None,'rankCausality':None,'notes':'Static primary-page inspection. Word count includes repeated navigation. Internal link patterns are not backlink evidence.'}
    except Exception as e:record={'url':url,'status':'unavailable','error':str(e)}
    records.append(record)
(ROOT/'seo/research/competitor-page-audits.json').write_text(json.dumps(records,indent=2)+'\n')
print([(x['url'],x.get('httpStatus',x.get('status')),x.get('approximateStaticTextWordsIncludingNavigation')) for x in records])
