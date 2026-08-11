# Changelog

All notable project changes will be documented here.

The project follows semantic versioning for public releases.

## Unreleased

### Added
- D30 / D90 / D180 break-even paid CPI calculations
- deterministic one-way sensitivity analysis for CPI, payer rate, and ARPPU
- low / base / high scenario table with payback and D30 / D90 / D180 ROAS
- sensitivity CSV export
- four additional unit tests covering break-even and scenario analysis

### Changed
- Payback & ROAS view now exposes acquisition-cost headroom at key checkpoints
- Streamlit navigation now includes a dedicated Break-even & Sensitivity workflow
- roadmap documentation updated to separate deterministic sensitivity from future retention uncertainty work

## 0.1.0 — pending tag

The reproducible open-source baseline is merged to `main` and includes:

### Added
- reusable `core.py` calculation layer
- cohort CSV import with a synthetic example file
- retention input validation
- power-law fit quality via R²
- D7 / D14 / D30 / D60 / D90 / D180 ROAS checkpoints
- forecast CSV export
- unit tests for retention, eCPI, LTV, payback, and ROAS calculations
- GitHub Actions test workflow for Python 3.11 and 3.12
- contributor guide, roadmap, `.gitignore`, and MIT license

### Changed
- Streamlit interface rewritten around the reusable calculation core
- project positioning expanded from a single ROAS prototype to Game Growth Toolkit
