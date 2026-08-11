# Contributing

Thanks for helping improve Game Growth Toolkit.

## Development setup

```bash
git clone https://github.com/Zine1993/roas.git
cd roas
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

## Before opening an issue

Please include:

- the question or growth workflow you are trying to solve
- your expected result
- the actual result
- sample or synthetic data when possible
- screenshots for UI problems
- Python and OS versions for installation/runtime bugs

Do not upload proprietary attribution exports or user-level production data.

## Pull requests

Keep pull requests focused and explain:

1. what problem is being solved
2. why the change is needed
3. how the result was validated
4. any assumptions or limitations introduced by the change

For model changes, include a small reproducible example or synthetic dataset that demonstrates the expected behavior.

## Good first contribution areas

- input validation and clearer error states
- sample cohort datasets
- retention-model comparisons
- fit-quality metrics
- sensitivity analysis
- CSV import/export
- documentation and translations
- test coverage for calculation functions

## Modeling principles

Growth forecasts can look precise while being wrong. New model features should prefer transparency over hidden heuristics. Assumptions should be visible, units should be explicit, and uncertainty should be documented.

## Code style

Keep functions small enough to test independently. As the project is refactored, calculation logic should be separated from Streamlit UI code so the core model can be reused in notebooks, scripts, and tests.

## Responsible data use

Use synthetic, anonymized, or explicitly shareable data in issues and pull requests. Never commit credentials, advertising IDs, raw user-level data, or private attribution exports.
