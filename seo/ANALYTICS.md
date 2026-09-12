# DirectSite GA4 setup — 12 September 2026

Google Analytics account/property and web stream created after explicit user approval of Google's Australian Terms of Service and Data Processing Terms. Optional account sharing disabled. Reporting: Melbourne timezone, AUD, Business & Industrial, small business. Web stream: DirectSite website, https://directsite.com.au, stream ID 15764835342; measurement ID G-1VQGEKY8YE. Enhanced measurement is disabled to avoid automatic form events and raw link/query collection.

## Deployment state

Deployed to production main as commit a1174d9 with explicit user approval. Live consent check confirmed no Google tag before consent or after rejection, and the correct tag after acceptance. Google Analytics Realtime received homepage and services pageviews. generate_lead is configured as a key event, counted once per event with no default monetary value. Realtime confirmed form_start, form_submit and generate_lead from the labelled test enquiry, each once. Key-event configuration was saved after that test, so retrospective key-event counting is not claimed.

## Collection behaviour

- Google tag loads only after the visitor chooses Allow analytics. No Google tag request before consent or after a saved refusal on a new page.
- Analytics preferences are available at the bottom of each page. Revocation disables GA, updates consent and removes first-party GA cookies.
- Advertising storage, user data and personalization remain denied; Google signals disabled. Analytics cookies expire after 180 days without renewal. This is separate from the six-calendar-month enquiry retention policy.
- One explicit page_view per page; automatic config pageview disabled. Form and query values never passed. Page location excludes query/hash; referrer reduced to origin.
- Existing allowlisted site events are forwarded; accepted form_submit also emits recommended generate_lead. No lead event for rejected submissions or booking-link clicks.
- Preview builds do not include the GA integration.

## Verification

Local tests cover no-consent/refusal gates, returning preferences, revocation, duplicate pageview suppression, accepted-lead mapping and PII stripping. Existing 13 Python tests and calculator/form/event tests pass. Live consent and pageview receipt verified. Completed Cal booking verification remains separate and outstanding.

Sources: https://developers.google.com/tag-platform/security/concepts/consent-mode and https://developers.google.com/tag-platform/gtagjs/reference and https://developers.google.com/analytics/devguides/collection/ga4/views
