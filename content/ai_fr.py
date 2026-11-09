"""20 AI-generated Financial Reporting questions."""
from ai_common import add, D, r, chf, n, pct, table
T = 'Financial Reporting'

def lease(p, rate, term):
 """Course method: PV of arrears payments, interest and balances rounded to cents."""
 p, rate = D(p), D(rate)
 pv = r(sum(p / (1 + rate) ** t for t in range(1, term + 1)), 2)
 rows, bal = [], pv
 for _ in range(term):
  interest = r(bal * rate, 2); principal = r(p - interest, 2); close = r(bal - principal, 2)
  rows.append((bal, interest, principal, close)); bal = close
 return pv, rows

# Lease scenario: Halvora AG
P, RATE, TERM = 6200, 0.07, 4
pv, rows = lease(P, RATE, TERM)
LEASE = ('On 1 January 2025, Halvora AG leases a packaging line from Krenn Leasing AG. The lease runs four years, '
         'which equals the line’s useful life. Halvora pays CHF 6,200 at the end of each year (31 December). '
         'The interest rate implicit in the lease is 7%. Halvora reports under IFRS and depreciates right-of-use assets straight-line.')
LA = ['IFRS 16 lessee; no residual value, purchase option, initial direct costs or incentives. Round interest and balances to cents; round the requested final amount up to the next franc.']
add('ai-fr-01', T, 'Leases', 'Medium', '(2 marks) At what amount does Halvora initially recognize the lease liability on 1 January 2025?',
 [(chf(pv, mode='up'), f'Discounting four payments of CHF 6,200 at 7% gives CHF {n(pv,2)}, which rounds up to {chf(pv,mode="up")}.', None),
  (chf(P*TERM), 'Adds the four payments without discounting. The liability is a present value, so the time value of money is missing.', 'lease-calculation'),
  (chf(P*TERM/1.07, mode='up'), 'Discounts the total of all payments by one year only. Each payment has to be discounted for its own year.', 'lease-calculation'),
  (chf(pv*D(1.07), mode='up'), 'Treats the payments as due in advance (annuity due). Halvora pays at year-end, so each payment is discounted one more year.', 'lease-calculation')],
 'a', 'The lease liability equals the present value of the outstanding lease payments, discounted at the implicit rate.', scenario=LEASE, assume=LA, ev='lease', marks=2,
 calc=f'PV = 6,200 × (1 − 1.07⁻⁴) / 0.07 = CHF {n(pv,2)} → {chf(pv,mode="up")}.',
 check={'f': 'p*(1-(1+i)**-4)/i', 'v': {'p': P, 'i': RATE}, 'x': pv, 'mode': 'up'}, group='Halvora AG lease')
i2 = rows[1][1]
add('ai-fr-02', T, 'Leases', 'Medium', '(2 marks) How much interest expense does Halvora recognize on the lease in 2026, the second lease year?',
 [(chf(rows[0][1], mode='up'), 'This is the 2025 interest. In 2026 interest is charged on the lower balance left after the first payment.', 'lease-wrong-year'),
  (chf(i2, mode='up'), f'Opening 2026 liability CHF {n(rows[1][0],2)} × 7% = CHF {n(i2,2)}, rounded up to {chf(i2,mode="up")}.', None),
  (chf(rows[1][2], mode='up'), 'This is the principal part of the 2026 payment, not the interest part.', 'lease-payment-split'),
  (chf(pv*D(0.07)*2, mode='up'), 'Adds two years of interest on the original liability. Interest is charged each year on the balance still outstanding.', 'lease-calculation')],
 'b', 'Interest for a year = opening lease liability × implicit rate. The rest of the payment reduces the liability.', scenario=LEASE, assume=LA, ev='lease', marks=2,
 calc=f'2025: {n(pv,2)} × 7% = {n(rows[0][1],2)}; principal {n(rows[0][2],2)}; closing {n(rows[0][3],2)}. 2026 interest = {n(rows[0][3],2)} × 7% = CHF {n(i2,2)} → {chf(i2,mode="up")}.',
 check={'f': '(p*(1-(1+i)**-4)/i*(1+i) - p)*i', 'v': {'p': P, 'i': RATE}, 'x': i2, 'mode': 'up'}, group='Halvora AG lease')
rou2 = pv * D(2) / D(4)
add('ai-fr-03', T, 'Leases', 'Medium', '(2 marks) What is the carrying amount of the right-of-use asset on 31 December 2026?',
 [(chf(rows[1][3], mode='up'), 'This is the lease liability after two payments. The asset is depreciated straight-line, so it falls faster than the liability.', 'lease-liability-as-asset'),
  (chf(pv*D(3)/D(4), mode='up'), 'Deducts only one year of depreciation. By 31 December 2026 two of four years have passed.', 'lease-wrong-year'),
  (chf(rou2, mode='up'), f'CHF {n(pv,2)} × 2/4 = CHF {n(rou2,2)}, rounded up to {chf(rou2,mode="up")}.', None),
  (chf(pv - 2*P, mode='up'), 'Subtracts the lease payments from the asset. Payments reduce the liability; the asset is reduced by depreciation.', 'lease-asset-liability-swap')],
 'c', 'The right-of-use asset starts at the initial liability and is depreciated straight-line over the four-year term.', scenario=LEASE, assume=LA, ev='lease', marks=2,
 calc=f'Annual depreciation = {n(pv,2)} / 4 = {n(pv/4,4)}. Carrying amount after two years = {n(rou2,2)} → {chf(rou2,mode="up")}.',
 check={'f': 'p*(1-(1+i)**-4)/i*2/4', 'v': {'p': P, 'i': RATE}, 'x': rou2, 'mode': 'up'}, group='Halvora AG lease')
add('ai-fr-04', T, 'Leases', 'Easy', '(1 mark) Which statement about Halvora’s lease is correct under IFRS 16?',
 [('The lease payments are recognized as rental expense; no asset or liability appears on the balance sheet.', 'That was operating-lease treatment before IFRS 16. A lessee now recognizes a right-of-use asset and a lease liability.', 'lease-off-balance-sheet'),
  ('Krenn Leasing AG, the lessor, recognizes the right-of-use asset.', 'The lessee recognizes the right-of-use asset. The lessor keeps the underlying asset or a lease receivable.', 'lease-role-confusion'),
  ('Halvora’s EBITDA is higher than it would be if the payments were rental expense.', 'Depreciation and interest replace rental expense, and both sit below EBITDA. EBITDA rises.', None),
  ('The right-of-use asset is not depreciated because Halvora does not own the line.', 'Ownership is not required. The right-of-use asset is depreciated over the lease term.', 'lease-no-depreciation')],
 'c', 'Under IFRS 16 the lessee shows depreciation and interest instead of a rental expense, which moves cost below EBITDA.', scenario=LEASE, assume=LA, ev='lease', marks=1, group='Halvora AG lease')

# Deferred tax scenario: Morvik AG
COST, LIFE, DB, RATE_T = 18_000_000, 5, 0.4, 0.21
book1, base1 = COST * 4 / 5, COST * 0.6
book2, base2 = COST * 3 / 5, COST * 0.6 * 0.6
dtl1, dtl2 = (book1 - base1) * RATE_T, (book2 - base2) * RATE_T
TAXS = ('On 1 January 2025, Morvik AG buys a CNC machine for CHF 18 million. In its IFRS accounts the machine is depreciated straight-line over five years with no residual value. '
        'For local tax purposes Morvik uses 40% declining-balance depreciation. The enacted tax rate is 21% for all years.')
add('ai-fr-05', T, 'Deferred taxes', 'Hard', '(3 marks) Which deferred tax balance does Morvik report for the machine on 31 December 2025?',
 [(f'Deferred tax liability of {chf(dtl1)}', f'Book value CHF {n(book1)} exceeds the tax base CHF {n(base1)} by CHF {n(book1-base1)}; × 21% = {chf(dtl1)}.', None),
  (f'Deferred tax asset of {chf(dtl1)}', 'The amount is right but the direction is reversed. Book value above tax base means more tax later, so it is a liability.', 'tax-direction'),
  (f'Deferred tax liability of {chf(book1-base1)}', 'This is the temporary difference before applying the 21% tax rate.', 'tax-rate-omitted'),
  (f'Deferred tax liability of {chf(book1*RATE_T)}', 'Applies the tax rate to the whole IFRS carrying amount instead of the difference to the tax base.', 'tax-gross-balance')],
 'a', 'Compare the IFRS carrying amount with the tax base. An asset with a higher book value than tax base creates a deferred tax liability.', scenario=TAXS, ev='tax', marks=3,
 calc=f'IFRS: 18,000,000 − 3,600,000 = {n(book1)}. Tax: 18,000,000 × 60% = {n(base1)}. Difference {n(book1-base1)} × 21% = {chf(dtl1)} DTL.',
 check={'f': '(c*4/5 - c*(1-d))*t', 'v': {'c': COST, 'd': DB, 't': RATE_T}, 'x': dtl1, 'same': 'b'}, group='Morvik AG deferred tax')
add('ai-fr-06', T, 'Deferred taxes', 'Hard', '(3 marks) By how much does Morvik’s deferred tax liability for the machine change during 2026?',
 [(f'Increase of {chf(dtl2)}', 'This is the closing 2026 balance, not the movement during the year.', 'tax-balance-vs-movement'),
  (f'Decrease of {chf(dtl2-dtl1)}', 'The direction is reversed. The gap between book value and tax base keeps widening in year two.', 'tax-direction'),
  (f'Increase of {chf(dtl2-dtl1)}', f'Closing DTL {chf(dtl2)} less opening DTL {chf(dtl1)} = increase of {chf(dtl2-dtl1)}.', None),
  (f'Increase of {chf((book2-base2)-(book1-base1))}', 'This is the change in the temporary difference before the 21% tax rate.', 'tax-rate-omitted')],
 'c', 'The deferred tax expense for the year is the change in the balance: closing DTL less opening DTL.', scenario=TAXS, ev='tax', marks=3,
 calc=f'31.12.2026: IFRS {n(book2)}, tax base {n(base2)}, difference {n(book2-base2)}, DTL {n(dtl2)}. Movement = {n(dtl2)} − {n(dtl1)} = +{chf(dtl2-dtl1)}.',
 check={'f': '(c*3/5 - c*(1-d)**2)*t - (c*4/5 - c*(1-d))*t', 'v': {'c': COST, 'd': DB, 't': RATE_T}, 'x': dtl2 - dtl1, 'same': 'b'}, group='Morvik AG deferred tax')
inv_cost, inv_book, allowed, rt = 240_000, 150_000, 0.25, 0.18
inv_base = inv_cost * (1 - allowed); dta = (inv_base - inv_book) * rt
add('ai-fr-07', T, 'Deferred taxes', 'Medium',
 '(3 marks) On 31 December 2025, Lunaris Textil AG writes down fabric inventory from CHF 240,000 to CHF 150,000 in its IFRS accounts. Tax rules allow only a 25% value adjustment now; the rest is deductible when the fabric is sold. The tax rate is 18%. Which statement is correct?',
 [(f'Temporary difference; deferred tax liability of {chf(dta)}', 'Book value is below the tax base, so Lunaris gets a future deduction. That is an asset, not a liability.', 'tax-direction'),
  (f'Permanent difference; no deferred tax', 'The extra write-down is deductible on sale, so the difference reverses. It is temporary.', 'tax-permanent-vs-temporary'),
  (f'Temporary difference; deferred tax asset of {chf(dta)}', f'Tax base 240,000 × 75% = {n(inv_base)}; book 150,000; difference {n(inv_base-inv_book)} × 18% = {chf(dta)} DTA.', None),
  (f'Temporary difference; deferred tax asset of {chf((inv_cost-inv_book)*rt)}', 'Taxes the whole book write-down of CHF 90,000. Part of it (25% of cost) is already deductible now.', 'tax-wrong-difference')],
 'c', 'If the tax base of an asset exceeds its carrying amount, the future deduction gives a deferred tax asset.', ev='tax', marks=3,
 calc=f'Tax base = 240,000 × (1 − 25%) = {n(inv_base)}. Deductible difference = {n(inv_base)} − 150,000 = {n(inv_base-inv_book)}. DTA = {n(inv_base-inv_book)} × 18% = {chf(dta)}.',
 check={'f': '(c*(1-a)-b)*t', 'v': {'c': inv_cost, 'b': inv_book, 'a': allowed, 't': rt}, 'x': dta, 'same': 'a'})
add('ai-fr-08', T, 'Deferred taxes', 'Easy', '(1 mark) Brontal AG pays a CHF 35,000 fine for a late regulatory filing. The fine is expensed in the IFRS accounts but is never tax-deductible. Which statement is correct?',
 [('It creates a deferred tax asset because the expense is not deducted now.', 'A deferred tax asset needs a future deduction. The fine will never be deductible.', 'tax-permanent-vs-temporary'),
  ('It is a permanent difference, so no deferred tax is recognized.', 'The difference never reverses. It affects the tax reconciliation but not deferred tax.', None),
  ('It creates a deferred tax liability of CHF 35,000.', 'There is no future taxable amount, and CHF 35,000 is the expense itself, not a tax amount.', 'tax-rate-omitted'),
  ('It is a temporary difference that reverses when the fine is paid.', 'Paying the fine does not make it deductible. The difference is permanent.', 'tax-permanent-vs-temporary')],
 'b', 'Only differences that reverse in future periods create deferred taxes.', ev='tax', marks=1)
td, old, new = 640_000, 0.2, 0.17
add('ai-fr-09', T, 'Deferred taxes', 'Medium', '(2 marks) Cavella AG has a taxable temporary difference of CHF 640,000 on a building. The current tax rate is 20%, but a rate of 17% has been enacted for the years in which the difference reverses. Which deferred tax liability does Cavella report?',
 [(chf(td*old), 'Uses today’s 20%. Deferred tax is measured at the rate expected when the difference reverses.', 'tax-wrong-rate'),
  (chf(td), 'This is the temporary difference itself, before any tax rate.', 'tax-rate-omitted'),
  (chf(td*(old-new)), 'This is only the effect of the rate change, not the balance.', 'tax-balance-vs-movement'),
  (chf(td*new), f'CHF 640,000 × 17% enacted reversal rate = {chf(td*new)}.', None)],
 'd', 'Deferred taxes use the tax rate that is enacted for the period in which the difference reverses.', ev='tax', marks=2,
 calc=f'640,000 × 17% = {chf(td*new)}.', check={'f': 'd*t', 'v': {'d': td, 't': new}, 'x': td*new})
add('ai-fr-10', T, 'Deferred taxes', 'Easy', '(1 mark) True or false: A deferred tax asset from deductible temporary differences is recognized only to the extent that future taxable profit is probable.',
 [('True', 'The asset only has value if there will be taxable profit to deduct against.', None),
  ('False', 'IFRS requires probable future taxable profit before a deferred tax asset is recognized.', 'tax-dta-recognition')],
 'a', 'A DTA is a future tax saving, so it needs probable taxable profit to be realized.', ev='tax', marks=1)

# Impairment scenario: Zentra Logistik AG
cost, life, years, viu, fv, dc = 420_000, 7, 3, 205_000, 228_000, 12_000
carry = cost - cost / life * years; ra = max(viu, fv - dc); loss = carry - ra
IMPS = ('Zentra Logistik AG bought a refrigerated truck on 1 January 2023 for CHF 420,000. It is depreciated straight-line over seven years with no residual value. '
        'At 31 December 2025, after a new emissions rule, Zentra tests the truck for impairment:\n\n'
        + table(['Item', 'CHF'], [['Value in use', '205,000'], ['Fair value', '228,000'], ['Costs of disposal', '12,000']]))
add('ai-fr-11', T, 'Impairment', 'Medium', '(3 marks) What impairment loss does Zentra recognize at 31 December 2025?',
 [(chf(carry-viu), 'Compares with value in use only. Fair value less costs of disposal (CHF 216,000) is higher and sets the recoverable amount.', 'impairment-viu-only'),
  (chf(carry-fv), 'Ignores the CHF 12,000 costs of disposal when measuring fair value less costs of disposal.', 'impairment-disposal-costs'),
  (chf(loss), f'Carrying amount {n(carry)}; recoverable amount = max(205,000; 216,000) = {n(ra)}; loss = {chf(loss)}.', None),
  ('No impairment loss', f'The carrying amount of {chf(carry)} exceeds both recoverable measures, so a loss is required.', 'impairment-no-loss')],
 'c', 'Recoverable amount is the higher of value in use and fair value less costs of disposal. The loss is carrying amount minus recoverable amount.', scenario=IMPS, ev='impairment', marks=3,
 calc=f'Carrying amount = 420,000 − 3 × 60,000 = {n(carry)}. FVLCD = 228,000 − 12,000 = 216,000. RA = {n(ra)}. Loss = {n(carry)} − {n(ra)} = {chf(loss)}.',
 check={'f': 'c - c/l*y - max(v, f - k)', 'v': {'c': cost, 'l': life, 'y': years, 'v': viu, 'f': fv, 'k': dc}, 'x': loss}, group='Zentra Logistik impairment')
dep26 = ra / (life - years)
add('ai-fr-12', T, 'Impairment', 'Hard', '(2 marks) The remaining useful life of the truck is unchanged. What depreciation does Zentra charge in 2026?',
 [(chf(cost/life), 'Keeps the old charge based on original cost. After an impairment, depreciation is based on the new carrying amount.', 'impairment-loss-vs-value'),
  (chf(dep26), f'New carrying amount {n(ra)} spread over the four remaining years = {chf(dep26)}.', None),
  (chf(ra/life), 'Spreads the new carrying amount over the full seven-year life instead of the four years left.', 'impairment-remaining-life'),
  (chf(viu/(life-years)), 'Bases the new carrying amount on value in use. The higher fair value less costs of disposal (CHF 216,000) is the recoverable amount.', 'impairment-viu-only')],
 'b', 'After an impairment, the reduced carrying amount is depreciated over the remaining useful life.', scenario=IMPS, ev='impairment', marks=2,
 calc=f'{n(ra)} / (7 − 3) = {chf(dep26)}.', check={'f': 'max(v, f - k)/(l - y)', 'v': {'l': life, 'y': years, 'v': viu, 'f': fv, 'k': dc}, 'x': dep26}, group='Zentra Logistik impairment')
add('ai-fr-13', T, 'Impairment', 'Easy', '(1 mark) Which situation is most likely an indicator that Zentra’s other trucks may be impaired?',
 [('Fuel prices fall for six months.', 'Lower operating costs usually raise expected cash flows. That points away from impairment.', 'impairment-indicator'),
  ('Zentra wins a five-year delivery contract with a supermarket chain.', 'A new contract supports future cash flows from the trucks.', 'impairment-indicator'),
  ('A new law bans the truck type from city centres from 2027.', 'A legal change that limits use reduces expected cash flows, which is an external impairment indicator.', None),
  ('Zentra changes its auditor.', 'A change of auditor says nothing about the economic value of the trucks.', 'impairment-indicator')],
 'c', 'Impairment indicators are events that suggest an asset’s recoverable amount may have fallen below its carrying amount.', ev='impairment', marks=1)
add('ai-fr-14', T, 'Impairment', 'Easy', '(1 mark) True or false: Under IFRS, an asset is impaired whenever its value in use is below its carrying amount, regardless of its fair value less costs of disposal.',
 [('True', 'Value in use is only one of the two measures. A higher fair value less costs of disposal can support the carrying amount.', 'impairment-viu-only'),
  ('False', 'The test uses the higher of the two measures. If either one covers the carrying amount, there is no impairment.', None)],
 'b', 'Recoverable amount = max(value in use, fair value less costs of disposal).', ev='impairment', marks=1)

gw, yrs = 1_350_000, 5
add('ai-fr-15', T, 'Goodwill', 'Medium', '(2 marks) On 1 January 2025, Selvia Holding recognizes goodwill of CHF 1,350,000. It amortizes goodwill straight-line over five years under Swiss GAAP FER. No impairment occurs. What is the goodwill carrying amount on 31 December 2026 under Swiss GAAP FER and under IFRS?',
 [(f'FER {chf(gw - 2*gw/yrs)}; IFRS {chf(gw)}', f'FER: two years of amortization at CHF {n(gw/yrs)}. IFRS does not amortize goodwill; it is tested for impairment yearly.', None),
  (f'FER {chf(gw)}; IFRS {chf(gw - 2*gw/yrs)}', 'Swaps the frameworks. IFRS does not amortize goodwill; FER does.', 'goodwill-framework'),
  (f'FER {chf(gw - 2*gw/yrs)}; IFRS {chf(gw - 2*gw/yrs)}', 'Applies amortization under IFRS. IFRS only tests goodwill for impairment.', 'goodwill-ifrs-amortization'),
  (f'FER {chf(gw - gw/yrs)}; IFRS {chf(gw)}', 'Deducts one year of amortization. By 31 December 2026 two years have passed.', 'goodwill-wrong-year')],
 'a', 'Swiss GAAP FER amortizes capitalized goodwill (usually over five years, at most 20). IFRS does not amortize goodwill and tests it for impairment at least annually.', ev='goodwill', marks=2,
 calc=f'FER: 1,350,000 − 2 × 270,000 = {chf(gw-2*gw/yrs)}. IFRS: {chf(gw)}.',
 check={'f': '(g - 2*g/y, g)', 'v': {'g': gw, 'y': yrs}, 'x': (gw - 2*gw/yrs, gw), 'same': 'b'})
add('ai-fr-16', T, 'Goodwill', 'Easy', '(1 mark) Which statement on goodwill is correct?',
 [('Under IFRS, goodwill is amortized over a maximum of 20 years.', 'IFRS does not amortize goodwill. The 20-year cap is a Swiss GAAP FER rule.', 'goodwill-ifrs-amortization'),
  ('Goodwill is not tested for impairment because it has no market price.', 'Under IFRS goodwill is tested for impairment at least once a year.', 'goodwill-no-impairment'),
  ('Under Swiss GAAP FER, goodwill may be offset directly against equity at acquisition, with the effect disclosed in the notes.', 'FER allows this alternative to capitalizing and amortizing goodwill.', None),
  ('Goodwill must be expensed in full in the year of acquisition under both frameworks.', 'Neither framework requires immediate expensing.', 'goodwill-immediate-expense')],
 'c', 'FER lets companies either capitalize and amortize goodwill or offset it against equity; IFRS capitalizes it and tests for impairment.', ev='goodwill', marks=1)

add('ai-fr-17', T, 'Accounting frameworks', 'Easy', '(1 mark) Which statement about the Swiss Code of Obligations (CO) is correct?',
 [('The CO is based on the true-and-fair-view principle and forbids hidden reserves.', 'The CO follows prudence and allows hidden reserves. True and fair view is the aim of FER and IFRS.', 'framework-objective'),
  ('The CO is based on prudence, so hidden reserves are allowed in the statutory accounts.', 'Prudence lets companies understate assets and overstate provisions, creating hidden reserves.', None),
  ('Companies that apply IFRS no longer need to prepare CO statutory accounts.', 'The CO is the law. Standards such as IFRS or FER come on top of it.', 'standards-replace-law'),
  ('The CO is a rule-based standard issued by the IASB.', 'The CO is Swiss law, not an IASB standard.', 'framework-classification')],
 'b', 'Swiss statutory accounts follow the CO and its prudence principle; FER, IFRS and US GAAP aim at a true and fair view.', ev='frameworks', marks=1)
add('ai-fr-18', T, 'Accounting frameworks', 'Easy', '(1 mark) What is a disadvantage of principle-based standards compared with rule-based standards?',
 [('They need more professional judgment, so similar transactions can be reported differently.', 'Flexibility is the trade-off: more judgment means less comparability.', None),
  ('They are much longer and more detailed.', 'That describes rule-based standards such as US GAAP.', 'principles-no-guidance'),
  ('They cannot be used by listed companies.', 'IFRS is principle-based and widely used by listed companies.', 'listing-standard'),
  ('They guarantee identical treatment of all transactions.', 'Principles leave room for judgment, so they do not guarantee identical treatment.', 'principles-perfect-comparability')],
 'a', 'Principle-based standards give flexibility and require judgment, which can reduce comparability.', ev='frameworks', marks=1)
add('ai-fr-19', T, 'Pensions', 'Easy', '(1 mark) Under which plan does the employee, not the employer, carry the investment risk?',
 [('A defined benefit plan', 'In a defined benefit plan the employer promises the benefit, so it carries the investment risk.', 'pension-plan-risk'),
  ('A defined contribution plan', 'The employer pays fixed contributions; the final benefit depends on investment returns, so the employee carries the risk.', None),
  ('Both plans place the risk on the employer', 'Only the defined benefit plan does.', 'pension-plan-risk'),
  ('Neither plan has investment risk', 'Both plans invest assets; the question is who carries the shortfall.', 'pension-plan-risk')],
 'b', 'Defined contribution: risk with the employee. Defined benefit: risk with the employer.', ev='pensions', marks=1)
add('ai-fr-20', T, 'Pensions', 'Medium', '(1 mark) True or false: Under a defined benefit plan, if plan assets earn less than expected, the employer may have to increase its contributions to meet the promised pensions.',
 [('True', 'The benefit is fixed, so a shortfall in returns has to be funded by the employer.', None),
  ('False', 'In a defined benefit plan the promise is fixed, so the employer covers shortfalls.', 'pension-plan-risk')],
 'a', 'A defined benefit plan promises a benefit level. Poor returns increase the employer’s obligation.', ev='pensions', marks=1)
