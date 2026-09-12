"""Validate every emitted HTML route and local reference without network access."""
import json,pathlib,re,sys,urllib.parse,xml.etree.ElementTree as ET
from html.parser import HTMLParser
from content_model import check_collection
ROOT=pathlib.Path(__file__).resolve().parents[1]
class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.tags=[];self.ids=set();self.links=[];self.text='';self.title='';self.h1=[];self.current=None;self.schemas=[];self.script=None
    def handle_starttag(self,tag,attrs):
        a=dict(attrs);self.tags.append((tag,a))
        if 'id' in a:self.ids.add(a['id'])
        if tag in {'a','link','script','img'}:
            value=a.get('href') or a.get('src')
            if value:self.links.append((tag,value))
        if tag in {'title','h1'}:self.current=tag
        if tag=='h1':self.h1.append('')
        if tag=='script' and a.get('type')=='application/ld+json':self.script=''
    def handle_endtag(self,tag):
        if tag==self.current:self.current=None
        if tag=='script' and self.script is not None:self.schemas.append(json.loads(self.script));self.script=None
    def handle_data(self,value):
        if self.current=='title':self.title+=value
        if self.current=='h1':self.h1[-1]+=value
        if self.script is not None:self.script+=value
        self.text+=value
def parse(path):
    d=Document();d.feed(path.read_text());return d
def validate():
    pages=json.loads((ROOT/'content/pages.json').read_text());check_collection(pages)
    manifest=json.loads((ROOT/'seo/content-manifest.json').read_text());info=json.loads((ROOT/'dist/build-info.json').read_text())
    docs={r['slug']:parse(ROOT/'dist'/r['slug'].strip('/')/'index.html') for r in manifest}
    titles=set();headings=set();errors=[];edges={s:set() for s in docs}
    for slug,d in docs.items():
        if not d.title or d.title in titles:errors.append(slug+' duplicate/missing title')
        titles.add(d.title)
        if len(d.h1)!=1 or not d.h1[0] or d.h1[0] in headings:errors.append(slug+' duplicate/missing H1')
        headings.update(d.h1)
        canon=[a.get('href') for t,a in d.tags if t=='link' and a.get('rel')=='canonical']
        if canon!=['https://directsite.com.au'+slug]:errors.append(slug+' canonical mismatch')
        robots=[a.get('content','') for t,a in d.tags if t=='meta' and a.get('name')=='robots']
        if len(robots)!=1 or ('noindex' in robots[0])==info['production']:errors.append(slug+' indexability mismatch')
        for name,attr in [('description','name'),('og:title','property'),('og:description','property'),('twitter:title','name')]:
            if len([a for t,a in d.tags if t=='meta' and a.get(attr)==name and a.get('content')])!=1:errors.append(slug+' missing/duplicate '+name)
        if not d.schemas:errors.append(slug+' missing schema')
        for schema in d.schemas:
            if schema.get('@context')!='https://schema.org':errors.append(slug+' invalid schema context')
            for node in schema.get('@graph',[]):
                if node.get('@type') in ['LocalBusiness','AggregateRating','Review','Person']:errors.append(slug+' unsupported evidence-dependent schema')
        for tag,a in d.tags:
            if tag=='label' and a.get('for') and a['for'] not in d.ids:errors.append(slug+' dangling form label')
            if tag=='img' and 'alt' not in a:errors.append(slug+' missing alt text')
        for tag,link in d.links:
            url=urllib.parse.urlsplit(link)
            if url.scheme or url.netloc:continue
            target=urllib.parse.urljoin(slug,link).split('#')[0].split('?')[0]
            if target in docs:
                if tag=='a':edges[slug].add(target)
                if url.fragment and url.fragment not in docs[target].ids and url.fragment!='book':errors.append(slug+' broken fragment '+link)
            elif not (ROOT/'dist'/target.lstrip('/')).is_file():errors.append(slug+' broken local reference '+link)
    reachable={'/'};pending=['/']
    while pending:
        for child in edges[pending.pop()]-reachable:reachable.add(child);pending.append(child)
    if reachable!=set(docs):errors.append('Orphan routes: '+str(set(docs)-reachable))
    ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'};index=ET.parse(ROOT/'dist/sitemap.xml');urls=[]
    for loc in index.findall('.//s:loc',ns):
        path=ROOT/'dist'/urllib.parse.urlsplit(loc.text).path.lstrip('/')
        urls += [x.text for x in ET.parse(path).findall('.//s:url/s:loc',ns)]
    expected={r['canonical'] for r in manifest if r['indexable']} if info['production'] else set()
    if len(urls)!=len(set(urls)) or set(urls)!=expected:errors.append('Sitemap inclusion mismatch')
    for file in (ROOT/'dist').rglob('*.html'):
        if '__WEB3FORMS_KEY__' in file.read_text():errors.append('Unresolved integration token')
    report={'routes':len(docs),'productionOutput':info['production'],'errors':errors,'checks':['unique titles/H1s','canonicals','metadata','JSON-LD structure','local links/fragments/assets','hub reachability','sitemap equality','indexability','form label references'],'limitations':['Schema.org external validator not run','HTTP/CDN validation separate','Browser accessibility and field Core Web Vitals require separate measurements']}
    (ROOT/'seo/audit/static-qa.json').write_text(json.dumps(report,indent=2)+'\n')
    if errors:raise AssertionError('\n'.join(errors))
    print(f'PASS: {len(docs)} routes; metadata, graph, links and sitemap verified.')
    return report
if __name__=='__main__':validate()
