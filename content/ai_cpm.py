"""20 AI-generated Cost and Performance Management questions."""
from ai_common import add, D, r, chf, n, pct, table, none_wrong, none_right
T = 'Cost and Performance Management'
MIS = 'cost and performance management-calculation'

debt, kd, eq, ke, tax = 18_000_000, D('0.06'), 27_000_000, D('0.11'), D('0.20')
wacc = (debt * kd * (1 - tax) + eq * ke) / (debt + eq)
divs = {'Industrial': (4_200_000, 30_000_000, 4_000_000, 33_600_000), 'Consumer': (2_100_000, 14_000_000, 2_500_000, 16_800_000)}
eva = {k: v[0] * (1 - tax) - (v[1] - v[2]) * wacc for k, v in divs.items()}
NOR = ('Nordwerk Holding AG is financed with debt of CHF 18 million (market value) at an interest rate of 6% and equity with a market value of CHF 27 million; shareholders require a return of 11%. The tax rate is 20%. '
       'Its two divisions report for 2025:\n\n' + table(['Division', 'EBIT', 'Total assets', 'Current liabilities', 'Revenue'],
       [[k, chf(v[0]), chf(v[1]), chf(v[2]), chf(v[3])] for k, v in divs.items()]))
G = 'Nordwerk Holding'
add('ai-cpm-01', T, 'Weighted average cost of capital', 'Medium', '(2 marks) Calculate Nordwerk’s WACC using market-value weights.',
 [(pct(100 * (debt * kd + eq * ke) / (debt + eq), 2), 'Uses the pre-tax cost of debt. Interest is tax-deductible, so use 6% × (1 − 20%).', MIS),
  (pct(100 * wacc, 2), f'(18m × 6% × 0.8 + 27m × 11%) / 45m = {pct(100*wacc,2)}.', None),
  (pct(100 * (kd * (1 - tax) + ke) / 2, 2), 'Averages the two rates equally instead of weighting by market values.', MIS),
  (pct(100 * (eq * kd * (1 - tax) + debt * ke) / (debt + eq), 2), 'Swaps the weights of debt and equity.', MIS), none_wrong('b')],
 'b', 'WACC = [D × kd × (1 − t) + E × ke] / (D + E), with market values.', scenario=NOR, ev='cpm', group=G,
 calc=f'Debt: 18m × 4.8% = 0.864m. Equity: 27m × 11% = 2.97m. WACC = 3.834m / 45m = {pct(100*wacc,2)}.',
 check={'f': '100*(d*a*(1 - t) + e*b)/(d + e)', 'v': {'d': debt, 'a': kd, 'e': eq, 'b': ke, 't': tax}, 'x': 100 * wacc, 'dp': 2, 'unit': 'percent'})
i = divs['Industrial']
add('ai-cpm-02', T, 'Economic value added', 'Hard', '(3 marks) Calculate the EVA of the Industrial division.',
 [(chf(i[0] - (i[1] - i[2]) * wacc), 'Uses EBIT before tax. EVA starts from after-tax operating income.', MIS), (chf(i[0] * (1 - tax) - i[1] * wacc), 'Charges capital on total assets; current liabilities should be deducted.', MIS),
  (chf((i[1] - i[2]) * wacc), 'This is the capital charge only.', MIS), (chf(eva['Industrial']), f'3,360,000 − 26,000,000 × 8.52% = {chf(eva["Industrial"])}.', None), none_wrong('d')],
 'd', 'EVA = EBIT × (1 − t) − WACC × (total assets − current liabilities).', scenario=NOR, ev='cpm', group=G,
 calc=f'NOPAT = 4,200,000 × 0.8 = 3,360,000. Invested capital = 26,000,000. Capital charge = 26,000,000 × {pct(100*wacc,2)} = {n((i[1]-i[2])*wacc)}. EVA = {chf(eva["Industrial"])}.',
 check={'f': 'x*(1 - t) - (a - c)*(d*k*(1 - t) + e*q)/(d + e)', 'v': {'x': i[0], 'a': i[1], 'c': i[2], 'd': debt, 'k': kd, 'e': eq, 'q': ke, 't': tax}, 'x': eva['Industrial']})
c_ = divs['Consumer']
add('ai-cpm-03', T, 'Economic value added', 'Hard', '(3 marks) Calculate the EVA of the Consumer division.',
 [(chf(eva['Consumer']), f'1,680,000 − 11,500,000 × 8.52% = {chf(eva["Consumer"])}.', None), (chf(c_[0] * (1 - tax)), 'This is NOPAT, before the capital charge.', MIS),
  (chf(c_[0] * (1 - tax) - c_[1] * wacc), 'Charges capital on total assets.', MIS), (chf(c_[0] - (c_[1] - c_[2]) * wacc), 'Uses EBIT before tax.', MIS), none_wrong('a')],
 'a', 'EVA = NOPAT − WACC × invested capital.', scenario=NOR, ev='cpm', group=G,
 calc=f'NOPAT 1,680,000; capital 11,500,000 × {pct(100*wacc,2)} = {n((c_[1]-c_[2])*wacc)}; EVA = {chf(eva["Consumer"])}.',
 check={'f': 'x*(1 - t) - (a - c)*(d*k*(1 - t) + e*q)/(d + e)', 'v': {'x': c_[0], 'a': c_[1], 'c': c_[2], 'd': debt, 'k': kd, 'e': eq, 'q': ke, 't': tax}, 'x': eva['Consumer']})
add('ai-cpm-04', T, 'Return on investment', 'Easy', '(2 marks) Calculate the Industrial division’s return on investment, defined as EBIT / total assets.',
 [(pct(100 * D(i[0]) / i[1], 1), '4,200,000 / 30,000,000 = 14.0%.', None), (pct(100 * D(i[0]) / (i[1] - i[2]), 1), 'Uses assets net of current liabilities. The definition given uses total assets.', MIS),
  (pct(100 * D(i[0]) / i[3], 1), 'This is return on sales.', MIS), (pct(100 * i[0] * (1 - tax) / i[1], 1), 'Uses after-tax EBIT.', MIS), none_wrong('a')],
 'a', 'ROI = income / investment, using the definitions given.', scenario=NOR, ev='cpm', group=G,
 calc='4,200,000 / 30,000,000 = 14.0%.', check={'f': '100*x/a', 'v': {'x': i[0], 'a': i[1]}, 'x': 100 * D(i[0]) / i[1], 'dp': 1, 'unit': 'percent'})
add('ai-cpm-05', T, 'Return on sales', 'Easy', '(2 marks) Calculate the Consumer division’s return on sales (EBIT / revenue).',
 [(pct(100 * D(c_[0]) / c_[1], 1), 'Divides by total assets.', MIS), (pct(100 * c_[0] * (1 - tax) / c_[3], 1), 'Uses after-tax EBIT.', MIS),
  (pct(100 * D(c_[0]) / c_[3], 1), '2,100,000 / 16,800,000 = 12.5%.', None), (pct(100 * D(c_[3]) / c_[1], 1), 'This is asset turnover × 100, not return on sales.', MIS), none_wrong('c')],
 'c', 'Return on sales = EBIT / revenue.', scenario=NOR, ev='cpm', group=G,
 calc='2,100,000 / 16,800,000 = 12.5%.', check={'f': '100*x/s', 'v': {'x': c_[0], 's': c_[3]}, 'x': 100 * D(c_[0]) / c_[3], 'dp': 1, 'unit': 'percent'})
ri = i[0] - D('0.10') * i[1]
add('ai-cpm-06', T, 'Residual income', 'Medium', '(2 marks) Nordwerk sets a required return of 10% on total assets for residual income. What is the Industrial division’s residual income?',
 [(chf(ri), '4,200,000 − 10% × 30,000,000 = 1,200,000.', None), (chf(i[0] * (1 - tax) - D('0.10') * i[1]), 'Uses after-tax EBIT; residual income here uses EBIT.', MIS),
  (chf(i[0] - D('0.10') * (i[1] - i[2])), 'Deducts current liabilities; the definition uses total assets.', MIS), (chf(D('0.10') * i[1]), 'This is the required return only.', MIS), none_wrong('a')],
 'a', 'Residual income = income − required rate × investment.', scenario=NOR, ev='cpm', group=G,
 calc='4,200,000 − 3,000,000 = CHF 1,200,000.', check={'f': 'x - 0.10*a', 'v': {'x': i[0], 'a': i[1]}, 'x': ri})
ebit7, ros7 = 3_150_000, D('0.14')
add('ai-cpm-07', T, 'Return on sales', 'Medium', '(2 marks) The Outdoor division of Selmar AG reports EBIT of CHF 3,150,000 and a return on sales of 14%. Calculate the division’s revenue.',
 [(chf(ebit7 * ros7), 'Multiplies by the ratio instead of dividing.', MIS), (chf(ebit7 / ros7), '3,150,000 / 0.14 = 22,500,000.', None),
  (chf(ebit7 * (1 + ros7)), 'Adds 14% to EBIT.', MIS), (chf(ebit7 / (1 - ros7)), 'Divides by 86%.', MIS), none_wrong('b')],
 'b', 'Revenue = EBIT / return on sales.', ev='cpm', calc='3,150,000 / 0.14 = CHF 22,500,000.', check={'f': 'x/r', 'v': {'x': ebit7, 'r': ros7}, 'x': ebit7 / ros7})
add('ai-cpm-08', T, 'Return on investment', 'Medium', '(2 marks) A division has a return on sales of 8% and an asset turnover (revenue / total assets) of 1.5. What is its ROI (EBIT / total assets)?',
 [('9.5%', 'Adds the two figures.', MIS), ('5.3%', 'Divides return on sales by asset turnover.', MIS), ('12.0%', 'ROI = return on sales × asset turnover = 8% × 1.5 = 12%.', None), ('18.8%', 'Divides asset turnover by return on sales.', MIS), none_wrong('c')],
 'c', 'DuPont: ROI = (EBIT / revenue) × (revenue / assets).', ev='cpm', calc='8% × 1.5 = 12.0%.', check={'f': '100*r*t', 'v': {'r': 0.08, 't': 1.5}, 'x': 12, 'dp': 1, 'unit': 'percent'})

BSC = [
 ('ai-cpm-09', 'Balanced scorecard perspectives', 'Easy', '(1 mark) Which measure belongs to the learning-and-growth perspective of the balanced scorecard?', [
  ('Training hours per employee', 'It tracks investment in people’s skills.', None), ('Market share', 'Customer perspective.', 'bsc-perspective'), ('Defect rate in production', 'Internal business process perspective.', 'bsc-perspective'), ('Return on investment', 'Financial perspective.', 'bsc-perspective')], 'a'),
 ('ai-cpm-10', 'Balanced scorecard perspectives', 'Easy', '(1 mark) Which measure belongs to the internal-business-process perspective?', [
  ('Customer satisfaction score', 'Customer perspective.', 'bsc-perspective'), ('Order-to-delivery cycle time', 'It measures how well a core process works.', None), ('Revenue growth', 'Financial perspective.', 'bsc-perspective'), ('Employee turnover', 'Learning and growth perspective.', 'bsc-perspective')], 'b'),
 ('ai-cpm-11', 'Balanced scorecard perspectives', 'Easy', '(1 mark) Which question does the customer perspective of the balanced scorecard answer?', [
  ('How do we look to shareholders?', 'Financial perspective.', 'bsc-perspective'), ('What must we excel at internally?', 'Internal business process perspective.', 'bsc-perspective'),
  ('How do customers see us?', 'That is the customer perspective.', None), ('How can we keep improving and creating value?', 'Learning and growth perspective.', 'bsc-perspective')], 'c'),
 ('ai-cpm-12', 'Balanced scorecard measures', 'Easy', '(1 mark) Which is a financial-perspective measure?', [
  ('Number of new patents', 'Learning and growth or process perspective.', 'bsc-perspective'), ('Percentage of on-time deliveries', 'Customer or process perspective.', 'bsc-perspective'),
  ('Employee satisfaction', 'Learning and growth perspective.', 'bsc-perspective'), ('Economic value added', 'EVA is a financial measure.', None)], 'd'),
 ('ai-cpm-13', 'Balanced scorecard purpose', 'Easy', '(1 mark) Which statement best describes the purpose of the balanced scorecard?', [
  ('It replaces financial measures with non-financial ones.', 'It keeps financial measures and adds others.', 'bsc-purpose'), ('It translates strategy into measures across several perspectives and reduces the focus on short-term financial results.', 'It balances financial and non-financial, short- and long-term measures.', None),
  ('It is used mainly for external reporting.', 'It is an internal management tool.', 'bsc-purpose'), ('It ranks employees by salary.', 'It is not a pay ranking.', 'bsc-purpose')], 'b'),
 ('ai-cpm-14', 'Balanced scorecard implementation', 'Medium', '(1 mark) Which statement about implementing a balanced scorecard is correct?', [
  ('The more measures, the better the scorecard.', 'Too many measures dilute focus.', 'bsc-implementation'), ('Measures should be linked by cause and effect to the strategy.', 'A good scorecard tells the strategy as a chain of cause and effect.', None),
  ('Non-financial measures should be left out because they are hard to quantify.', 'Non-financial measures are central to the scorecard.', 'bsc-implementation'), ('Each perspective should be managed independently of the others.', 'Perspectives are linked.', 'bsc-implementation')], 'b'),
]
for ident, sub, diff, prompt, opts, key in BSC:
 add(ident, T, sub, diff, prompt, opts + [none_wrong(key)], key, 'The balanced scorecard measures performance in four linked perspectives: financial, customer, internal business process, and learning and growth.', ev='cpm')

add('ai-cpm-15', T, 'Weighted average cost of capital', 'Easy', '(1 mark) Why are market values preferred to book values when weighting WACC?',
 [('Market values reflect what investors currently require on the capital they could withdraw.', 'They measure the opportunity cost of capital today.', None), ('Book values change daily and are too volatile.', 'Market values are the ones that move daily.', MIS),
  ('Book values are not available for listed companies.', 'Book values are always in the balance sheet.', MIS), ('Market values ignore taxes.', 'Weights are unrelated to taxes.', MIS), none_wrong('a')],
 'a', 'WACC weights use market values because they reflect investors’ current claims.', ev='cpm')
add('ai-cpm-16', T, 'Economic value added', 'Easy', '(1 mark) What does a positive EVA mean?',
 [('The division earns more after tax than the cost of the capital it uses.', 'NOPAT exceeds the capital charge.', None), ('The division has positive EBIT.', 'Positive EBIT can still be below the capital charge.', MIS),
  ('The division’s ROI is above its return on sales.', 'EVA compares profit with capital cost, not two ratios.', MIS), ('The division has no debt.', 'EVA says nothing about the financing mix of a division.', MIS), none_wrong('a')],
 'a', 'EVA > 0 means value is created above the cost of capital.', ev='cpm')
add('ai-cpm-17', T, 'Return on investment', 'Medium', '(1 mark) A division earns an ROI of 18%. Its cost of capital is 10%. The manager rejects a project with an expected ROI of 14%. Which problem does this show?',
 [('ROI can lead managers to reject projects that would add value, because they lower the division’s average ROI.', 'The project beats the 10% cost of capital but would dilute the 18% ROI, so goal congruence fails.', None),
  ('ROI ignores the size of the investment.', 'ROI is a ratio of income to investment; the issue here is the incentive.', MIS), ('The project has a negative EVA.', 'At 14% vs 10% the project has a positive EVA.', MIS),
  ('ROI cannot be used for divisions.', 'ROI is commonly used for divisions.', MIS), none_wrong('a')],
 'a', 'ROI-based targets can conflict with company-wide value creation; EVA and residual income avoid this.', ev='cpm')
inc18, assets18 = 2_400_000, 16_000_000
add('ai-cpm-18', T, 'Return on investment', 'Medium', '(2 marks) Ventara AG’s Services division earns EBIT of CHF 2,400,000 on total assets of CHF 16,000,000. Management sells idle equipment worth CHF 1,000,000 at book value and uses the cash to repay group debt; EBIT is unchanged. What is the division’s new ROI (EBIT / total assets)?',
 [(pct(100 * D(inc18) / assets18, 1), 'This is the ROI before the asset sale.', MIS), (pct(100 * D(inc18) / (assets18 + 1_000_000), 1), 'Adds the equipment instead of removing it.', MIS),
  (pct(100 * D(inc18 - 1_000_000) / assets18, 1), 'Deducts the sale from EBIT; the sale at book value has no profit effect.', MIS), (pct(100 * D(inc18) / (assets18 - 1_000_000), 1), '2,400,000 / 15,000,000 = 16.0%.', None), none_wrong('d')],
 'd', 'Reducing the asset base with unchanged income raises ROI.', ev='cpm',
 calc='2,400,000 / 15,000,000 = 16.0%.', check={'f': '100*x/(a - s)', 'v': {'x': inc18, 'a': assets18, 's': 1_000_000}, 'x': 100 * D(inc18) / (assets18 - 1_000_000), 'dp': 1, 'unit': 'percent'})
d19, e19, kd19, ke19, t19 = 6_000_000, 9_000_000, D('0.05'), D('0.12'), D('0.25')
w19 = 100 * (d19 * kd19 * (1 - t19) + e19 * ke19) / (d19 + e19)
add('ai-cpm-19', T, 'Weighted average cost of capital', 'Medium', '(2 marks) Hallwil Systems AG has debt with a market value of CHF 6 million at 5% and equity with a market value of CHF 9 million at a required return of 12%. The tax rate is 25%. Calculate WACC.',
 [(pct(100 * (d19 * kd19 + e19 * ke19) / (d19 + e19), 2), 'Uses the pre-tax cost of debt.', MIS), (pct(100 * (e19 * kd19 * (1 - t19) + d19 * ke19) / (d19 + e19), 2), 'Swaps the weights.', MIS),
  (pct(100 * (kd19 * (1 - t19) + ke19) / 2, 2), 'Uses equal weights.', MIS), (pct(100 * (d19 * kd19 + e19 * ke19) * (1 - t19) / (d19 + e19), 2), 'Applies the tax shield to equity too. Only interest is tax-deductible.', MIS), none_right(f'(6m × 5% × 0.75 + 9m × 12%) / 15m = {pct(w19,2)}, which is not listed.')],
 'e', 'WACC = [D × kd × (1 − t) + E × ke] / (D + E).', ev='cpm',
 calc=f'Debt 6m × 3.75% = 0.225m; equity 9m × 12% = 1.08m; WACC = 1.305m / 15m = {pct(w19,2)}.', check={'f': '100*(d*a*(1 - t) + e*b)/(d + e)', 'v': {'d': d19, 'a': kd19, 'e': e19, 'b': ke19, 't': t19}, 'x': w19, 'dp': 2, 'unit': 'percent'})
add('ai-cpm-20', T, 'Balanced scorecard perspectives', 'Medium', '(1 mark) A hotel chain wants higher repeat bookings. Which chain of balanced-scorecard objectives shows a plausible cause-and-effect link, from the bottom up?',
 [('Revenue growth → staff training → guest satisfaction → faster check-in', 'The order is reversed; financial results come last.', 'bsc-implementation'),
  ('Staff training → faster check-in → guest satisfaction → revenue growth', 'Learning and growth drives processes, which drive customers, which drive financial results.', None),
  ('Guest satisfaction → revenue growth → faster check-in → staff training', 'Financial results do not cause process improvements in this chain.', 'bsc-implementation'),
  ('Faster check-in → revenue growth → staff training → guest satisfaction', 'The perspectives are out of order.', 'bsc-implementation'), none_wrong('b')],
 'b', 'Learning and growth → internal processes → customer → financial.', ev='cpm')
