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

## Run tests

Before opening a pull request, run:

```bash
python -m compileall app.py core.py
python -m unittest discover -s tests -v
```

The same unit-test suite runs automatically on pull requests with Python 3.11 and 3.12.

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

For model changes, include a small reproducible example or synthetic dataset that demonstrates the expected behavior and add or update unit tests for calculation changes.

## Good first contribution areas

- exponential/logarithmic retention-model comparisons
- confidence or scenario bands
- CPI break-even analysis
- sensitivity analysis
- common MMP import templates
- country/channel comparisons
- notebook examples
- documentation and translations

## Modeling principles

Growth forecasts can look precise while being wrong. New model features should prefer transparency over hidden heuristics. Assumptions should be visible, units should be explicit, and uncertainty should be documented.

A better fit metric is not automatically a better forecasting model. Model changes should explain why an approach is appropriate for the intended cohort horizon and what can make it fail.

## Code structure

Keep calculation logic in `core.py` or future core-package modules rather than embedding it in Streamlit event/UI code. UI code should call tested functions so the same calculations can eventually be reused in notebooks, scripts, and APIs.

## Responsible data use

Use synthetic, anonymized, or explicitly shareable data in issues and pull requests. Never commit credentials, advertising IDs, raw user-level data, or private attribution exports.

## License

By contributing, you agree that your contribution will be licensed under the repository's MIT License.
