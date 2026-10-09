# Implementation checks

Validated on 9 October 2026. All checks passed on the final implementation.

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

## Limits

This is a Chromium regression check and visual review, not a formal accessibility certification. Safari, Firefox and assistive-technology sessions were not independently tested. Browser data belongs to its browser/origin; automatic cross-device synchronization is not implemented. The existing GitHub Pages configuration serves the main branch from the repository root.
