# Game Growth Toolkit

[![Tests](https://github.com/Zine1993/roas/actions/workflows/tests.yml/badge.svg)](https://github.com/Zine1993/roas/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Open-source growth analytics for mobile apps and games.

Game Growth Toolkit helps independent developers, UA teams, and growth analysts turn early cohort signals into transparent acquisition and payback scenarios. The current Streamlit app focuses on retention-curve fitting, monetization adjustments, effective CPI, LTV forecasting, and ROAS/payback estimation through Day 180.

## Why this project exists

Early-stage teams often have incomplete cohort data but still need to answer practical questions:

- Is this CPI sustainable?
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
- Export the full 180-day forecast to CSV
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

## Reusable calculation layer

The forecasting logic is separated from Streamlit in [`core.py`](core.py). Current public functions cover:

- retention validation
- power-law fitting
- eCPI
- cumulative LTV
- payback day
- ROAS checkpoints

This makes the model easier to test and provides a base for future notebooks, scripts, and APIs.

## Important limitations

This is a planning and scenario-analysis tool, not a production attribution system or a substitute for cohort-level revenue data.

The current model intentionally stays simple and interpretable. Real-world LTV can differ materially because of payer conversion timing, repeat purchase behavior, ad revenue, whales, refunds, taxes, regional mix, campaign mix, reactivation, attribution windows, and changes in acquisition quality.

A high R² only describes fit to the supplied retention points; it does not guarantee that the Day-180 extrapolation is correct.

Do not use the output as financial or investment advice.

## Roadmap

See [ROADMAP.md](ROADMAP.md). Near-term priorities now include:

- compare power-law, exponential, and logarithmic retention models
- confidence/scenario bands
- CPI break-even and sensitivity analysis
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

The project is under active redevelopment from an internal growth-modeling prototype into a reusable open-source toolkit. See [CHANGELOG.md](CHANGELOG.md) for the current unreleased milestone. The first tagged release is planned as `v0.1.0` after the open-source readiness changes are reviewed and merged.

## License

MIT. See [LICENSE](LICENSE).
