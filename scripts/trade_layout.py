"""Clean, homepage-aligned presentation for DirectSite's priority trade pages."""
import html

H = html.escape


def render_trade(p, meta, production, modal, modal_css, cta, footer, links, site_nav):
    t = p['trade']
    jobs = ''.join('<span>' + H(job) + '</span>' for job in t['jobs'])
    offers = [
        ('Website', 'A fast, polished site that makes your services and next step clear.'),
        ('SEO', 'Useful service content, technical SEO and local visibility work.'),
        ('Growth', 'Focused ads, enquiry routing and follow-up workflows when you need them.'),
    ]
    cards = ''.join(
        '<article class="trade-offer"><p>' + label + '</p><h3>' + copy + '</h3></article>'
        for label, copy in offers
    )
    primary = ''.join(
        '<section class="trade-detail" id="section-' + str(i) + '"><p class="trade-number">0' + str(i + 1) + '</p><div><h2>' + H(section['heading']) + '</h2><p>' + H(section['body']) + '</p></div></section>'
        for i, section in enumerate(p['sections'][:3])
    )
    more = ''.join(
        '<section><h3>' + H(section['heading']) + '</h3><p>' + H(section['body']) + '</p></section>'
        for section in p['sections'][3:]
    )
    faqs = ''.join(
        '<details><summary>' + H(faq['question']) + '</summary><p>' + H(faq['answer']) + '</p></details>'
        for faq in p['faqs']
    )
    sources = ''.join(
        '<li><a href="' + H(source['url'], quote=True) + '">' + H(source['title']) + '</a></li>'
        for source in p['sources']
    )
    return f'''<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f4ead5">{meta(p,production)}<script>document.documentElement.classList.add("site-nav-ready")</script><link rel="icon" href="/favicon.svg">{modal_css}<link rel="stylesheet" href="/fonts.css"><link rel="stylesheet" href="/growth.css"><link rel="stylesheet" href="/trades.css"><script src="/events.js" defer></script><script src="/site-nav.js" defer></script></head>
<body class="growth-page trade-page trade-{t['theme']}"><a class="skip-link" href="#main-content">Skip to content</a><header class="growth-wrap">{site_nav()}</header>
<main id="main-content"><div class="growth-wrap"><nav class="growth-breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/industries/">Industries</a> / {H(t['label'])}</nav>
<header class="trade-hero"><p class="growth-kicker">Websites and growth for {H(t['label'])}</p><h1>{H(p['h1'])}</h1><p class="growth-answer">{H(p['answer'])}</p><div class="trade-jobs" aria-label="Featured services">{jobs}</div><div class="growth-actions">{cta('trade_hero')}<a class="trade-text-link" href="#services">See what we can do ↓</a></div></header>
<section class="trade-services" id="services"><div class="trade-section-head"><p class="growth-kicker">Start with what matters</p><h2>One clear site. The right support around it.</h2></div><div class="trade-offers">{cards}</div></section>
<div class="trade-details">{primary}</div>
<details class="trade-more"><summary>More ways we can help {H(t['label'])} businesses</summary><div>{more}</div></details>
<section class="trade-start"><div><p class="growth-kicker">Built before you buy</p><h2>See your website before you commit.</h2><p>A real working demo within 48 hours. Review it, request changes and agree the price before payment.</p></div><div>{cta('trade_bottom')}</div></section>
<section class="trade-faq growth-faq"><div><p class="growth-kicker">Common questions</p><h2>What you may want to know.</h2></div><div>{faqs}</div></section>
<nav class="trade-related" aria-label="Related resources"><h2>Keep exploring</h2>{links(p['related'])}</nav><details class="trade-research"><summary>Research behind this page</summary><p>Reviewed <time datetime="{p['lastReviewed']}">16 September 2026</time>. Sources inform our recommendations and are not endorsements. Provider features can change.</p><ul>{sources}</ul></details>
</div></main>{footer()}{modal}<script src="/demo-form.js" defer></script><script src="/form-accessibility.js" defer></script></body></html>'''
