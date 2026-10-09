# ACA practice & notebook

A local study tool with 143 imported exam-bank questions and 36 generated questions. There are 161 scored questions and 18 unresolved originals in **Source review**. The [content validation report](CONTENT_VALIDATION.md) identifies every unresolved question and explains the study clarifications.

## Launch

No installation or build is needed. Use Python 3 and a modern browser.

```sh
cd aca-practice
python3 -m http.server 8011 --bind 127.0.0.1
```

Open **http://127.0.0.1:8011**. Keep the terminal running; press Ctrl+C to stop it. Opening `index.html` directly will not load the separate JSON bank reliably.

Use the same browser, address and port each time. `localhost` and `127.0.0.1` have separate browser storage, as do different ports. Private browsing may discard saved data when the browser closes.

## What changed on 9 October 2026

Added all 51 Management Accounting questions. 46 are scored; five need further source review. Cost flows, CVP, job costing and pricing are now available in the topic filter and home-page topic cards. The refresh adds a study overview, more space for calculations, compact mobile setup and short transitions. Reduced-motion preferences turn animations off. Existing question IDs, notes, snapshots and history remain compatible.

## Practice

1. Choose mixed practice, a topic, or review of questions whose latest attempt was incorrect or "I don't know". Filters include topic, focus, estimated difficulty and question origin.
2. Write in **Calculations / reasoning / notes**. Drafts and selected answers save as you work. Check the visible save status.
3. Submit an answer or choose **I don't know**. Feedback explains the rule, calculation and distractors. After an error, a suggested follow-up uses a different scenario.
4. Edit your draft after feedback if useful. The notes saved with the original attempt stay unchanged.
5. Open **Learning history** for topic statistics, misconception tags, saved notes, past snapshots and retries. Each retry adds an attempt.

Accuracy means correct / (correct + incorrect). Unknown responses are separate. Neither a small sample nor a high retry percentage establishes mastery. Source marks are preserved; generated questions have no official marks.

## Back up and restore

**Export JSON** downloads drafts, selected answers, timestamps, attempt snapshots, history and the current session. Store this file somewhere you already sync if you want a backup across devices.

**Import JSON** validates a backup before asking to merge it. Distinct attempts are retained, duplicate attempts are ignored, and the more recently saved draft wins per question. An existing local session is kept. Invalid files or conflicting attempt IDs leave current data untouched.

**Reset study data** requires confirmation. Export first if you want to retain your work. Data is local to this browser and can also be cleared in browser settings. Use one study tab at a time; changes from another tab pause saving to avoid overwriting either copy. If saving fails, export before closing. Unreadable stored data is protected and has a recovery download.

The backup format accepts the question IDs in this bank. A backup from a different question collection needs migration before import.

## Publish with GitHub Pages

Repository: [alekswithk/aca-practice](https://github.com/alekswithk/aca-practice).

1. Open [Settings → Pages](https://github.com/alekswithk/aca-practice/settings/pages).
2. Under **Source**, select **Deploy from a branch**.
3. Choose **main** and **/ (root)**, then click **Save**.
4. Wait for the deployment to complete. The shareable address will be **https://alekswithk.github.io/aca-practice/**.

The app uses relative paths and ordinary HTML/CSS/JavaScript/JSON. The entry point and `.nojekyll` are at the repository root; no build step is required. Pages is enabled for `main` at the repository root. [GitHub's publishing instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) describe these settings.

[GitHub Pages hosts static files](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages). It can share the tool and question bank across devices; notes and attempts remain in each device's browser. Automatic cross-device history sync needs an additional storage/authentication design in that later phase. For now, export/import transfers the learning data. Export locally before moving to the hosted address, then import there.

## Files and checks

- `content/questions.json`: delivered question data, independent of interface code.
- `content/management_accounting.py`: Management Accounting import and reviewed teaching feedback.
- `content/build_bank.py`: source importer and authored definitions. Requires the original parent course folders to rebuild; it is not needed to run the app.
- `content/validate_bank.py`: structure and independent numerical checks. Original-excerpt comparisons also run when the parent course-source files are present; a standalone clone reports those comparisons as skipped.
- `core.mjs`: grading, filtering, follow-ups, statistics and backup validation.
- `app.js`, `index.html`, `styles.css`: interface and browser persistence.
- `tests/core.test.mjs`, `tests/browser.test.mjs`: runnable regression checks.

From this folder:

```sh
python3 content/validate_bank.py
node tests/core.test.mjs
```

The browser check requires Playwright and Chromium for development only. It uses the existing local Playwright installation if available, or a package identified by `PLAYWRIGHT_MODULE`. With the local server running:

```sh
node tests/browser.test.mjs
```

`ACA_TEST_URL` can point to another server. `ACA_TEST_OUTPUT` changes the screenshot folder, which defaults to `aca-practice-check` in the system temporary directory. See [TEST_REPORT.md](TEST_REPORT.md) for the checks performed and remaining limits.
