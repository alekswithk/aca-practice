"""20 AI-generated Management Accounting questions (five options, CHF with ’ separators)."""
from ai_common import add, D, r, chf, n, pct, table, none_wrong, none_right
T = 'Management Accounting'
S = '’'
c = lambda x, dp=0, mode='half': chf(x, dp, S, mode)
u = lambda x, dp=0, mode='half': n(x, dp, S, mode)

# Scenario A: Talvik Keramik AG
mat, wage, rate, fm, fo, price, q = D('2.40'), 32, 8, 54_000, 18_000, 12, 9_000
var = mat + D(wage) / rate; cogm = var * q + fm; unit = (cogm + fo) / q; oi = price * q - cogm - fo
be = (fm + fo) / (price - var); be_up = r(be, 0, 'up')
TAL = ('Talvik Keramik AG makes hand-thrown coffee mugs. Clay and glaze cost CHF 2.40 per mug. Potters are paid CHF 32 per hour and make eight mugs per hour.\n\n'
       'Fixed manufacturing costs are CHF 54’000 this year. Fixed costs not assigned to manufacturing (administration and marketing) are CHF 18’000. All other costs are variable manufacturing costs as described.')
G = 'Talvik Keramik'
add('ai-ma-01', T, 'Manufacturing cost flows', 'Easy', '(2 marks) Talvik makes and sells 9’000 mugs this year. Calculate the total cost of goods manufactured.',
 [(c(var*q), 'Leaves out the fixed manufacturing costs, which are part of manufacturing cost.', 'manufacturing-overhead-omitted'),
  (c(cogm), f'(2.40 + 32/8) × 9’000 + 54’000 = {c(cogm)}.', None),
  (c(cogm + fo), 'Adds the non-manufacturing fixed costs, which are period costs.', 'period-cost-in-inventory'),
  (c((mat + wage) * q + fm), 'Uses the hourly wage per mug instead of dividing it by eight mugs per hour.', 'labor-productivity'),
  none_wrong('b')],
 'b', 'COGM = direct materials + direct labor + manufacturing overhead for the units made.', scenario=TAL, ev='ma-flow', group=G,
 calc=f'Variable cost per mug = 2.40 + 4.00 = 6.40. COGM = 6.40 × 9’000 + 54’000 = {c(cogm)}.', check={'f': '(m + w/k)*q + f', 'v': {'m': mat, 'w': wage, 'k': rate, 'q': q, 'f': fm}, 'x': cogm})
add('ai-ma-02', T, 'Manufacturing cost flows', 'Medium', '(3 marks) Calculate the total cost per mug (manufacturing and non-manufacturing) at 9’000 mugs.',
 [(c(cogm/q, 2), 'This is the manufacturing cost per mug only; it leaves out the CHF 18’000 of other fixed costs.', 'total-versus-unit-cost'),
  (c(var, 2), 'This is the variable cost per mug only.', 'fixed-cost-omitted'),
  (c(unit, 2), f'({u(cogm)} + 18’000) / 9’000 = {c(unit,2)}.', None),
  (c((cogm + fo) / 10_000, 2), 'Divides by 10’000 mugs instead of the 9’000 made.', 'total-cost-reconciliation'),
  none_wrong('c')],
 'c', 'Full unit cost = (all manufacturing costs + non-manufacturing costs) / units.', scenario=TAL, ev='ma-flow', group=G,
 calc=f'({u(cogm)} + 18’000) / 9’000 = {c(unit,2)}.', check={'f': '((m + w/k)*q + f + o)/q', 'v': {'m': mat, 'w': wage, 'k': rate, 'q': q, 'f': fm, 'o': fo}, 'x': unit, 'dp': 2})
add('ai-ma-03', T, 'CVP analysis', 'Medium', '(3 marks) Calculate Talvik’s operating income if it sells 9’000 mugs at CHF 12 each.',
 [(c(price*q - cogm), 'Leaves out the CHF 18’000 of non-manufacturing fixed costs.', 'period-cost-omitted'),
  (c(-oi), 'Right amount but the wrong sign. Costs exceed revenue, so this is a loss.', 'loss-sign'),
  (c(price*q - var*q), 'This is the contribution margin, before fixed costs.', 'contribution-versus-profit'),
  (c(oi), f'108’000 − {u(cogm)} − 18’000 = {c(oi)}.', None),
  none_wrong('d')],
 'd', 'Operating income = revenue − all costs (manufacturing and non-manufacturing).', scenario=TAL, ev='ma-cvp', group=G,
 calc=f'Revenue 108’000 − COGM {u(cogm)} − other fixed 18’000 = {c(oi)}.', check={'f': 'p*q - (m + w/k)*q - f - o', 'v': {'p': price, 'm': mat, 'w': wage, 'k': rate, 'q': q, 'f': fm, 'o': fo}, 'x': oi, 'same': 'b'})
add('ai-ma-04', T, 'CVP analysis', 'Hard', '(3 marks) How many mugs must Talvik sell at CHF 12 at least, so that it does not make a loss?',
 [(u(r(fm/(price-var), 0, 'up')) + ' mugs', 'Uses only the fixed manufacturing costs. The CHF 18’000 of other fixed costs must also be covered.', 'fixed-cost-omitted'),
  (u(r((fm+fo)/price, 0, 'up')) + ' mugs', 'Divides fixed costs by the price instead of the contribution margin per mug.', 'cvp-break-even-profit'),
  (u(r(be, 0, 'down')) + ' mugs', 'Rounds down. At this volume Talvik still makes a small loss.', 'minimum-quantity-rounding'),
  (u(be_up) + ' mugs', f'72’000 / (12 − 6.40) = {u(be,2)}, rounded up to {u(be_up)} mugs.', None),
  none_wrong('d')],
 'd', 'Break-even units = fixed costs / contribution margin per unit, rounded up to whole units.', scenario=TAL, ev='ma-cvp', group=G,
 calc=f'Contribution margin per mug = 12 − 6.40 = 5.60. 72’000 / 5.60 = {u(be,2)} → {u(be_up)} mugs.', check={'f': '(f + o)/(p - m - w/k)', 'v': {'p': price, 'm': mat, 'w': wage, 'k': rate, 'f': fm, 'o': fo}, 'x': be, 'mode': 'up', 'unit': 'units'})

# Scenario B: Bergluft Velo AG
p, v, F, tax, target, qty = 450, 270, 1_260_000, D('0.25'), 189_000, 9_500
cmr = D(p - v) / p; ber = F / cmr; pre = target / (1 - tax); units = (F + pre) / (p - v); ni = (qty * (p - v) - F) * (1 - tax)
BERG = ('Bergluft Velo AG runs e-bike service centres. The average service package sells for CHF 450. Parts and other variable costs are CHF 270 per package. Fixed costs are CHF 1’260’000 per year. The income tax rate is 25%.')
G = 'Bergluft Velo'
add('ai-ma-05', T, 'CVP analysis', 'Easy', '(1 mark) Calculate the contribution margin ratio.',
 [(pct(100 * (1 - cmr), 0), 'This is the variable-cost ratio, not the contribution margin ratio.', 'cvp-cost-ratio'),
  (pct(100 * cmr, 0), f'(450 − 270) / 450 = {pct(100*cmr,0)}.', None),
  (pct(100 * D(p - v) / v, 0), 'Divides the contribution margin by variable cost instead of price.', 'markup-denominator'),
  (pct(25, 0), 'This is the tax rate.', 'tax-rate-versus-cost-ratio'),
  none_wrong('b')],
 'b', 'Contribution margin ratio = contribution margin per unit / price.', scenario=BERG, ev='ma-cvp', group=G,
 calc=f'180 / 450 = {pct(100*cmr,0)}.', check={'f': '100*(p - v)/p', 'v': {'p': p, 'v': v}, 'x': 100 * cmr, 'unit': 'percent'})
add('ai-ma-06', T, 'CVP analysis', 'Medium', '(2 marks) Calculate the break-even revenue.',
 [(c(F / (1 - cmr)), 'Divides fixed costs by the variable-cost ratio instead of the contribution margin ratio.', 'cvp-cost-ratio'),
  (c(F / cmr * (1 - tax)), 'Applies the tax rate. At break-even there is no profit, so tax plays no role.', 'tax-affects-break-even'),
  (c(ber), f'1’260’000 / 40% = {c(ber)}.', None),
  (c(F / (p - v)), 'This is break-even in packages, not in CHF.', 'cvp-ratio-scale'),
  none_wrong('c')],
 'c', 'Break-even revenue = fixed costs / contribution margin ratio.', scenario=BERG, ev='ma-cvp', group=G,
 calc=f'1’260’000 / 0.40 = {c(ber)}.', check={'f': 'F*p/(p - v)', 'v': {'F': F, 'p': p, 'v': v}, 'x': ber})
add('ai-ma-07', T, 'CVP analysis', 'Hard', '(3 marks) How many service packages must Bergluft sell to earn a net income after taxes of CHF 189’000?',
 [(u((F + target) / (p - v)), 'Uses the after-tax target without grossing it up for tax.', 'tax-gross-up-omitted'),
  (u((F + target * (1 + tax)) / (p - v)), 'Grosses up by multiplying with 1.25. The pre-tax target is 189’000 / (1 − 25%).', 'tax-gross-up-direction'),
  (u(F / (p - v)), 'This is the break-even volume; it ignores the profit target.', 'target-profit-omitted'),
  (u(units), f'Pre-tax target = 189’000 / 0.75 = 252’000. (1’260’000 + 252’000) / 180 = {u(units)}.', None),
  none_wrong('d')],
 'd', 'Units = (fixed costs + target net income / (1 − tax rate)) / contribution margin per unit.', scenario=BERG, ev='ma-cvp', group=G,
 calc=f'252’000 pre-tax; (1’260’000 + 252’000) / 180 = {u(units)} packages.', check={'f': '(F + t/(1 - x))/(p - v)', 'v': {'F': F, 't': target, 'x': tax, 'p': p, 'v': v}, 'x': units, 'unit': 'units'})
add('ai-ma-08', T, 'CVP analysis', 'Medium', '(2 marks) Calculate Bergluft’s net income after taxes if it sells 9’500 service packages.',
 [(c(qty * (p - v) - F), 'This is operating income before tax.', 'tax-net-versus-operating'),
  (c((qty * (p - v) - F) * tax), 'This is the income tax, not the net income.', 'tax-amount-versus-profit'),
  (c(qty * (p - v) * (1 - tax)), 'Applies tax to the contribution margin and forgets the fixed costs.', 'fixed-cost-omitted'),
  (c(qty * p * (1 - tax) - F), 'Taxes revenue instead of operating income.', 'tax-net-versus-operating'),
  none_right(f'(9’500 × 180 − 1’260’000) × 0.75 = {c(ni)}, which is not listed.')],
 'e', 'Net income = (units × contribution margin − fixed costs) × (1 − tax rate).', scenario=BERG, ev='ma-cvp', group=G,
 calc=f'Operating income = 1’710’000 − 1’260’000 = 450’000. Net income = 450’000 × 0.75 = {c(ni)}.', check={'f': '(q*(p - v) - F)*(1 - x)', 'v': {'q': qty, 'p': p, 'v': v, 'F': F, 'x': tax}, 'x': ni})
add('ai-ma-09', T, 'CVP analysis', 'Medium', '(2 marks) The tax rate rises from 25% to 30%. How does this affect Bergluft’s break-even point?',
 [('The break-even point rises by 5%.', 'Tax only applies to profit. At break-even, profit is zero.', 'tax-affects-break-even'),
  ('The break-even point falls because contribution margin rises.', 'Tax does not change price or variable cost.', 'tax-changes-price'),
  ('The break-even point is unchanged, but more packages are needed to reach the same after-tax target.', 'Break-even has no profit and so no tax. An after-tax target needs a larger pre-tax profit.', None),
  ('The break-even point doubles.', 'There is no link between the tax rate and break-even volume.', 'tax-affects-break-even'),
  none_wrong('c')],
 'c', 'Taxes affect target-profit volumes, not the break-even point.', scenario=BERG, ev='ma-cvp', group=G)

# Scenario C: Sorvino Möbel AG
bdm, pur, edm, dl, il, total, bw, ew, bfg, efg, rev = 36_000, 214_000, 28_000, 96_000, 41_000, 412_000, 18_000, 25_000, 44_000, 31_000, 655_000
dm = bdm + pur - edm; other = total - dm - dl - il; cogm2 = total + bw - ew; cogs = cogm2 + bfg - efg; gm = rev - cogs
SOR = ('Sorvino Möbel AG reports the following for 2025 (CHF):\n\n' + table(['Item', 'CHF'], [
 ['Revenue', u(rev)], ['Beginning inventory of direct materials, 1 January', u(bdm)], ['Purchases of direct materials', u(pur)], ['Ending inventory of direct materials, 31 December', u(edm)],
 ['Direct manufacturing labor', u(dl)], ['Indirect manufacturing labor', u(il)], ['Total manufacturing costs incurred in 2025', u(total)],
 ['Beginning work-in-process, 1 January', u(bw)], ['Ending work-in-process, 31 December', u(ew)], ['Beginning finished goods, 1 January', u(bfg)], ['Ending finished goods, 31 December', u(efg)]]))
G = 'Sorvino Möbel'
add('ai-ma-10', T, 'Manufacturing cost flows', 'Easy', '(2 marks) What is the amount of direct materials used?',
 [(c(pur), 'Purchases are not usage; the inventory change must be included.', 'inventory-flow-direction'),
  (c(pur + edm - bdm), 'Reverses the inventory adjustment.', 'inventory-flow-direction'),
  (c(dm), f'36’000 + 214’000 − 28’000 = {c(dm)}.', None),
  (c(bdm + pur), 'This is materials available, before deducting ending inventory.', 'inventory-flow-direction'),
  none_wrong('c')],
 'c', 'Materials used = beginning inventory + purchases − ending inventory.', scenario=SOR, ev='ma-flow', group=G,
 calc=f'{u(bdm)} + {u(pur)} − {u(edm)} = {c(dm)}.', check={'f': 'a + b - c', 'v': {'a': bdm, 'b': pur, 'c': edm}, 'x': dm})
add('ai-ma-11', T, 'Manufacturing cost flows', 'Medium', '(3 marks) What are the other manufacturing overhead costs (besides indirect labor)?',
 [(c(total - dm - dl), 'Leaves indirect labor inside the “other” figure.', 'overhead-double-count'),
  (c(other), f'412’000 − 222’000 − 96’000 − 41’000 = {c(other)}.', None),
  (c(total - pur - dl - il), 'Uses purchases instead of materials used.', 'materials-versus-manufacturing'),
  (c(total - dm - dl - il + bw - ew), 'Adds the work-in-process change. That belongs in COGM, not in costs incurred.', 'wip-versus-costs-incurred'),
  none_wrong('b')],
 'b', 'Manufacturing costs incurred = direct materials used + direct labor + manufacturing overhead.', scenario=SOR, ev='ma-flow', group=G,
 calc=f'{u(total)} − {u(dm)} − {u(dl)} − {u(il)} = {c(other)}.', check={'f': 't - (a + b - e) - d - i', 'v': {'t': total, 'a': bdm, 'b': pur, 'e': edm, 'd': dl, 'i': il}, 'x': other})
add('ai-ma-12', T, 'Manufacturing cost flows', 'Medium', '(2 marks) What is the cost of goods manufactured?',
 [(c(total), 'This is costs incurred; the work-in-process change is missing.', 'beginning-wip-omitted'),
  (c(total - bw + ew), 'Reverses the work-in-process adjustment.', 'inventory-flow-direction'),
  (c(cogm2 + bfg - efg), 'This is cost of goods sold, one step further.', 'finished-goods-adjustment-omitted'),
  (c(cogm2), f'412’000 + 18’000 − 25’000 = {c(cogm2)}.', None),
  none_wrong('d')],
 'd', 'COGM = manufacturing costs incurred + beginning WIP − ending WIP.', scenario=SOR, ev='ma-flow', group=G,
 calc=f'{u(total)} + {u(bw)} − {u(ew)} = {c(cogm2)}.', check={'f': 't + a - b', 'v': {'t': total, 'a': bw, 'b': ew}, 'x': cogm2})
add('ai-ma-13', T, 'Manufacturing cost flows', 'Hard', '(4 marks) What is the cost of goods sold?',
 [(c(cogs), f'COGM {u(cogm2)} + 44’000 − 31’000 = {c(cogs)}.', None),
  (c(cogm2), 'This is COGM; the finished-goods change is missing.', 'finished-goods-adjustment-omitted'),
  (c(cogm2 - bfg + efg), 'Reverses the finished-goods adjustment.', 'inventory-flow-direction'),
  (c(total + bfg - efg), 'Skips the work-in-process adjustment.', 'beginning-wip-omitted'),
  none_wrong('a')],
 'a', 'COGS = COGM + beginning finished goods − ending finished goods.', scenario=SOR, ev='ma-flow', group=G,
 calc=f'COGM = {u(total)} + {u(bw)} − {u(ew)} = {u(cogm2)}. COGS = {u(cogm2)} + {u(bfg)} − {u(efg)} = {c(cogs)}.', check={'f': 't + a - b + c - d', 'v': {'t': total, 'a': bw, 'b': ew, 'c': bfg, 'd': efg}, 'x': cogs})
add('ai-ma-14', T, 'Manufacturing cost flows', 'Medium', '(2 marks) What is Sorvino’s gross margin for 2025?',
 [(c(rev - cogm2), 'Deducts COGM instead of COGS.', 'cogs-versus-profit'),
  (c(rev - total), 'Deducts costs incurred instead of COGS.', 'cogs-versus-profit'),
  (c(rev - cogs - il), 'Deducts indirect labor a second time; it is already in COGS.', 'overhead-double-count'),
  (c(rev - dm - dl), 'Deducts only prime costs and leaves out overhead and inventory changes.', 'manufacturing-overhead-omitted'),
  none_right(f'655’000 − {u(cogs)} = {c(gm)}, which is not listed.')],
 'e', 'Gross margin = revenue − cost of goods sold.', scenario=SOR, ev='ma-flow', group=G,
 calc=f'655’000 − {u(cogs)} = {c(gm)}.', check={'f': 'r - (t + a - b + c - d)', 'v': {'r': rev, 't': total, 'a': bw, 'b': ew, 'c': bfg, 'd': efg}, 'x': gm})

# Scenario D: Clinica Ostblick (job costing)
brev, bdl, bind, margin = 18_400_000, 5_750_000, 9_890_000, D('0.14')
ratej = D(bind) / bdl
rates, hours = [380, 240, 85], [6, 6, 14]
labor = sum(a * b for a, b in zip(rates, hours)); ind = labor * ratej; pricej = labor * (1 + ratej) / (1 - margin)
CLI = ('Clinica Ostblick is a private clinic for orthopaedic surgery. Its 2026 budget (CHF):\n\n' + table(['Budget item', 'CHF'], [['Revenues', u(brev)], ['Direct labor costs', u(bdl)], ['Indirect patient costs', u(bind)], ['Operating income', u(brev - bdl - bind)]]) +
       '\n\nIndirect patient costs are allocated using direct labor costs as the allocation base. Patient Huber’s knee operation requires:\n\n' +
       table(['Staff', 'Hours', 'CHF per hour'], [['Surgeon', '6', '380'], ['Anaesthetist', '6', '240'], ['Surgical nurse', '14', '85']]))
G = 'Clinica Ostblick'
add('ai-ma-15', T, 'Job costing', 'Easy', '(2 marks) Calculate the budgeted indirect-cost rate.',
 [(pct(100 * D(bdl) / bind, 0), 'Inverts the ratio: direct labor / indirect costs.', 'overhead-allocation-base'),
  (pct(100 * D(bind) / brev, 0), 'Uses revenue as the base. The allocation base is direct labor cost.', 'overhead-allocation-base'),
  (pct(100 * ratej, 0), f'9’890’000 / 5’750’000 = {pct(100*ratej,0)}.', None),
  (pct(100 * D(bind + bdl) / bdl, 0), 'Adds direct labor to the numerator.', 'overhead-rate-application'),
  none_wrong('c')],
 'c', 'Indirect-cost rate = budgeted indirect costs / budgeted allocation base.', scenario=CLI, ev='ma-job', group=G,
 calc=f'{u(bind)} / {u(bdl)} = {pct(100*ratej,0)}.', check={'f': '100*i/d', 'v': {'i': bind, 'd': bdl}, 'x': 100 * ratej, 'unit': 'percent'})
add('ai-ma-16', T, 'Job costing', 'Medium', '(3 marks) Calculate the indirect patient costs allocated to Patient Huber’s operation. Round the final result to a whole franc.',
 [(c(labor), 'This is the direct labor cost, not the allocated indirect cost.', 'direct-versus-indirect-cost'),
  (c(ind), f'Direct labor CHF {u(labor)} × 172% = {c(ind)}.', None),
  (c(labor * (1 + ratej)), 'This is direct plus indirect cost, not indirect cost alone.', 'overhead-rate-application'),
  (c(sum(hours) * 380 * ratej), 'Uses the surgeon’s rate for all hours.', 'overhead-allocation-base'),
  none_wrong('b')],
 'b', 'Allocated indirect cost = allocation base used by the job × indirect-cost rate.', scenario=CLI, ev='ma-job', group=G,
 calc=f'Labor = 6×380 + 6×240 + 14×85 = {u(labor)}. Indirect = {u(labor)} × 1.72 = {u(ind,2)} → {c(ind)}.',
 check={'f': '(a*x + b*y + c*z)*i/d', 'v': {'a': 380, 'x': 6, 'b': 240, 'y': 6, 'c': 85, 'z': 14, 'i': bind, 'd': bdl}, 'x': ind})
add('ai-ma-17', T, 'Pricing and target costing', 'Hard', '(3 marks) What price should the clinic charge Patient Huber so that it earns an operating income of 14% on revenue? Round the final result to a whole franc.',
 [(c(labor * (1 + ratej) * (1 + margin)), 'Adds 14% to cost. The target is 14% of revenue, so divide by 0.86.', 'margin-versus-markup'),
  (c(labor * (1 + ratej)), 'This is total cost, with no profit.', 'markup-omitted'),
  (c(labor / (1 - margin)), 'Leaves out the indirect costs.', 'manufacturing-overhead-omitted'),
  (c(pricej), f'Total cost {u(labor*(1+ratej),2)} / (1 − 14%) = {c(pricej)}.', None),
  none_wrong('d')],
 'd', 'Price for a margin m on revenue = total cost / (1 − m).', scenario=CLI, ev='ma-price', group=G,
 calc=f'Total cost = {u(labor)} + {u(ind,2)} = {u(labor*(1+ratej),2)}. Price = {u(labor*(1+ratej),2)} / 0.86 = {u(pricej,2)} → {c(pricej)}.',
 check={'f': '(a*x + b*y + c*z)*(1 + i/d)/(1 - m)', 'v': {'a': 380, 'x': 6, 'b': 240, 'y': 6, 'c': 85, 'z': 14, 'i': bind, 'd': bdl, 'm': margin}, 'x': pricej})

tp, tm = 140, D('0.18')
add('ai-ma-18', T, 'Pricing and target costing', 'Medium', '(3 marks) Fennex AG sells a kitchen blender for CHF 160. A competitor launches a similar model at CHF 139, so Fennex will cut its price to CHF 140. Fennex wants an operating income of 18% of revenue. What is the target cost per blender?',
 [(c(160 * (1 - tm), 2), 'Uses the old price of CHF 160 instead of the new target price.', 'target-margin-base'),
  (c(tp / (1 + tm), 2), 'Treats 18% as a markup on cost. The margin is on revenue.', 'margin-versus-markup'),
  (c(tp * (1 - tm), 2), f'140 × (1 − 18%) = {c(tp*(1-tm),2)}.', None),
  (c(139 * (1 - tm), 2), 'Uses the competitor’s price instead of Fennex’s target price.', 'target-margin-base'),
  none_wrong('c')],
 'c', 'Target cost = target price − target operating income per unit.', ev='ma-price',
 calc=f'140 − 18% × 140 = {c(tp*(1-tm),2)}.', check={'f': 'p*(1 - m)', 'v': {'p': tp, 'm': tm}, 'x': tp * (1 - tm), 'dp': 2})
inv, roi, units_k, pk = 3_600_000, D('0.13'), 9_000, 380
toi = inv * roi; mk = 100 * toi / (units_k * pk - toi)
add('ai-ma-19', T, 'Pricing and target costing', 'Hard', '(3 marks) Kordia AG has invested CHF 3’600’000 in a plant for industrial dehumidifiers and wants a 13% return on this investment as operating income. It plans to sell 9’000 units at CHF 380 each. What markup percentage on full cost does this price imply? Round to one decimal.',
 [(pct(100 * toi / (units_k * pk)), 'Divides the target income by revenue. A markup is based on cost.', 'markup-denominator'),
  (pct(mk), f'Target income 468’000; full cost = 3’420’000 − 468’000 = 2’952’000; 468’000 / 2’952’000 = {pct(mk)}.', None),
  (pct(13, 1), 'This is the return on investment, not the markup on cost.', 'investment-versus-cost'),
  (pct(100 * roi * units_k * pk / (units_k * pk - roi * units_k * pk)), 'Applies the 13% to revenue instead of to the CHF 3’600’000 investment.', 'investment-versus-cost'),
  none_wrong('b')],
 'b', 'Markup on full cost = target operating income / full cost, where full cost = revenue − target operating income.', ev='ma-price',
 calc=f'Target income = 13% × 3’600’000 = 468’000. Revenue = 9’000 × 380 = 3’420’000. Full cost = 2’952’000. Markup = {pct(mk)}.',
 check={'f': '100*i*r/(q*p - i*r)', 'v': {'i': inv, 'r': roi, 'q': units_k, 'p': pk}, 'x': mk, 'dp': 1, 'unit': 'percent'})
add('ai-ma-20', T, 'Cost concepts', 'Easy', '(1 mark) Which of the following statements is incorrect?',
 [('Variable costs in total change in proportion to activity.', 'Correct statement: total variable cost moves with volume.', 'negative-question-stem'),
  ('Fixed costs per unit fall as production volume rises.', 'Correct statement: the same fixed total is spread over more units.', 'negative-question-stem'),
  ('Direct costs can be traced to a cost object in an economically feasible way.', 'Correct statement: that is the definition of a direct cost.', 'negative-question-stem'),
  ('Period costs are included in inventory until the goods are sold.', 'Incorrect, and therefore the answer: period costs are expensed when incurred; product costs go into inventory.', None),
  none_wrong('d')],
 'd', 'Product costs are inventoried; period costs are expensed in the period.', ev='ma-costs')
