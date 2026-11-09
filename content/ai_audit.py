"""20 AI-generated Auditing questions."""
from ai_common import add, chf, n, table
T = 'Auditing'

ebt, inv_err, sale_err, m = 1_800_000, 140_000, 20_000, 0.05
mat = ebt * m; net = -inv_err + sale_err
MAT = ('Gravita Uhren AG is subject to an ordinary audit of its 2025 financial statements. It is a highly successful, profit-oriented watchmaker with stable earnings. The auditors found two misstatements:\n\n'
       '1. Finished watches worth CHF 140,000 were counted twice in the year-end inventory count.\n'
       '2. A CHF 20,000 sale delivered and invoiced on 30 December 2025 was not recorded.\n\n'
       + table(['Account, 31.12.2025 (CHF)', 'Amount'], [['Total assets', '62,000,000'], ['Revenue', '24,500,000'], ['Cost of goods sold', '15,900,000'],
                                                         ['Operating expenses', '6,300,000'], ['Interest expense', '500,000'], ['Earnings before taxes', n(ebt)]]))
MA = ['Study clarification: use 5% of stable pre-tax profit as the illustrative quantitative threshold, as in the tutorial examples in this app. This is not an official exam rule.']
G = 'Gravita Uhren materiality'
add('ai-au-01', T, 'Materiality', 'Easy', '(1 mark) Which benchmark should the auditors use for preliminary materiality, following the rationale discussed in the tutorials?',
 [('Materiality based on total assets', 'Assets suit asset-heavy or loss-making entities. Gravita is profitable with stable earnings, so users focus on profit.', 'materiality-benchmark'),
  ('Materiality based on income before taxes', 'For a stable, profit-oriented company, pre-tax income is the figure users care most about.', None),
  ('Materiality based on cost of goods sold', 'Cost of goods sold is not a standard materiality benchmark.', 'materiality-benchmark'),
  ('No materiality is needed in an ordinary audit', 'Every audit needs a materiality level to plan and evaluate misstatements.', 'materiality-audit-scope')],
 'b', 'Profit-oriented companies with stable earnings use income before taxes as the benchmark.', scenario=MAT, assume=MA, ev='materiality', group=G)
add('ai-au-02', T, 'Materiality', 'Medium', '(1 mark) What is the preliminary materiality level for Gravita?',
 [(chf(mat), f'5% × CHF {n(ebt)} = {chf(mat)}.', None),
  (chf(24_500_000 * m), 'Applies the profit percentage to revenue.', 'materiality-benchmark'),
  (chf(62_000_000 * m), 'Applies the profit percentage to total assets.', 'materiality-benchmark'),
  (chf(ebt * 0.5), 'Uses 50% instead of 5%.', 'materiality-mechanical')],
 'a', 'Materiality = benchmark × percentage.', scenario=MAT, assume=MA, ev='materiality', group=G,
 calc=f'5% × {n(ebt)} = {chf(mat)}.', check={'f': 'e*p', 'v': {'e': ebt, 'p': m}, 'x': mat})
add('ai-au-03', T, 'Materiality', 'Hard', '(2 marks) Based on the materiality level and the misstatements found, will the auditors advise Gravita to correct them? If so, what is the effect of the correction?',
 [(f'Yes; increase in earnings before taxes of {chf(-net)}', 'Gets the size right but the direction wrong. Removing the double-counted inventory lowers profit more than the missing sale raises it.', 'misstatement-direction'),
  (f'Yes; decrease in earnings before taxes of {chf(inv_err+sale_err)}', 'Treats the unrecorded sale as another overstatement. Recording the sale increases profit.', 'misstatement-direction'),
  (f'Yes; decrease in earnings before taxes of {chf(-net)}', f'Inventory correction −140,000, sale +20,000, net −120,000. That exceeds materiality of {chf(mat)}.', None),
  ('No correction needed', 'The net effect of CHF 120,000 is above the CHF 90,000 materiality level.', 'materiality-ignore-aggregation')],
 'c', 'Aggregate the misstatements with their signs and compare the net effect with materiality.', scenario=MAT, assume=MA, ev='materiality', group=G,
 calc=f'Materiality {n(mat)}. Correction = −140,000 + 20,000 = −120,000 (decrease in EBT), above materiality.',
 check={'f': 'a - b', 'v': {'a': inv_err, 'b': sale_err}, 'x': -net, 'same': 'a'})
add('ai-au-04', T, 'Materiality', 'Medium', '(1 mark) Novaterra Biotech AG, a research company, has made losses in each of its first four years. Which benchmark is most suitable for its preliminary materiality?',
 [('Income before taxes', 'Pre-tax income is negative and volatile, so it gives an unstable or meaningless threshold.', 'materiality-benchmark'),
  ('Total assets', 'For a loss-making company, a balance-sheet benchmark such as total assets gives a stable base.', None),
  ('Net income after taxes', 'After-tax income is also negative and volatile.', 'materiality-benchmark'),
  ('The audit fee', 'The fee says nothing about what users of the statements would consider material.', 'materiality-mechanical')],
 'b', 'Choose a stable benchmark that matters to users. When profit is negative or volatile, total assets is used.', ev='materiality')

BRUNN = table(['Brunnwald AG (unlisted)', '2025', '2024'], [['Total assets', 'CHF 24 million', 'CHF 22 million'], ['Revenue', 'CHF 36 million', 'CHF 38 million'], ['Full-time positions (annual average)', '270', '260']])
add('ai-au-05', T, 'Audit scope', 'Medium', '(2 marks) Brunnwald AG reports the figures below. Under the CO, an ordinary audit is required if two of the thresholds CHF 20 million total assets, CHF 40 million revenue and 250 full-time positions are exceeded in two consecutive years.\n\n' + BRUNN + '\n\nWhich statement is correct?',
 [('Brunnwald needs only a limited audit because its revenue is below CHF 40 million.', 'Revenue is one of three tests. Total assets and staff both exceed their thresholds in both years.', 'audit-scope'),
  ('Brunnwald needs an ordinary audit because total assets and staff exceed the thresholds in both years.', 'Two of three thresholds are exceeded in two consecutive years.', None),
  ('Brunnwald can opt out of any audit because it is not listed.', 'Opting out is only possible for companies with no more than ten full-time positions on annual average and shareholder consent.', 'audit-opt-out'),
  ('Brunnwald needs an ordinary audit only once it is listed.', 'Listing is one trigger, but the size test applies to unlisted companies as well.', 'audit-scope')],
 'b', 'Ordinary audit: listed companies, companies exceeding two of three size thresholds in two consecutive years, and companies required to prepare consolidated accounts.', ev='legal')
add('ai-au-06', T, 'Audit scope', 'Easy', '(1 mark) Which company can opt out of a limited audit with the consent of all shareholders?',
 [('An unlisted company with eight full-time positions on annual average', 'Opting out is allowed for companies with no more than ten full-time positions, if all shareholders agree.', None),
  ('A listed company with eight employees', 'Listed companies always need an ordinary audit.', 'audit-scope'),
  ('A company that must prepare consolidated accounts', 'These companies need an ordinary audit.', 'audit-scope'),
  ('An unlisted company with 40 full-time positions', 'With more than ten full-time positions, opting out is not possible.', 'audit-opt-out')],
 'a', 'Opting out requires no more than ten full-time positions on annual average and the consent of all shareholders.', ev='legal')
add('ai-au-07', T, 'Assurance', 'Easy', '(1 mark) What level of assurance does a limited audit under the Swiss CO provide?',
 [('Reasonable assurance, the same as an ordinary audit', 'An ordinary audit gives reasonable assurance; a limited audit gives less.', 'audit-assurance-level'),
  ('Absolute assurance that the accounts contain no errors', 'No audit gives absolute assurance.', 'audit-guarantee'),
  ('Limited assurance, expressed as a negative conclusion (“nothing has come to our attention…”)', 'A limited audit uses fewer procedures and states that nothing was found suggesting a material misstatement.', None),
  ('No assurance, because only the board signs the accounts', 'A limited audit still provides limited assurance.', 'audit-assurance-level')],
 'c', 'Ordinary audit: reasonable assurance, positive opinion. Limited audit: limited assurance, negative conclusion.', ev='audit')

for ident, prompt, key, why in [
 ('ai-au-08', '(1 mark) The auditor of Vellano Foods AG finds that inventory is overstated by an amount that is material and affects most areas of the financial statements. Management refuses to correct it. Which opinion is issued?', 'c', 'A material and pervasive misstatement leads to an adverse opinion.'),
 ('ai-au-09', '(1 mark) The auditor of Duran Optik AG finds a material misstatement in provisions. It is confined to that one item and is not pervasive. Management refuses to correct it. Which opinion is issued?', 'b', 'A material but not pervasive misstatement leads to a qualified opinion.'),
 ('ai-au-10', '(1 mark) A fire destroyed most accounting records of Kalmo Bau AG and the auditor cannot obtain sufficient appropriate evidence for most balances. Which opinion is issued?', 'd', 'If evidence is missing and the possible effects are material and pervasive, the auditor disclaims an opinion.')]:
 opts = [('Unmodified opinion', 'An unmodified opinion means no material misstatement was found and enough evidence was obtained.', 'audit-opinion-types'),
         ('Qualified opinion', 'A qualified opinion is for a material issue that is not pervasive.', 'audit-opinion-scope'),
         ('Adverse opinion', 'An adverse opinion is for material and pervasive misstatements.', 'audit-opinion-scope'),
         ('Disclaimer of opinion', 'A disclaimer is used when the auditor cannot obtain enough evidence and the possible effects are pervasive.', 'audit-opinion-scope')]
 i = 'abcd'.index(key); opts[i] = (opts[i][0], why, None)
 add(ident, T, 'Audit opinions', 'Medium', prompt, opts, key, 'Opinion type depends on whether the problem is a misstatement or missing evidence, and whether it is pervasive.', ev='opinion')

add('ai-au-11', T, 'Audit procedures', 'Easy', '(1 mark) Which of the following is an analytical procedure for revenue at Mirabel Hotels AG?',
 [('Comparing revenue per available room with the prior year and the regional average', 'Comparing a ratio with an expectation is an analytical procedure.', None),
  ('Inspecting a sample of guest invoices and matching them to bank receipts', 'This tests individual transactions: a test of details.', 'audit-analytical-vs-details'),
  ('Sending confirmation requests to corporate clients', 'Confirmations test specific balances: a test of details.', 'audit-analytical-vs-details'),
  ('Observing the night audit at the front desk', 'Observation of a process is not an analytical procedure.', 'audit-procedure-type')],
 'a', 'Analytical procedures evaluate plausible relationships among data; tests of details examine individual items.', ev='procedures')
add('ai-au-12', T, 'Audit procedures', 'Easy', '(1 mark) Which of the following is not an analytical procedure for accounts receivable?',
 [('Comparing days sales outstanding with the prior year', 'This is a ratio comparison, so it is analytical.', 'audit-analytical-vs-details'),
  ('Comparing the share of overdue receivables with last year', 'An ageing trend is analytical.', 'audit-analytical-vs-details'),
  ('Tracing selected receivables to cash received after year-end', 'Checking subsequent receipts for selected balances is a test of details.', None),
  ('Comparing the allowance for doubtful accounts with receivables over time', 'A ratio trend is analytical.', 'audit-analytical-vs-details')],
 'c', 'Tests of details look at specific items and supporting documents.', ev='procedures')
add('ai-au-13', T, 'Audit procedures', 'Medium', '(2 marks) Payroll expense at Fenwick Logistik AG rose 22% while headcount stayed flat. The auditor notes the gap, then selects ten employees and agrees their pay to contracts and bank transfers. How are the two steps classified?',
 [('Both steps are analytical procedures', 'Agreeing individual pay to contracts and transfers is a test of details.', 'audit-analytical-vs-details'),
  ('First a test of details, then an analytical procedure', 'The order is reversed.', 'audit-analytical-vs-details'),
  ('First an analytical procedure, then a test of details', 'Comparing expense growth with headcount is analytical; checking selected employees is a test of details.', None),
  ('Both steps are tests of controls', 'Neither step tests whether a control operated.', 'audit-procedure-type')],
 'c', 'Analytics point to risk; tests of details then examine specific items.', ev='procedures')
add('ai-au-14', T, 'Key Audit Matters', 'Medium', '(1 mark) Which statement about Key Audit Matters (KAMs) is correct?',
 [('KAMs are separate opinions on individual accounts.', 'KAMs do not change or split the audit opinion.', 'kam-routine-vs-significant'),
  ('KAMs describe the matters of most significance in the audit, such as complex valuations or impairment tests.', 'They highlight areas of significant auditor judgment.', None),
  ('KAMs list all errors that management corrected during the audit.', 'KAMs are not a list of corrected errors.', 'kam-routine-vs-significant'),
  ('KAMs usually cover routine disclosures such as directors’ fees.', 'Routine items are rarely KAMs.', 'kam-routine-vs-significant')],
 'b', 'KAMs tell users where the auditor focused most judgment; they are not separate opinions.', ev='kam')
add('ai-au-15', T, 'Going concern', 'Easy', '(1 mark) True or false: Management is responsible for assessing whether the company can continue as a going concern, and the auditor evaluates whether that assessment is appropriate.',
 [('True', 'Management makes the assessment; the auditor obtains evidence and concludes on it.', None),
  ('False', 'Both have roles: management assesses, the auditor evaluates.', 'going-concern-responsibility')],
 'a', 'Going concern: management assesses, the auditor evaluates and reports on material uncertainty.', ev='going')
add('ai-au-16', T, 'Expectation gap', 'Medium', '(1 mark) Many retail investors believe that a clean audit opinion guarantees the company will not fail. Which part of the audit expectation gap does this reflect?',
 [('Performance gap', 'The performance gap is about auditors not meeting existing standards.', 'expectation-gap-taxonomy'),
  ('Knowledge gap', 'The public misunderstands what an audit is and does.', None),
  ('Evolution gap', 'The evolution gap is about where the profession should develop in future.', 'expectation-gap-taxonomy'),
  ('Independence gap', 'This is not one of the three components discussed.', 'expectation-gap-taxonomy')],
 'b', 'The ACCA splits the expectation gap into knowledge, performance and evolution gaps.', ev='gap')
add('ai-au-17', T, 'Three Lines Model', 'Easy', '(1 mark) In the Three Lines Model, which role does internal audit play?',
 [('First line: running operations and managing risk day to day', 'That is operational management.', 'three-lines-first'),
  ('Second line: setting risk and compliance policies', 'That is risk management and compliance.', 'three-lines-governance'),
  ('Third line: independent and objective assurance to the board', 'Internal audit gives independent assurance on governance, risk and control.', None),
  ('External assurance provider reporting to shareholders', 'That is the external auditor, outside the three lines.', 'internal-external-audit')],
 'c', 'Internal audit is the third line; external audit sits outside the model.', ev='lines')
add('ai-au-18', T, 'Independence', 'Medium', '(1 mark) Which situation is not compatible with auditor independence under CO Article 728?',
 [('The audit partner attends a public seminar on watch industry trends.', 'General education does not threaten independence.', 'independence-familiarity'),
  ('The audit partner’s spouse is the CFO of the audit client.', 'A close family link to a person in a key financial role is incompatible.', None),
  ('The audit firm charges a fee agreed in advance with the board.', 'An agreed audit fee is normal.', 'audit-fee-drivers'),
  ('The audit team asks management for explanations of unusual items.', 'Asking questions is part of the audit.', 'independence-governance')],
 'b', 'Close personal relationships with people in key positions at the client impair independence.', ev='legal')
add('ai-au-19', T, 'Professional skepticism', 'Medium', '(1 mark) The CFO of Marlo AG gives the auditor a signed customer letter that contradicts the shipping records. What does professional skepticism require?',
 [('Accept the letter because the CFO is responsible for the financial statements', 'Management’s responsibility does not make its evidence conclusive.', 'skepticism-management'),
  ('Investigate the inconsistency, for example by contacting the customer directly', 'A questioning mind follows up contradictory evidence with independent sources.', None),
  ('Ignore the shipping records because a signed letter is stronger evidence', 'Conflicting evidence must be resolved, not ignored.', 'skepticism-inconsistency'),
  ('Rely on internal controls instead of the evidence', 'Controls do not resolve a specific contradiction.', 'skepticism-controls')],
 'b', 'Professional skepticism means a questioning mind and critical assessment of evidence.', ev='audit')
add('ai-au-20', T, 'Internal controls', 'Easy', '(1 mark) Which is an inherent limitation of an internal control system?',
 [('It cannot prevent collusion between employees or management override.', 'Controls rely on people and can be bypassed.', None),
  ('It always detects fraud.', 'No control system detects every fraud.', 'controls-objectives'),
  ('It makes an external audit unnecessary.', 'Good controls do not replace the external audit.', 'controls-objectives'),
  ('It guarantees the company’s profitability.', 'Controls give reasonable assurance on objectives, not profit.', 'controls-objectives')],
 'a', 'Internal controls provide reasonable, not absolute, assurance.', ev='audit')
