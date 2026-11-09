"""20 AI-generated Variances questions."""
from ai_common import add, D, chf, n, table, none_wrong, none_right
T = 'Variances'
MIS = 'variances-calculation'
fu = lambda x: f'{chf(abs(x))} {"F" if x > 0 else "U"}'   # signed effect on operating income: + favorable

# Scenario A: Rheintal Bikes AG
bp, bv, bf, bq = 1_180, 640, 2_700_000, 7_500
aq, ap, avc, af = 8_200, 1_150, 5_371_000, 2_760_000
static = bq * (bp - bv) - bf; flex = aq * (bp - bv) - bf; actual = aq * ap - avc - af
RH = ('Rheintal Bikes AG prepared the following static budget and reports these actual results for 2025:\n\n'
      + table(['', 'Static budget', 'Actual'], [['Units sold', n(bq), n(aq)], ['Selling price per unit (CHF)', n(bp), n(ap)], ['Variable costs (CHF)', f'{bv} per unit', n(avc)], ['Fixed costs (CHF)', n(bf), n(af)]]))
G = 'Rheintal Bikes flexible budget'
add('ai-var-01', T, 'Flexible budgets', 'Medium', '(2 marks) What is the flexible-budget operating income?',
 [(chf(static), 'This is the static-budget operating income for 7,500 units.', MIS), (chf(actual), 'This is actual operating income.', MIS),
  (chf(flex), f'8,200 × (1,180 − 640) − 2,700,000 = {chf(flex)}.', None), (chf(aq * (ap - bv) - bf), 'Uses the actual price. The flexible budget uses budgeted prices and costs at actual volume.', MIS), none_wrong('c')],
 'c', 'Flexible budget = budgeted prices and costs × actual output, with budgeted fixed costs.', scenario=RH, ev='variance', group=G,
 calc=f'8,200 × 540 = 4,428,000 − 2,700,000 = {chf(flex)}.', check={'f': 'q*(p - v) - f', 'v': {'q': aq, 'p': bp, 'v': bv, 'f': bf}, 'x': flex})
add('ai-var-02', T, 'Sales-volume variance', 'Medium', '(2 marks) What is the sales-volume variance in operating income?',
 [(fu(flex - static), f'Flexible {n(flex)} − static {n(static)} = {fu(flex-static)}.', None), (fu(static - flex), 'Correct amount, wrong direction. Selling more units than planned is favorable.', MIS),
  (fu((aq - bq) * bp), 'Uses the selling price instead of the contribution margin per unit.', MIS), (fu(actual - flex), 'This is the flexible-budget variance.', MIS), none_wrong('a')],
 'a', 'Sales-volume variance = flexible-budget amount − static-budget amount.', scenario=RH, ev='variance', group=G,
 calc=f'(8,200 − 7,500) × 540 = {fu(flex-static)}.', check={'f': '(a - b)*(p - v)', 'v': {'a': aq, 'b': bq, 'p': bp, 'v': bv}, 'x': flex - static, 'same': 'b'})
add('ai-var-03', T, 'Flexible-budget variance', 'Medium', '(2 marks) What is the flexible-budget variance in operating income?',
 [(fu(actual - static), 'This is the static-budget variance.', MIS), (fu(flex - actual), 'Correct amount, wrong direction. Actual income is below the flexible budget.', MIS),
  (fu(actual - flex), f'Actual {n(actual)} − flexible {n(flex)} = {fu(actual-flex)}.', None), (fu((ap - bp) * aq), 'This is only the selling-price variance.', MIS), none_wrong('c')],
 'c', 'Flexible-budget variance = actual result − flexible-budget amount.', scenario=RH, ev='variance', group=G,
 calc=f'Actual = 9,430,000 − 5,371,000 − 2,760,000 = {n(actual)}. {n(actual)} − {n(flex)} = {fu(actual-flex)}.',
 check={'f': 'q*a - c - g - (q*(p - v) - f)', 'v': {'q': aq, 'a': ap, 'c': avc, 'g': af, 'p': bp, 'v': bv, 'f': bf}, 'x': actual - flex, 'same': 'b'})
add('ai-var-04', T, 'Static-budget variance', 'Easy', '(2 marks) What is the static-budget variance in operating income?',
 [(fu(flex - static), 'This is the sales-volume variance.', MIS), (fu(static - actual), 'Correct amount, wrong direction. Actual income is below the static budget.', MIS),
  (fu(actual - flex), 'This is the flexible-budget variance.', MIS), (fu(actual - static), f'{n(actual)} − {n(static)} = {fu(actual-static)}.', None), none_wrong('d')],
 'd', 'Static-budget variance = actual result − static-budget amount = sales-volume variance + flexible-budget variance.', scenario=RH, ev='variance', group=G,
 calc=f'{n(actual)} − {n(static)} = {fu(actual-static)}.', check={'f': 'q*a - c - g - (b*(p - v) - f)', 'v': {'q': aq, 'a': ap, 'c': avc, 'g': af, 'b': bq, 'p': bp, 'v': bv, 'f': bf}, 'x': actual - static, 'same': 'b'})
spv = (ap - bp) * aq
add('ai-var-05', T, 'Flexible-budget variance', 'Medium', '(2 marks) What is the selling-price variance?',
 [(fu(spv), f'(1,150 − 1,180) × 8,200 = {fu(spv)}.', None), (fu((ap - bp) * bq), 'Uses budgeted units. The price variance uses actual units sold.', MIS),
  (fu(-spv), 'Correct amount, wrong direction. A lower price than planned is unfavorable.', MIS), (fu(aq * ap - bq * bp), 'This is the total revenue variance, not the price part.', MIS), none_wrong('a')],
 'a', 'Selling-price variance = (actual price − budgeted price) × actual units sold.', scenario=RH, ev='variance', group=G,
 calc=f'−30 × 8,200 = {fu(spv)}.', check={'f': '(b - a)*q', 'v': {'a': ap, 'b': bp, 'q': aq}, 'x': -spv, 'same': 'c'})

# Scenario B/C: Sanoro Pasta AG materials and labor
units, sq, sp, aqm, apm = 50_000, D('0.6'), D('1.10'), 31_200, D('1.04')
sh, sr, ah, ar = D('0.05'), 36, 2_640, D('37.50')
dpv = (apm - sp) * aqm; dev = (aqm - units * sq) * sp; dfv = aqm * apm - units * sq * sp
lpv = (ar - sr) * ah; lev = (ah - units * sh) * sr
SAN = ('Sanoro Pasta AG produced 50,000 packs of tagliatelle in March. Standards and actual data:\n\n'
       + table(['', 'Standard per pack', 'Actual for March'], [['Flour', '0.6 kg at CHF 1.10/kg', '31,200 kg at CHF 1.04/kg'], ['Direct labor', '0.05 hours at CHF 36/hour', '2,640 hours at CHF 37.50/hour']])
       + '\n\nAll flour purchased in March was used in March.')
G = 'Sanoro Pasta variances'
# positive inputs = unfavorable cost variances
fc = lambda x: f'{chf(abs(x))} {"U" if x > 0 else "F"}'
add('ai-var-06', T, 'Direct material price variance', 'Easy', '(2 marks) What is the direct material price variance?',
 [(fc(dpv), f'(1.04 − 1.10) × 31,200 = {fc(dpv)}.', None), (fc((apm - sp) * units * sq), 'Uses the standard quantity allowed. The price variance uses the actual quantity.', MIS),
  (fc(-dpv), 'Correct amount, wrong direction. Paying less than standard is favorable.', MIS), (fc(dfv), 'This is the total flexible-budget variance for materials.', MIS), none_wrong('a')],
 'a', 'Price variance = (actual price − budgeted price) × actual input quantity.', scenario=SAN, ev='variance', group=G,
 calc=f'−0.06 × 31,200 = {fc(dpv)}.', check={'f': '(s - a)*q', 'v': {'a': apm, 's': sp, 'q': aqm}, 'x': -dpv, 'same': 'c'})
add('ai-var-07', T, 'Direct material variances', 'Medium', '(2 marks) What is the direct material efficiency variance?',
 [(fc((aqm - units * sq) * apm), 'Uses the actual price. Efficiency variances use the budgeted price.', MIS), (fc(-dev), 'Correct amount, wrong direction. Using more flour than allowed is unfavorable.', MIS),
  (fc(dev), f'(31,200 − 30,000) × 1.10 = {fc(dev)}.', None), (fc(aqm * sp - units * sp), 'Compares kilograms with packs; the standard quantity is 0.6 kg per pack.', MIS), none_wrong('c')],
 'c', 'Efficiency variance = (actual input − budgeted input allowed for actual output) × budgeted price.', scenario=SAN, ev='variance', group=G,
 calc=f'Allowed = 50,000 × 0.6 = 30,000 kg. (31,200 − 30,000) × 1.10 = {fc(dev)}.', check={'f': '(a - u*q)*p', 'v': {'a': aqm, 'u': units, 'q': sq, 'p': sp}, 'x': dev, 'same': 'b'})
add('ai-var-08', T, 'Direct material variances', 'Medium', '(2 marks) What is the flexible-budget variance for direct materials?',
 [(fc(dpv - dev), 'Subtracts the efficiency variance instead of adding it.', MIS), (fc(aqm * apm - units * sq * apm), 'Values the flexible budget at the actual price.', MIS),
  (fc(-dfv), 'Correct amount, wrong direction. Actual cost is below the flexible budget.', MIS), (fc(dfv), f'Actual 32,448 − flexible 33,000 = {fc(dfv)}.', None), none_wrong('d')],
 'd', 'Flexible-budget variance = price variance + efficiency variance = actual cost − flexible-budget cost.', scenario=SAN, ev='variance', group=G,
 calc=f'Actual = 31,200 × 1.04 = 32,448. Flexible = 30,000 × 1.10 = 33,000. Variance = {fc(dfv)} (= 1,872 F + 1,320 U).', check={'f': 'u*q*p - a*c', 'v': {'a': aqm, 'c': apm, 'u': units, 'q': sq, 'p': sp}, 'x': -dfv, 'same': 'c'})
add('ai-var-09', T, 'Direct material standards', 'Easy', '(1 mark) What is the budgeted (standard) flour cost per pack?',
 [(chf(sq * sp, 2), f'0.6 kg × CHF 1.10 = {chf(sq*sp,2)}.', None), (chf(sq * apm, 2), 'Uses the actual price.', MIS), (chf(D(aqm) / units * apm, 3), 'This is the actual cost per pack.', MIS),
  (chf(sp, 2), 'This is the price per kilogram, not per pack.', MIS), none_wrong('a')],
 'a', 'Standard cost per unit = standard quantity per unit × standard price.', scenario=SAN, ev='variance', group=G,
 calc=f'0.6 × 1.10 = {chf(sq*sp,2)}.', check={'f': 'q*p', 'v': {'q': sq, 'p': sp}, 'x': sq * sp, 'dp': 2})
add('ai-var-10', T, 'Direct labor price variance', 'Easy', '(2 marks) What is the direct labor price variance?',
 [(fc((ar - sr) * units * sh), 'Uses the standard hours allowed instead of actual hours.', MIS), (fc(lpv), f'(37.50 − 36) × 2,640 = {fc(lpv)}.', None),
  (fc(-lpv), 'Correct amount, wrong direction. Paying more per hour is unfavorable.', MIS), (fc(lpv + lev), 'This is the total labor flexible-budget variance.', MIS), none_wrong('b')],
 'b', 'Labor price variance = (actual rate − budgeted rate) × actual hours.', scenario=SAN, ev='variance', group=G,
 calc=f'1.50 × 2,640 = {fc(lpv)}.', check={'f': '(a - s)*h', 'v': {'a': ar, 's': sr, 'h': ah}, 'x': lpv, 'same': 'c'})
add('ai-var-11', T, 'Direct labor price variance', 'Medium', '(2 marks) What is the direct labor efficiency variance?',
 [(fc((ah - units * sh) * ar), 'Values the extra hours at the actual rate instead of the budgeted rate.', MIS), (chf(ah * sr), 'This is actual hours at the budgeted rate, one input to the variance, not the variance itself.', MIS),
  (fc(lpv), 'This is the labor price variance.', MIS), (fc(lev + lpv), 'Adds the price variance.', MIS), none_right(f'(2,640 − 2,500) × 36 = {fc(lev)}, which is not listed.')],
 'e', 'Labor efficiency variance = (actual hours − hours allowed for actual output) × budgeted rate.', scenario=SAN, ev='variance', group=G,
 calc=f'Allowed = 50,000 × 0.05 = 2,500 h. (2,640 − 2,500) × 36 = {fc(lev)}.', check={'f': '(h - u*q)*s', 'v': {'h': ah, 'u': units, 'q': sh, 's': sr}, 'x': lev})

# Scenario D: Lumatec AG overhead
bu, bmh, bvoh, au, amh, avoh, bfoh, afoh = 6_000, 18_000, 252_000, 6_600, 20_500, 279_000, 540_000, 556_000
vr = D(bvoh) / bmh; mhu = D(bmh) / bu; allowed = au * mhu; fr = D(bfoh) / bmh
flexv = allowed * vr; spend = avoh - amh * vr; eff = (amh - allowed) * vr; fbv = avoh - flexv; fspend = afoh - bfoh; pvv = bfoh - allowed * fr
LUM = ('Lumatec AG allocates manufacturing overhead on machine-hours. Data for 2025:\n\n'
       + table(['', 'Budget', 'Actual'], [['Output (units)', n(bu), n(au)], ['Machine-hours', n(bmh), n(amh)], ['Variable manufacturing overhead (CHF)', n(bvoh), n(avoh)], ['Fixed manufacturing overhead (CHF)', n(bfoh), n(afoh)]]))
G = 'Lumatec overhead variances'
add('ai-var-12', T, 'Variable-overhead budgets', 'Medium', '(2 marks) What is the flexible-budget amount for variable manufacturing overhead?',
 [(chf(amh * vr), 'Uses actual machine-hours. The flexible budget uses hours allowed for actual output.', MIS), (chf(bvoh), 'This is the static budget.', MIS),
  (chf(flexv), f'6,600 units × 3 MH × CHF 14 = {chf(flexv)}.', None), (chf(avoh), 'This is the actual variable overhead.', MIS), none_wrong('c')],
 'c', 'Flexible budget = budgeted rate × budgeted input allowed for actual output.', scenario=LUM, ev='variance', group=G,
 calc=f'Rate = 252,000 / 18,000 = 14 per MH; 3 MH per unit; 6,600 × 3 × 14 = {chf(flexv)}.', check={'f': 'a*m/b*v/m', 'v': {'a': au, 'm': bmh, 'b': bu, 'v': bvoh}, 'x': flexv})
add('ai-var-13', T, 'Variable-overhead variances', 'Hard', '(2 marks) What is the variable-overhead spending variance?',
 [(fc(spend), f'279,000 − 20,500 × 14 = 279,000 − 287,000 = {fc(spend)}.', None), (fc(fbv), 'This is the flexible-budget variance.', MIS),
  (fc(-spend), 'Correct amount, wrong direction. Actual overhead is below the budget for actual hours.', MIS), (fc(eff), 'This is the efficiency variance.', MIS), none_wrong('a')],
 'a', 'Spending variance = actual variable overhead − (actual hours × budgeted rate).', scenario=LUM, ev='variance', group=G,
 calc=f'{fc(spend)}.', check={'f': 'a - h*v/m', 'v': {'a': avoh, 'h': amh, 'v': bvoh, 'm': bmh}, 'x': spend, 'same': 'c'})
add('ai-var-14', T, 'Variable-overhead variances', 'Hard', '(2 marks) What is the variable-overhead efficiency variance?',
 [(fc((amh - bmh) * vr), 'Compares with budgeted hours for budgeted output instead of hours allowed for actual output.', MIS), (fc(-eff), 'Correct amount, wrong direction. More hours than allowed is unfavorable.', MIS),
  (fc(spend), 'This is the spending variance.', MIS), (fc(eff), f'(20,500 − 19,800) × 14 = {fc(eff)}.', None), none_wrong('d')],
 'd', 'Efficiency variance = (actual hours − hours allowed) × budgeted rate.', scenario=LUM, ev='variance', group=G,
 calc=f'Allowed = 6,600 × 3 = 19,800 MH. (20,500 − 19,800) × 14 = {fc(eff)}.', check={'f': '(h - a*m/b)*v/m', 'v': {'h': amh, 'a': au, 'm': bmh, 'b': bu, 'v': bvoh}, 'x': eff, 'same': 'b'})
add('ai-var-15', T, 'Variable-overhead variances', 'Medium', '(2 marks) Which expression calculates the variable-overhead flexible-budget variance, and what is its amount for Lumatec?',
 [(f'Actual variable overhead − static budget; {fc(avoh - bvoh)}', 'Uses the static budget instead of the flexible budget.', MIS),
  (f'Actual variable overhead − flexible-budget amount; {fc(fbv)}', f'279,000 − 277,200 = {fc(fbv)} (= 8,000 F spending + 9,800 U efficiency).', None),
  (f'Flexible budget − static budget; {fc(flexv - bvoh)}', 'This is a sales-volume type comparison, not the flexible-budget variance.', MIS),
  (f'Actual variable overhead − actual hours × budgeted rate; {fc(spend)}', 'This is the spending variance.', MIS), none_wrong('b')],
 'b', 'Flexible-budget variance = actual − flexible budget = spending + efficiency variance.', scenario=LUM, ev='variance', group=G,
 calc=f'{n(avoh)} − {n(flexv)} = {fc(fbv)}.', check={'f': 'c - a*v/b', 'v': {'c': avoh, 'a': au, 'v': bvoh, 'b': bu}, 'x': fbv})
add('ai-var-16', T, 'Fixed-overhead variances', 'Easy', '(2 marks) What is the fixed-overhead spending (flexible-budget) variance?',
 [(fc(fspend), f'556,000 − 540,000 = {fc(fspend)}.', None), (fc(-fspend), 'Correct amount, wrong direction. Spending more than budgeted is unfavorable.', MIS),
  (fc(afoh - allowed * fr), 'Compares actual with allocated fixed overhead; that mixes in the volume variance.', MIS), (fc(pvv), 'This is the production-volume variance.', MIS), none_wrong('a')],
 'a', 'Fixed overhead spending variance = actual fixed overhead − budgeted fixed overhead.', scenario=LUM, ev='variance', group=G,
 calc=f'{n(afoh)} − {n(bfoh)} = {fc(fspend)}.', check={'f': 'a - b', 'v': {'a': afoh, 'b': bfoh}, 'x': fspend, 'same': 'b'})
add('ai-var-17', T, 'Fixed-overhead variances', 'Hard', '(3 marks) What is the fixed-overhead production-volume variance?',
 [(fc(-pvv), 'Correct amount, wrong direction. Output above budget allocates more fixed overhead than budgeted, which is favorable.', MIS),
  (fc(bfoh - amh * fr), 'Uses actual machine-hours instead of hours allowed for actual output.', MIS),
  (fc(pvv), f'Budget 540,000 − allocated 19,800 × 30 = 594,000 → {fc(pvv)}.', None), (fc(fspend), 'This is the spending variance.', MIS), none_wrong('c')],
 'c', 'Production-volume variance = budgeted fixed overhead − fixed overhead allocated to actual output.', scenario=LUM, ev='variance', group=G,
 calc=f'Rate = 540,000 / 18,000 = 30 per MH. Allocated = 19,800 × 30 = 594,000. 540,000 − 594,000 = {fc(pvv)}.', check={'f': 'a*h*b/(c*h) - b', 'v': {'a': au, 'h': bmh, 'b': bfoh, 'c': bu}, 'x': -pvv, 'same': 'a'})
add('ai-var-18', T, 'Direct material variances', 'Easy', '(1 mark) Which expression calculates the direct material efficiency variance?',
 [('(Actual price − budgeted price) × actual quantity', 'That is the price variance.', MIS),
  ('(Actual quantity − budgeted quantity allowed for actual output) × budgeted price', 'Quantity difference valued at the budgeted price.', None),
  ('(Actual quantity − budgeted quantity for budgeted output) × actual price', 'Uses the static-budget quantity and the actual price.', MIS),
  ('Actual cost − static-budget cost', 'That is a static-budget variance.', MIS), none_wrong('b')],
 'b', 'Efficiency variances isolate quantity effects at budgeted prices.', ev='variance')
add('ai-var-19', T, 'Sales-volume variance', 'Easy', '(1 mark) A company reports a favorable sales-volume variance in operating income. What does this mean?',
 [('Actual selling prices were above budget.', 'That is a favorable selling-price variance.', MIS), ('Actual costs were below the flexible budget.', 'That is a favorable flexible-budget cost variance.', MIS),
  ('More units were sold than planned in the static budget.', 'Selling more units adds contribution margin compared with the static budget.', None),
  ('Actual operating income exceeded the flexible budget.', 'That is a favorable flexible-budget variance.', MIS), none_wrong('c')],
 'c', 'The sales-volume variance compares the flexible budget with the static budget; only volume differs.', ev='variance')
srev, su, au2 = 1_920_000, 16_000, 17_500
add('ai-var-20', T, 'Flexible budgets', 'Easy', '(2 marks) Vexa Tools AG’s static budget shows revenue of CHF 1,920,000 for 16,000 units. Actual volume is 17,500 units. What revenue appears in the flexible budget?',
 [(chf(srev), 'This is the static budget.', MIS), (chf(D(srev) / su * au2), f'CHF 120 × 17,500 = {chf(D(srev)/su*au2)}.', None),
  (chf(D(srev) * su / au2), 'Scales in the wrong direction.', MIS), (chf(srev + au2 - su), 'Adds the unit difference to revenue.', MIS), none_wrong('b')],
 'b', 'Flexible-budget revenue = budgeted price × actual volume.', ev='variance',
 calc=f'1,920,000 / 16,000 = 120 per unit. 120 × 17,500 = {chf(D(srev)/su*au2)}.', check={'f': 'r/s*a', 'v': {'r': srev, 's': su, 'a': au2}, 'x': D(srev) / su * au2})
