# Game Growth Toolkit

Open-source growth analytics for mobile apps and games.

This project helps independent developers, UA teams, and growth analysts turn a few early cohort signals into practical acquisition and payback estimates. The current Streamlit app focuses on retention-curve fitting, monetization adjustments, effective CPI, LTV forecasting, and payback-period estimation.

## Why this project exists

Early-stage teams often have incomplete cohort data but still need to answer questions such as:

- Is this CPI sustainable?
- What happens if new-user payer rate is weaker than the mature-user average?
- How much does organic uplift change effective acquisition cost?
- When does a cohort break even?
- How sensitive is D180 ROAS to retention or monetization assumptions?

Commercial analytics suites can be expensive or too heavy for small teams. Game Growth Toolkit aims to provide a transparent, inspectable, self-hosted alternative for modeling these questions.

## Current features

- Fit a power-law retention curve from 2–10 observed cohort points
- Forecast retention through Day 180
- Adjust payer rate and ARPPU for new-user monetization discounts
- Model organic uplift and platform revenue share
- Estimate effective CPI (eCPI)
- Forecast cumulative LTV
- Estimate payback day and D180 ROAS
- Interactive charts and editable assumptions in Streamlit

## Quick start

```bash
git clone https://github.com/Zine1993/roas.git
cd roas
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

## How the model works

### 1. Retention

Observed retention points are fit with a power-law curve:

```text
R(t) = a * t^b
```

The fitted curve is projected to Day 180.

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

### 4. LTV and payback

Daily net revenue is estimated from payer rate, ARPPU, retention, and platform share. Cumulative LTV is compared with eCPI to estimate payback day and D180 ROAS.

## Important limitations

This is a planning and scenario-analysis tool, not a production attribution system or a substitute for cohort-level revenue data.

The current model intentionally stays simple and interpretable. Real-world LTV can differ materially because of payer conversion timing, repeat purchase behavior, ad revenue, whales, refunds, taxes, regional mix, campaign mix, reactivation, attribution windows, and changes in acquisition quality.

Do not use the output as financial or investment advice.

## Roadmap

See [ROADMAP.md](ROADMAP.md). Near-term priorities include:

- CSV cohort import
- multiple retention models and goodness-of-fit comparison
- confidence intervals and sensitivity analysis
- D7 / D14 / D30 / D60 / D90 ROAS reporting
- country and channel scenario comparison
- exportable reports
- sample datasets and reproducible examples

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, issue, and pull-request guidance.

Useful contribution areas include modeling, validation, UX, documentation, sample datasets, and connectors for common mobile measurement exports.

## Project principles

1. **Transparent assumptions** — every output should be explainable.
2. **Useful with small datasets** — independent developers should be able to use it early.
3. **No vendor lock-in** — local and self-hostable by default.
4. **Evidence over magic** — models should expose fit quality, caveats, and uncertainty as the project matures.
5. **Practical growth workflows** — prioritize questions that UA and product teams actually need to answer.

## Status

The project is under active redevelopment from an internal growth-modeling prototype into a reusable open-source toolkit. The first public milestone is to make the current model reproducible, documented, and easy for contributors to extend.

## License

A formal open-source license will be added before the first tagged public release. Until then, please open an issue before redistributing substantial portions of the project.
