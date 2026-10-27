# Implementation checks

## Workspace update, 27 October 2026

Practice navigation checks now cover Previous/Next across submitted and unsubmitted questions, preservation of selections, drafts and option order after reload, and avoiding duplicate attempts or repeated follow-up questions. Core backup checks validate the saved option-order cache and reject malformed entries. The browser suite also checks Skip, selected-only answer highlighting in practice and exam review, removal of card instructions and slider tick labels, and a single question-count display with a step of five.

The core tests, content validator, filter regression, content-refresh browser regression and new workspace browser regression passed in Chromium. The content bank still contains 254 records, with 236 scored and 18 excluded. The validator recomputed 106 numerical results. Three source-excerpt comparisons were skipped because the original files are outside this repository.

`node tests/workspace.test.mjs` checks side-by-side explanations on desktop, optional notes below the study panels, green/red answer states, draft restoration and immutable submitted notes. Typing in notes does not trigger answer shortcuts. It also checks the circular theme change, reduced-motion and unsupported-browser fallbacks, exam navigation and flag markers, restored timers and answers, export of exam flags/notes, and final submission. Practice and exam layouts fit at 375, 768, 1024 and 1440 pixels; enlarged text also fits. No page errors were reported.

Desktop and phone screenshots were inspected. The original `tests/browser.test.mjs` predates the current interface and remains a legacy suite with stale selectors and layout assumptions; the current workspace suite covers the changed interactions. Safari, Firefox and physical phones were not tested.

## Earlier checks

Updated 25 October 2026.

## Current content refresh

- Content validation passes for 254 records, including all 30 additions. It independently recomputes 106 numerical results and compares every available local source excerpt. Only the external Budgeting and Variances source is unavailable for exact comparison.
- Core tests pass, including grading after shuffling, backup validation and preservation of drafts and attempt history across bank versions. A direct comparison confirms all 224 previously committed question records are unchanged.
- `tests/filter-regression.test.mjs` passes with 236 scored questions, including the existing Budgeting and Variances pools.
- `tests/content-refresh.test.mjs` passes in Chromium. Both new topics are available in practice, focus filters, topic exams, controlling exams and full exams. All seven new exercise tables retain their rows and row headers, align numbers, fit within the page at 375, 768 and 1440 pixels, scroll horizontally on a phone and remain available in learning history. Correct submission of an EVA exercise also passes.
- Desktop and mobile EVA screenshots were visually reviewed. No overlap or page overflow was found.

The older `tests/browser.test.mjs` stops at its first assertion: it expects the removed source-review counter to contain `(18)`, while the current interface leaves that hidden counter empty. The committed app already has this behavior. That suite has not been rewritten in this content update, and its later checks were not rerun successfully. Current Safari, Firefox and physical-device checks were not performed. Publication is checked separately against the hosted files after deployment.

## Previous verification, 9 October 2026

The following records describe the earlier interface and are retained as historical verification.

## Content and core logic

`python3 content/validate_bank.py` passed: 179 records, all 143 source imports preserved, 36 generated questions, 89 independently recomputed numerical results, 161 scored questions and 18 excluded questions.

`node tests/core.test.mjs` passed:

- Every scored question has exactly one correct answer after five different option permutations. The independent numerical check also verifies every new numeric option, including “none” answers, against the result. Unresolved questions cannot be graded.
- Notes snapshots stay unchanged when drafts are edited.
- Unknown responses are recorded separately, with no distractor misconception tag.
- Filters select the requested topic, focus, difficulty and origin. Correct retries clear a question from the outstanding-misses set without deleting its history.
- Follow-ups use another relevant scenario and match the diagnosed misconception where available.
- Accuracy excludes unknown responses and retains repeated attempts.
- Export/import round trips preserve drafts, selections, timestamps, session state and attempt history. Re-imports deduplicate; conflicting IDs and malformed data are rejected without changing the local state.

The previous 128 question records were compared with the committed bank and are identical. Legacy bank-version backups preserve drafts, immutable attempts and shuffled session order. All 51 Management Accounting records are present; filters return 46 scored questions and exclude five unresolved records.

## Browser flows

`node tests/browser.test.mjs` passed using Chromium:

- Feedback and original student-answer excerpts stay hidden before submission. Original option labels remain attached to shuffled answers so letter references stay valid.
- Draft notes, selections and shuffled option order restore after reload. A complete persistent-browser restart restores notes and the submitted attempt.
- Submission snapshots remain unchanged after feedback edits and retries. The history view retains correct, incorrect and unknown attempts separately.
- An error offers another question targeting the misconception, with different numbers/scenario.
- Export downloads valid JSON. Import confirmation and cancellation work, backups merge once, and invalid backups leave data untouched.
- Reset requires confirmation. Escape cancels even after an earlier confirmed reset or import. Native dialog return values are reset whenever a dialog opens.
- The skip link, radio selection by Space/arrow keys, submission by Enter and feedback focus work. The import control has a visible keyboard focus indicator.
- Layouts at 375, 768, 1024 and 1440 pixels have no horizontal page overflow. Large text and reduced-motion mode were checked. On narrow screens, the notebook appears before submission and feedback.
- Corrupt saved data remains untouched and offers a recovery download. Failed storage writes show a save failure; current in-memory notes can still be exported.
- Topic cards start sessions in the selected topic. Management Accounting grading, notebook capture, history statistics and its five review entries were checked in the browser.
- Fresh mobile setup panels collapse so the study area is easier to reach. Reduced-motion mode disables animations, confirmed through computed styles.
- No JavaScript page errors were recorded.

Desktop and mobile screenshots were visually inspected. Text, controls, feedback and the notebook fit without overlap or clipping.

## Apple design checks

Applied the requested `apple-design` skill and the companion `emil-design-eng` guidance from `emilkowalski/skills`, commit `e8a175d`.

- Verified press feedback starts during pointer-down, before session creation on release.
- Questions have no entry animation. Keyboard submission retains focus and has no running animation or transition. Pointer feedback uses 160ms transitions.
- Touch emulation does not match mouse hover styling. Phone selects and notebook inputs use at least 16px text. Notes remain selectable.
- Study navigation stays at the viewport top while scrolling. The desktop, phone and large-text layout checks still pass.
- Emulated reduced-transparency and increased-contrast preferences disable toolbar blur and strengthen separation. Reduced-motion still disables animation and press movement.
- Visually inspected the updated desktop and phone welcome screens and notebook. No clipping or overlap was found.

## Limits

This is a Chromium regression check and visual review, not a formal accessibility certification. Safari, Firefox, physical phones and assistive-technology sessions were not independently tested. Touch checks used Chromium emulation; actual iPhone keyboard/zoom and translucency behavior still need a device check. Browser data belongs to its browser/origin; automatic cross-device synchronization is not implemented. The existing GitHub Pages configuration serves the main branch from the repository root.
