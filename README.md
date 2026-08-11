# Game Growth Toolkit

[![Tests](https://github.com/Zine1993/roas/actions/workflows/tests.yml/badge.svg)](https://github.com/Zine1993/roas/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Turn a few early cohort points into payback, ROAS, and break-even CPI — locally, transparently, and without a proprietary analytics stack.**

Game Growth Toolkit is an open-source scenario-planning app for **mobile game/app developers, UA teams, and growth analysts**. Give it early retention data plus monetization and acquisition assumptions; it fits a retention curve and shows what those assumptions imply through Day 180.

**Use it to answer questions like:**

- Is a $3 CPI sustainable for this cohort?
- What is the highest paid CPI I can afford and still reach 100% ROAS by D30, D90, or D180?
- When does this cohort pay back?
- What do D7 / D14 / D30 / D60 / D90 / D180 ROAS look like?
- Does CPI, payer rate, or ARPPU matter most to the outcome?
- How much should I trust the retention fit behind the forecast?

## 60-second demo

Start with a tiny cohort CSV:

```csv
Day,Rate%
1,35.0
3,22.0
7,12.0
14,7.5
30,4.5
```

Using the app's default **synthetic** assumptions — $3 paid CPI, 20% organic lift, 5% mature payer rate, 0.5x new-user payer multiplier, $50 mature ARPPU, 0.8x new-user ARPPU multiplier, and 30% platform cut — the model currently produces approximately:

| Output | Synthetic example |
| --- | ---: |
| Retention fit R² | 0.986 |
| D30 ROAS | 87.5% |
| Estimated payback | Day 39 |
| D90 ROAS | 154.0% |
| D180 ROAS | 216.8% |
| D180 break-even paid CPI | $6.50 |

These numbers are **not benchmarks and not promises**. They only demonstrate how the toolkit turns explicit assumptions into a reproducible scenario. Replace the sample data and assumptions with your own aggregated cohort inputs.

## Quick start

```bash
git clone https://github.com/Zine1993/roas.git
cd roas
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

Then open the local Streamlit URL, import a cohort CSV or use the bundled sample, and adjust the assumptions.

A synthetic example is included at [`examples/sample_cohort.csv`](examples/sample_cohort.csv).

## What you get

### Retention

- fit a decaying power-law curve from observed cohort points
- validate duplicate, invalid, and non-monotonic inputs
- forecast retention through Day 180
- show fit quality with R²
- import `Day,Rate%` cohort CSVs

### Monetization & acquisition

- apply separate mature-user and new-user payer/ARPPU assumptions
- model organic lift and platform/distribution share
- calculate effective CPI (eCPI)
- forecast cumulative LTV and payback day

### Decision outputs

- D7 / D14 / D30 / D60 / D90 / D180 ROAS
- D30 / D90 / D180 break-even paid CPI
- one-way low/base/high sensitivity for CPI, payer rate, and ARPPU
- forecast and sensitivity CSV exports

### Engineering quality

- reusable calculation layer in [`core.py`](core.py)
- deterministic model functions separated from Streamlit UI
- unit tests
- GitHub Actions CI on Python 3.11 and 3.12
- MIT licensed

## Why this exists

Early-stage teams often need to make UA decisions before they have months of mature cohort data. The usual alternatives are a spreadsheet full of hidden assumptions or an analytics suite that may be too expensive, too heavy, or too opaque for the question at hand.

Game Growth Toolkit aims to sit in the middle: **small enough to inspect, practical enough to use, and explicit enough to challenge.**

It is deliberately not an attribution platform. It does not reconcile installs across ad networks, ingest user-level events, or claim to know a "true" LTV. It turns the assumptions you provide into a transparent scenario so you can reason about acquisition decisions.

## How the model works

### 1. Retention

Observed retention points are fit with a power-law curve:

```text
R(t) = a * t^b
```

The fit is constrained to a non-increasing curve and projected to Day 180. R² describes how well the curve explains the supplied points; it does **not** guarantee long-horizon forecast accuracy.

### 2. Monetization

```text
new_user_payer_rate = active_payer_rate * payer_multiplier
new_user_arppu = active_arppu * arppu_multiplier
```

Daily net revenue is estimated from retained users, payer rate, ARPPU, and platform share.

### 3. Acquisition cost

```text
eCPI = paid_CPI / (1 + organic_lift)
```

### 4. Payback and ROAS

Cumulative LTV is compared with eCPI to estimate payback day and checkpoint ROAS.

### 5. Break-even paid CPI

At a target day, 100% ROAS means cumulative LTV equals eCPI:

```text
break_even_paid_CPI(day) = cumulative_LTV(day) * (1 + organic_lift)
```

### 6. Sensitivity

The sensitivity view changes **one input at a time** around the baseline and recalculates payback plus D30 / D90 / D180 ROAS. It is deterministic scenario analysis, not a probability distribution or confidence interval.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Important limitations

This is a planning and scenario-analysis tool, not a production attribution system or a substitute for cohort-level revenue data.

Real-world LTV can differ materially because of payer conversion timing, repeat purchases, ad revenue, whales, refunds, taxes, regional mix, campaign mix, reactivation, attribution windows, and changes in acquisition quality. A high R² only describes fit to the supplied retention points. One-way sensitivity does not model correlated inputs or statistical uncertainty.

Do not use the output as financial or investment advice.

## Roadmap & open work

The next public work is intentionally visible in Issues:

- [#2 — Compare retention models and expose model-selection evidence](https://github.com/Zine1993/roas/issues/2)
- [#4 — Add cohort import templates for common mobile measurement exports](https://github.com/Zine1993/roas/issues/4)
- [#5 — Model payer conversion timing and repeat purchases](https://github.com/Zine1993/roas/issues/5)

See [ROADMAP.md](ROADMAP.md) for the longer roadmap.

## Contributing

Contributions and real-world workflow feedback are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

If you use Singular, AppsFlyer, Adjust, store analytics, or your own cohort exports, the most useful feedback is often not "add more AI" — it is **which input format, forecast assumption, or decision output makes the current workflow annoying**.

Please use synthetic, anonymized, or aggregated data in public issues.

## Launch status

The open-source baseline and break-even/sensitivity workflow are merged to `main`. The repository is being prepared for its first tagged public milestone, `v0.1.0`.

See [`docs/RELEASE_NOTES_v0.1.0.md`](docs/RELEASE_NOTES_v0.1.0.md) for prepared release notes and [`docs/LAUNCH_KIT.md`](docs/LAUNCH_KIT.md) for launch/community copy.

If this replaces even one awkward spreadsheet for you, a ⭐ helps signal that this workflow is worth continuing — and an Issue describing what is missing is even more useful.

## License

MIT. See [LICENSE](LICENSE).
