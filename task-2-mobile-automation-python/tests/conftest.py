"""
Shared fixtures: CLI platform selection, per-test driver lifecycle, and
screenshot-on-failure (attached to both Allure and a local file for
quick debugging without opening a report).
"""
from __future__ import annotations

import allure
import pytest

from src.driver_factory import build_driver


def pytest_addoption(parser):
    parser.addoption(
        "--platform",
        action="store",
        default="android",
        choices=["android", "ios"],
        help="Which platform to run against. Run pytest twice (once per value) for full "
             "cross-platform coverage - see the README for a two-line CI matrix example.",
    )


@pytest.fixture(scope="function")
def platform_name(request):
    return request.config.getoption("--platform")


@pytest.fixture
def driver(platform_name, request):
    drv = build_driver(platform_name)
    yield drv

    # `rep_call` is attached by pytest_runtest_makereport below and is only
    # present once the test body has actually run.
    failed = getattr(request.node, "rep_call", None) is not None and request.node.rep_call.failed
    if failed:
        _attach_failure_screenshot(drv, request.node.name)

    drv.quit()


def _attach_failure_screenshot(drv, scenario_name: str) -> None:
    png_bytes = drv.get_screenshot_as_png()

    allure.attach(png_bytes, name="Failure screenshot", attachment_type=allure.attachment_type.PNG)

    from pathlib import Path
    from datetime import datetime

    screenshots_dir = Path(__file__).parent / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in scenario_name)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    target = screenshots_dir / f"{safe_name}-{timestamp}.png"
    target.write_bytes(png_bytes)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Stashes each phase's report on the test item so fixtures can check
    request.node.rep_call.failed during their own teardown."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

