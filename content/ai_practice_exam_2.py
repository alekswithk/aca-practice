"""Questions from the unofficial ACA practice exam 2 (ACA_Probeklausur_2.pdf).

53 questions: Part 1 (Accounting & Auditing, 31) and Part 2 (Controlling, 22), wording as in the PDF.
The solutions file supplied with this exam contained the solutions of practice exam 1, so the answer key and the
explanations below were worked out from the course methods. Every numeric answer is recomputed here and again in
validate_bank.py. The questions join the practice bank (set = "bank"), sorted into the tool's topics, marked AI-generated.
"""
from ai_common import add as _add, EV, D, n, chf, table, none_wrong, none_right

SRC = 'ACA_Probeklausur_2.pdf'
EV['pe2-ifrs9'] = {'path': SRC, 'section': 'Part 1, questions 10–11: IFRS 9 classification and bonds'}
EV['pe2-ifrs18'] = {'path': SRC, 'section': 'Part 1, question 12: IFRS 18 management-defined performance measures'}
EV['pe2-ias38'] = {'path': SRC, 'section': 'Part 1, question 13: IAS 38 internally generated intangibles'}
GROUP = 'ACA practice exam 2 (unofficial)'
LEVEL = {1: 'Easy', 2: 'Medium', 3: 'Hard', 4: 'Hard'}


def add(ident, number, topic, subtopic, marks, prompt, opts, key, explanation, **k):
 q = _add('pe2-' + ident, topic, subtopic, LEVEL[marks], f'({marks} mark{"s" if marks > 1 else ""}) {prompt}', opts, key, explanation,
          group=GROUP, **k)
 part = 'Part 1 (Accounting & Auditing)' if ident.startswith('1-') else 'Part 2 (Controlling)'
 q['evidence'].append({'path': SRC, 'section': f'{part}, question {number} (answer key derived; no official solution)'})
 return q


# ======================= PART 1 – ACCOUNTING & AUDITING =======================
CS, FR, AU = 'Consolidated Statements', 'Financial Reporting', 'Auditing'

add('1-01', '1', CS, 'Accounting frameworks', 1, 'A company wants to list its shares on SIX Swiss Exchange under the International Reporting Standard. Which accounting standard(s) may it apply?',
 [('Any of the three standards', 'The International Reporting Standard does not accept the CO or Swiss GAAP FER.', 'framework-listing'),
  ('Swiss Code of Obligations (CO)', 'The CO alone is not accepted for a SIX listing.', 'framework-listing'),
  ('Swiss GAAP FER', 'Swiss GAAP FER is accepted for the Swiss Reporting Standard, not the International Reporting Standard.', 'framework-listing'),
  ('IFRS or US GAAP', 'The International Reporting Standard requires IFRS or US GAAP.', None)], 'd',
 'A listing under SIX’s International Reporting Standard requires IFRS or US GAAP; Swiss GAAP FER is accepted only under the Swiss Reporting Standard.', ev='frameworks')

add('1-02', '2', CS, 'Accounting frameworks', 1, 'Under the Swiss Code of Obligations, companies may deliberately create hidden reserves, e.g. through additional depreciation.',
 [('True', 'The CO follows the prudence principle and allows hidden reserves, e.g. extra depreciation.', None),
  ('False', 'The CO does allow hidden reserves; true-and-fair frameworks (FER, IFRS) do not.', 'framework-objective')], 'a',
 'The CO is prudence-oriented and permits hidden reserves. Swiss GAAP FER, IFRS and US GAAP aim at a true and fair view and do not.', ev='frameworks')

add('1-03', '3', CS, 'Consolidation concepts', 1, 'Which of the following is not a required element of control according to IFRS 10?',
 [('Holding more than 50% of the share capital of the investee', 'Not required: control can exist without a majority of the shares (e.g. through contracts or voting agreements).', None),
  ('Power over the investee', 'Power is one of the three elements of control.', 'ownership-control'),
  ('The ability to use the power over the investee to affect the amount of the returns', 'The link between power and returns is one of the three elements.', 'ownership-control'),
  ('Exposure, or rights, to variable returns from the involvement with the investee', 'Exposure to variable returns is one of the three elements.', 'ownership-control')], 'a',
 'IFRS 10 control = power + exposure to variable returns + ability to use the power to affect the returns. A share majority is a typical indicator, not a requirement.', ev='acquisition')

add('1-04', '4', FR, 'Goodwill', 1, 'How is goodwill from a business combination treated subsequently under IFRS?',
 [('It is expensed immediately in the year of acquisition', 'Goodwill is recognised as an asset, not expensed.', 'goodwill-policy'),
  ('It is amortised over a maximum of 20 years', 'IFRS does not amortise goodwill; amortisation is the Swiss GAAP FER / CO approach.', 'goodwill-policy'),
  ('It is offset directly against equity', 'Offsetting against equity is a Swiss GAAP FER option, not allowed under IFRS.', 'goodwill-policy'),
  ('It is not amortised, but tested for impairment at least annually', 'IFRS: no amortisation, annual impairment test.', None)], 'd',
 'Under IFRS, goodwill is not amortised but tested for impairment at least annually (impairment-only approach).', ev='goodwill')

o5, s5, p5, d5 = 2_000, D('0.4'), 500, 200
v5 = o5 + s5 * (p5 - d5)
add('1-05', '5', CS, 'Equity method', 2, 'Gamma AG acquired 40% of Delta AG on 1st January 2025 for CHF 2,000,000 (significant influence). At that date, the fair value of Delta AG’s net assets was CHF 4,000,000 and equal to its book value. In 2025, Delta AG reports a net profit of CHF 500,000 and pays a total dividend of CHF 200,000. What is the carrying amount of the investment in Delta AG in Gamma AG’s consolidated balance sheet on 31st December 2025 (in CHF thousand)?',
 [('1,720', 'Subtracts the share of profit instead of adding it: 2,000 − 200 − 80.', 'equity-ignore-profit'),
  ('2,300', 'Adds 100% of profit less dividend (300) instead of the 40% share.', 'equity-whole-reserves'),
  ('2,120', '2,000 + 40% × 500 − 40% × 200 = 2,120.', None),
  ('2,200', 'Ignores the dividend, which reduces the investment.', 'equity-ignore-dividends')], 'c',
 'Equity method: opening amount + share of profit − share of dividends. Fair value equals book value, so there is no hidden-reserve depreciation; the goodwill of 400 inside the price is not amortised.',
 ev='equity', calc=f'2,000 + 40% × 500 (200) − 40% × 200 (80) = {n(v5)}.',
 check={'f': 'o + s*(p - d)', 'v': {'o': o5, 's': s5, 'p': p5, 'd': d5}, 'x': v5})

MUTTER = ('Mutter AG acquired 80% of Tochter AG on 31.12.2025 for CHF 3,000,000. The following are the account balances as of the acquisition date. During 2025, Mutter AG granted a loan of CHF 400,000 to Tochter AG. '
          'Additionally, Tochter AG has CHF 500,000 of hidden reserves in its non-current assets, which are not included in the accounts below. Ignore deferred taxes.\n\n'
          + table(['Account (CHF)', 'Mutter AG', 'Tochter AG'],
                  [['Investment in Tochter AG', '3,000,000', '–'], ['Loan receivable from Tochter AG', '400,000', '–'], ['Other Non-Current Assets', '5,000,000', '3,200,000'],
                   ['Current Assets', '1,600,000', '800,000'], ['Long-term Debt', '3,000,000', '–'], ['Loan payable to Mutter AG', '–', '400,000'],
                   ['Accounts Payable', '1,000,000', '1,100,000'], ['Equity', '6,000,000', '2,500,000']]))
pr, sh, eq, hr = 3_000_000, D('0.8'), 2_500_000, 500_000
gw = pr - sh * (eq + hr); nci = (1 - sh) * (eq + hr)
add('1-06', '6', CS, 'Acquisition accounting', 3, 'Does Mutter AG recognise any goodwill related to the acquisition of Tochter AG? If so, what is the amount of goodwill according to the method you learned in class?',
 [('No goodwill is recognised.', 'The price of 3,000,000 exceeds the acquired share of fair-value net assets (2,400,000).', 'goodwill-zero'),
  ('Yes; CHF 1,000,000', 'Ignores the hidden reserves: 3,000,000 − 80% × 2,500,000.', 'goodwill-ignore-reserves'),
  ('Yes; CHF 600,000', '3,000,000 − 80% × (2,500,000 + 500,000) = 600,000.', None),
  ('Yes; CHF 500,000', 'Subtracts 100% of the book equity (3,000,000 − 2,500,000) and ignores the hidden reserves.', 'goodwill-wrong-share')], 'c',
 'Goodwill = purchase price − parent’s share of the fair value of net assets. The intragroup loan does not change Tochter’s net assets.', scenario=MUTTER, ev='acquisition',
 calc=f'Fair value of net assets = 2,500,000 + 500,000 = 3,000,000; 80% = 2,400,000; goodwill = 3,000,000 − 2,400,000 = {chf(gw)}.',
 check={'f': 'p - s*(e + h)', 'v': {'p': pr, 's': sh, 'e': eq, 'h': hr}, 'x': gw})

add('1-07', '7', CS, 'Acquisition accounting', 2, 'What is the amount of the “Non-Controlling Interest” in Mutter AG’s consolidated balance sheet on 31.12.2025?',
 [('There is no non-controlling interest, since Mutter AG has control.', 'Control does not remove the outside shareholders: 20% of Tochter belongs to them.', 'nci-none'),
  ('CHF 500,000', 'Ignores the hidden reserves: 20% × 2,500,000.', 'nci-ignore-reserves'),
  ('CHF 750,000', 'Uses 25% instead of the 20% minority share.', 'nci-parent-share'),
  ('CHF 600,000', '20% × 3,000,000 = 600,000.', None)], 'd',
 'NCI = minority share × fair value of net assets.', scenario=MUTTER, ev='acquisition', calc=f'20% × (2,500,000 + 500,000) = {chf(nci)}.',
 check={'f': '(1 - s)*(e + h)', 'v': {'s': sh, 'e': eq, 'h': hr}, 'x': nci})

teq = 6_000_000 + nci
add('1-08', '8', CS, 'Acquisition accounting', 2, 'What is the total equity (including non-controlling interest) in Mutter AG’s consolidated balance sheet on 31.12.2025?',
 [('CHF 6,600,000', 'Mutter’s equity 6,000,000 + NCI 600,000 = 6,600,000.', None),
  ('CHF 6,500,000', 'Uses an NCI without the hidden reserves (500,000).', 'nci-ignore-reserves'),
  ('CHF 6,000,000', 'Leaves out the non-controlling interest.', 'parent-equity-includes-nci'),
  ('CHF 8,500,000', 'Adds Tochter’s equity, which is eliminated at acquisition.', 'equity-add-subsidiary')], 'a',
 'At acquisition, the subsidiary’s equity is eliminated. Group equity = parent equity + NCI.', scenario=MUTTER, ev='acquisition',
 calc=f'6,000,000 + 600,000 = {chf(teq)}.', check={'f': 'm + (1 - s)*(e + h)', 'v': {'m': 6_000_000, 's': sh, 'e': eq, 'h': hr}, 'x': teq})

ta = 10_000_000 - pr - 400_000 + 4_000_000 + hr + gw
add('1-09', '9', CS, 'Acquisition accounting', 2, 'What are the total assets in Mutter AG’s consolidated balance sheet on 31.12.2025?',
 [('CHF 11,700,000', '10,000,000 − 3,000,000 − 400,000 + 4,000,000 + 500,000 + 600,000 = 11,700,000.', None),
  ('CHF 14,000,000', 'Adds both balance sheets without any elimination.', 'consolidation-parent-only'),
  ('CHF 12,100,000', 'Does not eliminate the intragroup loan of 400,000.', 'intragroup-not-eliminated'),
  ('CHF 11,100,000', 'Leaves out goodwill of 600,000.', 'goodwill-zero')], 'a',
 'Consolidated assets = parent assets − investment − intragroup receivable + subsidiary assets + hidden reserves + goodwill.', scenario=MUTTER, ev='acquisition',
 calc='Mutter 10,000,000 − investment 3,000,000 − loan 400,000 + Tochter 4,000,000 + hidden reserves 500,000 + goodwill 600,000 = 11,700,000. '
      'Check: debt 3,000,000 + AP 2,100,000 + equity 6,000,000 + NCI 600,000 = 11,700,000.',
 check={'f': 'a - p - l + b + h + p - s*(e + h)', 'v': {'a': 10_000_000, 'p': pr, 'l': 400_000, 'b': 4_000_000, 'h': hr, 's': sh, 'e': eq}, 'x': ta})

# ---------- Topic 2: Selected Topics in Accounting ----------
add('1-10', '10', FR, 'Financial instruments', 1, 'Under IFRS 9, a bond investment whose cash flows are solely payments of principal and interest and which is held in a “hold to collect” business model is measured at:',
 [('Fair value through profit or loss (FVTPL)', 'FVTPL is the residual category, e.g. for trading assets.', 'ifrs9-classification'),
  ('Amortised cost', 'SPPI cash flows + hold to collect → amortised cost.', None),
  ('The lower of cost or market', 'That is not an IFRS 9 measurement category.', 'ifrs9-classification'),
  ('Fair value through other comprehensive income (FVOCI)', 'FVOCI is for “hold to collect and sell”.', 'ifrs9-classification')], 'b',
 'IFRS 9: SPPI cash flows held to collect → amortised cost; held to collect and sell → FVOCI; otherwise FVTPL.', ev='pe2-ifrs9')

add('1-11', '11', FR, 'Financial instruments', 1, 'If a bond’s coupon rate is higher than the market interest rate at issuance, the bond is issued at a premium, and under the effective interest method its carrying amount decreases over the term towards the face value.',
 [('True', 'Coupon above market rate → premium; the premium is amortised, so the carrying amount falls to face value.', None),
  ('False', 'The statement is correct: a premium bond’s carrying amount declines towards face value.', 'bond-amortisation-direction')], 'a',
 'A coupon above the market rate makes the bond worth more than face value. Interest expense (market rate × carrying amount) is below the coupon, so the carrying amount falls towards face value.', ev='pe2-ifrs9')

add('1-12', '12', FR, 'Presentation (IFRS 18)', 1, 'Which statement about management-defined performance measures (MPMs) under IFRS 18 is correct?',
 [('MPMs may no longer be disclosed by companies reporting under IFRS', 'IFRS 18 regulates MPMs; it does not ban them.', 'ifrs18-mpm'),
  ('MPMs replace the operating profit subtotal in the income statement', 'Operating profit becomes a required subtotal; MPMs do not replace it.', 'ifrs18-mpm'),
  ('MPMs are only disclosed in the management report and are not audited', 'MPMs move into the notes and are therefore audited.', 'ifrs18-mpm'),
  ('MPMs are disclosed in the notes, reconciled to the most comparable IFRS subtotal, and are subject to audit', 'That is the IFRS 18 requirement.', None)], 'd',
 'IFRS 18 requires MPMs to be disclosed in a single note, reconciled to the most comparable IFRS subtotal, which brings them into the audited financial statements.', ev='pe2-ifrs18')

add('1-13', '13', FR, 'Intangible assets', 1, 'Under IFRS (IAS 38), an internally generated brand may be recognised as an intangible asset in the balance sheet if its value can be estimated reliably by an external brand ranking.',
 [('True', 'IAS 38 prohibits recognising internally generated brands, whatever a ranking says.', 'intangible-recognition'),
  ('False', 'Internally generated brands, mastheads and customer lists may not be recognised.', None)], 'b',
 'IAS 38 explicitly prohibits recognising internally generated brands; only acquired brands are recognised.', ev='pe2-ias38')

vu = D(120_000) / D('1.1') + D(130_000) / D('1.1') ** 2 + D(140_000) / D('1.1') ** 3
loss = 400_000 - max(D(310_000), vu)
add('1-14', '14', FR, 'Impairment', 2, 'A cash-generating unit has a carrying amount of CHF 400,000. Its fair value less costs of disposal is CHF 310,000. Management expects net cash flows of CHF 120,000, CHF 130,000 and CHF 140,000 over the next three years (end of year); the discount rate is 10%. What is the impairment loss? (Choose the answer closest to your result.)',
 [('CHF 78,300', 'Value in use 321,713 > FVLCD 310,000; loss = 400,000 − 321,713 = 78,287.', None),
  ('No impairment loss is recognised.', 'The carrying amount of 400,000 exceeds the recoverable amount of about 321,700.', 'impairment-no-loss'),
  ('CHF 90,000', 'Uses fair value less costs of disposal, but value in use is higher.', 'impairment-fvlcd-only'),
  ('CHF 10,000', 'Uses undiscounted cash flows (390,000) as value in use.', 'impairment-undiscounted')], 'a',
 'Recoverable amount = max(FVLCD, value in use). Value in use is the present value of the future cash flows.', ev='impairment',
 calc='VIU = 120,000 / 1.1 + 130,000 / 1.1² + 140,000 / 1.1³ = 109,091 + 107,438 + 105,184 = 321,713. Loss = 400,000 − 321,713 = 78,287 ≈ 78,300.',
 check={'f': 'c - max(f, a/1.1 + b/1.1**2 + d/1.1**3)', 'v': {'c': 400_000, 'f': 310_000, 'a': 120_000, 'b': 130_000, 'd': 140_000}, 'x': loss, 'dp': -2})

SIGMA = ('On 1st January 2025, Sigma AG leases a fleet of delivery vans. The lease runs for 5 years, with annual payments of CHF 20,000 due every 31st December. '
         'The interest rate implicit in the lease is 6% p.a. The right-of-use asset is depreciated on a straight-line basis over the lease term. Sigma AG reports under IFRS. '
         'Use two decimal places during calculations and choose the answer closest to your result.')
p, i = 20_000, D('0.06')
pv = p * (1 - (1 + i) ** -5) / i
add('1-15', '15', FR, 'Leases', 2, 'At what amount are the lease liability and the right-of-use asset initially recognised on 1.1.2025?',
 [('CHF 74,726', 'Does not match 20,000 × 4.21236 (annuity factor 6%, 5 years).', 'lease-calculation'),
  ('CHF 89,302', 'This is the liability at 31.12.2025 before the first payment (PV × 1.06).', 'lease-wrong-year'),
  ('CHF 84,247', '20,000 × 4.21236 = 84,247.27.', None),
  ('CHF 100,000', 'The undiscounted sum of the payments; IFRS 16 uses the present value.', 'lease-undiscounted')], 'c',
 'Lease liability and right-of-use asset start at the present value of the lease payments.', scenario=SIGMA, ev='lease',
 calc='PV = 20,000 × (1 − 1.06⁻⁵) / 0.06 = 20,000 × 4.21236 = 84,247.27.',
 check={'f': 'p*(1 - (1 + i)**-5)/i', 'v': {'p': p, 'i': i}, 'x': pv})

bal = pv * (1 + i) - p
add('1-16', '16', FR, 'Leases', 3, 'What is the carrying amount of the lease liability on 31.12.2025?',
 [('CHF 80,000', 'Deducts one payment from the undiscounted 100,000.', 'lease-undiscounted'),
  ('CHF 67,398', 'This is the right-of-use asset after one year (84,247 × 4/5).', 'lease-liability-as-asset'),
  ('CHF 69,302', '84,247.27 + interest 5,054.84 − payment 20,000 = 69,302.11.', None),
  ('CHF 64,247', 'Deducts the whole payment as repayment and forgets the interest of 5,054.84.', 'lease-payment-split')], 'c',
 'Closing liability = opening liability + interest − payment.', scenario=SIGMA, ev='lease',
 calc='Interest 2025 = 84,247.27 × 6% = 5,054.84. Repayment = 20,000 − 5,054.84 = 14,945.16. Liability = 84,247.27 − 14,945.16 = 69,302.11.',
 check={'f': 'p*(1 - (1 + i)**-5)/i*(1 + i) - p', 'v': {'p': p, 'i': i}, 'x': bal})

add('1-17', '17', FR, 'Leases', 1, 'Under IFRS 16, a lessee may choose not to recognise a right-of-use asset and lease liability for short-term leases (12 months or less) and leases of low-value assets.',
 [('True', 'IFRS 16 offers these two recognition exemptions.', None),
  ('False', 'IFRS 16 does allow the exemptions for short-term and low-value leases.', 'lease-off-balance-sheet')], 'a',
 'IFRS 16 lets lessees expense short-term (≤ 12 months) and low-value leases instead of recognising them on the balance sheet.', ev='lease')

dt = 500_000 * D('0.18')
add('1-18', '18', FR, 'Deferred taxes', 2, 'In its IFRS financial statements, Tech AG capitalises development costs of CHF 500,000 as an intangible asset. For tax purposes, these costs were fully deducted as an expense in the same year. The tax rate is 18%. Which statement is correct?',
 [('Temporary difference; deferred tax asset of CHF 90,000', 'Direction reversed: an asset above its tax value gives a deferred tax liability.', 'tax-direction'),
  ('Temporary difference; deferred tax liability of CHF 90,000', 'Asset: group value 500,000 > tax value 0 → taxable difference → DTL of 500,000 × 18%.', None),
  ('Permanent difference; no deferred taxes', 'The asset is amortised later in the IFRS accounts, so the difference reverses: it is temporary.', 'tax-permanent-vs-temporary'),
  ('Temporary difference; deferred tax liability of CHF 500,000', 'Forgets the tax rate.', 'tax-rate-omitted')], 'b',
 'An asset with a higher group value than tax value creates a taxable temporary difference and a deferred tax liability.', ev='tax',
 calc='(500,000 − 0) × 18% = 90,000 deferred tax liability.', check={'f': 'b*t', 'v': {'b': 500_000, 't': D('0.18')}, 'x': dt, 'same': 'a'})

add('1-19', '19', FR, 'Pensions', 1, 'The defined benefit obligation of a pension plan amounts to CHF 12.0 million; the fair value of the plan assets is CHF 10.5 million. What does the company report in its IFRS balance sheet?',
 [('A net defined benefit asset of CHF 1.5 million', 'Direction reversed: the obligation exceeds the plan assets, so the plan is underfunded.', 'pension-net-position'),
  ('A liability of CHF 12.0 million', 'The plan assets are netted against the obligation.', 'pension-net-position'),
  ('A liability of CHF 22.5 million', 'Adds the plan assets instead of deducting them.', 'pension-net-position'),
  ('A net defined benefit liability of CHF 1.5 million', '12.0 − 10.5 = 1.5 million underfunding.', None)], 'd',
 'The balance sheet shows the net position: DBO − fair value of plan assets. Underfunding → net defined benefit liability.', ev='pensions',
 calc='12.0 − 10.5 = 1.5 million net defined benefit liability.', check={'f': 'o - a', 'v': {'o': D('12.0'), 'a': D('10.5')}, 'x': D('1.5'), 'dp': 1, 'unit': 'MCHF', 'same': 'a'})

# ---------- Topic 3: Auditing ----------
add('1-20', '20', AU, 'Audit market', 1, 'The collapse of which audit firm (following the Enron scandal in 2001/2002) reduced the “Big Five” to the “Big Four”?',
 [('Arthur Andersen', 'Arthur Andersen was Enron’s auditor and collapsed in 2002.', None),
  ('BDO', 'BDO was never part of the Big Five.', 'audit-market'),
  ('Price Waterhouse', 'Price Waterhouse merged with Coopers & Lybrand into PwC in 1998.', 'audit-market'),
  ('Grant Thornton', 'Grant Thornton was never part of the Big Five.', 'audit-market')], 'a',
 'Arthur Andersen was convicted in connection with Enron (later overturned) and collapsed, leaving the Big Four.', ev='audit')

add('1-21', '21', AU, 'Independence', 1, 'Who elects the statutory auditor of a Swiss stock corporation (AG)?',
 [('The board of directors', 'The board proposes the auditor, but cannot appoint the body that checks its own work.', 'auditor-appointment'),
  ('The audit committee', 'The audit committee may prepare the proposal, but does not elect the auditor.', 'auditor-appointment'),
  ('The general meeting of shareholders', 'The general meeting elects the statutory auditor.', None),
  ('FINMA', 'FINMA supervises financial institutions; it does not elect auditors of an AG.', 'auditor-appointment')], 'c',
 'Under Swiss company law, the general meeting of shareholders elects the statutory auditor.', ev='legal')

add('1-22', '22', AU, 'Audit scope', 2, 'Which of the following Swiss companies is subject to a limited audit (assume no opting-out)?',
 [('Company A: shares listed on SIX, 50 FTE', 'Listed companies always need an ordinary audit, whatever their size.', 'audit-scope-thresholds'),
  ('Company B: total assets CHF 25 m, revenue CHF 30 m, 300 FTE in 2024 and in 2025', 'B exceeds two thresholds (assets, FTE) in both years → ordinary audit.', 'audit-scope-thresholds'),
  ('Company D: bonds outstanding, total assets CHF 5 m, 30 FTE', 'Companies with bonds outstanding are public companies and need an ordinary audit.', 'audit-scope-thresholds'),
  ('Company C: total assets CHF 18 m, revenue CHF 45 m, 260 FTE in 2024; total assets CHF 19 m, revenue CHF 38 m, 240 FTE in 2025', 'C exceeds two thresholds only in 2024, not in two consecutive years → limited audit.', None)], 'd',
 'Ordinary audit for listed companies, companies with bonds outstanding, and companies exceeding 2 of 3 thresholds (total assets > CHF 20 m, revenue > CHF 40 m, > 250 FTE) in two consecutive years. Otherwise limited audit.', ev='legal')

add('1-23', '23', AU, 'Independence', 1, 'Which of the following is incompatible with auditor independence according to CO Art. 728?',
 [('The audit fee is agreed in advance at market conditions', 'A market-rate fee agreed in advance is normal.', 'auditor-independence'),
  ('The auditor reports significant findings to the audit committee', 'Reporting to the audit committee is part of the auditor’s role.', 'auditor-independence'),
  ('The lead auditor holds a significant shareholding in the audit client', 'A direct financial interest in the client impairs independence.', None),
  ('The auditor attends the general meeting', 'The auditor may attend (and sometimes must); this does not impair independence.', 'auditor-independence')], 'c',
 'CO Art. 728 lists direct or significant indirect participation in the client’s share capital as incompatible with independence.', ev='legal')

add('1-24', '24', AU, 'Audit risk', 1, 'The auditor assesses both inherent risk and control risk as high. To keep the overall audit risk at an acceptable level, the auditor must:',
 [('Issue a qualified opinion', 'A high risk assessment does not decide the opinion; it decides how much work is needed.', 'audit-risk-model'),
  ('Accept a higher detection risk and perform fewer substantive procedures', 'Wrong direction: with high inherent and control risk, detection risk must be lowered.', 'audit-risk-model'),
  ('Rely more on the client’s internal controls', 'Control risk is high, so the controls cannot be relied on.', 'audit-risk-model'),
  ('Reduce the detection risk by performing more (or more extensive) substantive procedures', 'Audit risk = IR × CR × DR; high IR and CR require a low DR.', None)], 'd',
 'Audit risk = inherent risk × control risk × detection risk. With IR and CR high, the auditor lowers detection risk through more substantive work.', ev='audit')

add('1-25', '25', AU, 'Audit procedures', 1, 'Sending confirmation letters to customers primarily provides evidence for which assertion about accounts receivable?',
 [('Existence', 'A customer confirming the balance shows the receivable exists.', None),
  ('Classification', 'Confirmations say little about how a balance is classified.', 'assertions'),
  ('Presentation', 'Presentation is about disclosure, not whether the balance exists.', 'assertions'),
  ('Completeness', 'Confirmations of recorded balances cannot reveal unrecorded receivables.', 'assertions')], 'a',
 'Confirming recorded receivables with customers tests existence (overstatement). Completeness needs tests from source documents to the records.', ev='procedures')

add('1-26', '26', AU, 'Key Audit Matters', 1, 'In Switzerland, the communication of Key Audit Matters (ISA 701) in the audit report is required for:',
 [('All companies subject to a limited audit', 'A limited audit report contains no KAMs.', 'kam-scope'),
  ('No companies; it is voluntary', 'KAMs are required for listed companies.', 'kam-scope'),
  ('All companies subject to an ordinary audit', 'KAMs are required only for listed companies, not every ordinary audit.', 'kam-scope'),
  ('Listed companies', 'KAMs are required in the audit reports of listed companies.', None)], 'd',
 'Key Audit Matters must be communicated for listed companies; other companies may include them voluntarily.', ev='kam')

add('1-27', '27', AU, 'Key Audit Matters', 1, 'Which topics are among the most common Key Audit Matters of Swiss companies?',
 [('Employee satisfaction and CSR ratings', 'These are not audit matters of the financial statements.', 'kam-topics'),
  ('Goodwill (impairment) and revenue recognition', 'Judgement-heavy areas such as goodwill impairment and revenue are the most frequent KAMs.', None),
  ('Office equipment and petty cash', 'These are low-risk, immaterial areas.', 'kam-topics'),
  ('Dividend policy and share buybacks', 'These are capital decisions, not areas of significant audit judgement.', 'kam-topics')], 'b',
 'KAMs are the areas of most significant audit judgement; goodwill impairment and revenue recognition lead the list.', ev='kam')

add('1-28', '28', AU, 'Going concern', 1, 'An unmodified audit opinion without any reference to going concern guarantees that the company will continue its business for at least the next twelve months.',
 [('True', 'An audit gives reasonable, not absolute assurance and cannot guarantee future events.', 'expectation-gap'),
  ('False', 'The opinion is no guarantee of the company’s future survival.', None)], 'b',
 'An audit provides reasonable assurance on the financial statements. It is no guarantee of the company’s future: a typical expectation-gap misunderstanding.', ev='going')

add('1-29', '29', AU, 'Audit opinions', 1, 'The auditor is unable to obtain sufficient appropriate audit evidence on inventory and on the company’s ability to continue as a going concern. The possible effects are material and pervasive. Which opinion is issued?',
 [('Adverse opinion', 'An adverse opinion is for misstatements that are found, not for missing evidence.', 'opinion-type'),
  ('Disclaimer of opinion', 'Missing evidence with possibly material and pervasive effects → disclaimer.', None),
  ('Qualified opinion', 'A qualified opinion fits material but not pervasive effects.', 'opinion-type'),
  ('Unmodified opinion with an emphasis of matter', 'An emphasis of matter cannot replace missing evidence.', 'opinion-type')], 'b',
 'Scope limitation (no sufficient evidence) with possible effects that are material and pervasive → disclaimer of opinion.', ev='opinion')

SEE = ('Seeblick Consulting AG (unlisted) is subject to an Ordinary Audit of its 2025 financial statements. Its earnings have been volatile in recent years and are close to break-even in 2025. '
       'The audit firm uses the following rules of thumb: 5% of EBT, 0.5% of revenue, 1% of total assets or 2% of equity. If EBT is not a meaningful benchmark, the firm uses revenue.\n\n'
       + table(['Key figures 2025 (CHF)', 'Amount'], [['Revenue', '36,000,000'], ['Earnings before Tax (EBT)', '150,000'], ['Total Assets', '50,000,000'], ['Equity', '20,000,000']]))
add('1-30', '30', AU, 'Materiality', 2, 'Which overall materiality should the auditor most likely apply?',
 [('CHF 7,500', '5% of EBT; EBT close to break-even is not a meaningful benchmark.', 'materiality-benchmark'),
  ('CHF 500,000', '1% of total assets; the firm falls back on revenue, not total assets.', 'materiality-benchmark'),
  ('CHF 400,000', '2% of equity; the firm falls back on revenue, not equity.', 'materiality-benchmark'),
  ('CHF 180,000', '0.5% × 36,000,000 = 180,000.', None)], 'd',
 'Volatile earnings close to break-even make EBT unsuitable, so the firm uses revenue.', scenario=SEE, ev='materiality',
 calc='0.5% × 36,000,000 = 180,000.', check={'f': '0.005*r', 'v': {'r': 36_000_000}, 'x': D('0.005') * 36_000_000})

add('1-31', '31', AU, 'Audit opinions', 2, 'During the audit, two misstatements are identified: (i) revenue of CHF 120,000 was recognised in 2025 although the service was only rendered in January 2026, and (ii) inventory is overstated by CHF 40,000. Management corrects misstatement (i), but refuses to correct (ii). Which audit opinion is appropriate?',
 [('Disclaimer of opinion', 'The auditor has the evidence; a disclaimer is for missing evidence.', 'opinion-type'),
  ('Qualified opinion', 'Only 40,000 remains uncorrected, below materiality of 180,000.', 'materiality-aggregation'),
  ('Unmodified opinion', 'The only uncorrected misstatement (40,000) is below materiality (180,000).', None),
  ('Adverse opinion', 'There is no material, let alone pervasive, uncorrected misstatement.', 'opinion-type')], 'c',
 'Misstatement (i) was corrected. The remaining 40,000 is below overall materiality of 180,000, so the statements are not materially misstated.', scenario=SEE, ev='opinion')


# ============================ PART 2 – CONTROLLING ============================
MA, BU, VA, CB, CP = 'Management Accounting', 'Budgeting', 'Variances', 'Capital Budgeting', 'Cost and Performance Management'

TESSIN = table(['Tessin Furniture AG, 2025', 'CHF'],
               [['Beginning inventory of direct materials, Jan 1, 2025', '25,000'], ['Purchases of direct materials', '170,000'],
                ['Ending inventory of direct materials, Dec 31, 2025', '15,000'], ['Direct manufacturing labor', '75,000'], ['Indirect manufacturing labor', '30,000'],
                ['Other manufacturing overhead (plant utilities, depreciation)', '80,000'], ['Sales commissions', '40,000']])
cc = 75_000 + 30_000 + 80_000
add('2-1-1', '1.1', MA, 'Manufacturing cost flows', 2, 'Tessin Furniture AG reported the following for 2025. What are Tessin’s conversion costs for 2025?',
 [('CHF 365,000', 'This is total manufacturing cost (materials used 180,000 + conversion 185,000).', 'conversion-vs-prime'),
  ('CHF 255,000', 'This is prime cost: direct materials 180,000 + direct labor 75,000.', 'conversion-vs-prime'),
  ('CHF 185,000', 'Direct labor 75,000 + manufacturing overhead 110,000 = 185,000.', None),
  ('CHF 225,000', 'Includes sales commissions, which are period costs.', 'period-costs-inventoriable'),
  none_wrong('c')], 'c',
 'Conversion costs = direct manufacturing labor + manufacturing overhead. Materials are prime costs; sales commissions are period costs.', scenario=TESSIN, ev='ma-flow',
 calc='75,000 + 30,000 + 80,000 = 185,000.', check={'f': 'dl + il + oh', 'v': {'dl': 75_000, 'il': 30_000, 'oh': 80_000}, 'x': cc})

add('2-1-2', '1.2', MA, 'Cost concepts', 1, 'Which of the following is a period cost for a manufacturing company?',
 [('Rent of the factory building', 'Factory rent is manufacturing overhead, an inventoriable cost.', 'period-costs-inventoriable'),
  ('Direct materials', 'Direct materials are inventoriable.', 'period-costs-inventoriable'),
  ('Salaries of the sales staff', 'Selling costs are expensed in the period: period costs.', None),
  ('Depreciation of a production machine', 'Production depreciation is manufacturing overhead, an inventoriable cost.', 'period-costs-inventoriable'),
  none_wrong('c')], 'c',
 'Inventoriable costs are all manufacturing costs. Selling and administrative costs are period costs.', ev='ma-costs')

u13 = (360_000 + D(90_000) / D('0.75')) / (120 - 72)
add('2-1-3', '1.3', MA, 'CVP analysis', 2, 'Jura Watches sells a product at CHF 120 per unit. Variable costs are CHF 72 per unit and annual fixed costs are CHF 360,000. The income tax rate is 25%. How many units must Jura sell to achieve a target net income of CHF 90,000?',
 [('9,375 units', 'Uses the after-tax target of 90,000 instead of the pre-tax 120,000.', 'cvp-tax-omitted'),
  ('12,500 units', 'Divides by an after-tax contribution margin (36) and mixes pre- and after-tax figures.', 'cvp-tax-omitted'),
  ('7,500 units', 'This is the breakeven point; the target income is missing.', 'cvp-target-omitted'),
  ('10,000 units', '(360,000 + 120,000) / 48 = 10,000.', None),
  none_wrong('d')], 'd',
 'Convert the target net income to pre-tax: 90,000 / (1 − 25%) = 120,000. Units = (fixed costs + pre-tax target) / contribution margin per unit.', ev='ma-cvp',
 calc='Pre-tax target = 90,000 / 0.75 = 120,000. CM per unit = 120 − 72 = 48. Units = (360,000 + 120,000) / 48 = 10,000.',
 check={'f': '(f + t/(1 - x))/(p - v)', 'v': {'f': 360_000, 't': 90_000, 'x': D('0.25'), 'p': 120, 'v': 72}, 'x': u13, 'unit': 'units'})

ua = 470_000 - 30_000 * D(480_000) / 32_000
add('2-2-1', '2.1', MA, 'Job costing', 2, 'Engadin Machining allocates manufacturing overhead using a budgeted rate based on machine-hours. Budgeted overhead is CHF 480,000 and budgeted machine-hours are 32,000. Actual machine-hours were 30,000 and actual overhead costs were CHF 470,000. What is the over- or underallocated manufacturing overhead?',
 [('CHF 30,000 underallocated', 'Compares allocated overhead with budgeted (480,000) instead of actual overhead.', 'overhead-allocation'),
  ('CHF 20,000 underallocated', 'Allocated 30,000 × 15 = 450,000 < actual 470,000 → 20,000 underallocated.', None),
  ('CHF 10,000 overallocated', 'Compares actual with budgeted overhead instead of allocated overhead.', 'overhead-allocation'),
  ('CHF 20,000 overallocated', 'Right size, wrong direction: actual costs exceed the allocated amount.', 'overhead-allocation'),
  none_wrong('b')], 'b',
 'Allocated overhead = budgeted rate × actual hours. Actual above allocated → underallocated.', ev='ma-job',
 calc='Rate = 480,000 / 32,000 = 15 per MH. Allocated = 30,000 × 15 = 450,000. Actual 470,000 − 450,000 = 20,000 underallocated.',
 check={'f': 'a - h*b/m', 'v': {'a': 470_000, 'h': 30_000, 'b': 480_000, 'm': 32_000}, 'x': ua, 'same': 'd'})

LOTSCH = ('Lötschberg AG produces two products, Classic and Premium, and uses an activity-based costing (ABC) system. The following data apply:\n\n'
          + table(['Activity', 'Overhead costs', 'Activity level'], [['Purchase orders', 'CHF 180,000', '600 orders'], ['Machine setups', 'CHF 300,000', '250 setups'],
                                                                  ['Quality control', 'CHF 120,000', '4,000 inspection-hours'], ['Total', 'CHF 600,000', '']])
          + '\n\n' + table(['', 'Classic', 'Premium'], [['Production units', '20,000', '5,000'], ['Purchase orders', '200', '400'], ['Setups', '50', '200'], ['Inspection-hours', '1,000', '3,000']]))
abc = (400 * D(180_000) / 600 + 200 * D(300_000) / 250 + 3_000 * D(120_000) / 4_000) / 5_000
add('2-2-2', '2.2', MA, 'Activity-based costing', 4, 'Using ABC, what are the estimated overhead costs per unit of Premium?',
 [('CHF 90.00', '(120,000 + 240,000 + 90,000) / 5,000 = 90.00.', None),
  ('CHF 7.50', 'This is Classic’s ABC overhead per unit.', 'abc-wrong-product'),
  ('CHF 72.00', 'Too low: Premium uses 400 × 300 + 200 × 1,200 + 3,000 × 30 = 450,000 of overhead.', 'abc-calculation'),
  ('CHF 24.00', 'Spreads total overhead evenly over all 25,000 units (600,000 / 25,000).', 'abc-plantwide-units'),
  none_wrong('a')], 'a',
 'ABC: one rate per activity, then charge each product by its use of each activity.', scenario=LOTSCH, ev='ma-job',
 calc='Rates: orders 180,000 / 600 = 300; setups 300,000 / 250 = 1,200; inspections 120,000 / 4,000 = 30. '
      'Premium: 400 × 300 + 200 × 1,200 + 3,000 × 30 = 120,000 + 240,000 + 90,000 = 450,000 → 450,000 / 5,000 = 90.00.',
 check={'f': '(a*s/sa + b*m/ma + c*i/ia)/u', 'v': {'a': 400, 's': 180_000, 'sa': 600, 'b': 200, 'm': 300_000, 'ma': 250, 'c': 3_000, 'i': 120_000, 'ia': 4_000, 'u': 5_000}, 'x': abc, 'dp': 2})

tp = 30 + D(600_000) / 20_000 + D('0.16') * 2_500_000 / 20_000
add('2-3-1', '3.1', MA, 'Pricing and target costing', 2, 'Pilatus Pumps has invested CHF 2,500,000 in a production line and targets a return on investment of 16%. It plans to sell 20,000 pumps per year. Variable costs are CHF 30 per pump and fixed costs are CHF 600,000 per year. What is the target price per pump (cost-plus pricing based on full costs)?',
 [('CHF 50.00', 'Leaves out the fixed cost per unit (30).', 'full-cost-omitted'),
  ('CHF 60.00', 'This is the full cost per unit, without the target return.', 'markup-omitted'),
  ('CHF 80.00', 'Full cost 60 + target return 400,000 / 20,000 = 20 → 80.', None),
  ('CHF 69.60', 'Applies 16% to the cost per unit instead of to the investment.', 'markup-roi-confusion'),
  none_wrong('c')], 'c',
 'Target price = full cost per unit + target operating income per unit, with target operating income = ROI × investment.', ev='ma-price',
 calc='Full cost = 30 + 600,000 / 20,000 = 60. Target income = 16% × 2,500,000 = 400,000 → 20 per pump. Price = 80.',
 check={'f': 'v + f/q + r*i/q', 'v': {'v': 30, 'f': 600_000, 'q': 20_000, 'r': D('0.16'), 'i': 2_500_000}, 'x': tp, 'dp': 2})

red = 150 - 160 * D('0.8')
add('2-3-2', '3.2', MA, 'Pricing and target costing', 2, 'Aare Audio currently produces a speaker at a full cost of CHF 150 per unit. Due to competition, the market price drops to CHF 160. Management targets an operating income of 20% of the selling price. By how much must the full cost per unit be reduced?',
 [('CHF 16.67', 'Treats 20% as a markup on cost (160 / 1.2 = 133.33) instead of a margin on the price.', 'markup-on-price'),
  ('CHF 22.00', 'Target cost = 160 × 0.8 = 128; reduction = 150 − 128 = 22.', None),
  ('CHF 10.00', 'This is the gap between price and current cost, not the needed cost reduction.', 'target-margin-absolute'),
  ('CHF 32.00', 'This is the target operating income per unit (20% × 160).', 'target-margin-absolute'),
  none_wrong('b')], 'b',
 'Target cost = target price × (1 − target margin); the cost reduction is the current cost minus the target cost.', ev='ma-price',
 calc='Target cost = 160 × (1 − 20%) = 128. Reduction = 150 − 128 = 22.', check={'f': 'c - p*(1 - m)', 'v': {'c': 150, 'p': 160, 'm': D('0.2')}, 'x': red, 'dp': 2})

lab = (30_000 + D('0.2') * 40_000 - 6_000) * D('0.75') * 40
add('2-4-1', '4.1', BU, 'Direct labor budget', 3, 'Emmental Dairy expects to sell 30,000 units in Q1 and 40,000 units in Q2. The targeted ending finished goods inventory of each quarter is 20% of the next quarter’s sales; the beginning inventory of Q1 is 6,000 units. Each unit requires 0.75 direct manufacturing labor-hours at CHF 40 per hour. What is the budgeted direct manufacturing labor cost for Q1?',
 [('CHF 1,280,000', 'Forgets the 0.75 hours per unit: 32,000 × 40.', 'labor-budget-hours'),
  ('CHF 1,140,000', 'Too high: Q1 production is 32,000 units × 0.75 h × 40.', 'labor-budget-hours'),
  ('CHF 900,000', 'Uses Q1 sales (30,000) instead of Q1 production (32,000).', 'purchases-production-base'),
  ('CHF 960,000', '32,000 units × 0.75 h × CHF 40 = 960,000.', None),
  none_wrong('d')], 'd',
 'Production = sales + ending inventory − beginning inventory; labor cost = production × hours per unit × wage rate.', ev='budget',
 calc='Q1 production = 30,000 + 20% × 40,000 − 6,000 = 32,000 units. Hours = 24,000. Cost = 24,000 × 40 = 960,000.',
 check={'f': '(s + e*n - b)*h*w', 'v': {'s': 30_000, 'e': D('0.2'), 'n': 40_000, 'b': 6_000, 'h': D('0.75'), 'w': 40}, 'x': lab})

pay = D('0.3') * 90_000 * D('0.98') + D('0.7') * 120_000
GRISCH = table(['', 'October', 'November', 'December'], [['Budgeted purchases (CHF)', '100,000', '120,000', '90,000']])
add('2-4-2', '4.2', BU, 'Cash disbursements', 2, 'Grischun Trading pays 30% of its purchases in the month of purchase (taking a 2% cash discount) and the remaining 70% in the following month. What are the budgeted cash payments for purchases in December?',
 [('CHF 99,000', 'Does not match 26,460 + 84,000.', 'cash-disbursement-timing'),
  ('CHF 111,000', 'Forgets the 2% cash discount: 27,000 + 84,000.', 'cash-discount-omitted'),
  ('CHF 90,000', 'This is December’s purchases, not December’s payments.', 'cash-disbursement-timing'),
  ('CHF 108,000', 'Does not match 26,460 + 84,000.', 'cash-disbursement-timing'),
  none_right('December = 30% × 90,000 × 0.98 + 70% × 120,000 = 26,460 + 84,000 = 110,460, which is not listed.')], 'e',
 'Payments in a month = 30% of this month’s purchases less the 2% discount + 70% of last month’s purchases.', scenario=GRISCH, ev='budget',
 calc='30% × 90,000 × 0.98 = 26,460; 70% × 120,000 = 84,000; total 110,460.',
 check={'f': 'a*d*(1 - c) + b*n', 'v': {'a': D('0.3'), 'd': 90_000, 'c': D('0.02'), 'b': D('0.7'), 'n': 120_000}, 'x': pay})

add('2-5-1', '5.1', VA, 'Flexible-budget variance', 2, 'Toggenburg Textiles budgeted a selling price of CHF 40 per unit and sales of 10,000 units. Actually, it sold 9,500 units at CHF 42 per unit. What is the selling-price variance?',
 [('CHF 20,000 unfavorable', 'Uses budgeted units (10,000) and the wrong direction.', 'variance-direction'),
  ('CHF 20,000 favorable', 'Uses budgeted units (10,000); the price variance uses actual units sold.', 'variance-quantity-base'),
  ('CHF 19,000 unfavorable', 'Right size, wrong direction: a higher price than budgeted is favorable.', 'variance-direction'),
  ('CHF 21,000 favorable', 'Does not match (42 − 40) × 9,500.', 'variance-quantity-base'),
  none_right('(42 − 40) × 9,500 = 19,000 favorable, which is not listed.')], 'e',
 'Selling-price variance = (actual price − budgeted price) × actual units sold.', ev='variance',
 calc='(42 − 40) × 9,500 = 19,000 F. No option shows 19,000 favorable.')

lev = (12_600 - 8_000 * D('1.5')) * 32
add('2-5-2', '5.2', VA, 'Direct labor price variance', 3, 'Zug Instruments has a standard of 1.5 direct labor-hours per unit at CHF 32 per hour. In April, it produced 8,000 units using 12,600 labor-hours; total direct labor costs were CHF 409,500. What is the direct labor efficiency variance?',
 [('CHF 25,500 unfavorable', 'This is the total flexible-budget variance (409,500 − 384,000).', 'variance-type'),
  ('CHF 19,200 unfavorable', '(12,600 − 12,000) × 32 = 19,200 U.', None),
  ('CHF 19,500 unfavorable', 'Uses the actual rate of 32.50 instead of the standard rate of 32.', 'efficiency-actual-price'),
  ('CHF 6,300 unfavorable', 'This is the price (rate) variance: (32.50 − 32) × 12,600.', 'variance-type'),
  none_wrong('b')], 'b',
 'Efficiency variance = (actual hours − standard hours for actual output) × standard rate.', ev='variance',
 calc='Standard hours = 8,000 × 1.5 = 12,000. (12,600 − 12,000) × 32 = 19,200 U. (Actual rate = 409,500 / 12,600 = 32.50; price variance = 6,300 U.)',
 check={'f': '(a - u*s)*r', 'v': {'a': 12_600, 'u': 8_000, 's': D('1.5'), 'r': 32}, 'x': lev})

add('2-5-3', '5.3', VA, 'Flexible budgets', 1, 'A flexible budget is based on:',
 [('Budgeted output and actual prices', 'A flexible budget adjusts the output, not the prices.', 'flexible-budget-basis'),
  ('Actual output and actual prices', 'That is the actual result.', 'flexible-budget-basis'),
  ('Actual output and budgeted prices / standard costs', 'The flexible budget restates the budget for the actual output.', None),
  ('Budgeted output and budgeted prices', 'That is the static budget.', 'flexible-budget-basis'),
  none_wrong('c')], 'c',
 'Flexible budget = actual output × budgeted prices and standard costs.', ev='variance')

pvv = 360_000 - 11_000 * 2 * D(360_000) / (12_000 * 2)
add('2-6-1', '6.1', VA, 'Fixed-overhead variances', 3, 'Wallis Valves budgets fixed manufacturing overhead of CHF 360,000 for a denominator level of 12,000 units; fixed overhead is allocated at 2 machine-hours per unit. Actual output was 11,000 units and actual fixed overhead costs were CHF 372,000. What is the production-volume variance?',
 [('CHF 12,000 unfavorable', 'This is the spending variance (372,000 − 360,000).', 'variance-type'),
  ('CHF 30,000 unfavorable', '360,000 − 11,000 × 2 × 15 = 30,000 U.', None),
  ('CHF 30,000 favorable', 'Right size, wrong direction: output below the denominator level is unfavorable.', 'variance-direction'),
  ('CHF 42,000 unfavorable', 'This is the total underallocated fixed overhead (spending + volume).', 'variance-type'),
  none_wrong('b')], 'b',
 'Production-volume variance = budgeted fixed overhead − allocated fixed overhead (rate × standard hours for actual output).', ev='variance',
 calc='Rate = 360,000 / 24,000 MH = 15 per MH. Allocated = 11,000 × 2 × 15 = 330,000. 360,000 − 330,000 = 30,000 U.',
 check={'f': 'b - u*h*b/(d*h)', 'v': {'b': 360_000, 'u': 11_000, 'h': 2, 'd': 12_000}, 'x': pvv, 'same': 'c'})

add('2-6-2', '6.2', VA, 'Fixed-overhead variances', 1, 'An unfavorable production-volume variance indicates that:',
 [('Actual fixed overhead costs exceeded budgeted fixed overhead costs', 'That is an unfavorable spending variance.', 'fixed-overhead-variances'),
  ('Actual output was lower than the denominator level used to calculate the allocation rate', 'Less output → less fixed overhead allocated than budgeted.', None),
  ('Workers used more machine-hours than budgeted', 'That is a variable overhead efficiency variance.', 'fixed-overhead-variances'),
  ('The variable overhead rate per hour increased', 'That is a variable overhead spending variance.', 'fixed-overhead-variances'),
  none_wrong('b')], 'b',
 'The production-volume variance arises when actual output differs from the denominator level; below it, fixed overhead is underallocated (unfavorable).', ev='variance')

MATT = ('Matterhorn Logistics considers buying a sorting machine for CHF 150,000. It is expected to generate net cash inflows of CHF 50,000 at the end of each year for 4 years, '
        'with no disposal value and no taxes. The required rate of return is 10%; the present value annuity factor (4 years, 10%) is 3.170.')
npv = 50_000 * D('3.170') - 150_000
add('2-7-1', '7.1', CB, 'Net present value', 3, 'What is the net present value?',
 [('CHF 8,500', '50,000 × 3.170 − 150,000 = 8,500.', None),
  ('CHF −8,500', 'Right size, wrong sign: the PV of the inflows (158,500) exceeds the outlay.', 'npv-sign'),
  ('CHF 25,657', 'Does not match 158,500 − 150,000.', 'npv-calculation'),
  ('CHF 50,000', 'Undiscounted: 200,000 − 150,000.', 'npv-no-discounting'),
  none_wrong('a')], 'a',
 'NPV = annual inflow × annuity factor − initial investment.', scenario=MATT, ev='capital',
 calc='50,000 × 3.170 = 158,500. NPV = 158,500 − 150,000 = 8,500.',
 check={'f': 'c*a - i', 'v': {'c': 50_000, 'a': D('3.170'), 'i': 150_000}, 'x': npv, 'same': 'b'})

add('2-7-2', '7.2', CB, 'AARR and IRR', 2, 'In which range does the internal rate of return (IRR) lie?',
 [('Below 10%', 'NPV at 10% is positive, so the IRR is above 10%.', 'irr-concept'),
  ('Between 10% and 12%', 'At 12% the NPV is still positive (50,000 × 3.037 = 151,870 > 150,000).', 'irr-calculation'),
  ('Between 12% and 14%', 'Positive NPV at 12%, negative at 14% (50,000 × 2.914 = 145,700): IRR ≈ 12.6%.', None),
  ('Above 14%', 'At 14% the NPV is already negative.', 'irr-calculation'),
  none_wrong('c')], 'c',
 'The IRR is the rate where NPV = 0. Test rates: NPV > 0 at 12%, NPV < 0 at 14%, so the IRR lies in between (about 12.6%).', scenario=MATT, ev='capital',
 calc='Annuity factor 12%, 4 years ≈ 3.037 → PV 151,870 > 150,000. Factor 14% ≈ 2.914 → PV 145,700 < 150,000. IRR ≈ 12.6%.')

aarr = 100 * (50_000 - D(150_000) / 4) / 150_000
add('2-7-3', '7.3', CB, 'Accounting rate of return', 2, 'Compute the accrual accounting rate of return (AARR) based on the net initial investment (straight-line depreciation). (Round to one decimal.)',
 [('25.0%', 'Uses depreciation (37,500) instead of net income.', 'aarr-calculation'),
  ('16.7%', 'Based on the average investment of 75,000, not the net initial investment.', 'aarr-average-investment'),
  ('33.3%', 'Uses the cash inflow (50,000) and ignores depreciation.', 'aarr-cash-flow'),
  ('8.3%', '(50,000 − 37,500) / 150,000 = 8.3%.', None),
  none_wrong('d')], 'd',
 'AARR = average annual net income / net initial investment, where net income = cash inflow − depreciation.', scenario=MATT, ev='capital',
 calc='Depreciation = 150,000 / 4 = 37,500. Net income = 50,000 − 37,500 = 12,500. AARR = 12,500 / 150,000 = 8.3%.',
 check={'f': '100*(c - i/4)/i', 'v': {'c': 50_000, 'i': 150_000}, 'x': aarr, 'dp': 1, 'unit': 'percent'})

add('2-7-4', '7.4', CB, 'Payback period', 1, 'Which capital budgeting method ignores the time value of money?',
 [('Internal rate of return method', 'The IRR is a discounted cash flow method.', 'payback-concept'),
  ('Payback method', 'The (static) payback adds up undiscounted cash flows.', None),
  ('Net present value method', 'NPV discounts all cash flows.', 'payback-concept'),
  ('Discounted payback method', 'Discounted payback uses discounted cash flows, as the name says.', 'payback-concept'),
  none_wrong('b')], 'b',
 'The static payback method uses undiscounted cash flows and ignores the time value of money (and cash flows after the payback).', ev='capital')

add('2-8-1', '8.1', CP, 'Balanced scorecard perspectives', 1, 'Which of the following measures belongs to the customer perspective of the balanced scorecard?',
 [('Manufacturing yield', 'Manufacturing yield is an internal business process measure.', 'bsc-perspective'),
  ('Employee turnover rate', 'Employee turnover belongs to the learning and growth perspective.', 'bsc-perspective'),
  ('Market share in target segments', 'Market share is a customer perspective measure.', None),
  ('Return on capital employed', 'ROCE belongs to the financial perspective.', 'bsc-perspective'),
  none_wrong('c')], 'c',
 'Customer perspective: market share, customer acquisition, retention and satisfaction.', ev='cpm')

add('2-8-2', '8.2', CP, 'Balanced scorecard perspectives', 1, 'In a strategy map, which sequence correctly describes the typical cause-and-effect chain?',
 [('Internal Business Process → Learning & Growth → Financial → Customer', 'Learning & growth is the foundation, and financial results come last.', 'bsc-cause-effect'),
  ('Financial → Customer → Internal Business Process → Learning & Growth', 'This is the top-down reading order, not the cause-and-effect chain.', 'bsc-cause-effect'),
  ('Customer → Financial → Learning & Growth → Internal Business Process', 'Learning & growth drives processes, not the other way round.', 'bsc-cause-effect'),
  ('Learning & Growth → Internal Business Process → Customer → Financial', 'Skills and systems improve processes, which win customers, which drive financial results.', None),
  none_wrong('d')], 'd',
 'Strategy maps run bottom-up: learning & growth → internal processes → customer → financial.', ev='cpm')

add('2-9-1', '9.1', CP, 'Residual income', 2, 'The Outdoor division currently has invested capital of CHF 5,000,000 and an EBIT of CHF 800,000 (ROI = 16%). The required rate of return is 12%. The division manager considers a new project with an investment of CHF 1,000,000 and an annual EBIT of CHF 140,000. Which statement is correct?',
 [('Accepting the project increases the division’s ROI, but reduces its residual income by CHF 20,000', 'Both effects are reversed: ROI falls and residual income rises.', 'roi-vs-ri'),
  ('Accepting the project increases both the division’s ROI and its residual income', 'The project’s ROI (14%) is below 16%, so the division’s ROI falls.', 'roi-vs-ri'),
  ('Accepting the project reduces the division’s ROI to about 15.7%, but increases its residual income by CHF 20,000', 'ROI = 940,000 / 6,000,000 = 15.7%; project RI = 140,000 − 12% × 1,000,000 = +20,000.', None),
  ('Accepting the project reduces both the division’s ROI and its residual income', 'Residual income rises, because the project earns more than 12%.', 'roi-vs-ri'),
  none_wrong('c')], 'c',
 'A project earning above the required rate (14% > 12%) raises residual income, but lowers ROI when it is below the current ROI (14% < 16%), the classic ROI underinvestment problem.', ev='cpm',
 calc='New ROI = (800,000 + 140,000) / (5,000,000 + 1,000,000) = 15.7%. Project RI = 140,000 − 120,000 = +20,000.')

RIGI = ('Rigi Group has two sources of funds: long-term debt with a market and book value of CHF 4,000,000 at an interest rate of 5%, and equity with a market value of CHF 6,000,000 '
        '(book value CHF 3,000,000). The cost of equity is 11% and the tax rate is 20%. The divisions report the following:\n\n'
        + table(['Division', 'EBIT', 'Total assets', 'Current liabilities'], [['Industrial', 'CHF 1,000,000', 'CHF 6,500,000', 'CHF 500,000'], ['Consumer', 'CHF 700,000', 'CHF 4,000,000', 'CHF 300,000']]))
wacc = (4_000_000 * D('0.05') * D('0.8') + 6_000_000 * D('0.11')) / 10_000_000
eva = 1_000_000 * D('0.8') - wacc * (6_500_000 - 500_000)
add('2-9-2', '9.2', CP, 'Economic value added', 3, 'What is the EVA of the Industrial division? (Round interim results to four decimals.)',
 [('CHF 380,000', 'Weights the WACC with the book value of equity (7.0%) instead of market values.', 'wacc-book-values'),
  ('CHF 267,000', 'Charges capital on total assets (6,500,000) instead of total assets minus current liabilities.', 'eva-capital-base'),
  ('CHF 508,000', 'Uses pre-tax EBIT: 1,000,000 − 492,000.', 'eva-pretax'),
  ('CHF 308,000', '800,000 − 8.2% × 6,000,000 = 308,000.', None),
  none_wrong('d')], 'd',
 'EVA = EBIT × (1 − t) − WACC × (total assets − current liabilities), with the WACC weighted at market values.', scenario=RIGI, ev='cpm',
 calc='WACC = (4 m × 5% × (1 − 20%) + 6 m × 11%) / 10 m = (160,000 + 660,000) / 10,000,000 = 8.2%. EVA = 1,000,000 × 0.8 − 8.2% × 6,000,000 = 800,000 − 492,000 = 308,000.',
 check={'f': 'e*(1 - t) - (a - l)*(d*rd*(1 - t) + q*re)/(d + q)', 'v': {'e': 1_000_000, 't': D('0.2'), 'a': 6_500_000, 'l': 500_000, 'd': 4_000_000, 'rd': D('0.05'), 'q': 6_000_000, 're': D('0.11')}, 'x': eva})
