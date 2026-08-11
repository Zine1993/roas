# Game Growth Toolkit v0.1.0

## First public milestone

Game Growth Toolkit turns a small set of mobile app/game cohort inputs into transparent retention, payback, ROAS, and break-even CPI scenarios.

This first public milestone is about making the original internal ROAS prototype reproducible, inspectable, and useful to other developers and growth teams.

## What is included

### Cohort and retention modeling

- import retention points from a simple `Day,Rate%` CSV
- validate duplicate, invalid, and non-monotonic retention inputs
- fit a decaying power-law retention curve
- forecast retention through Day 180
- expose R² so users can see in-sample fit quality

### Monetization and acquisition assumptions

- separate mature-user payer rate and ARPPU from new-user multipliers
- model organic uplift
- model platform/distribution revenue share
- calculate effective CPI (eCPI)

### Payback and ROAS

- forecast cumulative LTV
- estimate payback day
- report D7 / D14 / D30 / D60 / D90 / D180 ROAS
- export the Day-180 forecast to CSV

### Break-even and sensitivity

- calculate maximum paid CPI for 100% ROAS at D30 / D90 / D180
- compare current CPI with model-implied acquisition headroom
- run deterministic low/base/high one-way sensitivity for CPI, payer rate, and ARPPU
- export sensitivity scenarios to CSV

### Open-source foundation

- calculation logic extracted into `core.py`
- unit test coverage for retention fitting, eCPI, LTV, payback, ROAS, break-even CPI, and sensitivity
- GitHub Actions CI on Python 3.11 and 3.12
- synthetic sample cohort
- contributor guide, roadmap, changelog, and MIT license

## Quick start

```bash
git clone https://github.com/Zine1993/roas.git
cd roas
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

## What this release is not

Game Growth Toolkit is not an MMP, attribution platform, financial reporting system, or a claim that sparse early cohorts can predict the future with certainty.

The current model is intentionally simple. Long-horizon results can be wrong when payer timing, repeat purchases, whales, ad revenue, refunds, regional mix, campaign quality, reactivation, or retention-model choice differ from the assumptions.

The point of the toolkit is to make those assumptions visible and testable rather than hide them in a spreadsheet or black box.

## What we want feedback on

The most useful early feedback is concrete workflow friction:

- Which cohort export should be easier to import?
- Which assumption do you currently keep in a spreadsheet?
- Which checkpoint or break-even question is missing?
- Which model output would actually change a UA decision?
- Where does the current model diverge from the way your game/app monetizes?

Please use synthetic, anonymized, or aggregated data in public issues.

## Next

Active roadmap items include:

- #2 compare power-law, exponential, and logarithmic retention models
- #4 add import templates for common MMP/store cohort exports
- #5 model payer conversion timing and repeat purchases

Thanks to anyone willing to test an early release and challenge the assumptions.