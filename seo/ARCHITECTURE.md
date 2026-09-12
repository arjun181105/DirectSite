# Architecture and operating rules

## Rendering and intent ownership

Python generates crawlable HTML, with JavaScript only for interactive controls and forms. No JavaScript rendering is needed to read the page content, navigation, canonicals or JSON-LD. The homepage owns the brand and offer; `/web-design/` owns broad Australian service intent; `/small-business-web-design/` narrows the buyer; `/website-redesign/` addresses migration and existing sites. `/website-design/` redirects to `/web-design/` to consolidate synonymous intent.

Industry and location hubs connect to individually authored pages. No city × industry × suburb multiplication exists. Melbourne has real sources and an explicit remote-service position. Additional metros remain unpublished. Hubs return contextual links from children via breadcrumbs; commercial pages link to relevant cost guidance, comparisons and tools. All rendered routes are reachable from the homepage. Shared company links expose about, process and contact.

## Publication gate

`check_collection` rejects duplicate slugs, titles, H1s, descriptions, primary keywords and long copied sections. Indexable entries require a reviewed status, documented unique value, explicit keyword and at least two related pages. Commercial/editorial pages require at least 430 substantive words; hubs, company and tool pages require 160. These are editorial safeguards, not Google word-count rules. Location pages require sources; commercial pages require specific FAQs. Buyer guides require disclosure and at least three sources. Research and case studies require evidence; case studies also require publication permission.

The gate does not prove expertise, verify every claim or detect semantic paraphrase. A human editor must verify truth, usefulness, permissions and freshness before each production expansion. `reviewed` currently records the implementation review, not business-owner sign-off. Do not turn on `indexable` to bypass missing evidence.

## URLs, metadata and crawling

Canonical origin: `https://directsite.com.au`; lowercase, trailing-slash content URLs. The Vercel config adds a permanent www-to-apex host redirect and `/website-design/` alias redirect. Verify both on the connected project after deployment. HTTP-to-HTTPS is already observed live. Query variants canonicalize to clean paths. Missing pages return 404 locally and use the static 404 document on hosting.

Every generated page has a unique title, description and H1, absolute canonical, social metadata and descriptive links. Production creates a sitemap index segmented by type and excludes unpublished routes. Preview builds include noindex and an empty sitemap. The local preview server adds a noindex header; Vercel preview deployments must also be protected/noindex at the hosting level because the configured production command emits indexable HTML.

Robots preserves the live wildcard Allow policy. OAI-SearchBot access and GPTBot training access are independent; neither explicit group was needed to preserve the user's existing policy. Robots text does not establish real WAF access for verified bots. Confirm with hosting logs.

## Schema and answer retrieval

A stable Organization and WebSite entity supports per-page WebPage, Service or Article nodes and BreadcrumbList. Sources and author/review attribution are visible. No fabricated person, address, review score, aggregate rating or LocalBusiness office is declared. Visible FAQs support readers without promising FAQ rich results. There is no special AI schema, fake citation markup or keyword-only crawler page.

Informational answers appear near the top, followed by details, comparisons where useful and sources. Published price examples identify the provider and GST basis; they are not market averages or a DirectSite quote. Buyer guides disclose DirectSite's interest and avoid invented objective rankings.

## Conversion and tools

A reusable demo form is available on each authored page with a real Cal fallback for visitors without JavaScript. Industry/service/location pages have hero, mid-page and final CTA placements. The 48-hour demo, no deposit, free prepayment revisions and $0 rejection promise are retained. Launch timing is tied to approval and required access.

The form waits for HTTP success and JSON `success: true`, disables repeat in-flight requests and displays retryable errors. Services enquiries now send the chosen service and contact details. Keyboard focus is trapped and restored, backgrounds become inert, Escape closes and labels are associated with inputs. Mocked acceptance does not prove inbox delivery.

ROI and cost tools use explicit editable assumptions and validate inputs. ROI output distinguishes revenue, contribution and payback; zero or negative uplift cannot produce finite payback. The checklist is a manual review with optional device-only persistence. No tool claims an SEO score, scans arbitrary customer URLs or collects sensitive information.

## Measurement

Allowlisted events: page_view, cta_click, form_start, form_step_complete, form_submit, demo_requested, form_error, booking_link_click, call_booking. `form_submit` means API acceptance, not delivery. `call_booking` follows Cal's bookingSuccessfulV2 event; booking status may still require confirmation, so reconcile against actual scheduled/attended calls before reporting sales conversions. A calendar link click is not a booking.

The key outcome is qualified Australian enquiries and paying clients by landing page. Connect GA4/GTM with approved consent rules, GSC and Bing, then reconcile accepted submissions with CRM outcome data. Search discovery frequencies and quality scores are not business results.
