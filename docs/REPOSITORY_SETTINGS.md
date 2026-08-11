# Repository settings for launch

These are the recommended GitHub repository settings for the first public launch.

## About / description

**Description**

> Open-source mobile growth modeling: retention → payback, ROAS, break-even CPI, and sensitivity analysis.

**Website**

Leave empty until there is a stable public demo or project page. Do not point the repository to a temporary local/tunnel URL.

## Recommended topics

Use the most specific topics first:

- mobile-games
- user-acquisition
- roas
- ltv
- retention
- growth-analytics
- cohort-analysis
- app-growth
- streamlit
- python

## Social preview

Recommended GitHub social preview size: 1280 × 640.

The visual should communicate the workflow rather than use a generic AI graphic. Suggested composition:

- headline: `Retention → Payback → ROAS`
- subhead: `Open-source mobile growth scenario modeling`
- three output cards: `D180 ROAS`, `Payback Day`, `Break-even CPI`
- small footer: `Game Growth Toolkit`

Avoid placing synthetic example numbers on the social preview; numbers can be mistaken for benchmarks when the image is shared without context.

## v0.1.0 release checklist

After the launch-preparation PR is merged to `main`:

1. Open **Releases → Draft a new release**.
2. Create tag `v0.1.0` targeting `main`.
3. Release title: `Game Growth Toolkit v0.1.0`.
4. Paste/adapt `docs/RELEASE_NOTES_v0.1.0.md` into the release body.
5. Mark it as the latest release; do not mark it as a pre-release if the merged CI is green.
6. Publish the release.
7. Verify the README badge/links and Quick start from a fresh clone.
8. Start community launch using `docs/LAUNCH_KIT.md`.

## First-week signal tracking

Do not optimize around vanity metrics alone. Track:

- stars
- unique issue authors
- clone/traffic trend if GitHub Insights is available
- installation/runtime bugs
- requests for real import formats
- which outputs people say they would use for a decision
- external contributors / PRs

The strongest signal for the next roadmap item is repeated concrete workflow friction, not raw page views.