# Daily research instructions for the Opportunity Radar

These instructions are followed every morning by a scheduled Claude task. Edit this file to change what it looks for; the schedule itself does not need to change.

## Who the Radar serves

South Africans looking for free, official opportunities:

- learners and students: bursaries, scholarships, study funding, study abroad;
- job seekers: learnerships, internships, youth employment programmes, public service graduate programmes;
- small businesses, co-operatives and informal traders: grants, blended finance, business support, supplier development;
- NPOs and community organisations: grants and funding calls from government, development agencies and established foundations.

Priority order: national programmes open to all South Africans, then the Free State, then other provinces and large municipalities, then international programmes that accept South Africans.

## What to do on each run

1. Read `data/opportunities.json` and `data/archive.json`.
2. **Check every existing item** against its official page:
   - correct the open and close dates if the official source has changed them;
   - when an `expected` item's call has been officially published, set the real dates and remove `expected`;
   - set `checked` to today's date only for items you actually verified today;
   - if the official page has gone or the programme has ended, move the item to `data/archive.json`.
3. **Archive** items whose `close` date is more than 30 days in the past and that are not `rolling`. Before moving them, add a `next` line saying when the next round has opened in recent years, if the official source shows this.
4. **Search for new opportunities**: at least 10 searches across the categories above. Focus on calls that opened or were announced in the last 14 days, and on calls opening in the next 60 days.
5. **Add only verified items.** An item may be added only if you found it on the official website of the organisation that runs it (a `.gov.za` site, the funder's own site, or the official portal it names). News sites, bursary aggregators and social media can point you to an opportunity, but they are never enough on their own. Put the official page in `link`, and the page you verified against in `source` if it differs.
6. Run `python3 tools/validate.py`. Fix every error it reports. Never push a file that fails.
7. Set `scanned` to today's date, commit with a message summarising the changes (for example: "2026-11-22: added 2, updated 3, archived 1"), and push to `main`.
8. Finish with a short report: what you added, changed and archived, and anything you could not verify.

## Rules

- Never invent or guess an amount, date, eligibility rule, phone number or link. If the official source does not state it, leave the field out.
- If a date is a well-founded estimate from previous years, set `"expected": true` and say so in `note`.
- Set `conf` to `High` only when every detail comes from the official source; use `Medium` when some details come from reputable reporting that cites the source.
- Do not add paid services, application agents, loans from private lenders, pyramid or "investment" schemes, or anything that charges an application fee.
- Warn about scams in `note` where they are common for that programme (for example, fake NSFAS or SASSA posts).
- Write in plain British English for a reader who may be in Grade 11. Short sentences. No dashes: use commas, colons or full stops. Amounts as `R6 600`.
- Keep the list focused: at most 60 open items. If it would grow past 60, archive the weakest (lowest value, narrowest audience) first.
- Make no other changes to the repository besides the two data files, unless this file asks you to.

## Field reference

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Permanent lowercase id with hyphens, such as `funza-new`. Never reuse or change an id; the website gives each one its own page. |
| `title` | yes | Name of the opportunity. |
| `type` | yes | Short label: Bursary, Scholarship, Grant, Learnership, Internship, Jobs and learnerships, Business support, Loan and support, Blended finance, Tender, Exchange, Competition. |
| `cat` | yes | One or more of `study`, `work`, `business`, `abroad`. |
| `who` | yes | One or more of `learner`, `student`, `jobseeker`, `business`, `org`. |
| `prov` | no | Province, if the opportunity is limited to one. |
| `by` | yes | Organisation that runs it. |
| `elig` | yes | Who can apply. |
| `get` | yes | What the applicant receives. |
| `open`, `close` | no | `YYYY-MM-DD`. An item needs `close`, `"rolling": true` or `"expected": true`. |
| `rolling` | no | `true` if there is no deadline. |
| `expected` | no | `true` if the dates are estimates from previous years. |
| `estimate`, `closeText` | no | Use together when there is no single deadline, for example "Most close between December and February". |
| `diff` | yes | Competition level: `Low`, `Medium`, `High`. |
| `conf` | yes | Confidence in the details: `High`, `Medium`, `Low`. |
| `needs` | no | Documents or registrations needed. |
| `step` | yes | The first practical thing to do. |
| `link` | yes | Official page, `https://` only. |
| `source` | no | Official page used to verify, if different from `link`. |
| `note`, `next` | no | Extra warning or context; `next` says when the next round usually opens. |
| `tags` | no | `value` (high value) and/or `gem` (less publicised). |
| `checked` | yes | Date the item was last verified against its official source. |
| `added` | no | Date the item was first added. |
