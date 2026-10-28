# ACA practice & notebook

A local study tool with 218 imported exam-bank questions and 36 generated questions. There are 236 scored questions and 18 unresolved originals excluded from scored practice. The [content validation report](CONTENT_VALIDATION.md) identifies every unresolved question and explains the study clarifications.

## Launch

No installation or build is needed. Use Python 3 and a modern browser.

```sh
cd aca-practice
python3 -m http.server 8011 --bind 127.0.0.1
```

Open **http://127.0.0.1:8011**. Keep the terminal running; press Ctrl+C to stop it. Opening `index.html` directly will not load the separate JSON bank reliably.

Use the same browser, address and port each time. `localhost` and `127.0.0.1` have separate browser storage, as do different ports. Private browsing may discard saved data when the browser closes.

## What changed on 27 October 2026

Home and the ACA logo open the topic picker for focused revision. Returning Home preserves the current session, answers and notes; Resume session returns to it. The exam timer pauses while away from the study view. Active sessions use a wider question panel and collapse setup controls, with focus moving to the current question on start, navigation and reload.

Practice places the worked explanation beside the question on wide screens. Optional calculations and notes sit below both panels. Previous returns to an earlier question with its answer, feedback, notes and option order intact. Returning to a submitted question does not add another attempt. After checking, only the submitted choice is highlighted: green when correct, red when incorrect. Skip leaves all choices neutral. The session-length slider has one question-count display and moves in steps of five.

Exams keep answers hidden until submission, use Next and Finish buttons, and show a yellow flag beside questions marked for review. Flags, answers, notes and the countdown restore after reloading. Card instructions have been removed; save status and save-failure warnings remain.

The interface uses neutral light and dark surfaces from the Ledger design preview. The existing theme switch reveals the new theme in a circle, inspired by [Lightswind Toggle Theme](https://lightswind.com/components/toggle-theme). Primary buttons use a short [ripple](https://lightswind.com/components/ripple-button). Both effects use browser APIs and CSS, with no new dependencies. Reduced motion disables them, and browsers without View Transitions switch themes immediately. Cards have no hover background animation.

## What changed on 25 October 2026

Added 30 questions from the local exam banks: 14 Capital Budgeting and 16 Cost and Performance Management. Both topics are available in practice, focus filters, topic exams, controlling exams and full exams. Seven exercises include data tables for cash-flow timing or profit-center figures. Tables align numeric columns, scroll within the question on narrow screens and remain visible in learning history. The source excerpts and answer options are retained. All 224 earlier question records and IDs are unchanged.

## Earlier additions

Added all 51 Management Accounting questions. 46 are scored; five need further source review. Cost flows, CVP, job costing and pricing are now available in the topic filter and home-page topic cards. The refresh adds a study overview, more space for calculations, compact mobile setup and short transitions. Reduced-motion preferences turn animations off. Existing question IDs, notes, snapshots and history remain compatible.

## Design approach

The interface follows [apple-design](https://github.com/emilkowalski/skills/blob/main/skills/apple-design/SKILL.md) and [emil-design-eng](https://github.com/emilkowalski/skills/blob/main/skills/emil-design-eng/SKILL.md), reviewed at repository commit `e8a175d` on 9 October 2026.

System typography, quiet surfaces and floating study navigation keep the question and explanation prominent. Press feedback starts on pointer-down; the action commits on release. Questions and keyboard actions update immediately. Phone inputs use at least 16px text. Reduced-motion, reduced-transparency and increased-contrast preferences are supported. Native controls and CSS keep the app independent of UI libraries.

## Practice

1. Choose mixed practice, a topic, or review of questions whose latest attempt was incorrect or "I don't know". Filters include topic, focus, estimated difficulty and question origin.
2. Open **Calculations & notes** below the question if you want to record your working. Drafts and selected answers save as you work. Check the visible save status.
3. Check an answer or choose **Skip**. Feedback explains the rule, calculation and distractors. After an error, a suggested follow-up uses a different scenario.
4. Edit your draft after feedback if useful. The notes saved with the original attempt stay unchanged.
5. Open **Learning history** for topic statistics, misconception tags, saved notes, past snapshots and retries. Each retry adds an attempt.

Accuracy means correct / (correct + incorrect). Unknown responses are separate. Neither a small sample nor a high retry percentage establishes mastery. Source marks are preserved; generated questions have no official marks.

## Back up and restore

**Export JSON** downloads drafts, selected answers, timestamps, attempt snapshots, history and the current session. Store this file somewhere you already sync if you want a backup across devices.

**Import JSON** validates a backup before asking to merge it. Distinct attempts are retained, duplicate attempts are ignored, and the more recently saved draft wins per question. An existing local session is kept. Invalid files or conflicting attempt IDs leave current data untouched.

**Reset study data** requires confirmation and resets guest progress in this browser. It is disabled while signed in. Export first if you want to retain your work. Use one study tab at a time. If saving fails, export before closing. Unreadable stored data is protected and has a recovery download.

The backup format accepts the question IDs in this bank. A backup from a different question collection needs migration before import.

## Account saving

Open **Account & sync** and choose **Continue with Google**. Answers, attempts, notes and progress save locally first, then sync to your account. **Sync now** retries a failed cloud save. Each account has a separate browser copy; signing out returns to guest progress.

A login reminder appears once per browser when a signed-out visitor first opens this version. **Not now** or Escape dismisses it. Clearing browser storage allows it to appear again.

Choose **Add this browser's guest progress** after signing in to bring earlier local work into your account. Existing guest data is preserved. See [Supabase setup](SUPABASE_SETUP.md) for the database SQL, Google login, deployment steps, checks and sync limitations.

## Publish with GitHub Pages

Repository: [alekswithk/aca-practice](https://github.com/alekswithk/aca-practice).

1. Open [Settings → Pages](https://github.com/alekswithk/aca-practice/settings/pages).
2. Under **Source**, select **Deploy from a branch**.
3. Choose **main** and **/ (root)**, then click **Save**.
4. Wait for the deployment to complete. The shareable address will be **https://alekswithk.github.io/aca-practice/**.

The app uses relative paths and ordinary HTML/CSS/JavaScript/JSON. The entry point and `.nojekyll` are at the repository root; no build step is required. Pages is enabled for `main` at the repository root. [GitHub's publishing instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) describe these settings.

[GitHub Pages hosts static files](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages). Signed-in progress syncs through Supabase once the [dashboard setup](SUPABASE_SETUP.md) is complete and these files are deployed. Guest notes and attempts stay in each device's browser. Export locally before moving to the hosted address, then import there.

## Files and checks

- `content/questions.json`: delivered question data, independent of interface code.
- `content/management_accounting.py`: Management Accounting import and reviewed teaching feedback.
- `content/capital_performance.py`: Capital Budgeting and Cost and Performance Management imports, source excerpts and exercise tables.
- `content/build_bank.py`: source importer and authored definitions. Requires the original parent course folders to rebuild; it is not needed to run the app.
- `content/validate_bank.py`: structure and independent numerical checks. Original-excerpt comparisons also run when the parent course-source files are present; a standalone clone reports those comparisons as skipped.
- `core.mjs`: grading, filtering, follow-ups, statistics and backup validation.
- `app.js`, `index.html`, `styles.css`: interface and browser persistence.
- `tests/core.test.mjs`, `tests/workspace.test.mjs`: grading, backups and current workspace regression checks.

From this folder:

```sh
python3 content/validate_bank.py
node tests/core.test.mjs
```

The browser check requires Playwright and Chromium for development only. It uses the existing local Playwright installation if available, or a package identified by `PLAYWRIGHT_MODULE`. With the local server running:

```sh
node tests/content-refresh.test.mjs
node tests/filter-regression.test.mjs
node tests/workspace.test.mjs
```

`ACA_TEST_URL` can point to another server. `ACA_TEST_OUTPUT` changes the screenshot folder. `PLAYWRIGHT_EXECUTABLE_PATH` selects an existing Chromium executable if it is installed separately from Playwright. See [TEST_REPORT.md](TEST_REPORT.md) for the checks performed and the older browser suite's stale interface assertions.
