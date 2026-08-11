# Roadmap

Game Growth Toolkit is moving from a single Streamlit prototype toward a reusable open-source growth analytics toolkit for mobile apps and games.

## Milestone 0.1 — Reproducible core

- [x] Document the existing retention, monetization, eCPI, LTV, and payback model
- [x] Fix missing runtime dependencies
- [ ] Add input validation for invalid or non-monotonic cohort points
- [ ] Extract calculation functions from the Streamlit UI
- [ ] Add unit tests for retention fitting, eCPI, cumulative LTV, and payback calculations
- [ ] Add synthetic sample cohorts
- [ ] Add an open-source license

## Milestone 0.2 — Better forecasting

- [ ] Compare power-law, exponential, and logarithmic retention models
- [ ] Report goodness-of-fit metrics
- [ ] Add confidence intervals or scenario bands
- [ ] Add D7 / D14 / D30 / D60 / D90 / D180 ROAS outputs
- [ ] Add payer conversion timing and repeat-purchase assumptions
- [ ] Support ad-revenue scenarios

## Milestone 0.3 — Real growth workflows

- [ ] CSV cohort import
- [ ] Import templates for common MMP / store exports
- [ ] Country comparison
- [ ] Channel comparison
- [ ] CPI break-even calculator
- [ ] Sensitivity analysis for CPI, retention, payer rate, and ARPPU
- [ ] Exportable HTML/CSV reports

## Milestone 0.4 — Reusable analytics layer

- [ ] Separate core Python package from the Streamlit application
- [ ] Public calculation API
- [ ] Notebook examples
- [ ] Reproducible benchmark datasets
- [ ] Contributor documentation for adding new models

## What success looks like

The project should let an independent developer or growth analyst take a small set of cohort observations, understand the assumptions behind a forecast, compare scenarios, and make a better-informed acquisition decision without relying on a proprietary analytics stack.

Roadmap priorities can change based on contributor feedback and real usage. Please open an issue when proposing a new model or workflow so assumptions can be discussed before implementation.
