# Roadmap

Game Growth Toolkit is moving from a single Streamlit prototype toward a reusable open-source growth analytics toolkit for mobile apps and games.

## Milestone 0.1 — Reproducible core

- [x] Document the existing retention, monetization, eCPI, LTV, and payback model
- [x] Fix missing runtime dependencies
- [x] Add input validation for invalid or non-monotonic cohort points
- [x] Extract calculation functions from the Streamlit UI
- [x] Add unit tests for retention fitting, eCPI, cumulative LTV, payback, and ROAS calculations
- [x] Add synthetic sample cohorts
- [x] Add an open-source license
- [x] Add pull-request CI on supported Python versions

## Milestone 0.2 — Better forecasting

- [ ] Compare power-law, exponential, and logarithmic retention models — #2
- [x] Report goodness-of-fit metrics
- [ ] Add confidence intervals or scenario bands — follow-up to #2
- [x] Add D7 / D14 / D30 / D60 / D90 / D180 ROAS outputs
- [ ] Add payer conversion timing and repeat-purchase assumptions — #5
- [ ] Support ad-revenue scenarios

## Milestone 0.3 — Real growth workflows

- [x] CSV cohort import
- [ ] Import templates for common MMP / store exports — #4
- [ ] Country comparison
- [ ] Channel comparison
- [ ] CPI break-even calculator — #3
- [ ] Sensitivity analysis for CPI, retention, payer rate, and ARPPU — #3
- [ ] Exportable HTML reports
- [x] Exportable forecast CSV

## Milestone 0.4 — Reusable analytics layer

- [x] Separate core Python calculations from the Streamlit application
- [ ] Package-style public calculation API
- [ ] Notebook examples
- [ ] Reproducible benchmark datasets
- [ ] Contributor documentation for adding new models

## Active issues

- #2 — Compare retention models and expose model-selection evidence
- #3 — Add CPI break-even and sensitivity analysis
- #4 — Add cohort import templates for common mobile measurement exports
- #5 — Model payer conversion timing and repeat purchases

## What success looks like

The project should let an independent developer or growth analyst take a small set of cohort observations, understand the assumptions behind a forecast, compare scenarios, and make a better-informed acquisition decision without relying on a proprietary analytics stack.

Roadmap priorities can change based on contributor feedback and real usage. Please open an issue when proposing a new model or workflow so assumptions can be discussed before implementation.
