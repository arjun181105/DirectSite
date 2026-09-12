# DirectSite SEO, GEO and conversion handover

12 September 2026 · 32 routes deployed to production.

The production repository was identified and its baseline verified before integration. PR #1 merged into `arjun181105/DirectSite` and Vercel published the build at https://directsite.com.au. All 32 production routes passed status, canonical and indexability checks. The ten segmented sitemaps cover those 32 routes. Google Search Console and Bing accepted the sitemap index; Bing is processing it. A permanent www-to-apex redirect is active.

A labelled synthetic services enquiry was accepted by Web3Forms and verified in the existing recipient inbox. The Cal.com handoff displays available appointments and a details form; completed booking verification is outstanding. GA4 is deployed with visitor opt-in and optional account sharing disabled. Realtime received pageviews and a labelled accepted test enquiry; generate_lead is a key event.

Client proof is excluded by request. Email and legal trading name are unchanged. No terms page is requested. Enquiry retention is six calendar months; see `RETENTION.md`. Provider deletion automation has not been configured. Rankings, AI citations and revenue changes are not claimed.

## 1. What the audit discovered

The public sitemap listed only the homepage and services page. Both deliver static HTML through Vercel. The existing core offer was strong but had little dedicated content for trade, location or buyer intent. Homepage enquiry code advanced without validating the API result; services displayed success without making a submission. Those are direct conversion risks regardless of rankings.

The public robots file allowed crawling and linked its sitemap. HTTP apex redirected to HTTPS. HTTPS www returned 200 rather than redirecting to apex; canonical consolidation was incomplete. No GA4/GTM integration was found in the recovered page source. This does not prove there is no account-side measurement.

One live mobile Lighthouse run scored performance 82, accessibility 97 and SEO 100, with lab LCP 3.3 seconds and CLS 0.027. These are a dated lab observation, not field Core Web Vitals or a representative sample. The production framework, backend, deployment history, search traffic and indexing status cannot be established from public HTML.

## 2. What was implemented

A Python static generator, structured content model and publication gate; 30 authored pages plus the two retained baseline pages; six content hubs; repaired lead handling; shared accessible demo modal; three interactive tools; metadata and entity graph; internal links; segmented sitemaps; canonical/redirect configuration; self-hosted licensed fonts; source-backed research records; benchmark and AI monitoring infrastructure; executable QA.

Both production and preview builds pass validation. Thirteen Python tests plus JavaScript calculator, form and event checks pass. All 32 local routes returned 200, deliberate missing routes returned 404 and alias/slash redirects worked. The original 29 routes rendered at narrow width without horizontal overflow. All 32 local mobile Lighthouse runs scored 98–100 performance and 100 accessibility. Preview Lighthouse SEO scored 66 because the preview deliberately blocks indexing. The production static audit separately verifies indexability and sitemap inclusion. No production Lighthouse score for this implementation is claimed.

## 3–4. Pages and primary keywords

Paths below are deployed. Primary keywords express intended ownership, not achieved ranking.

| Path | Primary keyword | Status |
|---|---|---|
| `/industries/plumbers/` | web design for plumbers | New |
| `/industries/electricians/` | web design for electricians | New |
| `/industries/roofers/` | web design for roofers | New |
| `/industries/builders/` | web design for builders | New |
| `/industries/tradies/` | web design for tradies | New |
| `/industries/landscapers/` | web design for landscapers | New |
| `/industries/cleaners/` | web design for cleaners | New |
| `/industries/hvac/` | web design for hvac | New |
| `/web-design/` | custom web design australia | New |
| `/small-business-web-design/` | small business web design australia | New |
| `/website-redesign/` | website redesign australia | New |
| `/locations/melbourne/` | web design melbourne | New |
| `/guides/website-cost-australia/` | how much does a website cost in australia | New |
| `/guides/how-long-does-a-website-take/` | how long does it take to build a website | New |
| `/guides/small-business-website-checklist/` | what should a small business website include | New |
| `/compare/wix-vs-custom-website/` | wix vs custom website australia | New |
| `/compare/wordpress-vs-custom/` | wordpress vs custom website | New |
| `/best/web-design-companies-melbourne/` | best web design companies melbourne | New |
| `/tools/website-roi-calculator/` | website roi calculator | New |
| `/tools/website-cost-calculator/` | website cost calculator australia | New |
| `/tools/tradie-website-checklist/` | tradie website checklist | New |
| `/about/` | about directsite | New |
| `/process/` | directsite website process | New |
| `/contact/` | contact directsite | New |
| `/industries/` | website design by industry | New |
| `/locations/` | web design locations australia | New |
| `/guides/` | small business website guides | New |
| `/compare/` | website platform comparison | New |
| `/best/` | web design company buyer guides | New |
| `/tools/` | free website planning tools | New |
| `/` | DirectSite | Retained and enhanced |
| `/services/` | DirectSite digital services | Retained and enhanced |

## 5. Technical SEO changes

Unique titles, descriptions, H1s, absolute canonicals and social metadata; server-readable HTML; coherent trailing-slash routes; real 404 handling; `/website-design/` consolidation; Vercel www-to-apex redirect configuration; production-only sitemap inclusion; noindex preview; descriptive navigation and breadcrumbs. Fonts are self-hosted with license notices and optional loading. Form controls have labels and keyboard focus management. A deceptive unconditional success state was removed from both enquiry flows.

The static validator checks links, structured-data graphs, metadata and sitemap membership. It is not Google's Rich Results Test or Search Console URL Inspection. Production HTTP redirects and declared canonicals are verified; search-engine canonical selection, field caching behaviour and crawler-specific WAF access remain unverified. No fabricated field-performance report or external validator pass is recorded.

## 6. GEO / answer-engine changes

Commercial pages state the business served and concrete customer tasks. Informational pages give concise answers near the top, followed by useful detail and source links. Price examples are provider-specific, not unsupported averages. The Melbourne buyer guide discloses the publisher's interest, uses a small unranked shortlist and gives readers criteria for independent comparison. About/process/contact strengthen a consistent entity without inventing staff, offices or credentials.

Google's ordinary SEO requirements also apply to AI Overviews and AI Mode; no special AI markup is required. [Google's guidance](https://developers.google.com/search/docs/appearance/ai-features). OAI-SearchBot and GPTBot serve independent purposes; the live permissive robots policy is preserved. [OpenAI crawler documentation](https://developers.openai.com/api/docs/bots).

No AI citation or recommendation outcome has been measured. Clear structure supports retrieval eligibility; it cannot guarantee inclusion.

## 7. Internal linking architecture

Homepage → core services and hubs → relevant industry/location/editorial pages. Children link back through breadcrumbs and to related services, cost guidance and planning tools. Footer links establish company/process/contact. All implemented pages are reachable. There is no automatic city-by-industry multiplication. A plumber page addresses urgent calls and planned quotes; electrician, roofer and builder pages cover distinct qualification decisions. Melbourne describes remote delivery and uses local sources without claiming an office.

## 8. Schema added

Stable Organization and WebSite identities with page-specific WebPage, Service or Article and BreadcrumbList nodes. Visible publisher and review information match the graph. No invented LocalBusiness address, review aggregate, ratings or personal author is used. Visible FAQs remain useful content without unsupported promises of FAQ rich results. Schema validation is structural and local; post-deployment Google inspection remains outstanding.

## 9. Tools and assets

- **Website ROI calculator:** editable visitors, enquiry rates, close rate, customer value, margin and cost; shows incremental value and conditional payback. Assumptions are illustrative.
- **Website cost calculator:** explicit hours and rate assumptions; useful for scoping, not a DirectSite quote or researched market price.
- **Tradie website checklist:** 14 manual customer-journey checks, optional local save, reset and print. It is not an automated SEO certification.
- **Annual benchmark pipeline:** safe public-site scanner, proposed stratified sample, raw evidence and summary format. A nonrandom 20-site pilot produced 18 static observations and two unavailable records. No population statistic or quotable benchmark finding is published.
- **Case-study intake:** genuine client situation, changes, screenshots, dated metrics and publication consent. No fabricated example is indexed.

## 10. Research completed

226 query records cover the specified head, metro, industry, comparison and question families. Each has live search-discovery observations and raw source URL/title evidence. Australia was requested through query wording, not a verified Australian Google location setting. Result ordering is not represented as ranking.

Four primary competitor pages were directly inspected: [VisualWeb](https://visualweb.com.au/web-design-melbourne/), [Tradie Web Guys](https://www.tradiewebguys.com.au/), [Chromatix](https://www.chromatix.com.au/) and [Bold](https://www.boldagency.com.au/web-design/melbourne). Stored audits contain titles, headings, links and approximate static content depth. Search discovery also repeatedly surfaced directories and forums. Frequencies are query-level discovery counts, not backlinks, market share or AI citation counts.

**What competitors have that DirectSite lacks:** visible relevant project proof, deeper specialised service/location coverage, and—in VisualWeb's case—published scope/pricing examples. These are observed competitive assets, not a causal explanation of their Google rankings.

**What DirectSite can create that they cannot copy from DirectSite:** permissioned demo-to-launch timelines, real enquiry-delivery tests, transparent scope comparisons and a reproducible Australian website benchmark. These would be original to DirectSite. We have not established that no competitor anywhere has similar assets.

81 structured briefs and a 51-route unpublished backlog support future work. Completed-page briefs reflect authored content; future briefs remain planning scaffolds with evidence requirements and some intentionally unknown metadata. They need detailed editorial completion before publication.

## 11. Research still requiring additional access

Australian Google SERP positions, map packs, PAA, featured snippets, actual AI Overviews/AI Mode answers and cited URLs remain unverified. ChatGPT Search citation observations are also unmeasured. Forty prompt/platform records retain unknown values. No observed result is inferred from absence in a search-tool response.

Required next evidence: controlled locale-specific browser sessions or authorised SERP data; Search Console exports and inspection; Bing data; verified backlink reports; actual case studies; the predeclared benchmark sample; PageSpeed/CrUX data where available. The benchmark has infrastructure but no collected representative findings. New city pages require their own local evidence.

## 12. Biggest opportunities

Prioritise qualified trade and redesign enquiries before broad traffic. A small number of real plumber/electrician/builder projects would strengthen the existing commercial pages more than hundreds of synthetic suburb pages. Publish scope boundaries and permissioned outcomes. Link the usable calculators and checklist from genuine partner/editorial resources. Then collect the benchmark with a defensible sample and use findings to improve both content and product delivery.

Measure accepted leads, qualified calls and paying clients by landing page. Expand topics using actual GSC demand and customer questions. Refresh provider comparisons quarterly and immediately after material offer changes; update business claims whenever fulfilment changes.

## 13. Biggest risks and limits

Production source and deployment mapping are verified. The live services enquiry test reached the existing inbox. Domain restrictions and anti-spam settings remain account-side checks. The calendar handoff works; a real completed booking has not been tested.

GA4 collection and accepted-lead receipt are verified after visitor opt-in. Six-month enquiry retention is a recorded policy, not verified provider automation. Email and legal name are unchanged and no terms page is requested. Client proof is excluded. The quality gate does not replace editorial review or search demand, and rankings, citations and revenue remain unproven. Vercel preview builds automatically emit noindex and empty sitemaps even when the build command includes --production.

## 14. Next 20 pages

This is an editorial sequence based on offer fit and distinct customer needs, not measured search volumes. Client proof is deferred and terms are excluded by request. The first three entries below are now deployed; the remaining entries require completed briefs and evidence. Each planned page remains unpublished until its brief and evidence are complete.

| Priority | Path | Primary keyword |
|---|---|---|
| 1 | `/industries/landscapers/` | web design for landscapers |
| 2 | `/industries/cleaners/` | web design for cleaners |
| 3 | `/industries/hvac/` | web design for hvac |
| 4 | `/locations/sydney/` | web design sydney |
| 5 | `/locations/brisbane/` | web design brisbane |
| 6 | `/guides/website-seo-guide/` | website seo guide |
| 7 | `/guides/website-conversion-guide/` | website conversion guide |
| 8 | `/ecommerce-web-design/` | ecommerce web design |
| 9 | `/industries/concreters/` | web design for concreters |
| 10 | `/industries/painters/` | web design for painters |
| 11 | `/industries/solar/` | web design for solar |
| 12 | `/locations/perth/` | web design perth |
| 13 | `/locations/adelaide/` | web design adelaide |
| 14 | `/industries/mortgage-brokers/` | web design for mortgage brokers |
| 15 | `/industries/accountants/` | web design for accountants |
| 16 | `/industries/dentists/` | web design for dentists |
| 17 | `/compare/squarespace-vs-web-designer/` | squarespace vs web designer |
| 18 | `/compare/freelancer-vs-web-design-agency/` | freelancer vs web design agency |
| 19 | `/best/web-design-for-tradies/` | best web design for tradies |
| 20 | `/research/australian-small-business-website-benchmark-2026/` | australian small business website benchmark 2026 |

## 15. Backlink priorities

1. Permissioned client project write-ups and authentic partner references. Do not require clients to insert keyword-rich links.
2. Trade associations, beginning with [Master Plumbers](https://plumber.com.au/), where eligibility and editorial relevance are verified; offer the checklist or measured trade findings.
3. Original benchmark pitches to [SmartCompany](https://www.smartcompany.com.au/) and [Dynamic Business](https://dynamicbusiness.com/), after data collection and review.
4. Relevant podcast/editorial opportunities such as [The Site Shed](https://www.thesiteshed.com/); assess commercial conflicts and guest criteria first.
5. Accurate business profiles on relevant directories and chambers where eligible. No bulk spam, invented reviews or purchased ranking links.

The prospect dataset records verification limits and asset ideas. No contact person, placement, backlink or outreach response is invented; no outreach has been sent.

## 16. Exact queries to monitor

Track all commercial primary keywords in the table above, plus these question prompts monthly across Google Search, AI Overviews, AI Mode and ChatGPT Search:

- Who are the best web designers in Melbourne?
- What are the best web design companies in Australia?
- Who builds good websites for plumbers in Melbourne?
- What web design agency specialises in tradies?
- Who should I hire to redesign my small business website in Australia?
- How much does a website cost in Australia?
- What should a plumber website include?
- What should a tradie website include?
- Is Wix or a custom website better for a small business?
- What are the best affordable web design companies in Melbourne?

Record date, market/location, signed-in state, prompt, actual answer/position context, DirectSite mention, competitors, source URLs and retained evidence. Distinguish “feature not shown,” “unavailable” and an observed answer that omits DirectSite. The CLI calculates mention rates only over observed answers. No scheduled automation was created. Use the monitoring README and observation template.

## 17. Access and data for the next iteration

Production GitHub, Vercel, Search Console and Bing are connected. Remaining integration work: accept Google's Analytics agreement, create the web stream and verify GA4 events; complete a controlled booking test; verify provider retention/deletion settings and Web3Forms restrictions; connect CRM outcomes if available. No client proof or terms page is requested.

## DO THIS NEXT

1. Complete the pending Google Analytics legal agreement, create a web stream, install its measurement ID and verify accepted-lead and booking events.
2. Complete a controlled booking test and remove the test booking afterward.
3. Implement and verify six-month enquiry deletion in the actual providers without affecting unrelated messages.
4. Complete future briefs from observed demand and collect a defensible benchmark sample. Publish only reviewed pages and supported findings.
5. Recheck Search Console and Bing after processing to assess indexing; submissions alone do not establish indexing or rankings.
