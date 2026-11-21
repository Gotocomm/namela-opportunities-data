# Namela Opportunity Radar data

The verified list of open bursaries, scholarships, grants, learnerships and business support shown on **[opportunities.namela.org](https://opportunities.namela.org/)**, a free service of [Namela Development Institute](https://namela.org/), a registered South African non-profit.

- `data/opportunities.json`: open and upcoming opportunities.
- `data/archive.json`: closed or discontinued opportunities, kept for reference.
- `RESEARCH.md`: how the list is researched and verified, and what each field means.
- `tools/validate.py`: checks the data before it is published.

## How it updates

1. Every morning a scheduled research task checks each listing against its official source, archives closed ones and adds newly announced opportunities, following `RESEARCH.md`.
2. It validates the file and pushes it here.
3. The website downloads this file once a day, checks it again, and keeps the previous version if anything is wrong.

Government tenders are separate: the website pulls them every hour directly from National Treasury's eTenders feed.

## Corrections

Spotted a mistake or a new opportunity? Email radar@namela.org. Always confirm details on the official page before you apply. Namela is not the funder, does not process applications and cannot guarantee outcomes.
