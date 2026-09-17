# Task 2 (Python variant) — Wikipedia App Mobile Automation

Same scenario as the Java/Cucumber version in `../task-2-mobile-automation`,
built instead with **Python + Appium-Python-Client + pytest + pytest-bdd**.

## Stack

| Concern | Tool |
|---|---|
| Driver / gestures | `Appium-Python-Client`, `selenium` (W3C Actions for long-press) |
| BDD / Gherkin | `pytest-bdd` — reuses the *same* `.feature` file, Scenario Outline and all |
| Test runner | `pytest` |
| Reporting | `allure-pytest` |
| Parallel execution | `pytest-xdist` (`pytest -n auto`) |
| Screenshot on failure | a `conftest.py` hook, attached to Allure + saved to `tests/screenshots/` |

## Structure

```
config/config.yaml              # per-platform capabilities
src/
  config_reader.py
  driver_factory.py             # builds the Android/iOS driver
  pages/                        # Page Object Model, one file per screen
features/
  save_article_to_reading_list.feature
tests/
  conftest.py                   # driver fixture, --platform option, screenshot-on-failure
  step_defs/
    test_save_article_to_reading_list.py
```

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

You'll also need an Appium server running locally (`npm i -g appium && appium`),
plus an Android emulator/device or iOS simulator with the Wikipedia app
installed (or the APK/IPA placed under `./apps/`, as referenced by `config.yaml`).

## Run

```bash
pytest                                  # runs against android (the default)
pytest --platform=ios                   # runs against ios
pytest -n auto                          # parallel, across workers
pytest -m smoke                         # just the smoke-tagged scenario outline
pytest --alluredir=allure-results && allure serve allure-results   # reporting
```

### On cross-platform coverage

I initially wrote this to auto-run every scenario against Android *and* iOS
in one `pytest` invocation (mirroring the Java version's two-`<test>`-block
`testng.xml`), the same way that side does it. When I actually ran it, that
turned out not to work: pytest-bdd resolves each step's fixtures dynamically
at run time rather than through the static function signatures pytest normally
introspects to build parametrization, so `pytest_generate_tests` never sees the
platform fixture to multiply against. Rather than ship something that looked
right but silently only ran Android, I simplified to a `--platform` flag
(default `android`) and cross-platform coverage is one extra invocation:

```bash
pytest --platform=android && pytest --platform=ios
```

or, as a two-line CI matrix:

```yaml
strategy:
  matrix:
    platform: [android, ios]
steps:
  - run: pytest --platform=${{ matrix.platform }}
```

## How this was actually verified

Unlike the Java version, `pypi.org` **is** reachable from the sandbox this was
built in, so this one isn't just eyeballed:

- The real `Appium-Python-Client`, `selenium`, and `pytest-bdd` packages were
  installed and imported, and every locator strategy / options API used here
  (`AppiumBy.ACCESSIBILITY_ID`, `UiAutomator2Options`/`XCUITestOptions`
  property assignment, `ActionBuilder`/`PointerInput` for the long-press
  gesture) was checked against the real installed library, not memory.
- `pytest --collect-only` confirms all 3 scenarios collect cleanly (the
  Scenario Outline expands to 2 parametrized cases + the duplicate-check
  scenario = 3), with no import errors and no warnings.
- Every step definition, every page-object method, and the full long-press
  action chain were exercised **end to end** with a stubbed driver standing
  in for a real device connection (the sandbox has no Appium server or
  emulator). The dry run completed the entire duplicate-prevention scenario
  and walked the full happy-path scenario all the way to its final
  assertion, failing only where the stub itself couldn't fake a real
  removal — not on anything in this code.

What that dry run **can't** tell you: whether the actual resource-ids and
accessibility labels (`org.wikipedia:id/page_list_item_title`, `"Save
page"`, `"Create new reading list"`, etc.) match the current Wikipedia app
build. Those follow the app's known naming conventions but need a pass with
Appium Inspector against a live install before a real run — same caveat as
the Java version, and the same thing any candidate doing this exercise would
need to do.
