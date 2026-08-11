# Game Growth Toolkit

[![Tests](https://github.com/Zine1993/roas/actions/workflows/tests.yml/badge.svg)](https://github.com/Zine1993/roas/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Open-source growth analytics for mobile apps and games.

Game Growth Toolkit helps independent developers, UA teams, and growth analysts turn early cohort signals into transparent acquisition and payback scenarios. The current Streamlit app focuses on retention-curve fitting, monetization adjustments, effective CPI, LTV forecasting, break-even CPI, sensitivity analysis, and ROAS/payback estimation through Day 180.

## Why this project exists

Early-stage teams often have incomplete cohort data but still need to answer practical questions:

- Is this CPI sustainable?
- What is the highest CPI I can pay and still break even by D30, D90, or D180?
- Which assumption hurts the forecast most: CPI, payer rate, or ARPPU?
- What happens if new-user payer rate is weaker than the mature-user average?
- How much does organic uplift change effective acquisition cost?
- When does a cohort break even?
- What do D7, D14, D30, D60, D90, and D180 ROAS look like under the same assumptions?
- How trustworthy is the retention fit behind the forecast?

Commercial analytics suites can be expensive or too heavy for small teams. This project aims to provide a transparent, inspectable, self-hosted alternative for scenario modeling.

## Current features

- Fit a decaying power-law retention curve from observed cohort points
- Validate duplicate, invalid, and non-monotonic retention inputs
- Forecast retention through Day 180
- Report fit quality with R²
- Import cohort points from CSV
- Adjust payer rate and ARPPU for new-user monetization discounts
- Model organic uplift and platform/distribution share
- Estimate effective CPI (eCPI)
- Forecast cumulative LTV
- Estimate payback day
- Report D7 / D14 / D30 / D60 / D90 / D180 ROAS
- Calculate D30 / D90 / D180 break-even paid CPI
- Run one-way low/base/high sensitivity for CPI, payer rate, and ARPPU
- Export the full 180-day forecast and sensitivity scenarios to CSV
- Reusable Python calculation layer in `core.py`
- Unit tests and GitHub Actions CI on Python 3.11 and 3.12

## Quick start

```bash
git clone https://github.com/Zine1993/roas.git
cd roas
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Cohort CSV format

Use a CSV with `Day` and `Rate%` columns:

```csv
Day,Rate%
1,35.0
3,22.0
7,12.0
14,7.5
30,4.5
```

A synthetic example is included at [`examples/sample_cohort.csv`](examples/sample_cohort.csv). The Streamlit app can also download the same sample directly.

## How the model works

### 1. Retention

Observed retention points are fit with a power-law curve:

```text
R(t) = a * t^b
```

The fit is constrained to a non-increasing curve and projected to Day 180. R² is reported so users can see how well the fitted curve explains the observed cohort points.

### 2. Monetization

The app starts with mature active-user payer rate and ARPPU, then applies explicit discount factors for newly acquired users:

```text
new_user_payer_rate = active_payer_rate * payer_discount
new_user_arppu = active_arppu * arppu_discount
```

### 3. Acquisition cost

Organic uplift is converted into an effective CPI:

```text
eCPI = CPI / (1 + organic_lift)
```

### 4. LTV, payback, and ROAS

Daily net revenue is estimated from payer rate, ARPPU, retention, and platform share. Cumulative LTV is compared with eCPI to estimate payback day and checkpoint ROAS.

### 5. Break-even paid CPI

At a target day, 100% ROAS means cumulative LTV equals eCPI. With organic lift, the maximum paid CPI is:

```text
break_even_paid_CPI(day) = cumulative_LTV(day) * (1 + organic_lift)
```

The app reports this at D30, D90, and D180 so acquisition teams can compare current CPI with the model's implied ceiling.

### 6. Sensitivity analysis

The sensitivity view changes one assumption at a time around the baseline. Users choose +/- ranges for CPI, payer rate, and ARPPU, and the toolkit recalculates payback plus D30/D90/D180 ROAS for low/base/high scenarios.

This is deterministic one-way scenario analysis. It is intentionally not presented as a probability distribution or confidence interval.

## Reusable calculation layer

The forecasting logic is separated from Streamlit in [`core.py`](core.py). Current public functions cover:

- retention validation
- power-law fitting
- eCPI
- cumulative LTV
- payback day
- ROAS checkpoints
- break-even paid CPI
- deterministic scenario metrics
- one-way sensitivity analysis

This makes the model easier to test and provides a base for future notebooks, scripts, and APIs.

## Important limitations

This is a planning and scenario-analysis tool, not a production attribution system or a substitute for cohort-level revenue data.

The current model intentionally stays simple and interpretable. Real-world LTV can differ materially because of payer conversion timing, repeat purchase behavior, ad revenue, whales, refunds, taxes, regional mix, campaign mix, reactivation, attribution windows, and changes in acquisition quality.

A high R² only describes fit to the supplied retention points; it does not guarantee that the Day-180 extrapolation is correct. One-way sensitivity shows directional exposure to selected assumptions but does not model correlated inputs or statistical uncertainty.

Do not use the output as financial or investment advice.

## Roadmap

See [ROADMAP.md](ROADMAP.md). Near-term priorities now include:

- compare power-law, exponential, and logarithmic retention models
- confidence/scenario bands and retention sensitivity
- payer conversion timing and repeat-purchase assumptions
- country/channel comparison
- import templates for common MMP exports
- notebooks and a package-style public API

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, tests, issue, and pull-request guidance.

Useful contribution areas include modeling, validation, UX, documentation, sample datasets, and connectors/templates for common mobile measurement exports.

## Project principles

1. **Transparent assumptions** — every output should be explainable.
2. **Useful with small datasets** — independent developers should be able to use it early.
3. **No vendor lock-in** — local and self-hostable by default.
4. **Evidence over magic** — models expose fit quality, caveats, and uncertainty as the project matures.
5. **Practical growth workflows** — prioritize questions UA and product teams actually need to answer.

## Release status

The reproducible open-source baseline has been merged to `main`. A tagged `v0.1.0` release is still pending; ongoing work is documented in [CHANGELOG.md](CHANGELOG.md) and public issues.

## License

MIT. See [LICENSE](LICENSE).
