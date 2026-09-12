# Australian Small Business Website Benchmark 2026

Status: pipeline implemented; no representative sample collected, no findings published.

Proposed sample: 100 unique Australian small-business domains, balanced across five industries (plumbing, electrical, roofing, building, cleaning) and four metropolitan areas (Melbourne, Sydney, Brisbane, Perth): five per industry–city cell. This is a proposed stratified descriptive sample, not a population estimate. It excludes ecommerce-only businesses and web agencies. Define small-business eligibility and evidence before recruiting the sample; do not imply headcount can be inferred from a homepage.

Create a dated sampling frame from public business directories or association membership lists whose terms permit research. Store source URL, selection reason, industry, location and inclusion/exclusion decisions. Deduplicate by registrable business/domain, record a deterministic random seed and retain the eligible frame. Missing sites are nonresponses, not automatic failures. Replacements must follow a predeclared selection order. Never sample only poor-performing sites to make a headline.

The scanner processes only explicitly listed HTTPS hostnames. It rejects private IPs and cross-host redirects, pins the checked address, verifies TLS, respects robots, pauses between requests, limits redirects and caps each HTML response at 2 MB. It makes no authenticated requests and submits no forms. A blocked or unavailable site is recorded, not worked around. Raw HTML, response headers, UTC timestamp and SHA-256 remain alongside each observation.

Static metrics: HTML bytes, title, description, number of tel links and form elements. These do not establish visible calls to action or a working form. HTML bytes are not image weight. Request duration is not LCP or page-load duration. A single-page scan does not establish page count.

Manual protocol: use a documented 390×844 viewport at 100% zoom. Record visible phone, above-fold CTA, service-area clarity, review evidence, keyboard use and quote process; distinguish unknown from absent. Do not submit test enquiries to unrelated businesses. Record screenshots only with an appropriate basis for retaining and publishing them, and remove personal data from publication outputs.

Performance extension: collect PageSpeed mobile and desktop lab reports using an operator-supplied Google API key, preserving request settings, report timestamp and raw report. Use three lab runs and report the median, not the best. Store CrUX field data separately; missing field data means insufficient/unavailable data, not failure. Never label a Lighthouse lab score a Core Web Vitals pass.

Statistics: publish sample n and denominator for every measurement and breakdown. Report medians and distributions for continuous measures. Disclose sample-frame and selection bias. Do not generalise a five-site cell to an entire industry. A second reviewer must verify a subset of manual observations and resolve differences before publication.

Run `python3 scripts/benchmark.py` to generate empty, honest summary outputs. After constructing the sample file, `--scan` performs public requests. Each entry requires `id`, `url`, `industry`, `location`, `selectionReason`, `sourceUrl`. No chart or quotable finding is generated from an empty sample. The report remains gated until sample review, measurement validation and publication rights are complete.
