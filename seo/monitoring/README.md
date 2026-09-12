# GEO and conversion measurement

`prompts.json` contains ten exact prompts across four platforms. `../research/ai-citations.json` is an empty 40-row measurement register. A null mention is unmeasured, never a negative result. The 226 discovery searches do not populate AI citations.

For each monthly observation, record UTC date, platform, Australia/city setting, language, whether signed in, exact prompt, session/model where visible, answer excerpt, cited page URLs, competitor names and a saved screenshot or export. A URL present in ordinary search results is not an AI citation. If no AI Overview renders, record `not_shown` and its evidence; if the platform is inaccessible, record `unavailable`. Repeat the same setup, and note material interface changes.

Do not use browser automation to mass-scrape Google results. Use manual checks or an appropriately licensed SERP provider. No automated recurring task was scheduled because the requested deliverable is a prompt set and measurement infrastructure; platform access remains to be established.

Calculate mention rate only among measured rows for the same platform and date window. Report unavailable/not-shown counts separately. Store citations as exact URLs with context. Do not treat the ordering of citations as a brand ranking. Compare landing-page impressions, qualified enquiries and bookings alongside citation visibility.

Analytics hooks are emitted into `window.dataLayer` and `directsite:analytics`. Event names: `page_view`, `cta_click`, `form_start`, `form_step_complete`, `form_submit`, `demo_requested`, `call_booking`, `booking_link_click`, `form_error`. `form_submit` follows successful API acknowledgement. A booking-link click is distinct from Cal.com's `bookingSuccessfulV2` event, which indicates creation and may still require confirmation. Never infer attendance or a paid sale.

`referral_source=chatgpt.com` is recorded when the arrival has the exact `utm_source=chatgpt.com` or a ChatGPT referrer. Other sources are grouped as `other`. Current hooks deliberately do not persist cross-page attribution; configure consent-aware session attribution in the chosen analytics platform. No form values or raw URL queries enter the analytics payload.

No GA4/GTM property was detected in the recovered source. Connect the hooks to the real property, verify consent requirements for the actual implementation and mark only appropriate accepted enquiries/bookings as key events. Use GSC page/query dimensions and CRM qualification outcomes to decide what to expand. Do not optimise solely for button clicks.
