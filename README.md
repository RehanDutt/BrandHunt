# BrandHunt

A sponsorship lead-generation tool for event teams. Give it a category such as "beverage", "fintech" or "sportswear", and it returns a working contact list: candidate brands in that space, a likely marketing or sponsorship contact address for each, and a validation status for every address.

Built to replace the manual version of this job: searching for brands one at a time, digging through websites for a contact, and guessing at email formats.

**Status:** working prototype. It does the search-and-assemble work reliably. Contact discovery is partly inferential, and the Limitations section below is specific about where.

## What it does

```
category -> brand discovery -> domain resolution -> email inference -> validation -> export
```

1. **Brand discovery.** Queries the Serper.dev search API for companies active in the given category and extracts candidate brand names and homepages.
2. **Domain resolution.** Resolves each candidate to a root domain for the contact step.
3. **Email inference.** Generates likely contact addresses from common corporate patterns such as `marketing@` and `sponsorship@`, applied to that domain.
4. **Validation.** Checks each address against the Hunter.io API. Addresses Hunter can confirm are marked `Verified`. The rest stay `Pattern Match`, meaning plausible in format but unconfirmed in fact.
5. **Export.** Renders the result in a Streamlit table and writes a formatted `.xlsx` via XlsxWriter.

## Output

| Field | Description |
|---|---|
| `Company` | Brand name as extracted from search results |
| `Lead Name` | Named individual where discoverable, otherwise the role (e.g. "Sponsorship Head") |
| `Designation` | Department or role the address is intended to reach |
| `Contact Email` | Inferred or discovered address |
| `Verification` | `Verified (Hunter.io)` or `Pattern Match`, explained below |

### Reading the verification column

This is the field that matters, so it is worth being precise about it.

**`Verified (Hunter.io)`** means Hunter.io returned a positive result for this address. Reasonably high confidence.

**`Pattern Match`** means the address follows a standard corporate format for a real domain, but nothing has confirmed it exists. Treat it as a lead to test, not a confirmed contact.

In a typical run most rows come back as `Pattern Match`. That is expected, because Hunter.io's coverage is thin for smaller and regional Indian brands. **The "Verification Rate" shown in the UI measures how many addresses were successfully generated and format-checked. It is not a deliverability estimate.** Expect bounces on `Pattern Match` rows and warm up your sending domain accordingly.

## Limitations

Known and unfixed. Read before relying on output.

**Brand extraction picks up navigation text.** Company names are parsed from search result pages, and site navigation sometimes survives the parse. Rows reading `Home`, `Our Brands` or `Explore Our Brands` are menu items, not companies. Roughly a third of rows in an average run need manual review. Filtering is on the roadmap.

**Most contacts are role-level, not people.** Unless a named contact appears in the search results, `Lead Name` falls back to a generic role label. The tool finds a route into the marketing function. It does not reliably identify the individual who owns sponsorship decisions.

**Coverage skews to brands with search presence.** Companies with weak SEO are under-represented regardless of how relevant they are to the category.

**No deduplication across runs.** Running the same category twice returns overlapping results with no memory of what was already contacted.

**Single-region tuning.** Email patterns and search behaviour are tuned for Indian corporate domains and have not been tested elsewhere.

## Tech stack

| Layer | Choice |
|---|---|
| Language | Python |
| UI | Streamlit with custom CSS |
| Search | Serper.dev API |
| Email validation | Hunter.io API |
| Data handling | Pandas |
| Export | XlsxWriter |

### Project layout

```
├── app/           # Streamlit UI components and layout
├── collectors/    # search and scraping, brand and domain gathering
├── engines/       # email inference and validation logic
├── services/      # API clients and shared helpers
├── run.py
├── streamlit_app.py
└── requirements.txt
```

## Setup

Requires Python 3.9+ and free-tier API keys from [Serper.dev](https://serper.dev) and [Hunter.io](https://hunter.io).

```bash
git clone https://github.com/RehanDutt/BrandHunt.git
cd BrandHunt
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
SERPER_API_KEY=your_serper_key_here
HUNTER_API_KEY=your_hunter_key_here
```

Keys are read from the environment and are never committed. `.env` is gitignored.

### Run

```bash
streamlit run streamlit_app.py
```

Then open the local URL Streamlit prints, usually `http://localhost:8501`.

## Usage

1. Enter a target industry or keyword, such as `Beverage`, `Fintech` or `Athleisure`.
2. Set lead volume with the slider.
3. Click **Run Engine**.
4. Review the table, discard any rows that are clearly navigation artifacts, and click **Download Leads List (XLSX)**.

Both APIs are rate-limited on their free tiers. Large volumes will throttle.

## Roadmap

- [ ] Filter navigation text out of brand extraction
- [ ] Deduplicate across runs with a local contact store
- [ ] Try multiple email patterns per domain and keep the first that validates
- [ ] Surface a confidence score rather than a binary verification flag
- [ ] Optional LinkedIn enrichment for named contacts

## Notes

Built to solve a real problem: finding sponsors for college events. It reduces the search-and-assemble work substantially, but the output is a starting list that still needs a human pass before anyone gets emailed.

Use it within the terms of service of both APIs, and within applicable rules on unsolicited commercial email.

Built by [Rehan Dutt](https://github.com/RehanDutt)
