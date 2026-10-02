# Content validation — Phase 1

Bank version: 2026-09-30.1. Content gate passed before interface implementation.

**128 questions imported/authored: 115 validated for scoring, 13 unresolved for review.** All 92 question bodies actually present in the three banks were imported: 25 Consolidated Statements, 25 Financial Reporting, 42 Auditing. Batch headings mention some absent questions; absent bodies were not invented. The Financial Reporting bank places ABC questions 14–15 after AlphaTech; their ABC context is restored explicitly.

## Generated coverage

36 original study questions: 6 equity method, 6 impairment, 6 analytical procedures versus tests of details, 6 acquisition accounting, and 12 deferred tax. Each area mixes recognition, short applications and multi-step reasoning. Difficulty is an estimated study rating; generated questions have no official marks. Recent learner successes did not remove any topic. Tax distractors distinguish the temporary difference, the rate-adjusted amount, asset/liability direction and balance versus movement.

## Validation performed

- Read the bank wording and relevant Week 1–3 lesson sections. Student answers were never used as the key. No separate official exam solution bank was available.
- Reviewed every scored option for one defensible answer under the displayed assumptions. All 115 scored questions have exactly one stable correct option ID, a rule explanation, and specific option feedback/misconception tags.
- Independently recomputed 48 numerical results with a separate Decimal-based checker using discounted individual cash flows, carrying values, fair-value net assets, tax bases and signed profit corrections. Compared with both declared results and correct numeric option text where present. This is a separate calculation implementation; semantic review was performed by the author, not an external examiner.
- Verified source counts, unique IDs, distinct options, exact original raw excerpts, metadata, preserved marks, nonempty evidence and exclusion of unresolved keys. Ran `python3 content/validate_bank.py` successfully.
- Corrected a generated equity roll-forward arithmetic slip during this gate: 95,000 + 14,000 − 6,000 − 2,000 = **101,000**, with the key, option and calculation updated together.
- Units are explicit CHF or MCHF. Lease intermediate balances use cents; required final amounts round upward to CHF 1. Tax amounts apply enacted reversal rates. Partial goodwill, deferred-tax treatment of uplifts, dividend timing and DTA recovery assumptions are displayed per scenario.

## Source discrepancies and clarifications

Examples: Financial Reporting Batch 5 Q5 is **b**, the adverse price decline, rather than recorded c. Batch 1 Q5 is **b** despite the student’s “marked incorrect” note. OnOff Q28 is **d**, a CHF 4,500 net decrease under the stated correction assumptions, rather than recorded c. Mutter’s audit requirement follows listed status, not its two-year size figures. Goodwill under FER is graded only after specifying its capitalization policy; direct equity offset is an alternative taught in the lecture.

The local Quick Reference contains an erroneous acquisition-equity formula. Keys use the detailed lesson’s acquisition-date elimination, not that shortcut. General course discussions allow other-framework proportionate joint-venture accounting; current IFRS joint ventures use equity accounting. Lease transcript operating/finance concepts are not treated as current IFRS lessee exemptions.

All original wording, options and recorded answers remain in `original`; shared scenarios are preserved separately. Added assumptions, repaired context and option clarifications are recorded in `changes`. Illustrative 5% materiality percentages are explicitly authored study assumptions, not claimed to be present in the student tutorial or official exam rules. Audit market answers are tied to the historical course chart; sustainability answers concern its 2024 sample.

## Unresolved source questions — excluded from scoring

| ID | Source question | Reason |
|---|---|---|
| cs-06 | IFRS joint venture — Question 4 / Q4 | Under current IFRS 11 a joint venture uses the equity method. Both proportionate consolidation (b) and full consolidation (c) are disallowed for this joint venture. The question has two correct responses; the course also discusses other-framework joint ventures. |
| cs-08 | Equity method — Swiss reporting and equity method, Question 4 / Q4 | The scenario names investor X, rather than investee Y, as earning profit and paying dividends. Option d is missing. If those amounts belonged to Y, 249.5 + 35% × (86.5 − 50.5) = 262.1 MCHF, but the source cannot be graded as written. |
| cs-15 | Acquisition accounting — AS20, Questions 16–22 / Q16 | Option c is false in direction, but option b states an unadjusted share of profit even though depreciable hidden reserves need an adjustment. No useful life or adjusted-profit basis is supplied. The recorded A, B, D response also conflicts with a single false-answer task. |
| cs-20 | Acquisition accounting — AS20, Questions 16–22 / Q21 | Acquisition-date NCI would be CHF 1,580. The requested 31 December 2018 NCI requires post-acquisition profits, distributions and uplift depreciation, none supplied. |
| cs-21 | Acquisition accounting — AS20, Questions 16–22 / Q22 | CHF 128,000 is the acquisition-date parent equity. The requested year-end amount needs subsequent parent/group changes. “Equity” also needs a parent-attributable versus total-group definition. |
| cs-24 | Acquisition accounting — BigCorp/InnoTech (2023), Questions 10–12 / Q12 | Parent BigCorp equity is not supplied in the shared scenario. CHF 2,835,000 cannot be verified from the available bank text. |
| fr-04 | Batch 1 — Questions 9–15 / Q11 | Option b appears to describe the IAS 17 problem that IFRS 16 addressed, but says “a problem with IFRS 16”. Option a does not specify framework or exemptions; aircraft swapping in c depends on contract terms. The temporal and framework wording is ambiguous. |
| fr-22 | Batch 6 — AlphaTech lease and depreciation questions 13–15 / Q14 | Independent amortization gives third-year interest CHF 1,044.48 → CHF 1,045 under the specified upward rounding, and principal CHF 3,155.52 → CHF 3,156. None of the four options matches. Recorded option d (1,044) rounds downward. |
| au-02 | Batch 2 — Questions 3.1–3.5 / Q3.1 | The provided lesson materials do not define this research-specific use of “fee recovery”. Its original article or answer key is needed; recorded answer b is unverified. |
| au-04 | Batch 2 — Questions 3.1–3.5 / Q3.3 | A representation letter is signed by management, not the auditor; the recorded a is wrong. Statements b and d involve a Swiss court ruling and internal signing arrangements absent from the supplied lessons and may both be defensible. Cannot establish one correct option. |
| au-07 | Batch 3 — Fraud AG materiality, Questions 4.1–4.2 / Q4.2 | The omitted sale increases profit by 2,000 and the omitted damage claim reduces it by 2,000: net correction is zero, but gross errors cannot simply be ignored. The source gives no materiality percentage or qualitative assessment. At an illustrative 5% of 45,000 = 2,250, gross errors total 4,000. None of the options expresses correction with zero net profit effect. |
| au-08 | Batch 3 — Fraud AG materiality, Questions 4.1–4.2 / Q3.5 | The wording conflates unrecognized misstatements, disclosed valuation uncertainty and going-concern uncertainty. Adequate disclosure and material/pervasive effects are missing. Emphasis of matter is not a substitute for a necessary modification or the dedicated going-concern section. |
| au-15 | Batch 4 — Questions 16–23 / Q22 | Analytical procedures may themselves be substantive. “Greater focus on substantive procedures” does not distinguish limited from ordinary audit reliably, and “analytical and substantive” treats overlapping categories as exclusive. Source needs a clearer comparison. |

## Evidence references

- `ACA Course Materials/Week 1/Module 1 — Transcript Summary.md` — Sections 2–4: principles and Swiss reporting.
- `ACA Course Materials/Week 1/Module 1 — Transcript Summary.md` — Section 7: initial cost, profit, dividends and hidden-reserve depreciation. [Primary reference](https://www.ifrs.org/issued-standards/list-of-standards/ias-28-investments-in-associates-and-joint-ventures/).
- `ACA Course Materials/Week 1/Module 1 — Transcript Summary.md` — Section 6.2: partial goodwill and NCI.
- `ACA Course Materials/Week 2/Session2_Students.md` — Lease example: present value, interest and depreciation.
- `ACA Course Materials/Week 2/Session2_Students.md` — Impairment, slide 22: recoverable amount = max(FVLCD, VIU). [Primary reference](https://www.ifrs.org/issued-standards/list-of-standards/ias-36-impairment-of-assets/).
- `ACA Course Materials/Week 1/Lecture/Session1_Students.md` — Goodwill policy choices under IFRS and Swiss GAAP FER.
- `ACA Course Materials/Week 2/Module 2 — Transcript Summary.md` — Section 7: defined benefit obligations and investment risk.
- `ACA Course Materials/Week 2/Module 2 — Transcript Summary.md` — Sections 9.5–9.9: temporary differences, direction and tax rate. [Primary reference](https://www.ifrs.org/content/dam/ifrs/publications/pdf-standards/english/2021/issued/part-a/ias-12-income-taxes.pdf).
- `ACA Course Materials/Week 3/HS26_Session3_Students.md` — Slides 24 and 28: legal audit requirements and independence; course context.
- `ACA Course Materials/Week 3/HS26_Session3_Students.md` — Audit Market of all Firms in Switzerland: historical course chart.
- `ACA Course Materials/Week 3/Module 3 — Transcript Summary.md` — Sections 1, 4–6: audit purpose, reasonable assurance and evidence.
- `ACA Course Materials/Week 3/HS26_Tutorial_3_Auditing_student.md` — Task 3: materiality benchmark and misstatement effects; explicit study thresholds where added.
- `ACA Course Materials/Week 3/HS26_Session3_Students.md` — Slide 52: qualified, adverse and disclaimer opinions. [Primary reference](https://www.iaasb.org/publications/international-standard-auditing-isa-705-revised-modifications-opinion-independent-auditor-s-report-3).
- `ACA Course Materials/Week 3/HS26_Session3_Students.md` — Slide 51: management and auditor going-concern responsibilities.
- `ACA Course Materials/Week 3/HS26_Session3_Students.md` — The Audit Expectations Gap, ACCA source. [Primary reference](https://www.accaglobal.com/gb/en/professional-insights/global-profession/expectation-gap.html).
- `ACA Course Materials/Week 3/HS26_Session3_Students.md` — Slide 50: analytical procedures and tests of details.
- `ACA Course Materials/Week 3/HS26_Session3_Students.md` — Audit reports: significant audit judgments and Key Audit Matters.
- `ACA Course Materials/Week 3/HS26_Session3_Students.md` — Slide 14: Three Lines Model. [Primary reference](https://www.theiia.org/globalassets/documents/resources/the-iias-three-lines-model-an-update-of-the-three-lines-of-defense-july-2020/three-lines-model-updated-english.pdf).
- `ACA Course Materials/Week 3/HS26_Session3_Students.md` — Slide 21: 87 of 89 assured reports had limited assurance, 2024 sample.

## Reproduce the content gate

From `aca-practice/`:

```sh
python3 content/validate_bank.py
```

To re-import and rebuild after an intentional source/content edit, run `python3 content/build_bank.py` then re-run validation. The builder uses the parent course-source folders; the delivered app uses only `questions.json`.
