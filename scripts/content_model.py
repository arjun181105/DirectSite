"""Shared content validation. A score alone cannot publish a page."""
import re
from urllib.parse import urlparse

TYPES = {'service', 'industry', 'location', 'guide', 'comparison', 'buyer-guide', 'tool', 'hub', 'company', 'case-study', 'research'}

def words(page):
    return re.findall(r"\b[\w'-]+\b", ' '.join([page.get('answer', ''), *[s['body'] for s in page.get('sections', [])], *[f['answer'] for f in page.get('faqs', [])]]))

def quality(page):
    reasons = []
    if page['pageType'] not in TYPES: reasons.append('unknown page type')
    if not re.fullmatch(r'/[a-z0-9/-]*/', page['slug']): reasons.append('invalid route')
    if page.get('status') != 'reviewed': reasons.append('editorial review required')
    if not page.get('qualityEvidence'): reasons.append('missing unique-value review')
    if not page.get('primaryKeyword'): reasons.append('missing intent')
    if len(page.get('related', [])) < 2: reasons.append('needs contextual links')
    minimum = 160 if page['pageType'] in {'hub', 'company', 'tool'} else 430
    if len(words(page)) < minimum: reasons.append(f'needs substantive content ({len(words(page))}/{minimum} words)')
    if page['pageType'] in {'industry','location','service'} and len(page.get('faqs',[])) < 3: reasons.append('needs specific FAQs')
    if page['pageType'] == 'location' and not page.get('sources'): reasons.append('local evidence required')
    if page['pageType'] in {'case-study','research'} and not page.get('proofAvailable'): reasons.append('verified evidence required')
    if page['pageType'] in {'case-study','research'} and not page.get('evidence'): reasons.append('evidence records required')
    if page['pageType'] == 'case-study' and not page.get('publicationPermission'): reasons.append('publication permission required')
    if page['pageType'] == 'buyer-guide' and (not page.get('disclosure') or len(page.get('sources',[])) < 3): reasons.append('comparison evidence and disclosure required')
    for source in page.get('sources',[]):
        if urlparse(source['url']).scheme != 'https': reasons.append('invalid source URL')
    score = min(100, 20 + min(len(words(page)) // 20,30) + min(len(page.get('sections', []))*5,25) + min(len(page.get('faqs', []))*5,15) + (10 if page.get('qualityEvidence') else 0))
    return {'score': score, 'passed': not reasons, 'reasons': reasons}

def check_collection(pages):
    for field in ('slug','title','h1','description','primaryKeyword'):
        vals = [p[field].casefold() for p in pages]
        if len(vals) != len(set(vals)): raise ValueError(f'duplicate {field}')
    # Detect copied paragraphs independently of editor-supplied quality scores.
    owners = {}
    for p in pages:
        for section in p.get('sections', []):
            body = re.sub(r'\W+', ' ', section['body']).strip().lower()
            if len(body.split()) > 55 and body in owners: raise ValueError(f'duplicate section: {p["slug"]} and {owners[body]}')
            owners[body] = p['slug']
        result = quality(p)
        if p.get('indexable') and not result['passed']: raise ValueError(f'{p["slug"]}: {result["reasons"]}')
