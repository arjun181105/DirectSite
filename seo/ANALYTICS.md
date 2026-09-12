# DirectSite GA4 setup — 12 September 2026

Google Analytics account/property and web stream created after explicit user approval of Google's Australian Terms of Service and Data Processing Terms. Optional account sharing disabled. Reporting: Melbourne timezone, AUD, Business & Industrial, small business. Web stream: DirectSite website, https://directsite.com.au, stream ID 15764835342; measurement ID G-1VQGEKY8YE. Enhanced measurement is disabled to avoid automatic form events and raw link/query collection.

## Deployment state

Website integration is prepared and tested locally, but NOT deployed. Automatic approval review rejected the production commit/push, requiring explicit authorization to deploy the Analytics change to main. The existing 32-page site remains live without the GA tag. No live GA receipt or conversion is claimed.

## Collection behaviour

- Google tag loads only after the visitor chooses Allow analytics. No Google tag request before consent or after a saved refusal on a new page.
- Analytics preferences are available at the bottom of each page. Revocation disables GA, updates consent and removes first-party GA cookies.
- Advertising storage, user data and personalization remain denied; Google signals disabled. Analytics cookies expire after 180 days without renewal. This is separate from the six-calendar-month enquiry retention policy.
- One explicit page_view per page; automatic config pageview disabled. Form and query values never passed. Page location excludes query/hash; referrer reduced to origin.
- Existing allowlisted site events are forwarded; accepted form_submit also emits recommended generate_lead. No lead event for rejected submissions or booking-link clicks.
- Preview builds do not include the GA integration.

## Verification

Local tests cover no-consent/refusal gates, returning preferences, revocation, duplicate pageview suppression, accepted-lead mapping and PII stripping. Existing 13 Python tests and calculator/form/event tests pass. After deployment, verify the consent UI, GA Realtime receipt, accepted-lead events and any actual Cal booking event; mark appropriate key events in the property.

Sources: https://developers.google.com/tag-platform/security/concepts/consent-mode and https://developers.google.com/tag-platform/gtagjs/reference and https://developers.google.com/analytics/devguides/collection/ga4/views
