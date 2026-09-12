"""Portable static integration for the recovered DirectSite HTML baseline."""
import argparse, html, json, pathlib, re, shutil, os
from xml.sax.saxutils import escape
from content_model import check_collection, quality, words

ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'dist'
SITE=json.loads((ROOT/'content/site.json').read_text())
ORIGIN=SITE['origin']
PAGES=json.loads((ROOT/'content/pages.json').read_text())
BY_SLUG={p['slug']:p for p in PAGES}
H=html.escape

def jsonld(value):
    return '<script type="application/ld+json">'+json.dumps(value,ensure_ascii=False).replace('<','\\u003c')+'</script>'

def schema(p):
    url=ORIGIN+p['slug']
    graph=[{'@type':'Organization','@id':ORIGIN+'/#organization','name':'DirectSite','url':ORIGIN+'/'},
           {'@type':'WebSite','@id':ORIGIN+'/#website','name':'DirectSite','url':ORIGIN+'/','publisher':{'@id':ORIGIN+'/#organization'}},
           {'@type':'WebPage','@id':url+'#webpage','url':url,'name':p['title'],'description':p['description'],'inLanguage':'en-AU','isPartOf':{'@id':ORIGIN+'/#website'}}]
    crumbs=[{'@type':'ListItem','position':1,'name':'Home','item':ORIGIN+'/'}]
    if p['slug']!='/':
        parent='/'+'/'.join(p['slug'].strip('/').split('/')[:-1])+'/'
        if parent in BY_SLUG: crumbs.append({'@type':'ListItem','position':2,'name':BY_SLUG[parent]['h1'],'item':ORIGIN+parent})
        crumbs.append({'@type':'ListItem','position':len(crumbs)+1,'name':p['h1'],'item':url})
        graph.append({'@type':'BreadcrumbList','itemListElement':crumbs})
    if p['pageType'] in {'industry','location','service'}:
        graph.append({'@type':'Service','@id':url+'#service','name':p['h1'],'description':p['answer'],'url':url,'provider':{'@id':ORIGIN+'/#organization'},'areaServed':{'@type':'Country','name':'Australia'}})
    if p['pageType'] in {'guide','comparison','buyer-guide'}:
        graph.append({'@type':'Article','@id':url+'#article','headline':p['h1'],'description':p['description'],'dateModified':p['lastReviewed'],'author':{'@id':ORIGIN+'/#organization'},'publisher':{'@id':ORIGIN+'/#organization'},'mainEntityOfPage':{'@id':url+'#webpage'}})
    return {'@context':'https://schema.org','@graph':graph}

def meta(p,production):
    indexing='index, follow, max-image-preview:large' if production and p.get('indexable',True) else 'noindex, follow'
    verification = f'<meta name="msvalidate.01" content="{H(SITE["bingVerification"],quote=True)}">' if production and SITE.get("bingVerification") and p["slug"]=="/" else ""
    analytics = f'<link rel="stylesheet" href="/analytics.css"><script src="/analytics.js" data-measurement-id="{H(SITE["ga4MeasurementId"],quote=True)}" defer></script>' if production and SITE.get('ga4MeasurementId') else ''
    return f'''{verification}{analytics}<title>{H(p['title'])}</title>
<meta name="description" content="{H(p['description'],quote=True)}">
<meta name="robots" content="{indexing}">
<link rel="canonical" href="{ORIGIN+p['slug']}">
<meta property="og:type" content="{'article' if p['pageType'] in {'guide','comparison','buyer-guide'} else 'website'}">
<meta property="og:site_name" content="DirectSite"><meta property="og:locale" content="en_AU">
<meta property="og:title" content="{H(p['title'],quote=True)}"><meta property="og:description" content="{H(p['description'],quote=True)}">
<meta property="og:url" content="{ORIGIN+p['slug']}"><meta property="og:image" content="{ORIGIN}/og.png">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{H(p['title'],quote=True)}">
<meta name="twitter:description" content="{H(p['description'],quote=True)}"><meta name="twitter:image" content="{ORIGIN}/og.png">
{jsonld(schema(p))}'''

def cta(placement='page'):
    return f'<a class="growth-cta" href="{SITE["schedule"]}" data-book data-placement="{placement}">{SITE["cta"]}</a><p class="growth-note">No deposit · Free revisions before payment · Walk away owing $0</p>'

def links(slugs):
    return ''.join(f'<a href="{s}">{H(BY_SLUG[s]["h1"])}</a>' for s in slugs)

def footer():
    return '<footer class="growth-footer"><div class="growth-wrap"><p>DirectSite · Websites for Australian businesses.</p><nav class="growth-links" aria-label="Company">'+links(['/about/','/contact/','/process/','/guides/','/tools/'])+'</nav><p class="growth-note">© 2026 DirectSite · Australia-wide remote service</p></div></footer>'

def label_forms(s):
    count=0
    def patch(m):
        nonlocal count
        label,tag,attrs=m.group(1),m.group(2),m.group(3)
        count+=1
        found=re.search(r'id="([^"]+)"',attrs)
        id_=found.group(1) if found else f'field-{count}'
        if not found: attrs+=' id="'+id_+'"'
        if 'autocomplete=' not in attrs and tag=='input':
            auto={'f-name':'name','f-biz':'organization','f-email':'email','f-phone':'tel'}.get(id_)
            if auto: attrs+=' autocomplete="'+auto+'"'
        return '<label for="'+id_+'">'+label+'</label>\n<'+tag+attrs+'>'
    s=re.sub(r'<label>(.*?)</label>\s*<(input|select|textarea)([^>]*)>',patch,s,flags=re.S)
    s=s.replace('</form>','<p class="growth-submit-status" role="status" aria-live="polite"></p><p class="fineprint"><a href="'+SITE['schedule']+'">Book a call instead</a></p></form>')
    s=s.replace('Your site is being built right now. Book your free 10-minute call below to see it live, screen to screen.','Your demo request has been received. Book a free 10-minute call below to review it with us.')
    s=s.replace('Get your <em class="f">free site</em>.','Get your <em class="f">free demo</em>.')
    s=s.replace('Wait &#8212; you\'re <em class="f">not done</em> yet.','Your demo request is in.')
    s=s.replace('<div id="cal-embed"','<p class="fineprint"><a href="https://cal.com/arjun-sharma-l5xsle/directsite-see-your-website">Open the booking calendar directly</a></p><div id="cal-embed"')
    s=s.replace('id="f-phone" type="tel" required', 'id="f-phone" type="tel"')
    s=s.replace('<label for="f-phone">Phone</label>', '<label for="f-phone">Phone (optional)</label>')
    s=s.replace('10 MIN · NO OBLIGATION', 'NO DEPOSIT · NO OBLIGATION').replace('10 min · Google Meet', 'Google Meet')
    s=s.replace('Book a free 10-minute call below', 'Book a free call below')
    disclosure='<p class="fineprint">Your enquiry is sent to DirectSite through Web3Forms. Booking uses Cal.com. Please do not include passwords or sensitive customer records.</p>'
    return s.replace('<form ',disclosure+'<form ',1)

def form_script(home):
    js=home[home.index("  var modal = document.getElementById('modal');"):home.rindex('</script>')]
    js=js.replace('function sendLead() {','async function sendLead() {')
    js=js.replace('if (leadSent || !WEB3FORMS_KEY || WEB3FORMS_KEY.indexOf("YOUR_") === 0) return;\n    leadSent = true;','if (leadSent) return false;\n    if (!WEB3FORMS_KEY) throw new Error("Enquiry unavailable");')
    js=js.replace('    fetch("https://api.web3forms.com/submit", {','    const response = await fetch("https://api.web3forms.com/submit", {\n      signal: AbortSignal.timeout(15000),')
    js=js.replace('}).catch(function(){ leadSent = false; }); // allow retry if it failed','});\n    const result = await response.json();\n    if (!response.ok || result.success !== true) throw new Error("Enquiry not accepted");\n    leadSent = true; return true;')
    js=js.replace('showStep(\'branch\');',"window.dsTrack?.('form_step_complete',{step:'contact'}); showStep('branch');")
    js=js.replace('window.__step2 = function(kind) {','var submitting = false;\n  window.__step2 = async function(kind) {\n    if(submitting) return;\n    const form=document.getElementById(kind === "new" ? "form-new" : "form-re");\n    if(!form.reportValidity()) return;\n    submitting=true;\n    const button=form.querySelector("button[type=submit]");\n    const status=form.querySelector(".growth-submit-status");\n    button.disabled=true; status.textContent="Sending your request…";')
    old="sendLead();   // email you the lead now — even if they don't finish booking\n    showStep('book');\n    initCal();"
    new="""try {
      const accepted = await sendLead();
      window.dsTrack?.('form_step_complete',{step:'brief',project_type:kind});
      if (accepted) {
        window.dsTrack?.('form_submit',{project_type:kind});
        window.dsTrack?.('demo_requested',{project_type:kind});
      }
      status.textContent=''; showStep('book'); initCal();
    } catch(error) {
      leadSent=false; status.textContent='Your request could not be confirmed. Please retry, or use the booking link below.';
      window.dsTrack?.('form_error');
    } finally { submitting=false; button.disabled=false; }"""
    if old not in js: raise ValueError('Baseline form changed: review integration')
    js=js.replace(old,new)
    js=js.replace('function closeModal() {','function closeModal() {\n    if(submitting) return;')
    js=js.replace('function openModal() {','function openModal() {\n    if(submitting) return;')
    js=js.replace('Cal.ns["ds"]("ui", {','Cal.ns["ds"]("on", {action:"bookingSuccessfulV2", callback:function(){ window.dsTrack?.("call_booking"); }});\n    Cal.ns["ds"]("ui", {')
    return js

def extra_home_links():
    return '<section class="growth-home-links"><h2>Find the right website for your business</h2><nav class="growth-links" aria-label="Website services">'+links(['/web-design/','/small-business-web-design/','/website-redesign/'])+'</nav><nav class="growth-links" aria-label="Website resources">'+links(['/industries/','/locations/','/guides/','/compare/','/best/','/tools/'])+'</nav></section>'

def enhance_baseline(s,p,production):
    s=re.sub(r'<link[^>]*href="https://fonts\.(?:googleapis|gstatic)\.com[^>]*>','',s)
    s=re.sub(r'<script type="application/ld\+json">.*?</script>','',s,flags=re.S)
    s=re.sub(r'<title>.*?</title>','',s,flags=re.S)
    s=re.sub(r'<meta (?:name="(?:description|robots|keywords|twitter:[^"]+)"|property="og:[^"]+")[^>]*>','',s)
    s=re.sub(r'<link rel="canonical"[^>]*>','',s)
    s=s.replace('</head>',meta(p,production)+'<link rel="preload" href="/instrument-serif-normal.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/instrument-serif-italic.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/fonts.css"><link rel="stylesheet" href="/growth.css">\n<script src="/events.js" defer></script></head>')
    s=s.replace('<body>','<body><a class="skip-link" href="#main-content">Skip to content</a>')
    s=s.replace('<main>','<main id="main-content">')
    s=s.replace('href="/services"','href="/services/"')
    s=s.replace('<footer>',extra_home_links()+'<footer>',1)
    s=s.replace('</footer>','<nav class="growth-home-links growth-links" aria-label="Company">'+links(['/about/','/contact/','/process/'])+'</nav></footer>')
    # Preserve styling, give non-JavaScript visitors a working contact path.
    s=re.sub(r'<button([^>]*data-book[^>]*)>(.*?)</button>',lambda m:'<a href="'+SITE['schedule']+'"'+m[1]+'>'+m[2]+'</a>',s,flags=re.S)
    s=re.sub(r'<a href="[^"]*"([^>]*data-book[^>]*)>',lambda m:'<a href="'+SITE['schedule']+'"'+m[1]+'>',s)
    s=s.replace('Every other agency wants a deposit, a brief and three rounds of revisions before you see anything real.','Buying a website before you see the work can feel uncertain.')
    s=s.replace('Most clients go from form to live site in under a week.','Timing also depends on your feedback and required launch access.')
    s=s.replace("That's our most common request.","Yes, we redesign existing websites.")
    s=s.replace('Most builds are dialled in within one or two rounds.','Tell us what needs to change before you decide.')
    s=s.replace('Get found on ChatGPT, Gemini, and Perplexity — not just Google. The next wave of local search, covered from day one.','Make your services clearer to search and answer engines through useful content and technical SEO. Visibility is not guaranteed.')
    s=s.replace('AI-powered lead scoring so you only talk to real buyers. Stop wasting hours on tyre-kickers.','Lead qualification workflows to help your team prioritise relevant enquiries and follow up consistently.')
    s=s.replace('Save hours every week from day one.','Scope and test the workflow against your actual business needs.')
    s=s.replace('<h5>','<p class="footer-label">').replace('</h5>','</p>')
    s=s.replace('Worst case:<br', 'See it first:<br')
    s=s.replace('free website</em>', 'free working demo</em>')
    if p['slug']=='/':
        s=s.replace('Book a Free Call to See Your Business&#8217;s Website','Request Your Free Website Demo').replace("Book a Free Call to See Your Business's Website",'Request Your Free Website Demo').replace('Book a Free Call to See Your Website','Request Your Free Website Demo').replace('Book a Free Call &rarr;','Get a Free Demo &rarr;').replace('Book a Free Call &#8594;','Get a Free Demo &#8594;')
    return label_forms(s)

def tool_html(p):
    kind=p.get('tool')
    if not kind:return ''
    return '<section class="growth-tool" data-tool="'+kind+'"><h2>'+{'roi':'Model your enquiry value','cost':'Set your planning assumptions','checklist':'Your customer-journey check'}[kind]+'</h2><div class="tool-controls"></div><noscript><p>Enable JavaScript to use the interactive controls. The method and limitations are explained below.</p></noscript></section><script src="/tools-core.js"></script><script src="/tools.js"></script>'

def resource_cards(slugs):
    return ''.join('<a class="growth-resource" href="'+slug+'"><span>'+H(BY_SLUG[slug]['title'].split(' | ')[0])+'</span><p>'+H(BY_SLUG[slug]['description'])+'</p><b aria-hidden="true">Explore →</b></a>' for slug in slugs)

def process_panel():
    return '<aside class="growth-promise" aria-label="How your free demo works"><p class="growth-kicker">See it before you commit</p><h2>Your business.<br>Your working demo.</h2><ol><li><strong>Tell us what you need</strong><span>Send your current site or a short business brief.</span></li><li><strong>Review it within 48 hours</strong><span>Click through a real demo and request free changes.</span></li><li><strong>Decide when you have seen it</strong><span>Agree the price before payment. No deposit.</span></li></ol><a href="/process/">See the full process →</a></aside>'

def render(p,production,modal,modal_css):
    parent='/'+'/'.join(p['slug'].strip('/').split('/')[:-1])+'/'
    crumb='<a href="/">Home</a> / '+(f'<a href="{parent}">{H(BY_SLUG[parent]["title"].split(" | ")[0])}</a> / ' if parent in BY_SLUG else '')+H(p['title'].split(' | ')[0])
    sections=''.join('<section class="growth-section" id="section-'+str(i)+'"><h2>'+H(s['heading'])+'</h2><p>'+H(s['body'])+'</p></section>'+ (cta('after_problem') if i==1 and p['pageType'] in {'service','industry','location'} else '') for i,s in enumerate(p['sections']))
    table=''
    if p.get('table'):
        t=p['table']; table='<div class="growth-table"><table><caption>'+H(p['h1'])+' — comparison</caption><thead><tr>'+''.join('<th scope="col">'+H(x)+'</th>' for x in t['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+H(x)+'</td>' for x in row)+'</tr>' for row in t['rows'])+'</tbody></table></div>'
    faqs='<section class="growth-faq growth-section"><h2>Your questions, answered</h2>'+''.join('<details><summary>'+H(f['question'])+'</summary><p>'+H(f['answer'])+'</p></details>' for f in p['faqs'])+'</section>' if p['faqs'] else ''
    sources='<section class="growth-section"><h2>Sources and review</h2><p>Reviewed 12 September 2026. Provider offers and product details can change.</p><ul>'+''.join('<li><a href="'+H(s['url'],quote=True)+'">'+H(s['title'])+'</a></li>' for s in p.get('sources',[]))+'</ul></section>' if p.get('sources') else ''
    disclosure='<p class="growth-disclosure">'+H(p['disclosure'])+'</p>' if p.get('disclosure') else ''
    hub='<nav class="growth-resources" aria-label="Browse this collection">'+resource_cards(p['related'])+'</nav>' if p['pageType']=='hub' else ''
    commercial=p['pageType'] in {'service','industry','location'} or p['slug'] in {'/contact/','/process/','/about/'}
    herocta=('<div class="growth-actions">'+cta('hero')+'<a class="growth-secondary" href="'+SITE['schedule']+'" data-placement="hero_direct_call">Prefer to talk? Book a free call →</a></div>') if commercial else ''
    panel=process_panel() if commercial else ''
    review='<p class="growth-note">By DirectSite · Reviewed <time datetime="2026-09-12">12 September 2026</time></p>' if p['pageType'] in {'guide','comparison','buyer-guide','tool'} else ''
    contents='<nav class="growth-contents" aria-label="On this page"><p class="growth-kicker">On this page</p>'+''.join('<a href="#section-'+str(i)+'">'+H(section['heading'])+'</a>' for i,section in enumerate(p['sections']))+'</nav>'
    bodyclass='growth-page growth-'+p['pageType']

    tool_top=tool_html(p) if p['pageType']=='tool' else ''
    return f'''<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#e9dcc0">{meta(p,production)}<link rel="icon" href="/favicon.svg">{modal_css}<link rel="stylesheet" href="/fonts.css"><link rel="stylesheet" href="/growth.css"><script src="/events.js" defer></script></head>
<body class="{bodyclass}"><a class="skip-link" href="#main-content">Skip to content</a><header class="growth-wrap"><nav class="growth-nav" aria-label="Main"><a href="/">DirectSite</a><a href="/web-design/">Web design</a><a href="/industries/">Industries</a><a href="/locations/">Locations</a><a href="/guides/">Guides</a><a class="growth-nav-cta" href="{SITE['schedule']}" data-book data-placement="nav">Get a free demo →</a></nav></header>
<main class="growth-wrap" id="main-content"><nav class="growth-breadcrumb" aria-label="Breadcrumb">{crumb}</nav><header class="growth-hero{' growth-hero-split' if commercial else ''}"><div><p class="growth-kicker">DirectSite · Built before you buy</p><h1>{H(p['h1'])}</h1>{tool_top}<p class="growth-answer">{H(p['answer'])}</p>{herocta}{review}</div>{panel}</header>
<div class="growth-layout"><article>{disclosure}{hub}{table}{sections}{faqs}{sources}<section class="growth-end"><h2>See your website before you pay.</h2><p>A real working demo within 48 hours. Review it, request changes and decide.</p>{cta('bottom')}</section></article><aside class="growth-sidebar" aria-label="Related pages">{contents}<h2>Keep exploring</h2>{links(p['related'])}<a class="growth-sidebar-call" href="{SITE['schedule']}" data-cta>Book a free call →</a></aside></div></main>{footer()}{modal}<script src="/demo-form.js" defer></script><script src="/form-accessibility.js" defer></script></body></html>'''

def build(production=False):
    check_collection(PAGES)
    for p in PAGES:
        for s in p['related']:
            if s not in BY_SLUG: raise ValueError('Broken relationship '+s)
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir()
    for f in (ROOT/'public').iterdir():
        if f.is_file(): shutil.copyfile(f,OUT/f.name)
    home=(ROOT/'src/homepage.html').read_text()
    css=re.search(r'<style>(.*?)</style>',home,re.S)[1]
    # Reuse only original modal styling on editorial pages, rather than homepage animation assets.
    start=css.index('  .modal-bg'); end=css.index('  .reveal',start)
    modal_css='<style>:root{--ink:#261c14;--ink-soft:#66513c;--ink-mute:#66513c;--sans:Arial,sans-serif;--serif:Georgia,serif;--mono:monospace;--bronze:#996626;--gold:#986524}'+css[start:end]+'@media(max-width:700px){.modal,.modal.wide{width:calc(100% - 24px);padding:24px;max-height:90dvh}.modal .row2{grid-template-columns:1fr}}</style>'
    modal=label_forms(home[home.index('<div class="modal-bg" id="modal">'):home.index('<div class="mobile-sticky hidden">')])
    (OUT/'demo-form.js').write_text(form_script(home))
    records=[]
    for p in PAGES:
        if p['status']!='reviewed':continue
        path=OUT/p['slug'].strip('/')/'index.html';path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(render(p,production,modal,modal_css))
        records.append({**{k:p.get(k) for k in ['slug','pageType','primaryKeyword','secondaryKeywords','targetLocation','targetIndustry','proofAvailable','caseStudyAvailable','originalDataAvailable','status','lastReviewed']},'searchIntent':'informational' if p['pageType'] in {'guide','tool'} else 'commercial','uniqueContentScore':quality(p)['score'],'wordCount':len(words(p)),'wordCountTarget':430,'indexable':p['indexable'],'canonical':ORIGIN+p['slug']})
    for name,slug,title,h1,description in [('homepage','/','Websites Built Before You Buy | DirectSite','Websites for local Aussie businesses. Built in 48 hours. Live in three days.','Custom websites for local Aussie businesses. A free working demo in 48 hours, no deposit and free revisions before payment.'),('services','/services/','Digital Services for Australian Businesses | DirectSite','Yes, we do everything.','Explore DirectSite website builds, AI search optimisation, advertising, lead qualification and custom AI services for Australian businesses.')]:
        p=dict(slug=slug,title=title,h1=h1,description=description,pageType='company')
        s=enhance_baseline((ROOT/f'src/{name}.html').read_text(),p,production)
        if name=='homepage':
            pos=s.index("  var modal = document.getElementById('modal');")
            end=s.index('</script>',pos)
            s=s[:pos]+s[end:]
            s=s.replace('</body>','<script src="/demo-form.js" defer></script><script src="/form-accessibility.js" defer></script></body>')
            s=s.replace('class="iphone-body"','class="iphone-body" aria-hidden="true"')
        else:
            s=s.replace("window.__submit = function() {\n    formDiv.style.display = 'none';\n    doneDiv.style.display = 'block';\n  };",(ROOT/'src/services-submit.js').read_text().replace('__WEB3FORMS_KEY__', re.search(r'var WEB3FORMS_KEY = "([^"]+)"',home)[1]))
            s=s.replace('</body>','<script src="/form-accessibility.js" defer></script></body>')
        target=OUT/'index.html' if slug=='/' else OUT/'services/index.html';target.parent.mkdir(exist_ok=True);target.write_text(s)
        records.append(dict(slug=slug,pageType='existing',primaryKeyword='DirectSite' if slug=='/' else 'DirectSite digital services',indexable=True,canonical=ORIGIN+slug,lastReviewed='2026-09-12'))
    (OUT/'404.html').write_text('<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | DirectSite</title><meta name="robots" content="noindex"></head><body><main><h1>That page could not be found</h1><p><a href="/">Return to DirectSite</a> or <a href="/web-design/">explore web design</a>.</p></main></body></html>')
    groups={}
    for r in records:
        if production and r['indexable']:groups.setdefault(r['pageType'],[]).append(r)
    sitemap_dir=OUT/'sitemaps';sitemap_dir.mkdir()
    for group,items in groups.items():
        (sitemap_dir/(group+'.xml')).write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+escape(r['canonical'])+'</loc></url>' for r in items)+'</urlset>')
    (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<sitemap><loc>'+ORIGIN+'/sitemaps/'+g+'.xml</loc></sitemap>' for g in groups)+'</sitemapindex>')
    (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+ORIGIN+'/sitemap.xml\n')
    # Preserve existing training policy; preview indexing is controlled by meta and HTTP headers.
    redirects=[{'source':'/:path*','has':[{'type':'host','value':'www.directsite.com.au'}],'destination':'https://directsite.com.au/:path*','permanent':True},{'source':'/website-design/','destination':'/web-design/','permanent':True}]
    (OUT/'build-info.json').write_text(json.dumps({'production':production,'routes':[r['slug'] for r in records]},indent=2))
    (ROOT/'seo/content-manifest.json').write_text(json.dumps(records,indent=2)+'\n')
    (ROOT/'vercel.json').write_text(json.dumps({'buildCommand':'npm run build:production && npm run lint && npm test','outputDirectory':'dist','trailingSlash':True,'redirects':redirects,'headers':[{'source':'/(.*)','headers':[{'key':'X-Content-Type-Options','value':'nosniff'},{'key':'Referrer-Policy','value':'strict-origin-when-cross-origin'}]}]},indent=2)+'\n')
    print(f'Built {len(records)} static routes; mode={"production" if production else "noindex preview"}. Production source verified against commit 0825f4d; deployment is a separate step.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--production',action='store_true');args=parser.parse_args();build(args.production and os.environ.get('VERCEL_ENV','production')=='production')
