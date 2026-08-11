# Changelog

All notable project changes will be documented here.

The project follows semantic versioning for public releases.

## Unreleased

No user-visible changes are queued after the current `v0.1.0` release candidate.

## 0.1.0 — pending tag

First public milestone of Game Growth Toolkit.

### Added

- reusable `core.py` calculation layer
- cohort CSV import with a synthetic example file
- retention input validation for invalid, duplicate, and non-monotonic points
- decaying power-law retention fitting and R² fit quality
- D7 / D14 / D30 / D60 / D90 / D180 ROAS checkpoints
- cumulative LTV and payback estimation
- D30 / D90 / D180 break-even paid CPI calculations
- deterministic one-way sensitivity analysis for CPI, payer rate, and ARPPU
- low / base / high scenario table with payback and D30 / D90 / D180 ROAS
- forecast CSV and sensitivity CSV exports
- unit tests covering retention, eCPI, LTV, payback, ROAS, break-even CPI, and scenario analysis
- GitHub Actions CI for Python 3.11 and 3.12
- synthetic sample cohort
- contributor guide, roadmap, `.gitignore`, and MIT license
- structured GitHub bug and feature request forms
- pull request template with validation and model-assumption checks
- prepared v0.1.0 release notes and community launch kit

### Changed

- Streamlit interface rebuilt around the reusable calculation core
- project positioning expanded from a single ROAS prototype to Game Growth Toolkit
- Payback & ROAS view now exposes acquisition-cost headroom at key checkpoints
- navigation now includes a dedicated Break-even & Sensitivity workflow
- README redesigned around a first-60-seconds use case and synthetic example output
- roadmap documentation separates deterministic sensitivity from future statistical uncertainty work

### Notes

This milestone is a transparent scenario-planning toolkit, not an attribution system or a guarantee of long-horizon LTV accuracy. The first public tag should be created only after the launch-preparation pull request is reviewed, CI passes, and it is merged to `main`.
