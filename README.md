# DirectSite organic growth implementation

Deployed to https://directsite.com.au on 12 September 2026 from `arjun181105/DirectSite`. Production source was verified against commit `0825f4d`; PR #1 merged as `28186cd`. The site has 32 indexable routes. Google Search Console and Bing received the sitemap; www permanently redirects to apex. A labelled service enquiry was accepted and its inbox delivery verified. GA4 is deployed with visitor opt-in; Realtime pageviews and an accepted test lead are verified. Completed-booking verification remains outstanding. Client proof is excluded, email/legal name unchanged, no terms page requested. Six-month enquiry retention is recorded in `seo/RETENTION.md`; provider deletion automation is not yet configured.

## Run and verify

Requires Python 3.10+ and a current Node.js version supported by Lighthouse 13 (Node 22.19+ recommended).

```sh
npm ci
npm run build
npm run lint
npm test
npm run preview
```

Open http://127.0.0.1:8765. Default output deliberately uses `noindex`; its sitemap is empty. The local server always sends `X-Robots-Tag: noindex`, including when inspecting production output.

```sh
npm run build:production
npm run lint
npm test
npm run audit:http
```

Production builds emit 32 indexable routes and a segmented sitemap index. They do not deploy. `npm run build` restores preview mode. The Vercel build runs `npm run build:production && npm run lint && npm test`; `dist` is the output directory. The build regenerates `vercel.json`; change hosting rules in `scripts/build.py`.

## Edit the site

- `content/pages.json`: 30 authored pages, visible answers, sections, FAQs, sources, relationships and review evidence.
- `src/homepage.html`, `src/services.html`: recovered public baselines. `scripts/build.py` adds shared metadata, navigation, corrected forms and assets.
- `public/`: responsive styles, calculator logic, tracking, keyboard accessibility and licensed self-hosted fonts.
- `scripts/content_model.py`: publication gate. The numeric score cannot override a failed gate.
- `seo/content-manifest.json`: generated implemented-route inventory. Its `indexable` describes production eligibility; preview output remains noindex.
- `seo/planned-manifest.json`: 51 unpublished future routes. None are rendered automatically.
- `seo/briefs.json`: 81 structured records. Implemented briefs contain actual content structure; future briefs are evidence-required scaffolds, not finished articles.
- `content/case-study.template.json`: permissioned project intake. Complete visible content fields and evidence before adding an entry to pages.json.

Run `npm run research:plan` after content changes. This refreshes planning files and resets the case-study intake template, so keep completed client records in separate files. It preserves existing AI citation observations.

## Forms and analytics

The existing public Web3Forms browser key and Cal.com routes are retained. HTTP/API acceptance is checked before success. The key is a public client-side integration identifier, not an admin credential. Verify its domain restrictions, spam settings and intended recipient in the account. Mocked submissions cover acceptance, errors and retries. A live services enquiry reached the existing recipient inbox on 12 September 2026. Cal.com opens with available slots and the expected details form; a real completed booking remains unverified.

Local-only `?__qa__=success`, `reject` or `network` loads a test harness that intercepts submissions and Cal. Never deploy the preview server or test harness. Normal local preview can send real enquiries: use the QA query when testing forms.

`public/events.js` emits allowlisted `dataLayer` and DOM events. The deployed `public/analytics.js` connects them to GA4 after visitor opt-in; see `seo/ANALYTICS.md` for verified status. Do not send form values, email, phone, raw query strings or booking payloads to analytics. Test accepted leads separately from calendar links and actual booking events. Session-level attribution requires analytics configuration; current source classification is page-local.

## Research and maintenance

- `seo/REPORT.md`: all 17 requested handover deliverables and next actions.
- `seo/ARCHITECTURE.md`: route, indexing, schema and conversion design.
- `seo/audit/`: static, HTTP, browser and lab-performance evidence.
- `seo/research/`: 226 discovery query records, competitor inspections and outreach prospect ideas.
- `seo/benchmark/METHODOLOGY.md`: proposed sample and reproducible measurement pipeline. A 20-site discovery pilot has 18 observed records and two unavailable sites; no population findings are published.
- `seo/monitoring/README.md`: evidence-backed monthly AI-answer measurement workflow. No recurring automation was created.

Production rollout: compare against current source; preserve unrelated features and verified old URLs; deploy a protected preview; confirm forms in controlled account tests; check production canonical/redirect/indexing behavior; then submit the production sitemap through Search Console and Bing. Do not expose a preview domain as indexable. Keep the existing deployment available for rollback.

Vercel previews automatically use noindex and an empty sitemap through the VERCEL_ENV check, even when the configured command includes --production. The existing Vercel preview authentication remains enabled. Do not change it to bypass verification.
