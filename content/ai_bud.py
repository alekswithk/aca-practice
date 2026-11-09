"""20 AI-generated Budgeting questions."""
from ai_common import add, D, chf, n, pct, table, none_wrong, none_right
T = 'Budgeting'
MIS = 'budgeting-calculation'

# Scenario A: Altura Outdoor AG
bp_q, bp_p, tn_q, tn_p = 48_000, 95, 12_500, 340
bp_beg, bp_end, tn_prod, tn_end = 6_200, 4_800, 13_000, 2_100
fab, fab_beg, fab_end, fab_p = D('1.5'), 8_000, 6_500, D('7.20')
bp_h, tn_h = D('0.8'), D('2.5')
rev = bp_q * bp_p + tn_q * tn_p; bp_prod = bp_q + bp_end - bp_beg; tn_beg = tn_q + tn_end - tn_prod
fab_need = bp_prod * fab; fab_buy = fab_need + fab_end - fab_beg; fab_cost = fab_buy * fab_p; hours = bp_prod * bp_h + tn_prod * tn_h
ALT = ('Altura Outdoor AG plans its 2026 budget. It expects to sell 48,000 backpacks at CHF 95 and 12,500 tents at CHF 340.\n\n'
       + table(['Budget data', 'Backpacks', 'Tents'], [['Beginning finished goods (units)', n(bp_beg), '?'], ['Desired ending finished goods (units)', n(bp_end), n(tn_end)],
                                                       ['Planned production (units)', '?', n(tn_prod)], ['Sewing hours per unit', '0.8', '2.5']]) +
       '\n\nEach backpack uses 1.5 m² of fabric at CHF 7.20 per m². Fabric inventory is 8,000 m² at the start of the year; Altura wants 6,500 m² at year-end.')
G = 'Altura Outdoor budget'
add('ai-bud-01', T, 'Sales budget', 'Easy', '(2 marks) What is Altura’s budgeted revenue for 2026?',
 [(chf(bp_q * bp_p), 'Only backpacks. Tents must be included.', MIS), (chf(rev), f'48,000 × 95 + 12,500 × 340 = {chf(rev)}.', None),
  (chf(bp_prod * bp_p + tn_prod * tn_p), 'Uses production instead of sales volumes.', MIS), (chf((bp_q + tn_q) * (bp_p + tn_p) / 2), 'Uses an average price for all units; each product needs its own price.', MIS), none_wrong('b')],
 'b', 'Sales budget = budgeted units × budgeted price, product by product.', scenario=ALT, ev='budget', group=G,
 calc=f'4,560,000 + 4,250,000 = {chf(rev)}.', check={'f': 'a*b + c*d', 'v': {'a': bp_q, 'b': bp_p, 'c': tn_q, 'd': tn_p}, 'x': rev})
add('ai-bud-02', T, 'Production budget', 'Easy', '(2 marks) How many backpacks must Altura produce in 2026?',
 [(n(bp_q + bp_beg - bp_end), 'Reverses the inventory adjustment.', MIS), (n(bp_q + bp_end), 'Ignores the beginning inventory that is already available.', MIS),
  (n(bp_prod), f'48,000 + 4,800 − 6,200 = {n(bp_prod)}.', None), (n(bp_q), 'Equals sales; the inventory change is missing.', MIS), none_wrong('c')],
 'c', 'Production = budgeted sales + desired ending inventory − beginning inventory.', scenario=ALT, ev='budget', group=G,
 calc=f'{n(bp_q)} + {n(bp_end)} − {n(bp_beg)} = {n(bp_prod)}.', check={'f': 's + e - b', 'v': {'s': bp_q, 'e': bp_end, 'b': bp_beg}, 'x': bp_prod, 'unit': 'units'})
add('ai-bud-03', T, 'Production budget', 'Medium', '(2 marks) What beginning inventory of tents does Altura’s plan require?',
 [(n(tn_prod - tn_q + tn_end), 'Signs reversed on ending inventory.', MIS), (n(tn_q - tn_prod + tn_end + tn_end), 'Counts the ending inventory twice.', MIS),
  (n(tn_end), 'Assumes beginning equals ending inventory.', MIS), (n(tn_beg), f'Beginning = sales + ending − production = 12,500 + 2,100 − 13,000 = {n(tn_beg)}.', None), none_wrong('d')],
 'd', 'Rearrange the production formula: beginning inventory = sales + ending inventory − production.', scenario=ALT, ev='budget', group=G,
 calc=f'12,500 + 2,100 − 13,000 = {n(tn_beg)}.', check={'f': 's + e - p', 'v': {'s': tn_q, 'e': tn_end, 'p': tn_prod}, 'x': tn_beg, 'unit': 'units'})
add('ai-bud-04', T, 'Purchases budget', 'Hard', '(3 marks) What is the budgeted cost of fabric purchases for backpacks in 2026?',
 [(chf(fab_need * fab_p), 'This is the cost of fabric used; the fabric inventory change is missing.', MIS),
  (chf(bp_q * fab * fab_p + (fab_end - fab_beg) * fab_p), 'Bases fabric needs on sales instead of production.', MIS),
  (chf(fab_buy * fab_p), f'Fabric needed {n(fab_need)} m² + 6,500 − 8,000 = {n(fab_buy)} m²; × 7.20 = {chf(fab_cost)}.', None),
  (chf((fab_need + fab_beg - fab_end) * fab_p), 'Reverses the fabric inventory adjustment.', MIS), none_wrong('c')],
 'c', 'Purchases = materials needed for production + desired ending materials − beginning materials.', scenario=ALT, ev='budget', group=G,
 calc=f'Production {n(bp_prod)} × 1.5 = {n(fab_need)} m². Purchases = {n(fab_need)} + 6,500 − 8,000 = {n(fab_buy)} m². Cost = {n(fab_buy)} × 7.20 = {chf(fab_cost)}.',
 check={'f': '((s + e - b)*k + y - x)*c', 'v': {'s': bp_q, 'e': bp_end, 'b': bp_beg, 'k': fab, 'y': fab_end, 'x': fab_beg, 'c': fab_p}, 'x': fab_cost})
add('ai-bud-05', T, 'Direct labor budget', 'Medium', '(3 marks) How many sewing hours does Altura budget for 2026?',
 [(n(bp_q * bp_h + tn_q * tn_h), 'Uses sales volumes. Labor follows production.', MIS), (n(bp_prod * bp_h + tn_prod * tn_h), f'46,600 × 0.8 + 13,000 × 2.5 = {n(hours)} hours.', None),
  (n((bp_prod + tn_prod) * bp_h), 'Applies the backpack rate of 0.8 hours to tents too.', MIS), (n(bp_prod * bp_h), 'Only backpacks.', MIS), none_wrong('b')],
 'b', 'Direct labor hours = planned production × hours per unit, summed over products.', scenario=ALT, ev='budget', group=G,
 calc=f'{n(bp_prod*bp_h)} + {n(tn_prod*tn_h)} = {n(hours)} hours.', check={'f': '(s + e - b)*h + p*k', 'v': {'s': bp_q, 'e': bp_end, 'b': bp_beg, 'h': bp_h, 'p': tn_prod, 'k': tn_h}, 'x': hours, 'unit': 'units'})

# Scenario B: Mirelli Gelato cash collections
apr, may, jun = 82_000, 118_000, 164_000
cash_jun = D('0.2') * jun + D('0.8') * D('0.6') * may + D('0.8') * D('0.38') * apr
MIR = ('Mirelli Gelato GmbH budgets sales of CHF 82,000 in April, CHF 118,000 in May and CHF 164,000 in June. 20% of sales are paid in cash. '
       'The rest is sold on account: 60% of credit sales are collected in the following month, 38% two months after the sale, and 2% are never collected.')
G = 'Mirelli Gelato cash budget'
add('ai-bud-06', T, 'Cash collections', 'Hard', '(3 marks) How much cash does Mirelli collect in June?',
 [(chf(cash_jun), f'June cash 32,800 + 60% of May credit 56,640 + 38% of April credit 24,928 = {chf(cash_jun)}.', None),
  (chf(D('0.2') * jun + D('0.6') * may + D('0.38') * apr), 'Applies the collection rates to total sales instead of credit sales.', MIS),
  (chf(D('0.2') * jun + D('0.8') * D('0.6') * may), 'Leaves out the collections from April sales.', MIS),
  (chf(D('0.2') * jun + D('0.8') * D('0.38') * may + D('0.8') * D('0.6') * apr), 'Swaps the one-month and two-month collection rates.', MIS), none_wrong('a')],
 'a', 'Collections in a month = cash sales of the month + collections of earlier credit sales by their timing.', scenario=MIR, ev='budget', group=G,
 calc=f'0.2 × 164,000 = 32,800; 0.8 × 0.6 × 118,000 = 56,640; 0.8 × 0.38 × 82,000 = 24,928. Total {chf(cash_jun)}.',
 check={'f': 'c*j + (1-c)*a*m + (1-c)*b*p', 'v': {'c': 0.2, 'a': 0.6, 'b': 0.38, 'j': jun, 'm': may, 'p': apr}, 'x': cash_jun})
add('ai-bud-07', T, 'Cash collections', 'Easy', '(2 marks) How much of May’s sales does Mirelli expect never to collect?',
 [(chf(D('0.02') * may), 'Applies 2% to all of May’s sales, including the cash sales.', MIS), (chf(D('0.8') * D('0.02') * may), f'80% × 118,000 × 2% = {chf(D("0.8")*D("0.02")*may)}.', None),
  (chf(D('0.2') * may), 'This is the cash part of May sales.', MIS), (chf(D('0.8') * D('0.38') * may), 'This is the two-month collection, not the uncollectible part.', MIS), none_wrong('b')],
 'b', 'Bad debts apply only to credit sales.', scenario=MIR, ev='budget', group=G,
 calc=f'Credit sales 94,400 × 2% = {chf(D("0.8")*D("0.02")*may)}.', check={'f': '(1-c)*d*m', 'v': {'c': 0.2, 'd': 0.02, 'm': may}, 'x': D('0.8') * D('0.02') * may})

# Scenario C: Kiosko Retail purchases
s = {'Jan': 210_000, 'Feb': 180_000, 'Mar': 240_000, 'Apr': 260_000}
gm, inv = D('0.35'), D('0.15')
cogs = {k: v * (1 - gm) for k, v in s.items()}
feb = cogs['Feb'] + inv * cogs['Mar'] - inv * cogs['Feb']; mar = cogs['Mar'] + inv * cogs['Apr'] - inv * cogs['Mar']
KIO = ('Kiosko Retail AG forecasts sales of CHF 210,000 for January, CHF 180,000 for February, CHF 240,000 for March and CHF 260,000 for April. '
       'Its gross margin is 35% of sales. Ending inventory each month must equal 15% of the next month’s cost of goods sold.')
G = 'Kiosko Retail purchases'
add('ai-bud-08', T, 'Purchases budget', 'Medium', '(3 marks) What are Kiosko’s budgeted purchases for February?',
 [(chf(cogs['Feb']), 'This is February COGS; the inventory change is missing.', MIS), (chf(feb), f'COGS 117,000 + ending 23,400 − beginning 17,550 = {chf(feb)}.', None),
  (chf(s['Feb'] + inv * s['Mar'] - inv * s['Feb']), 'Uses sales prices instead of cost.', MIS), (chf(cogs['Feb'] + inv * cogs['Feb'] - inv * cogs['Mar']), 'Reverses the inventory adjustment.', MIS), none_wrong('b')],
 'b', 'Purchases = COGS + desired ending inventory − beginning inventory (all at cost).', scenario=KIO, ev='budget', group=G,
 calc=f'COGS Feb = 180,000 × 65% = 117,000. Ending = 15% × 156,000 = 23,400. Beginning = 15% × 117,000 = 17,550. Purchases = {chf(feb)}.',
 check={'f': 'b*g + i*c*g - i*b*g', 'v': {'b': s['Feb'], 'c': s['Mar'], 'g': 0.65, 'i': inv}, 'x': feb})
add('ai-bud-09', T, 'Purchases budget', 'Medium', '(3 marks) What are Kiosko’s budgeted purchases for March?',
 [(chf(cogs['Mar']), 'This is March COGS without the inventory change.', MIS), (chf(cogs['Mar'] + inv * s['Apr'] - inv * cogs['Mar']), 'Values the ending inventory at April’s selling price instead of cost.', MIS),
  (chf(s['Mar'] * gm), 'This is the gross margin, not purchases.', MIS), (chf(cogs['Mar'] + inv * s['Apr'] - inv * s['Mar']), 'Values the inventories at selling price.', MIS),
  none_right(f'156,000 + 25,350 − 23,400 = {chf(mar)}, which is not listed.')],
 'e', 'Purchases = COGS + desired ending inventory − beginning inventory.', scenario=KIO, ev='budget', group=G,
 calc=f'COGS Mar 156,000 + ending 15% × 169,000 = 25,350 − beginning 23,400 = {chf(mar)}.', check={'f': 'b*g + i*c*g - i*b*g', 'v': {'b': s['Mar'], 'c': s['Apr'], 'g': 0.65, 'i': inv}, 'x': mar})

# Scenario D: Feldhof Markt activity-based budget
rates = {'order': 75, 'delivery': 96, 'hour': 26, 'item': D('0.15')}
use = {'Dairy': (22, 40, 120, 28_000), 'Bakery': (18, 65, 150, 31_000), 'Drinks': (12, 20, 60, 15_500)}
cost = {k: sum(D(a) * D(b) for a, b in zip(rates.values(), v)) for k, v in use.items()}
deliv = 96 * sum(v[1] for v in use.values())
FEL = ('Feldhof Markt AG uses activity-based budgeting. Budgeted activity rates: ordering CHF 75 per order, delivery CHF 96 per delivery, shelf-stocking CHF 26 per hour and customer support CHF 0.15 per item sold.\n\n'
       + table(['Activity use', 'Dairy', 'Bakery', 'Drinks'], [['Orders', '22', '18', '12'], ['Deliveries', '40', '65', '20'], ['Shelf-stocking hours', '120', '150', '60'], ['Items sold', '28,000', '31,000', '15,500']]))
G = 'Feldhof Markt ABB'
add('ai-bud-10', T, 'Activity-based budgeting', 'Easy', '(2 marks) What is the total budgeted delivery cost for all three product lines?',
 [(chf(deliv), f'(40 + 65 + 20) × 96 = {chf(deliv)}.', None), (chf(65 * 96), 'Only bakery deliveries.', MIS), (chf(52 * 96), 'Uses the number of orders instead of deliveries.', MIS),
  (chf(125 * 75), 'Uses the ordering rate instead of the delivery rate.', MIS), none_wrong('a')],
 'a', 'Activity cost = activity rate × quantity of the cost driver.', scenario=FEL, ev='budget', group=G,
 calc=f'125 deliveries × 96 = {chf(deliv)}.', check={'f': 'r*(a + b + c)', 'v': {'r': 96, 'a': 40, 'b': 65, 'c': 20}, 'x': deliv})
add('ai-bud-11', T, 'Activity-based budgeting', 'Medium', '(2 marks) What are the total budgeted activity costs for bakery products?',
 [(chf(cost['Bakery'] - 31_000 * D('0.15')), 'Leaves out customer support costs.', MIS), (chf(cost['Dairy']), 'This is the dairy figure.', MIS),
  (chf(cost['Bakery'] + 18 * 75), 'Counts ordering costs twice.', MIS), (chf(cost['Bakery']), f'1,350 + 6,240 + 3,900 + 4,650 = {chf(cost["Bakery"])}.', None), none_wrong('d')],
 'd', 'Add each activity’s rate × driver quantity for the product line.', scenario=FEL, ev='budget', group=G,
 calc=f'18 × 75 + 65 × 96 + 150 × 26 + 31,000 × 0.15 = {chf(cost["Bakery"])}.', check={'f': 'a*75 + b*96 + c*26 + d*0.15', 'v': {'a': 18, 'b': 65, 'c': 150, 'd': 31_000}, 'x': cost['Bakery']})
add('ai-bud-12', T, 'Activity-based budgeting', 'Medium', '(2 marks) What are the total budgeted activity costs for dairy products?',
 [(chf(cost['Dairy']), f'1,650 + 3,840 + 3,120 + 4,200 = {chf(cost["Dairy"])}.', None), (chf(cost['Dairy'] - 120 * 26), 'Leaves out shelf-stocking.', MIS),
  (chf(cost['Drinks']), 'This is the drinks figure.', MIS), (chf(22 * 96 + 40 * 75 + 120 * 26 + 28_000 * D('0.15')), 'Swaps the ordering and delivery rates.', MIS), none_wrong('a')],
 'a', 'Add each activity’s rate × driver quantity for the product line.', scenario=FEL, ev='budget', group=G,
 calc=f'22 × 75 + 40 × 96 + 120 × 26 + 28,000 × 0.15 = {chf(cost["Dairy"])}.', check={'f': 'a*75 + b*96 + c*26 + d*0.15', 'v': {'a': 22, 'b': 40, 'c': 120, 'd': 28_000}, 'x': cost['Dairy']})

r13 = 386_000
add('ai-bud-13', T, 'Income statement budget', 'Easy', '(2 marks) Pavona Store AG forecasts March revenue of CHF 386,000 and cost of goods sold of 62% of revenue. What is the budgeted gross margin?',
 [(chf(r13 * D('0.62')), 'This is cost of goods sold.', MIS), (chf(r13 * D('0.38')), f'386,000 × 38% = {chf(r13*D("0.38"))}.', None),
  (chf(r13 / D('1.62')), 'Treats 62% as a markup on cost.', MIS), (chf(r13 * D('0.62') * D('0.38')), 'Multiplies both percentages.', MIS), none_wrong('b')],
 'b', 'Gross margin = revenue − COGS.', ev='budget', calc=f'386,000 × (1 − 62%) = {chf(r13*D("0.38"))}.', check={'f': 'r*(1 - c)', 'v': {'r': r13, 'c': 0.62}, 'x': r13 * D('0.38')})
r14, fx = 1_240_000, 310_000
oi14 = r14 * (1 - D('0.58') - D('0.06')) - fx
add('ai-bud-14', T, 'Income statement budget', 'Medium', '(3 marks) Tessin Velo AG budgets revenue of CHF 1,240,000. COGS is 58% of revenue, sales commissions are 6% of revenue and fixed operating expenses are CHF 310,000. What is budgeted operating income?',
 [(chf(r14 * D('0.42') - fx), 'Leaves out the 6% sales commissions.', MIS), (chf(r14 * D('0.36')), 'Leaves out the fixed operating expenses.', MIS),
  (chf(oi14), f'1,240,000 × 36% − 310,000 = {chf(oi14)}.', None), (chf(r14 * D('0.36') - fx * D('1.06')), 'Applies the commission rate to fixed costs.', MIS), none_wrong('c')],
 'c', 'Operating income = revenue − COGS − variable selling costs − fixed operating expenses.', ev='budget',
 calc=f'Contribution after COGS and commissions = 1,240,000 × 36% = 446,400. Less 310,000 = {chf(oi14)}.', check={'f': 'r*(1 - c - k) - f', 'v': {'r': r14, 'c': 0.58, 'k': 0.06, 'f': fx}, 'x': oi14})

# Sensitivity: Orbis Kaffee AG
units0, p0, vc0, fx0 = 290_000, 5, 870_000, 410_000
units1, p1 = units0 * D('0.92'), p0 * D('1.1')
rev1 = units1 * p1; oi0 = units0 * p0 - vc0 - fx0; oi1 = rev1 - vc0 * D('0.92') - fx0
ORB = ('Orbis Kaffee AG reports for 2025: sales CHF 1,450,000 on 290,000 units, cost of goods sold CHF 870,000 (fully variable), fixed operating expenses CHF 410,000 and operating income CHF 170,000. '
       'For 2026 management considers raising the price by 10%, which is expected to reduce volume by 8%.')
G = 'Orbis Kaffee price change'
add('ai-bud-15', T, 'Sensitivity analysis', 'Medium', '(2 marks) What is budgeted 2026 revenue if the price increase is implemented?',
 [(chf(units0 * p1), 'Ignores the 8% drop in volume.', MIS), (chf(rev1), f'266,800 units × CHF 5.50 = {chf(rev1)}.', None),
  (chf(units0 * p0 * D('1.02')), 'Nets the two percentages (+10% − 8% = +2%). They multiply.', MIS), (chf(units1 * p0), 'Ignores the price increase.', MIS), none_wrong('b')],
 'b', 'New revenue = new volume × new price.', scenario=ORB, ev='budget', group=G,
 calc=f'Volume 290,000 × 0.92 = 266,800; price 5.50; revenue {chf(rev1)}.', check={'f': 'q*(1 - d)*p*(1 + u)', 'v': {'q': units0, 'd': 0.08, 'p': p0, 'u': 0.1}, 'x': rev1})
add('ai-bud-16', T, 'Sensitivity analysis', 'Hard', '(3 marks) Should Orbis implement the price increase, based on operating income?',
 [(f'Yes, because operating income rises to {chf(oi1)}', f'Revenue {n(rev1)} − variable COGS {n(vc0*D("0.92"))} − fixed 410,000 = {chf(oi1)}, above 170,000.', None),
  (f'No, because operating income falls to {chf(units1*p0 - vc0*D("0.92") - fx0)}', 'Applies the lower volume but forgets the higher price.', MIS),
  (f'Yes, because operating income rises to {chf(rev1 - vc0 - fx0)}', 'Keeps COGS at the old volume. COGS is variable and falls by 8%.', MIS),
  ('No, because volume falls', 'Lower volume alone does not decide it; the price effect is larger.', MIS), none_wrong('a')],
 'a', 'Compare operating income before and after, with variable costs moving with volume.', scenario=ORB, ev='budget', group=G,
 calc=f'Revenue {n(rev1)}; COGS 870,000 × 0.92 = {n(vc0*D("0.92"))}; OI = {chf(oi1)} vs. {chf(oi0)}.', check={'f': 'q*(1 - d)*p*(1 + u) - v*(1 - d) - f', 'v': {'q': units0, 'd': 0.08, 'p': p0, 'u': 0.1, 'v': vc0, 'f': fx0}, 'x': oi1})
add('ai-bud-17', T, 'Master budget', 'Easy', '(2 marks) A master budget _____.',
 [('is prepared only for the cash account', 'The cash budget is one part of the master budget.', MIS),
  ('summarizes the operating and financial budgets of the whole organization for a period', 'It brings together operating budgets and financial budgets into one plan.', None),
  ('reports actual results at the end of the year', 'A budget is a plan, not a record of actual results.', MIS),
  ('is the same as a flexible budget', 'A flexible budget adjusts to actual volume; the master budget is the original plan.', MIS), none_wrong('b')],
 'b', 'The master budget is the comprehensive plan for a period, made of operating and financial budgets.', ev='budget')
add('ai-bud-18', T, 'Master budget', 'Medium', '(2 marks) Which of the following belongs to the financial budget rather than the operating budget?',
 [('Production budget', 'Part of the operating budget.', MIS), ('Direct materials purchases budget', 'Part of the operating budget.', MIS),
  ('Budgeted cash flow statement (cash budget)', 'The cash budget, capital expenditure budget and budgeted balance sheet form the financial budget.', None),
  ('Sales budget', 'The sales budget starts the operating budget.', MIS), none_wrong('c')],
 'c', 'Operating budgets lead to the budgeted income statement; financial budgets cover cash, capital spending and the balance sheet.', ev='budget')
add('ai-bud-19', T, 'Profit planning', 'Easy', '(2 marks) What is budgetary slack?',
 [('The difference between actual and budgeted sales', 'That is a sales variance.', MIS), ('Deliberately underestimating revenues or overestimating costs to make targets easier', 'Managers build in slack to protect themselves against missing targets.', None),
  ('Unused production capacity', 'That is idle capacity.', MIS), ('Cash kept for emergencies', 'That is a liquidity reserve.', MIS), none_wrong('b')],
 'b', 'Budgetary slack is a known risk of participative budgeting.', ev='budget')
mp, ap = 90_000, 120_000
paid = ap * D('0.4') * D('0.98') + mp * D('0.6')
add('ai-bud-20', T, 'Cash disbursements', 'Medium', '(3 marks) Gerber Bürobedarf AG buys goods on account for CHF 90,000 in March and CHF 120,000 in April. It pays 40% in the month of purchase and takes a 2% early-payment discount on that part; the remaining 60% is paid in full the following month. How much cash does Gerber pay to suppliers in April?',
 [(chf(ap * D('0.4') + mp * D('0.6')), 'Ignores the 2% discount.', MIS), (chf(paid), f'120,000 × 40% × 98% + 90,000 × 60% = 47,040 + 54,000 = {chf(paid)}.', None),
  (chf(ap * D('0.4') * D('0.98') + ap * D('0.6')), 'Pays April’s own 60% in April; it is paid in May.', MIS), (chf(mp * D('0.4') * D('0.98') + ap * D('0.6')), 'Swaps the March and April purchases.', MIS), none_wrong('b')],
 'b', 'Cash disbursements follow the payment pattern; discounts reduce the amount paid.', ev='budget',
 calc=f'47,040 + 54,000 = {chf(paid)}.', check={'f': 'a*0.4*0.98 + m*0.6', 'v': {'a': ap, 'm': mp}, 'x': paid})
