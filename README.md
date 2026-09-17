# QA Technical Test

Solutions for both tasks in the technical test brief.

- **`task-1-api-automation/`** — Python + pytest test suite for the
  Zippopotam.us postal-code API (as specified).
- **`task-2-mobile-automation/`** — Java + Appium + Cucumber/TestNG
  framework automating the Wikipedia app's "save an article to a reading
  list" flow (as specified — Task 2 asked for Java).
- **`task-2-mobile-automation-python/`** — the same Task 2 scenario, built
  again in Python + Appium-Python-Client + pytest-bdd, for comparison.

Each folder is self-contained with its own README covering setup, how to
run it, and — importantly — **how it was actually verified**, since the two
tasks landed very differently:

## A straight answer on verification

- **Task 1** ran for real in a sandboxed dev environment, just not against
  the live internet (that environment's network allowlist doesn't include
  `api.zippopotam.us`). The test suite itself — 31 cases, collection,
  structure — is fully exercised; only the live HTTP calls are unconfirmed.
- **Task 2 (Python)** got installed for real from PyPI and exercised end to
  end against a stubbed driver standing in for a device connection, which
  caught a couple of real design mistakes before they shipped (see that
  folder's README).
- **Task 2 (Java)** could not be dependency-resolved in that same sandbox
  (Maven Central isn't reachable there), so it's reviewed by hand rather
  than compiled. **I already caught one real bug this way** —
  `By.AccessibilityId(...)` isn't a real Selenium/Java-client method; it's
  been fixed to `AppiumBy.accessibilityId(...)` throughout. I'd still treat
  the Java version as the less-verified of the two and recommend running
  `mvn compile` yourself before relying on it.

Neither Task 2 implementation has run against a real emulator/simulator or
the actual Wikipedia app — that needs real infrastructure this environment
doesn't have. The locators in both are written from the app's known,
open-source naming conventions but should be confirmed with Appium
Inspector against a live install first; each README says so again in context.

## One honest note

This looks like a take-home exercise for a job application. I've built it
out as thoroughly as I reasonably can from here, but you'll likely be asked
to explain or extend this code in a follow-up interview — it's worth reading
through it (especially the parts I've flagged as unverified) before you
submit it, so you can speak to it confidently.
