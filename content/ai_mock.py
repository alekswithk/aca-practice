"""AI mock exam: 50 new questions in the layout of the past papers.
Part 1 (45 min, 45 marks): 10 Consolidated Statements, 10 Financial Reporting, 10 Auditing.
Part 2 (45 min, 45 marks): 6 Management Accounting, 4 Budgeting, 4 Variances, 3 Capital Budgeting, 3 Cost and Performance Management.
These questions are kept out of the practice pools and mixed exams.
"""
from ai_common import add as _add, D, r, chf, n, pct, table, none_wrong, none_right, QUESTIONS
S = '’'
ORDER = [0]
def add(ident, *a, **k):
 q = _add('mock-' + ident, *a, bank_set='mock-exam', group='AI mock exam', **k)
 ORDER[0] += 1; q['examOrder'] = ORDER[0]
 return q

# ---------- Part 1: Consolidated Statements ----------
CS = 'Consolidated Statements'
add('01', CS, 'Accounting frameworks', 'Easy', '(1 mark) Select the response that best fills in the blanks: US GAAP are ___-based, Swiss GAAP FER are ___-based, and both aim at a ___.',
 [('principle; rule; prudent view', 'Swaps the labels and uses the CO’s prudence objective.', 'framework-classification'),
  ('rule; principle; true and fair view', 'US GAAP: rules; FER: principles; both aim at a true and fair view.', None),
  ('rule; rule; true and fair view', 'FER is principle-based.', 'framework-classification'),
  ('principle; principle; prudent view', 'US GAAP is rule-based, and the objective is a true and fair view.', 'framework-objective')], 'b',
 'US GAAP is rule-based; FER and IFRS are principle-based; all three aim at a true and fair view.', ev='frameworks', marks=1)
add('02', CS, 'Consolidation concepts', 'Easy', '(1 mark) True or false: An associate in which the investor holds 35% of the voting rights is fully consolidated.',
 [('True', 'Full consolidation requires control. 35% normally gives significant influence, so the equity method applies.', 'ownership-control'),
  ('False', 'An associate is accounted for with the equity method.', None)], 'b', 'Control → full consolidation; significant influence → equity method.', ev='equity', marks=1)
pe = {'ca': 2_300_000, 'nca': 12_700_000, 'ap': 1_900_000, 'ltd': 5_100_000, 'eq': 8_000_000}
se = {'ca': 1_150_000, 'nca': 4_450_000, 'ap': 600_000, 'ltd': 900_000, 'eq': 4_100_000}
assert pe['ca'] + pe['nca'] == pe['ap'] + pe['ltd'] + pe['eq'] and se['ca'] + se['nca'] == se['ap'] + se['ltd'] + se['eq']
pr, sh, hr = 3_300_000, D('0.6'), 500_000
fv = se['eq'] + hr; gw = pr - sh * fv; nci = (1 - sh) * fv
TES = ('Tessaro AG acquired 60% of Rimini Tech AG on 31 December 2025 for CHF 3,300,000. Rimini owns a building with hidden reserves of CHF 500,000 that are not in its balances. '
       'Tessaro’s balances already include the investment in Rimini at CHF 3,300,000 within non-current assets.\n\n'
       + table(['Balance at 31.12.2025 (CHF)', 'Tessaro AG', 'Rimini Tech AG'], [['Current assets', n(pe['ca']), n(se['ca'])], ['Non-current assets', n(pe['nca']), n(se['nca'])],
               ['Accounts payable', n(pe['ap']), n(se['ap'])], ['Long-term debt', n(pe['ltd']), n(se['ltd'])], ['Equity', n(pe['eq']), n(se['eq'])]]))
TA = ['Course acquisition model: partial goodwill, NCI at proportionate fair-value net assets, no deferred tax on hidden reserves.']
add('03', CS, 'Acquisition accounting', 'Medium', '(2 marks) Does goodwill arise from the acquisition? If so, how much under the method learned in class?',
 [(f'Yes; {chf(pr - sh*se["eq"])}', 'Ignores the hidden reserves.', 'goodwill-ignore-reserves'), (f'Yes; {chf(gw)}', f'3,300,000 − 60% × 4,600,000 = {chf(gw)}.', None),
  ('No goodwill is recognized', 'The price exceeds the acquired share of CHF 2,760,000.', 'goodwill-zero'), (f'Yes; {chf(pr - (1-sh)*fv)}', 'Subtracts the NCI share instead of the parent’s share.', 'goodwill-wrong-share')], 'b',
 'Goodwill = price − parent share of fair-value net assets.', scenario=TES, assume=TA, ev='acquisition', calc=f'FV net assets = 4,600,000; 60% = 2,760,000; goodwill = {chf(gw)}.',
 check={'f': 'p - s*(e + h)', 'v': {'p': pr, 's': sh, 'e': se['eq'], 'h': hr}, 'x': gw})
add('04', CS, 'Acquisition accounting', 'Medium', '(2 marks) What is the non-controlling interest on Tessaro’s consolidated balance sheet at 31 December 2025?',
 [(chf((1-sh)*se['eq']), 'Leaves out the NCI share of the hidden reserves.', 'nci-ignore-reserves'), (chf(sh*fv), 'This is Tessaro’s share.', 'nci-parent-share'),
  (chf(nci), f'40% × 4,600,000 = {chf(nci)}.', None), (chf((1-sh)*pr), 'Bases NCI on the purchase price.', 'nci-purchase-price')], 'c',
 'NCI = minority share × fair-value net assets.', scenario=TES, assume=TA, ev='acquisition', calc=f'40% × 4,600,000 = {chf(nci)}.', check={'f': '(1-s)*(e + h)', 'v': {'s': sh, 'e': se['eq'], 'h': hr}, 'x': nci})
add('05', CS, 'Acquisition accounting', 'Easy', '(1 mark) What is the equity attributable to Tessaro AG shareholders on the consolidated balance sheet at 31 December 2025?',
 [(chf(pe['eq']), 'At acquisition the subsidiary’s equity is eliminated, so parent-attributable equity equals Tessaro’s equity.', None), (chf(pe['eq'] + se['eq']), 'Adds Rimini’s equity.', 'equity-add-subsidiary'),
  (chf(pe['eq'] + nci), 'Includes NCI.', 'parent-equity-includes-nci'), (chf(pe['eq'] + gw), 'Adds goodwill to equity.', 'goodwill-nci-confusion')], 'a',
 'Subsidiary equity is eliminated at acquisition.', scenario=TES, assume=TA, ev='acquisition', calc=f'{chf(pe["eq"])}.', check={'f': 'e', 'v': {'e': pe['eq']}, 'x': pe['eq']})
ta = pe['ca'] + pe['nca'] - pr + se['ca'] + se['nca'] + hr + gw
add('06', CS, 'Acquisition accounting', 'Hard', '(2 marks) What are total consolidated assets at 31 December 2025?',
 [(chf(ta), f'15,000,000 − 3,300,000 + 5,600,000 + 500,000 + {n(gw)} = {chf(ta)}.', None), (chf(pe['ca']+pe['nca']+se['ca']+se['nca']), 'Adds both balance sheets without eliminating the investment.', 'consolidation-parent-only'),
  (chf(ta - gw - hr), 'Forgets hidden reserves and goodwill.', 'goodwill-ignore-reserves'), (chf(ta - gw), 'Forgets goodwill.', 'goodwill-zero')], 'a',
 'Consolidated assets = parent assets − investment + subsidiary assets + hidden reserves + goodwill.', scenario=TES, assume=TA, ev='acquisition',
 calc=f'Check: liabilities 8,500,000 + equity 8,000,000 + NCI {n(nci)} = {n(ta)}.', check={'f': 'a - p + b + h + p - s*(e + h)', 'v': {'a': 15_000_000, 'p': pr, 'b': 5_600_000, 'h': hr, 's': sh, 'e': se['eq']}, 'x': ta})
op, sh2, prof, dv, dep = 2_000_000, D('0.25'), 640_000, 200_000, 80_000
cl = op + sh2 * (prof - dep - dv)
add('07', CS, 'Equity method', 'Medium', f'(2 marks) Gstaad Invest AG holds 25% of Alpina Hotels AG and applies the equity method. On 1 January 2025 the investment is CHF 2,000,000. In 2025 Alpina earns CHF 640,000 and pays dividends of CHF 200,000. Depreciation on hidden reserves identified at purchase is CHF 80,000 per year (for 100% of Alpina). What is the investment on 31 December 2025?',
 [(chf(op + sh2 * (prof - dv)), 'Ignores the hidden-reserve depreciation.', 'equity-ignore-reserves'), (chf(op + sh2 * (prof - dep)), 'Ignores the dividend.', 'equity-ignore-dividends'),
  (chf(op + sh2 * prof - dep - sh2 * dv), 'Deducts all of the hidden-reserve depreciation instead of 25%.', 'equity-whole-reserves'), (chf(cl), f'2,000,000 + 25% × (640,000 − 80,000 − 200,000) = {chf(cl)}.', None)], 'd',
 'Investment = opening + share of (profit − hidden-reserve depreciation) − share of dividends.', ev='equity', calc=f'2,000,000 + 160,000 − 20,000 − 50,000 = {chf(cl)}.',
 check={'f': 'o + s*(p - h - d)', 'v': {'o': op, 's': sh2, 'p': prof, 'h': dep, 'd': dv}, 'x': cl})
add('08', CS, 'Equity method', 'Easy', '(1 mark) Where does the investor show its share of an associate’s profit under the equity method?',
 [('As revenue, line by line with the associate’s sales', 'Line-by-line inclusion is full consolidation.', 'consolidation-parent-only'),
  ('As one line, “share of profit of associates”, in the income statement', 'The equity method reports one net figure.', None),
  ('Only in the notes', 'It is recognized in profit or loss.', 'equity-ignore-profit'), ('Directly in equity, never in profit or loss', 'The share of profit goes through the income statement.', 'equity-ignore-profit')], 'b',
 'The equity method is a one-line consolidation.', ev='equity', marks=1)
add('09', CS, 'Consolidation concepts', 'Easy', '(1 mark) Parent AG lends CHF 500,000 to its 100% subsidiary. How is the loan treated in the consolidated balance sheet?',
 [('It is shown as a receivable and a payable of CHF 500,000.', 'Intragroup balances must be eliminated.', 'intragroup-not-eliminated'), ('Only the receivable is shown.', 'Both sides are eliminated.', 'intragroup-not-eliminated'),
  ('Both the receivable and the payable are eliminated.', 'The group cannot owe money to itself.', None), ('It is added to goodwill.', 'Loans do not affect goodwill.', 'goodwill-net-assets')], 'c',
 'Intragroup receivables and payables are eliminated in consolidation.', ev='acquisition', marks=1)
add('10', CS, 'Consolidation concepts', 'Medium', '(2 marks) Lucerna AG (revenue CHF 5,400,000) sold goods for CHF 900,000 to its 100% subsidiary Monte SA (revenue CHF 2,200,000). Monte sold all of these goods to outside customers in the same year. What is consolidated revenue?',
 [(chf(7_600_000), 'No elimination of the intragroup sale.', 'intragroup-not-eliminated'), (chf(6_700_000), '5,400,000 + 2,200,000 − 900,000 = 6,700,000.', None),
  (chf(5_800_000), 'Eliminates the intragroup sale twice.', 'intragroup-not-eliminated'), (chf(4_500_000), 'Shows only the parent’s external revenue.', 'consolidation-parent-only')], 'b',
 'Intragroup sales are eliminated.', ev='acquisition', calc='5,400,000 + 2,200,000 − 900,000 = CHF 6,700,000.', check={'f': 'a + b - c', 'v': {'a': 5_400_000, 'b': 2_200_000, 'c': 900_000}, 'x': 6_700_000})

# ---------- Part 1: Financial Reporting ----------
FR = 'Financial Reporting'
add('11', FR, 'Leases', 'Easy', '(1 mark) Which statement about leasing under IFRS 16 is not true?',
 [('The lessee recognizes a right-of-use asset and a lease liability.', 'True statement.', 'lease-off-balance-sheet'), ('Lease payments are split into interest and repayment of the liability.', 'True statement.', 'lease-payment-split'),
  ('A lessee shows a five-year machine lease only as rental expense, off the balance sheet.', 'Not true, and therefore the answer: IFRS 16 puts leases on the lessee’s balance sheet.', None),
  ('The right-of-use asset is depreciated over the lease term.', 'True statement.', 'lease-no-depreciation')], 'c', 'IFRS 16 brings leases onto the lessee’s balance sheet.', ev='lease', marks=1)
p, i_, term = 9_000, D('0.06'), 5
pv = r(sum(p / (1 + i_) ** t for t in range(1, term + 1)), 2)
int1 = r(pv * i_, 2); bal1 = r(pv - (p - int1), 2); int2 = r(bal1 * i_, 2); rou2 = pv * 3 / 5
BRA = ('On 1 January 2025, Brava Logistik AG leases sorting equipment for five years, equal to its useful life. It pays CHF 9,000 at the end of each year. The implicit interest rate is 6%. Brava reports under IFRS and depreciates straight-line. '
       'Round interest and balances to cents and round the final answer up to the next franc.')
add('12', FR, 'Leases', 'Medium', '(2 marks) What is the carrying amount of the right-of-use asset on 31 December 2026?',
 [(chf(pv, mode='up'), 'This is the initial amount, before depreciation.', 'lease-wrong-year'), (chf(pv * 4 / 5, mode='up'), 'Deducts one year of depreciation instead of two.', 'lease-wrong-year'),
  (chf(rou2, mode='up'), f'PV {n(pv,2)} × 3/5 = {n(rou2,2)} → {chf(rou2,mode="up")}.', None), (chf(r(bal1 - (p - int2), 2), mode='up'), 'This is the lease liability after two payments.', 'lease-liability-as-asset')], 'c',
 'ROU asset = initial PV less straight-line depreciation.', scenario=BRA, ev='lease', calc=f'PV = 9,000 × 4.2124 = {n(pv,2)}; × 3/5 = {n(rou2,2)} → {chf(rou2,mode="up")}.',
 check={'f': 'p*(1-(1+i)**-5)/i*3/5', 'v': {'p': p, 'i': i_}, 'x': rou2, 'mode': 'up'})
add('13', FR, 'Leases', 'Medium', '(2 marks) How much of the 2026 lease payment is interest?',
 [(chf(int1, mode='up'), 'This is the 2025 interest.', 'lease-wrong-year'), (chf(int2, mode='up'), f'Opening 2026 liability {n(bal1,2)} × 6% = {n(int2,2)} → {chf(int2,mode="up")}.', None),
  (chf(p - int2, mode='up'), 'This is the repayment part.', 'lease-payment-split'), (chf(p * i_, mode='up'), 'Applies 6% to the payment instead of the liability.', 'lease-calculation')], 'b',
 'Interest = opening liability × rate.', scenario=BRA, ev='lease', calc=f'2025: interest {n(int1,2)}, closing {n(bal1,2)}. 2026 interest = {n(int2,2)} → {chf(int2,mode="up")}.',
 check={'f': '(p*(1-(1+i)**-5)/i*(1+i) - p)*i', 'v': {'p': p, 'i': i_}, 'x': int2, 'mode': 'up'})
c14 = 12_000_000; dtl = (c14 * D('0.75') - c14 * D('0.5')) * D('0.19')
add('14', FR, 'Deferred taxes', 'Hard', '(2 marks) Kandor AG buys a machine for CHF 12 million on 1 January 2025. IFRS: straight-line over four years, no residual value. Tax: 50% declining balance. Tax rate 19%. Which balance arises at 31 December 2025?',
 [(f'Deferred tax liability of {chf(dtl)}', f'Book 9,000,000 − tax base 6,000,000 = 3,000,000 × 19% = {chf(dtl)}.', None), (f'Deferred tax asset of {chf(dtl)}', 'Direction reversed: book above tax base means a liability.', 'tax-direction'),
  (f'Deferred tax liability of {chf(3_000_000)}', 'Forgets the tax rate.', 'tax-rate-omitted'), (f'Deferred tax liability of {chf(9_000_000 * D("0.19"))}', 'Taxes the whole book value.', 'tax-gross-balance')], 'a',
 'Book value above tax base → DTL = difference × rate.', ev='tax', calc=f'(9,000,000 − 6,000,000) × 19% = {chf(dtl)}.', check={'f': '(c*3/4 - c*0.5)*t', 'v': {'c': c14, 't': 0.19}, 'x': dtl, 'same': 'b'})
dta = (80_000 * D('0.8') - 50_000) * D('0.22')
add('15', FR, 'Deferred taxes', 'Medium', '(2 marks) Merano Moda AG writes down inventory from CHF 80,000 to CHF 50,000 in its IFRS accounts. Tax allows a 20% write-down now; the rest is deductible on sale. Tax rate 22%. Which statement is correct?',
 [(f'Temporary difference; deferred tax asset of {chf(dta)}', f'Tax base 64,000 − book 50,000 = 14,000 × 22% = {chf(dta)}.', None), (f'Temporary difference; deferred tax liability of {chf(dta)}', 'Direction reversed.', 'tax-direction'),
  ('Permanent difference; no deferred tax', 'The difference reverses on sale.', 'tax-permanent-vs-temporary'), (f'Temporary difference; deferred tax asset of {chf(30_000 * D("0.22"))}', 'Taxes the whole write-down.', 'tax-wrong-difference')], 'a',
 'Tax base above book value → DTA.', ev='tax', calc=f'(64,000 − 50,000) × 22% = {chf(dta)}.', check={'f': '(c*(1-a) - b)*t', 'v': {'c': 80_000, 'a': 0.2, 'b': 50_000, 't': 0.22}, 'x': dta, 'same': 'b'})
loss = 310_000 - max(265_000, 290_000 - 15_000)
add('16', FR, 'Impairment', 'Medium', '(2 marks) A packaging machine of Feldis AG has a carrying amount of CHF 310,000. Value in use is CHF 265,000; fair value is CHF 290,000 and costs of disposal are CHF 15,000. What impairment loss is recognized?',
 [(chf(45_000), 'Uses value in use, but fair value less costs of disposal is higher.', 'impairment-viu-only'), (chf(20_000), 'Ignores costs of disposal.', 'impairment-disposal-costs'),
  (chf(loss), f'Recoverable amount = max(265,000; 275,000) = 275,000. Loss = {chf(loss)}.', None), ('No impairment loss', 'Carrying amount exceeds recoverable amount.', 'impairment-no-loss')], 'c',
 'Loss = carrying amount − max(VIU, FVLCD).', ev='impairment', calc=f'310,000 − 275,000 = {chf(loss)}.', check={'f': 'c - max(v, f - d)', 'v': {'c': 310_000, 'v': 265_000, 'f': 290_000, 'd': 15_000}, 'x': loss})
add('17', FR, 'Goodwill', 'Medium', '(1 mark) True or false: Under IFRS, an impairment loss recognized on goodwill can be reversed in a later period if the business recovers.',
 [('True', 'IAS 36 prohibits reversing goodwill impairment.', 'goodwill-no-impairment'), ('False', 'Goodwill impairment losses are never reversed under IFRS.', None)], 'b', 'Goodwill impairment is permanent under IFRS.', ev='goodwill', marks=1)
add('18', FR, 'Goodwill', 'Easy', '(1 mark) Select the response that best fills in the blanks: Under Swiss GAAP FER, capitalized goodwill is ________; under IFRS it is ________.',
 [('not amortized; amortized', 'Swapped.', 'goodwill-framework'), ('amortized; not amortized but tested for impairment at least annually', 'FER amortizes; IFRS tests annually.', None),
  ('expensed immediately; amortized', 'Neither framework requires immediate expensing.', 'goodwill-immediate-expense'), ('amortized; amortized', 'IFRS does not amortize goodwill.', 'goodwill-ifrs-amortization')], 'b',
 'FER: amortize (or offset with equity). IFRS: impairment-only.', ev='goodwill', marks=1)
add('19', FR, 'Pensions', 'Easy', '(1 mark) Under a defined benefit plan, who mainly bears the investment risk?',
 [('The employee', 'That is a defined contribution plan.', 'pension-plan-risk'), ('The employer', 'The employer has promised the benefit and must fund shortfalls.', None),
  ('The state pension system', 'Not in an employer plan.', 'pension-plan-risk'), ('Nobody, because benefits are fixed', 'Fixed benefits are exactly why the employer bears the risk.', 'pension-plan-risk')], 'b', 'Defined benefit: employer risk.', ev='pensions', marks=1)
add('20', FR, 'Accounting frameworks', 'Easy', '(1 mark) What is an advantage of principle-based standards compared with rule-based standards?',
 [('They leave room for professional judgment, so the reporting can reflect the economic substance of a transaction.', 'Flexibility lets preparers reflect substance.', None),
  ('They guarantee identical treatment by all companies.', 'Judgment reduces uniformity.', 'principles-perfect-comparability'), ('They contain detailed bright-line rules for every case.', 'That describes rule-based standards.', 'principles-no-guidance'),
  ('They make audits unnecessary.', 'Audits are still required.', 'standards-replace-law')], 'a', 'Principles give flexibility and judgment.', ev='frameworks', marks=1)

# ---------- Part 1: Auditing ----------
AU = 'Auditing'
add('21', AU, 'Audit purpose', 'Easy', '(1 mark) What is the purpose of an external audit?',
 [('To guarantee that the company has no fraud', 'An audit gives reasonable, not absolute, assurance.', 'audit-guarantee'), ('To increase the confidence of intended users in the financial statements', 'That is the purpose.', None),
  ('To prepare the financial statements', 'Management prepares them.', 'audit-preparer'), ('To advise on the share price', 'Auditors do not value shares.', 'audit-stock-price')], 'b', 'Audits enhance users’ confidence.', ev='audit', marks=1)
add('22', AU, 'Audit purpose', 'Easy', '(1 mark) Who is responsible for preparing and fairly presenting the financial statements?',
 [('The external auditor', 'The auditor gives an opinion on them.', 'audit-preparer'), ('Internal audit', 'Internal audit gives assurance, it does not prepare the accounts.', 'internal-external-audit'),
  ('Management, under the oversight of the board', 'Responsibility lies with management and the board.', None), ('The shareholders', 'Shareholders approve, not prepare.', 'audit-preparer')], 'c', 'Management prepares; auditors opine.', ev='audit', marks=1)
ebt = 3_400_000; mat = ebt * D('0.05')
ROT = ('Rotblatt Maschinen AG is a profitable company with stable earnings and is subject to an ordinary audit. Earnings before taxes for 2025 are CHF 3,400,000. The auditors found two misstatements:\n\n'
       '1. A supplier invoice of CHF 60,000 for December repairs was not recorded.\n2. Spare parts inventory is overstated by CHF 140,000 because obsolete parts were not written down.')
add('23', AU, 'Materiality', 'Medium', '(2 marks) What is preliminary materiality, using the benchmark that fits Rotblatt?',
 [(chf(mat), '5% × 3,400,000 = 170,000.', None), (chf(ebt * D('0.01')), 'Uses 1% instead of 5%.', 'materiality-mechanical'), (chf(ebt), 'This is the benchmark, not materiality.', 'materiality-mechanical'), (chf(ebt * D('0.5')), 'Uses 50%.', 'materiality-mechanical')], 'a',
 'Stable profitable company → income before taxes.', scenario=ROT, assume=['Study clarification: 5% of stable pre-tax profit as the illustrative threshold. Not an official exam rule.'], ev='materiality',
 calc=f'5% × 3,400,000 = {chf(mat)}.', check={'f': 'e*0.05', 'v': {'e': ebt}, 'x': mat})
add('24', AU, 'Materiality', 'Hard', '(2 marks) Will the auditors advise Rotblatt to correct the misstatements? If so, what is the effect?',
 [('No correction needed', 'Combined, they reduce EBT by CHF 200,000, above the CHF 170,000 materiality.', 'materiality-ignore-aggregation'), ('Yes; decrease in earnings before taxes of CHF 140,000', 'Omits the unrecorded invoice.', 'misstatement-omitted-item'),
  ('Yes; increase in earnings before taxes of CHF 200,000', 'Direction reversed.', 'misstatement-direction'), ('Yes; decrease in earnings before taxes of CHF 200,000', 'Both errors overstate profit: −60,000 − 140,000 = −200,000, above materiality.', None)], 'd',
 'Aggregate misstatements and compare with materiality.', scenario=ROT, assume=['Study clarification: 5% of stable pre-tax profit as the illustrative threshold. Not an official exam rule.'], ev='materiality',
 calc='Correction = −60,000 − 140,000 = −200,000 > 170,000.', check={'f': 'a + b', 'v': {'a': 60_000, 'b': 140_000}, 'x': 200_000, 'same': 'c'})
add('25', AU, 'Audit opinions', 'Medium', '(2 marks) The auditor of Selva Holz AG could not attend the inventory count. Inventory is material but not pervasive, and no alternative evidence is available. Which opinion is issued?',
 [('Unmodified opinion', 'Evidence for a material item is missing.', 'audit-opinion-types'), ('Qualified opinion (“except for”)', 'Missing evidence on a material but not pervasive item leads to a qualified opinion.', None),
  ('Adverse opinion', 'Adverse is for material and pervasive misstatements.', 'audit-opinion-scope'), ('Disclaimer of opinion', 'A disclaimer is for pervasive effects.', 'audit-opinion-scope')], 'b', 'Not pervasive → qualified.', ev='opinion')
add('26', AU, 'Audit scope', 'Easy', '(1 mark) Which company must have an ordinary audit under the CO?',
 [('An unlisted company with CHF 10 million assets, CHF 15 million revenue and 60 employees', 'Below all thresholds.', 'audit-scope'), ('A company that is required to prepare consolidated accounts', 'This is one of the triggers for an ordinary audit.', None),
  ('Any company with more than ten employees', 'More than ten employees only removes the opt-out option.', 'audit-opt-out'), ('A family-owned company whose shareholders ask for no audit', 'Shareholders can only opt out under strict conditions.', 'audit-opt-out')], 'b',
 'Ordinary audit triggers: listing, size thresholds, consolidation duty.', ev='legal', marks=1)
add('27', AU, 'Audit procedures', 'Medium', '(2 marks) Which of the following is a test of details for inventory?',
 [('Comparing inventory turnover with the prior year', 'Analytical.', 'audit-analytical-vs-details'), ('Comparing gross margin by product line with budget', 'Analytical.', 'audit-analytical-vs-details'),
  ('Test-counting selected items and tracing them to the inventory listing', 'This examines specific items: a test of details.', None), ('Comparing the share of slow-moving items with last year', 'Analytical.', 'audit-analytical-vs-details')], 'c',
 'Tests of details examine individual items and documents.', ev='procedures')
add('28', AU, 'Key Audit Matters', 'Easy', '(1 mark) Which statement about Key Audit Matters is correct?',
 [('They replace the audit opinion.', 'The opinion stays; KAMs add information.', 'kam-routine-vs-significant'), ('They describe the matters of most significance in the audit of a listed company.', 'That is their role.', None),
  ('They list every adjustment proposed by the auditor.', 'Not a list of adjustments.', 'kam-routine-vs-significant'), ('They usually concern routine items like office rent.', 'Routine items are rarely KAMs.', 'kam-routine-vs-significant')], 'b', 'KAMs highlight significant judgments.', ev='kam', marks=1)
add('29', AU, 'Three Lines Model', 'Medium', '(2 marks) In the Three Lines Model, where does the compliance function belong?',
 [('First line', 'The first line runs operations.', 'three-lines-first'), ('Second line', 'Risk management and compliance support and monitor the first line.', None),
  ('Third line', 'The third line is internal audit.', 'three-lines-third'), ('Outside the model, like the external auditor', 'Compliance is inside the organization.', 'internal-external-audit')], 'b', 'Compliance and risk management form the second line.', ev='lines')
add('30', AU, 'Expectation gap', 'Easy', '(1 mark) Auditors fail to apply an existing auditing standard correctly. Which part of the expectation gap does this describe?',
 [('Knowledge gap', 'The knowledge gap is about users misunderstanding the audit.', 'expectation-gap-taxonomy'), ('Performance gap', 'Auditors not meeting existing standards is the performance gap.', None),
  ('Evolution gap', 'The evolution gap is about future developments.', 'expectation-gap-taxonomy'), ('Reporting gap', 'Not one of the three components discussed.', 'expectation-gap-taxonomy')], 'b', 'Knowledge, performance and evolution gaps.', ev='gap', marks=1)

# ---------- Part 2: Controlling ----------
MA = 'Management Accounting'
c = lambda x, dp=0, mode='half': chf(x, dp, S, mode)
u = lambda x, dp=0: n(x, dp, S)
pz, vz, fz, tz = 18, D('7.20'), 151_200, D('0.22')
cmz = pz - vz; bez = fz / cmz
OST = 'Ostello Kerzen AG sells scented candles for CHF 18 each. Variable costs are CHF 7.20 per candle and fixed costs are CHF 151’200 per year. The income tax rate is 22%.'
add('31', MA, 'CVP analysis', 'Easy', '(2 marks) How many candles must Ostello sell to break even?',
 [(u(fz / pz), 'Divides by price instead of contribution margin.', 'cvp-break-even-profit'), (u(fz / vz), 'Divides by variable cost.', 'cvp-break-even-profit'), (u(bez), '151’200 / 10.80 = 14’000.', None),
  (u(fz / cmz * (1 - tz)), 'Applies tax at break-even.', 'tax-affects-break-even'), none_wrong('c')], 'c', 'Break-even = fixed costs / contribution margin per unit.', scenario=OST, ev='ma-cvp',
 calc=f'151’200 / 10.80 = {u(bez)}.', check={'f': 'f/(p - v)', 'v': {'f': fz, 'p': pz, 'v': vz}, 'x': bez, 'unit': 'units'})
add('32', MA, 'CVP analysis', 'Medium', '(2 marks) What is the break-even revenue?',
 [(c(bez * pz), '14’000 × 18 = 252’000.', None), (c(fz / (1 - cmz / pz)), 'Divides by the variable-cost ratio.', 'cvp-cost-ratio'), (c(fz), 'This is fixed cost.', 'fixed-cost-omitted'), (c(bez * vz), 'Values break-even units at variable cost.', 'cvp-target-revenue'), none_wrong('a')], 'a',
 'Break-even revenue = fixed costs / CM ratio.', scenario=OST, ev='ma-cvp', calc=f'151’200 / 0.60 = {c(bez*pz)}.', check={'f': 'f*p/(p - v)', 'v': {'f': fz, 'p': pz, 'v': vz}, 'x': bez * pz})
tgt = 84_240; uz = (fz + tgt / (1 - tz)) / cmz
add('33', MA, 'CVP analysis', 'Hard', '(4 marks) How many candles must Ostello sell to earn a net income after taxes of CHF 84’240?',
 [(u((fz + tgt) / cmz), 'Does not gross up the after-tax target.', 'tax-gross-up-omitted'), (u((fz + tgt * (1 + tz)) / cmz), 'Grosses up by multiplying with 1.22.', 'tax-gross-up-direction'),
  (u(tgt / (1 - tz) / cmz), 'Forgets fixed costs.', 'fixed-cost-omitted'), (u(uz), 'Pre-tax target 108’000; (151’200 + 108’000) / 10.80 = 24’000.', None), none_wrong('d')], 'd',
 'Units = (F + target / (1 − t)) / CM per unit.', scenario=OST, ev='ma-cvp', calc=f'84’240 / 0.78 = 108’000; 259’200 / 10.80 = {u(uz)}.', check={'f': '(f + g/(1 - t))/(p - v)', 'v': {'f': fz, 'g': tgt, 't': tz, 'p': pz, 'v': vz}, 'x': uz, 'unit': 'units'})
add('34', MA, 'Manufacturing cost flows', 'Easy', '(2 marks) Vira Metallbau AG had direct materials of CHF 12’000 at the start of the year, purchased CHF 88’000 and had CHF 9’500 at year-end. What were direct materials used?',
 [(c(88_000), 'Purchases, not usage.', 'inventory-flow-direction'), (c(85_500), 'Reverses the inventory change.', 'inventory-flow-direction'), (c(100_000), 'Materials available, before ending inventory.', 'inventory-flow-direction'), (c(90_500), '12’000 + 88’000 − 9’500 = 90’500.', None), none_wrong('d')], 'd',
 'Used = beginning + purchases − ending.', ev='ma-flow', calc='12’000 + 88’000 − 9’500 = CHF 90’500.', check={'f': 'a + b - c', 'v': {'a': 12_000, 'b': 88_000, 'c': 9_500}, 'x': 90_500})
rate = D(1_365_000) / 975_000; lab = 120 * 95; price = lab * (1 + rate) / D('0.8')
add('35', MA, 'Job costing', 'Hard', '(4 marks) Studio Brenner, an architecture firm, budgets indirect costs of CHF 1’365’000 and direct labor costs of CHF 975’000; indirect costs are allocated on direct labor cost. A design job needs 120 hours at CHF 95. What price must the firm charge to earn an operating income of 20% of revenue?',
 [(c(lab * (1 + rate) * D('1.2')), 'Adds 20% to cost; the margin is on revenue.', 'margin-versus-markup'), (c(price), f'Labor 11’400; indirect 140% = 15’960; total 27’360; / 0.8 = {c(price)}.', None),
  (c(lab / D('0.8')), 'Ignores indirect costs.', 'manufacturing-overhead-omitted'), (c(lab * (1 + rate)), 'Total cost without profit.', 'markup-omitted'), none_wrong('b')], 'b',
 'Price = (direct + allocated indirect cost) / (1 − margin).', ev='ma-price', calc=f'Rate = 140%. Cost = 11’400 × 2.4 = 27’360. Price = {c(price)}.', check={'f': 'h*w*(1 + i/d)/(1 - m)', 'v': {'h': 120, 'w': 95, 'i': 1_365_000, 'd': 975_000, 'm': 0.2}, 'x': price})
add('36', MA, 'Pricing and target costing', 'Easy', '(1 mark) Which statement describes target costing?',
 [('Price = full cost + a fixed markup.', 'That is cost-plus pricing.', 'markup-cost-base'), ('Target cost = expected market price − desired profit per unit.', 'Start from the market price and work back to allowable cost.', None),
  ('Costs are allocated on direct labor hours.', 'That is overhead allocation.', 'overhead-allocation-base'), ('Only variable costs are relevant for pricing.', 'Not the target costing idea.', 'long-run-variable-only'), none_wrong('b')], 'b', 'Target costing is market-driven.', ev='ma-price')
BU = 'Budgeting'; MB = 'budgeting-calculation'
add('37', BU, 'Production budget', 'Easy', '(2 marks) Krona Ski AG plans to sell 34,000 pairs of skis. It has 4,200 pairs in stock and wants 5,500 pairs at year-end. How many pairs must it produce?',
 [('32,900', 'Reverses the inventory change.', MB), ('35,300', '34,000 + 5,500 − 4,200 = 35,300.', None), ('39,500', 'Ignores beginning inventory.', MB), ('34,000', 'Equals sales.', MB), none_wrong('b')], 'b',
 'Production = sales + ending − beginning.', ev='budget', calc='34,000 + 5,500 − 4,200 = 35,300.', check={'f': 's + e - b', 'v': {'s': 34_000, 'e': 5_500, 'b': 4_200}, 'x': 35_300, 'unit': 'units'})
add('38', BU, 'Cash collections', 'Medium', '(2 marks) Lago Fit AG budgets sales of CHF 150,000 in July and CHF 180,000 in August. 30% of sales are paid in cash; the rest is collected in full the following month. How much cash is collected in August?',
 [(chf(180_000), 'Assumes all of August’s sales are collected in August.', MB), (chf(159_000), '54,000 cash + 70% × 150,000 = 159,000.', None),
  (chf(171_000), 'Swaps the months.', MB), (chf(105_000), 'Leaves out August cash sales.', MB), none_wrong('b')], 'b', 'Collections = cash sales + earlier credit sales collected now.', ev='budget',
 calc='0.3 × 180,000 + 0.7 × 150,000 = 159,000.', check={'f': '0.3*a + 0.7*j', 'v': {'a': 180_000, 'j': 150_000}, 'x': 159_000})
pur = 200_000 * D('0.7') + D('0.2') * 250_000 * D('0.7') - D('0.2') * 200_000 * D('0.7')
add('39', BU, 'Purchases budget', 'Hard', '(4 marks) Bellavista Shop AG budgets sales of CHF 200,000 for September and CHF 250,000 for October. Cost of goods sold is 70% of sales. Ending inventory must equal 20% of the next month’s cost of goods sold. What are September purchases?',
 [(chf(140_000), 'COGS only.', MB), (chf(pur), '140,000 + 35,000 − 28,000 = 147,000.', None), (chf(210_000), 'Uses selling prices.', MB), (chf(133_000), 'Reverses the inventory change.', MB), none_wrong('b')], 'b',
 'Purchases = COGS + ending − beginning inventory.', ev='budget', calc='COGS 140,000; ending 20% × 175,000 = 35,000; beginning 20% × 140,000 = 28,000; purchases = 147,000.',
 check={'f': 's*0.7 + 0.2*o*0.7 - 0.2*s*0.7', 'v': {'s': 200_000, 'o': 250_000}, 'x': pur})
add('40', BU, 'Master budget', 'Easy', '(1 mark) Which budget is usually prepared first in the master budget?',
 [('Cash budget', 'Needs the operating budgets first.', MB), ('Production budget', 'Depends on sales.', MB), ('Sales budget', 'Everything else follows from expected sales.', None), ('Budgeted balance sheet', 'Prepared last.', MB), none_wrong('c')], 'c',
 'The sales forecast drives the master budget.', ev='budget')
VA = 'Variances'; MV = 'variances-calculation'
BRI = 'Brienz Holzwaren AG makes wooden toy trains. The standard is 2.5 kg of beech wood per train at CHF 8.00 per kg. In May it produced 4,000 trains and used 10,600 kg of wood bought at CHF 7.70 per kg.'
add('41', VA, 'Direct material price variance', 'Easy', '(2 marks) What is the direct material price variance?',
 [('CHF 3,180 F', '(7.70 − 8.00) × 10,600 = 3,180 F.', None), ('CHF 3,180 U', 'Direction reversed.', MV), ('CHF 3,000 F', 'Uses standard quantity.', MV), ('CHF 1,620 U', 'This is the total flexible-budget variance.', MV), none_wrong('a')], 'a',
 'Price variance uses actual quantity.', scenario=BRI, ev='variance', calc='0.30 × 10,600 = 3,180 F.', check={'f': '(s - a)*q', 'v': {'s': 8, 'a': D('7.70'), 'q': 10_600}, 'x': 3_180, 'same': 'b'})
add('42', VA, 'Direct material variances', 'Medium', '(2 marks) What is the direct material efficiency variance?',
 [('CHF 4,800 F', 'Direction reversed.', MV), ('CHF 4,620 U', 'Uses the actual price.', MV), ('CHF 4,800 U', '(10,600 − 10,000) × 8 = 4,800 U.', None), ('CHF 1,620 U', 'Flexible-budget variance.', MV), none_wrong('c')], 'c',
 'Efficiency = (actual qty − allowed qty) × standard price.', scenario=BRI, ev='variance', calc='Allowed 10,000 kg; 600 × 8 = 4,800 U.', check={'f': '(a - u*k)*p', 'v': {'a': 10_600, 'u': 4_000, 'k': D('2.5'), 'p': 8}, 'x': 4_800, 'same': 'a'})
svv = (5_600 - 5_000) * (60 - 35)
add('43', VA, 'Sales-volume variance', 'Medium', '(3 marks) Alpaca Textil AG budgeted 5,000 scarves at CHF 60 with variable costs of CHF 35 per scarf and fixed costs of CHF 80,000. It actually sold 5,600 scarves. What is the sales-volume variance in operating income?',
 [('CHF 36,000 F', 'Uses the selling price instead of contribution margin.', MV), ('CHF 15,000 F', '600 × 25 = 15,000 F.', None), ('CHF 15,000 U', 'Direction reversed.', MV), ('CHF 21,000 U', 'Uses variable cost.', MV), none_wrong('b')], 'b',
 'Sales-volume variance = (actual − budgeted units) × budgeted CM per unit.', ev='variance', calc='(5,600 − 5,000) × (60 − 35) = 15,000 F.', check={'f': '(a - b)*(p - v)', 'v': {'a': 5_600, 'b': 5_000, 'p': 60, 'v': 35}, 'x': svv, 'same': 'c'})
add('44', VA, 'Fixed-overhead variances', 'Easy', '(1 mark) Which fixed-overhead variance arises only because actual output differs from the output used to set the budgeted fixed-overhead rate?',
 [('Spending variance', 'The spending variance compares actual with budgeted fixed overhead; output plays no role.', MV), ('Efficiency variance', 'Fixed overhead has no efficiency variance.', MV),
  ('Production-volume variance', 'It is budgeted fixed overhead minus fixed overhead allocated to actual output, so it comes from the output level.', None), ('Price variance', 'Price variances apply to inputs such as materials and labor.', MV), none_wrong('c')], 'c',
 'Fixed overhead has a spending variance and a production-volume variance.', ev='variance')
CB = 'Capital Budgeting'; MC = 'capital budgeting-calculation'
add('45', CB, 'Payback period', 'Easy', '(2 marks) A packaging robot costs CHF 210,000 and saves CHF 48,000 per year for eight years. No taxes, no terminal value. What is the payback period, rounded to one decimal?',
 [('4.4 years', '210,000 / 48,000 = 4.375 → 4.4 years.', None), ('4.3 years', 'Rounds down.', MC), ('5.5 years', 'Uses income after depreciation.', MC), ('0.2 years', 'Inverts the ratio.', MC), none_wrong('a')], 'a',
 'Payback = investment / annual saving.', ev='capital', calc='210,000 / 48,000 = 4.375 → 4.4 years.', check={'f': 'c/s', 'v': {'c': 210_000, 's': 48_000}, 'x': D(210_000) / 48_000, 'dp': 1, 'unit': 'years'})
npv46 = 110_000 * (D('0.893') + D('0.797') + D('0.712')) + 40_000 * D('0.712') - 300_000
add('46', CB, 'Net present value', 'Hard', '(4 marks) Frutiger Druck AG considers a machine costing CHF 300,000. It saves CHF 110,000 per year for three years and can be sold for CHF 40,000 at the end of year 3. Required return 12%; no taxes. Use factors 0.893, 0.797, 0.712. Calculate the NPV and decide.',
 [('CHF 70,000; buy', 'Ignores discounting.', MC), ('CHF −35,780; do not buy', 'Leaves out the disposal value.', MC), (f'{chf(npv46)}; do not buy', f'PV savings 264,220 + PV disposal 28,480 − 300,000 = {chf(npv46)} < 0.', None),
  ('CHF 7,300; buy', 'Right size, wrong sign.', MC), none_wrong('c')], 'c',
 'Reject projects with negative NPV.', ev='capital', calc=f'110,000 × 2.402 = 264,220; 40,000 × 0.712 = 28,480; NPV = {chf(npv46)}.',
 check={'f': 's*(0.893 + 0.797 + 0.712) + d*0.712 - c', 'v': {'s': 110_000, 'd': 40_000, 'c': 300_000}, 'x': npv46, 'same': 'd'})
add('47', CB, 'AARR and IRR', 'Easy', '(1 mark) Which statement about AARR and IRR is true?',
 [('Both ignore the time value of money.', 'IRR considers it.', MC), ('AARR uses accounting income; IRR uses discounted cash flows.', 'That is the key difference.', None),
  ('IRR uses accounting income; AARR uses cash flows.', 'Swapped.', MC), ('Both always rank projects the same way.', 'They can rank differently.', MC), none_wrong('b')], 'b', 'AARR: accrual income. IRR: discounted cash flows.', ev='capital')
CP = 'Cost and Performance Management'; MP = 'cost and performance management-calculation'
w48 = (10_000_000 * D('0.07') * D('0.75') + 15_000_000 * D('0.12')) / 25_000_000
eva48 = 2_000_000 * D('0.75') - (12_000_000 - 1_500_000) * w48
add('48', CP, 'Economic value added', 'Hard', '(3 marks) Rhone Werke AG has debt (market value) of CHF 10 million at 7% and equity (market value) of CHF 15 million at a required return of 12%. Tax rate 25%. Its Pumps division has EBIT of CHF 2,000,000, total assets of CHF 12,000,000 and current liabilities of CHF 1,500,000. Calculate the division’s EVA.',
 [(chf(eva48), f'WACC = 9.30%; NOPAT 1,500,000 − 10,500,000 × 9.30% = {chf(eva48)}.', None), (chf(1_500_000), 'NOPAT without capital charge.', MP),
  (chf(2_000_000 - 10_500_000 * w48), 'Uses EBIT before tax.', MP), (chf(1_500_000 - 12_000_000 * w48), 'Uses total assets as capital.', MP), none_wrong('a')], 'a',
 'EVA = NOPAT − WACC × (assets − current liabilities).', ev='cpm', calc=f'WACC = (0.525m + 1.8m) / 25m = 9.30%. EVA = 1,500,000 − 976,500 = {chf(eva48)}.',
 check={'f': 'x*(1 - t) - (a - c)*(d*k*(1 - t) + e*q)/(d + e)', 'v': {'x': 2_000_000, 't': 0.25, 'a': 12_000_000, 'c': 1_500_000, 'd': 10_000_000, 'k': 0.07, 'e': 15_000_000, 'q': 0.12}, 'x': eva48})
add('49', CP, 'Return on sales', 'Easy', '(2 marks) A division earns EBIT of CHF 1,260,000 with a return on sales of 9%. What is its revenue?',
 [(chf(113_400), 'Multiplies instead of divides.', MP), (chf(14_000_000), '1,260,000 / 0.09 = 14,000,000.', None), (chf(1_373_400), 'Adds 9% to EBIT.', MP), (chf(1_384_615), 'Divides by 91%.', MP), none_wrong('b')], 'b',
 'Revenue = EBIT / ROS.', ev='cpm', calc='1,260,000 / 0.09 = CHF 14,000,000.', check={'f': 'x/r', 'v': {'x': 1_260_000, 'r': 0.09}, 'x': 14_000_000})
add('50', CP, 'Balanced scorecard perspectives', 'Easy', '(1 mark) Which question belongs to the learning-and-growth perspective?',
 [('How do customers see us?', 'Customer perspective.', 'bsc-perspective'), ('What processes must we excel at?', 'Internal process perspective.', 'bsc-perspective'),
  ('How do we look to shareholders?', 'Financial perspective.', 'bsc-perspective'), ('How can our people keep learning and improving?', 'Learning and growth.', None), none_wrong('d')], 'd', 'Four BSC perspectives.', ev='cpm')

marks = {'01':1,'02':1,'03':2,'04':2,'05':1,'06':2,'07':2,'08':1,'09':1,'10':2,'11':1,'12':2,'13':2,'14':2,'15':2,'16':2,'17':1,'18':1,'19':1,'20':1,
         '21':1,'22':1,'23':2,'24':2,'25':2,'26':1,'27':2,'28':1,'29':2,'30':1,
         '31':2,'32':2,'33':4,'34':2,'35':4,'36':1,'37':2,'38':2,'39':4,'40':1,'41':2,'42':2,'43':3,'44':1,'45':2,'46':4,'47':1,'48':3,'49':2,'50':1}
mock = [q for q in QUESTIONS if q['set'] == 'mock-exam']
for q in mock:
 k = q['id'].split('-')[1]
 assert q['marks'] in (None, marks[k]), (q['id'], q['marks'], marks[k])
 q['marks'] = marks[k]; q['examPart'] = 1 if int(k) <= 30 else 2
assert len(mock) == 50
assert sum(q['marks'] for q in mock if q['examPart'] == 1) == 45 and sum(q['marks'] for q in mock if q['examPart'] == 2) == 45
