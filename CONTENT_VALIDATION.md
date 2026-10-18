# Content validation — Phase 1

Bank version: 2026-10-09.1. Extension content gate passed before the interface refresh. The original bank was validated on 30 September 2026.

**179 questions imported/authored: 161 validated for scoring, 18 unresolved for review.** All 143 question bodies in four banks were imported: 25 Consolidated Statements, 25 Financial Reporting, 42 Auditing, 51 Management Accounting. Batch headings mention some absent questions; absent bodies were not invented. The Financial Reporting bank places ABC questions 14–15 after AlphaTech; their ABC context is restored explicitly.

## Generated coverage

36 original study questions: 6 equity method, 6 impairment, 6 analytical procedures versus tests of details, 6 acquisition accounting, and 12 deferred tax. Each area mixes recognition, short applications and multi-step reasoning. Difficulty is an estimated study rating; generated questions have no official marks. Recent learner successes did not remove any topic. Tax distractors distinguish the temporary difference, the rate-adjusted amount, asset/liability direction and balance versus movement.

## Validation performed

- Read the bank wording and relevant Week 1–3 lesson sections. Student answers were never used as the key. No separate official exam solution bank was available.
- Reviewed every scored option for one defensible answer under the displayed assumptions. All 161 scored questions have exactly one stable correct option ID, a rule explanation, and specific option feedback/misconception tags.
- Independently recomputed 89 numerical results with a separate Decimal-based checker using discounted individual cash flows, carrying values, fair-value net assets, tax bases and signed profit corrections. Compared with both declared results and correct numeric option text where present. This is a separate calculation implementation; semantic review was performed by the author, not an external examiner.
- Verified source counts, unique IDs, distinct options, exact original raw excerpts, metadata, preserved marks, nonempty evidence and exclusion of unresolved keys. Ran `python3 content/validate_bank.py` successfully.
- Corrected a generated equity roll-forward arithmetic slip during this gate: 95,000 + 14,000 − 6,000 − 2,000 = **101,000**, with the key, option and calculation updated together.
- Units are explicit CHF, MCHF, currency units, physical units or percentages. The inventory set does not specify a currency; none was invented. Lease intermediate balances use cents; required final amounts round upward to CHF 1. Tax amounts apply enacted reversal rates. Partial goodwill, deferred-tax treatment of uplifts, dividend timing and DTA recovery assumptions are displayed per scenario.

## Source discrepancies and clarifications

Examples: Financial Reporting Batch 5 Q5 is **b**, the adverse price decline, rather than recorded c. Batch 1 Q5 is **b** despite the student’s “marked incorrect” note. OnOff Q28 is **d**, a CHF 4,500 net decrease under the stated correction assumptions, rather than recorded c. Mutter’s audit requirement follows listed status, not its two-year size figures. Goodwill under FER is graded only after specifying its capitalization policy; direct equity offset is an alternative taught in the lecture.

The local Quick Reference contains an erroneous acquisition-equity formula. Keys use the detailed lesson’s acquisition-date elimination, not that shortcut. General course discussions allow other-framework proportionate joint-venture accounting; current IFRS joint ventures use equity accounting. Lease transcript operating/finance concepts are not treated as current IFRS lessee exemptions.

All original wording, options and recorded answers remain in `original`; shared scenarios are preserved separately. Added assumptions, repaired context and option clarifications are recorded in `changes`. Illustrative 5% materiality percentages are explicitly authored study assumptions, not claimed to be present in the student tutorial or official exam rules. Audit market answers are tied to the historical course chart; sustainability answers concern its 2024 sample.

## Management accounting extension, 9 October 2026

Imported all 51 questions from the requested Management Accounting file, retaining wording, shared scenarios, tables, A–E options and marks. IDs include batch and question number to avoid collisions. A local source copy is retained in the parent course folder. Existing 128 question records and IDs are unchanged. The interface retains each original option label during shuffling, so cross-references such as A)–D) and lettered distractor explanations remain meaningful. “None/all of the above” is displayed as “none/all of the other answers” to remove positional ambiguity; original wording remains in JSON and the source excerpt. This display clarification is also shown in each affected question’s source details.

46 additions are scored, with explanations, calculations and option-specific diagnostic feedback. Five are excluded below. The 41 new numerical results were independently recomputed using Decimal-based cost-flow, CVP, allocation, markup and target-cost models. Whole-unit tax targets also check that one fewer unit fails the target. Course evidence is Week 4's lecture summary and underlying transcripts for cost classifications, manufacturing cost flows, CVP, job costing and pricing. Supplied answers and displayed Ecoreps solutions were treated as claims to check, not as authoritative keys. This was an author review with an independent calculation implementation, not an external examiner review.

Documented clarifications include Kyle's malformed option E range; Café Baer's target-volume context for contribution margin; gross profit with separately listed sales salaries; minimum whole-unit quantities; pre-tax versus after-tax target terminology; rounding and relevant-range assumptions. Terra's six components sum to CHF 4,340,000, conflicting with the source total of CHF 4,335,000. The practice table uses the component sum and explicitly states this assumption; the original table is preserved. Terra's stray company name “Wilde’s” is also corrected with a change record.

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
| ma-08-7.3 | Batch 8 — SS20 Question 7: Costing and pricing decisions / Q7.3 | B and D can both describe profitable incremental supply when willingness to pay is the attainable selling price. No market condition distinguishes B from D. The source solution selects D, but its explanation adds an unstated competition assumption. Needs revised wording before scoring. |
| ma-10-1.2 | Batch 10 — SS21 Question 1: Management and cost accounting concepts / Q1.2 | The source selects B, but the supplied Week 4 lessons do not establish the stated cost-type / cost-center / cost-object accounting sequence or its “why” criterion. Need the corresponding lecture or authoritative solution context to validate every statement; source key alone is insufficient. |
| ma-11-2.1 | Batch 11 — SS21 Question 2: Rucksack AG costing and breakeven / Q2.1 | The scenario says 28,000 backpacks were produced, but their direct materials alone would be 28,000 × 3.20 = 89,600, exceeding the 60,000 company total. PCC I backpack wages alone would be 84,000, exceeding that center’s 56,000 total. The displayed overhead-rate calculation ignores these contradictory totals. Production quantity or cost-allocation table needs correction. For 2.3 the administration/distribution allocation base is also unstated. |
| ma-11-2.2 | Batch 11 — SS21 Question 2: Rucksack AG costing and breakeven / Q2.2 | The scenario says 28,000 backpacks were produced, but their direct materials alone would be 28,000 × 3.20 = 89,600, exceeding the 60,000 company total. PCC I backpack wages alone would be 84,000, exceeding that center’s 56,000 total. The displayed overhead-rate calculation ignores these contradictory totals. Production quantity or cost-allocation table needs correction. For 2.3 the administration/distribution allocation base is also unstated. |
| ma-11-2.3 | Batch 11 — SS21 Question 2: Rucksack AG costing and breakeven / Q2.3 | The scenario says 28,000 backpacks were produced, but their direct materials alone would be 28,000 × 3.20 = 89,600, exceeding the 60,000 company total. PCC I backpack wages alone would be 84,000, exceeding that center’s 56,000 total. The displayed overhead-rate calculation ignores these contradictory totals. Production quantity or cost-allocation table needs correction. For 2.3 the administration/distribution allocation base is also unstated. |

## Evidence references

- `ACA Course Materials/Week 1/Lecture Summary.md` — reporting principles, Swiss reporting, equity-method mechanics, partial goodwill, and NCI. [Primary reference for equity-method context](https://www.ifrs.org/issued-standards/list-of-standards/ias-28-investments-in-associates-and-joint-ventures/).
- `ACA Course Materials/Week 2/Session2_Students.md` — Lease example: present value, interest and depreciation.
- `ACA Course Materials/Week 2/Session2_Students.md` — Impairment, slide 22: recoverable amount = max(FVLCD, VIU). [Primary reference](https://www.ifrs.org/issued-standards/list-of-standards/ias-36-impairment-of-assets/).
- `ACA Course Materials/Week 1/Lecture/Session1_Students.md` — Goodwill policy choices under IFRS and Swiss GAAP FER.
- `ACA Course Materials/Week 2/Lecture Summary.md` — defined-benefit obligations, investment risk, temporary differences, direction, and tax rate. [Primary reference for deferred-tax context](https://www.ifrs.org/content/dam/ifrs/publications/pdf-standards/english/2021/issued/part-a/ias-12-income-taxes.pdf).
- `ACA Course Materials/Week 3/HS26_Session3_Students.md` — Slides 24 and 28: legal audit requirements and independence; course context.
- `ACA Course Materials/Week 3/HS26_Session3_Students.md` — Audit Market of all Firms in Switzerland: historical course chart.
- `ACA Course Materials/Week 3/Lecture Summary.md` — audit purpose, reasonable assurance, and evidence.
- `ACA Course Materials/Week 3/HS26_Tutorial_3_Auditing_student.md` — Task 3: materiality benchmark and misstatement effects; explicit study thresholds where added.
- `ACA Course Materials/Week 3/HS26_Session3_Students.md` — Slide 52: qualified, adverse and disclaimer opinions. [Primary reference](https://www.iaasb.org/publications/international-standard-auditing-isa-705-revised-modifications-opinion-independent-auditor-s-report-3).
- `ACA Course Materials/Week 3/HS26_Session3_Students.md` — Slide 51: management and auditor going-concern responsibilities.
- `ACA Course Materials/Week 3/HS26_Session3_Students.md` — The Audit Expectations Gap, ACCA source. [Primary reference](https://www.accaglobal.com/gb/en/professional-insights/global-profession/expectation-gap.html).
- `ACA Course Materials/Week 3/HS26_Session3_Students.md` — Slide 50: analytical procedures and tests of details.
- `ACA Course Materials/Week 3/HS26_Session3_Students.md` — Audit reports: significant audit judgments and Key Audit Matters.
- `ACA Course Materials/Week 3/HS26_Session3_Students.md` — Slide 14: Three Lines Model. [Primary reference](https://www.theiia.org/globalassets/documents/resources/the-iias-three-lines-model-an-update-of-the-three-lines-of-defense-july-2020/three-lines-model-updated-english.pdf).
- `ACA Course Materials/Week 3/HS26_Session3_Students.md` — Slide 21: 87 of 89 assured reports had limited assurance, 2024 sample.

- `ACA Course Materials/Week 4/Lecture Summary.md` — management-accounting foundations, cost flow, CVP, costing systems, and pricing.

## Reproduce the content gate

From `aca-practice/`:

```sh
python3 content/validate_bank.py
```

To re-import and rebuild after an intentional source/content edit, run `python3 content/build_bank.py` then re-run validation. The builder uses the parent course-source folders; the delivered app uses only `questions.json`.
