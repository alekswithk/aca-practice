"""Questions from the unofficial ACA practice exam (ACA_Probeklausur.pdf, solutions in ACA_Probeklausur_Loesungen.pdf).

51 questions: Part 1 (Accounting & Auditing, 29) and Part 2 (Controlling, 22), wording and answer key as in the PDFs.
They join the practice bank (set = "bank"), sorted into the tool's topics, and are marked AI-generated.
Every numeric answer is recomputed here and again in validate_bank.py.
"""
from ai_common import add as _add, EV, D, r, chf, n, table, none_wrong, none_right

EV['pe-ifrs18'] = {'path': 'ACA_Probeklausur_Loesungen.pdf', 'section': 'Part 1, question 15: IFRS 18 categories'}
EV['pe-bonds'] = {'path': 'ACA_Probeklausur_Loesungen.pdf', 'section': 'Part 1, question 16: effective interest method'}
GROUP = 'ACA practice exam (unofficial)'
LEVEL = {1: 'Easy', 2: 'Medium', 3: 'Hard', 4: 'Hard'}


def add(ident, number, topic, subtopic, marks, prompt, opts, key, explanation, **k):
 q = _add('pe-' + ident, topic, subtopic, LEVEL[marks], f'({marks} mark{"s" if marks > 1 else ""}) {prompt}', opts, key, explanation,
          group=GROUP, **k)
 part = 'Part 1 (Accounting & Auditing)' if ident.startswith('1-') else 'Part 2 (Controlling)'
 q['evidence'].append({'path': 'ACA_Probeklausur_Loesungen.pdf', 'section': f'{part}, question {number}'})
 return q


# ======================= PART 1 – ACCOUNTING & AUDITING =======================
CS, FR, AU = 'Consolidated Statements', 'Financial Reporting', 'Auditing'

add('1-01', '1', CS, 'Accounting frameworks', 1, 'Which of the following accounting standards is generally considered rule-based with extensive guidance?',
 [('Swiss Code of Obligations (CO)', 'The CO sets out few, general rules and is principle-based.', 'framework-classification'),
  ('IFRS', 'IFRS is principle-based.', 'framework-classification'),
  ('Swiss GAAP FER', 'Swiss GAAP FER is principle-based and deliberately short.', 'framework-classification'),
  ('US GAAP', 'US GAAP is rule-based, with roughly 25,000 pages of detailed guidance.', None)], 'd',
 'US GAAP is rule-based (about 25,000 pages). CO, IFRS and Swiss GAAP FER are principle-based.', ev='frameworks')

add('1-02', '2', FR, 'Goodwill', 1, 'Under Swiss GAAP FER, goodwill arising from an acquisition may be offset directly against equity instead of being capitalised.',
 [('True', 'FER lets the group either capitalise and amortise goodwill (e.g. over 5 years) or offset it directly against equity.', None),
  ('False', 'Offsetting against equity is an allowed option under FER (it is not allowed under IFRS).', 'goodwill-policy')], 'a',
 'Swiss GAAP FER offers a choice: capitalise and amortise goodwill, or offset it against equity (cf. the Dormakaba case, where the equity ratio dropped sharply).', ev='goodwill')

add('1-03', '3', CS, 'Consolidation concepts', 1, 'During 2025, a parent company sold goods to its 100% subsidiary for CHF 50,000. The goods had cost the parent CHF 40,000 and are still in the subsidiary’s inventory at year-end. Which statement is correct for the consolidated financial statements?',
 [('The intercompany profit of CHF 10,000 is eliminated, and inventory is shown at CHF 40,000.', 'The unrealised profit of 50,000 − 40,000 = 10,000 is eliminated; inventory stays at the group’s cost.', None),
  ('The inventory is shown at CHF 50,000, since the transaction took place at market price.', 'The price does not matter: from the group’s view no profit is realised until the goods are sold to outsiders.', 'intragroup-not-eliminated'),
  ('Revenue of CHF 50,000 is shown in the consolidated income statement.', 'Intragroup revenue is eliminated; the group has not sold anything to an outside party.', 'intragroup-not-eliminated'),
  ('No adjustment is necessary, since both companies are legally independent.', 'Consolidated statements treat the group as one entity, so intragroup transactions are eliminated.', 'consolidation-legal-entity')], 'a',
 'Only transactions with external parties are reported. The unrealised intercompany profit is eliminated and inventory is carried at the group’s cost of CHF 40,000.', ev='acquisition')

add('1-04', '4', CS, 'Consolidation concepts', 1, 'Entity A holds 35% of the voting rights in Entity B and has significant influence, but no control. How is Entity B classified, and which method is applied in A’s consolidated financial statements?',
 [('Joint venture – proportionate consolidation', 'A joint venture needs joint control. Significant influence at 35% makes B an associate.', 'ownership-control'),
  ('Financial asset – fair value', 'Significant influence goes beyond a passive financial investment.', 'ownership-control'),
  ('Associated company – equity method', '20% to below 50% with significant influence is an associate, accounted for with the equity method.', None),
  ('Subsidiary – full consolidation', 'Full consolidation requires control, which A does not have.', 'ownership-control')], 'c',
 '20% to <50% with significant influence is an associated company, accounted for using the equity method (one-line consolidation).', ev='equity')

o5, s5, p5, d5, h5, l5 = 900, D('0.3'), 400, 150, 500, 5
v5 = o5 + s5 * (p5 - d5 - D(h5) / l5)
add('1-05', '5', CS, 'Equity method', 3, 'Alpine AG acquired 30% of Berg AG on 1st January 2025 for CHF 900,000 (significant influence). At that date, Berg AG’s assets contained hidden reserves of CHF 500,000 (100% basis), relating to machinery with a remaining useful life of 5 years. In 2025, Berg AG reports a net profit of CHF 400,000 and pays a total dividend of CHF 150,000. What is the carrying amount of the investment in Berg AG in Alpine AG’s consolidated balance sheet on 31st December 2025 (in CHF thousand)?',
 [('990', 'Ignores the dividend: 900 + 120 − 30 = 990.', 'equity-ignore-dividends'),
  ('1,020', 'Ignores both the dividend and the hidden-reserve depreciation: 900 + 120.', 'equity-ignore-dividends'),
  ('945', '900 + 120 − 45 − 30 = 945.', None),
  ('975', 'Ignores the depreciation of the hidden reserves: 900 + 120 − 45.', 'equity-ignore-reserves')], 'c',
 'Equity method: opening amount + share of profit − share of dividends − share of the hidden-reserve depreciation.',
 ev='equity', calc=f'900 + 30% × 400 (120) − 30% × 150 (45) − 30% × 500 / 5 (30) = {n(v5)}.',
 check={'f': 'o + s*(p - d - h/l)', 'v': {'o': o5, 's': s5, 'p': p5, 'd': d5, 'h': h5, 'l': l5}, 'x': v5})

HOLD = ('HoldCo AG acquired 75% of Target AG on 31.12.2025 for CHF 2,400,000. The following are the account balances as of the acquisition date. '
        'Additionally, Target AG has CHF 400,000 of hidden reserves in its non-current assets, which are not included in the accounts below. Ignore deferred taxes.\n\n'
        + table(['Account (CHF)', 'HoldCo AG', 'Target AG'],
                [['Investment in Target AG', '2,400,000', '–'], ['Other Non-Current Assets', '4,600,000', '1,800,000'], ['Current Assets', '1,000,000', '600,000'],
                 ['Long-term Debt', '3,500,000', '900,000'], ['Accounts Payable', '500,000', '300,000'], ['Equity', '4,000,000', '1,200,000']]))
pr6, s6, e6, h6 = 2_400_000, D('0.75'), 1_200_000, 400_000
gw6 = pr6 - s6 * (e6 + h6); nci6 = (1 - s6) * (e6 + h6)
add('1-06', '6', CS, 'Acquisition accounting', 3, 'Does HoldCo AG recognise any goodwill related to the acquisition of Target AG? If so, what is the amount of goodwill according to the method you learned in class?',
 [('Yes; CHF 1,200,000', '2,400,000 − 75% × (1,200,000 + 400,000) = 1,200,000.', None),
  ('No goodwill is recognised.', 'The price of 2,400,000 exceeds the acquired share of fair-value net assets (1,200,000).', 'goodwill-zero'),
  ('Yes; CHF 800,000', 'Subtracts 100% of the fair-value net assets (2,400,000 − 1,600,000) instead of the 75% share.', 'goodwill-wrong-share'),
  ('Yes; CHF 1,500,000', 'Ignores the hidden reserves: 2,400,000 − 75% × 1,200,000.', 'goodwill-ignore-reserves')], 'a',
 'Goodwill = purchase price − parent’s share of the fair value of net assets (book equity + hidden reserves).', scenario=HOLD, ev='acquisition',
 calc=f'Fair value of net assets = 1,200,000 + 400,000 = 1,600,000; 75% = 1,200,000; goodwill = 2,400,000 − 1,200,000 = {chf(gw6)}.',
 check={'f': 'p - s*(e + h)', 'v': {'p': pr6, 's': s6, 'e': e6, 'h': h6}, 'x': gw6})

add('1-07', '7', CS, 'Acquisition accounting', 3, 'What is the amount of the “Non-Controlling Interest” in HoldCo’s consolidated balance sheet on 31.12.2025?',
 [('There is no non-controlling interest in this scenario.', '25% of Target AG belongs to outside shareholders, so an NCI arises.', 'nci-none'),
  ('CHF 600,000', 'Takes 25% of the purchase price, but NCI is based on Target’s net assets.', 'nci-purchase-price'),
  ('CHF 400,000', '25% × 1,600,000 = 400,000.', None),
  ('CHF 300,000', 'Ignores the hidden reserves: 25% × 1,200,000.', 'nci-ignore-reserves')], 'c',
 'NCI = minority share × fair value of net assets.', scenario=HOLD, ev='acquisition', calc=f'25% × 1,600,000 = {chf(nci6)}.',
 check={'f': '(1 - s)*(e + h)', 'v': {'s': s6, 'e': e6, 'h': h6}, 'x': nci6})

ta8 = 8_000_000 - pr6 + 2_400_000 + h6 + gw6
add('1-08', '8', CS, 'Acquisition accounting', 2, 'What are the total assets in HoldCo’s consolidated balance sheet on 31.12.2025?',
 [('CHF 9,200,000', 'Includes goodwill but leaves out the hidden reserves of 400,000.', 'hidden-reserves-omitted'),
  ('CHF 8,400,000', 'Leaves out goodwill of 1,200,000.', 'goodwill-zero'),
  ('CHF 10,400,000', 'Adds both balance sheets without eliminating the investment, hidden reserves or goodwill.', 'consolidation-parent-only'),
  ('CHF 9,600,000', '4,600,000 + 1,000,000 + 1,800,000 + 400,000 + 600,000 + 1,200,000 = 9,600,000.', None)], 'd',
 'Consolidated assets = parent assets without the investment + subsidiary assets + hidden reserves + goodwill.', scenario=HOLD, ev='acquisition',
 calc='Other NCA 4,600,000 + CA 1,000,000 + Target NCA 1,800,000 + hidden reserves 400,000 + Target CA 600,000 + goodwill 1,200,000 = 9,600,000. '
      'The investment (2,400,000) is eliminated. Check: debt 4,400,000 + AP 800,000 + equity 4,000,000 + NCI 400,000 = 9,600,000.',
 check={'f': 'a - p + b + h + p - s*(e + h)', 'v': {'a': 8_000_000, 'p': pr6, 'b': 2_400_000, 'h': h6, 's': s6, 'e': e6}, 'x': ta8})

# ---------- Topic 2: Selected Topics in Accounting ----------
add('1-09', '9', FR, 'Leases', 1, 'Under IFRS 16, which expenses does a lessee recognise in the income statement for a lease that was previously classified as an operating lease?',
 [('Depreciation of the right-of-use asset and interest expense on the lease liability', 'IFRS 16 splits the lease cost into depreciation and interest.', None),
  ('No expense, since the lease is recognised on the balance sheet', 'Recognising the lease on the balance sheet still creates expenses: depreciation and interest.', 'lease-no-expense'),
  ('Only interest expense on the lease liability', 'The right-of-use asset is also depreciated.', 'lease-no-depreciation'),
  ('Only the lease payment as an operating expense', 'That was the old operating-lease treatment; IFRS 16 removed it for lessees.', 'lease-off-balance-sheet')], 'a',
 'IFRS 16 eliminates the operating/finance distinction for lessees: the lease expense consists of depreciation and interest.', ev='lease')

add('1-10', '10', FR, 'Impairment', 1, 'Which of the following is not an indicator of impairment according to IAS 36?',
 [('Evidence of physical damage to the asset', 'Physical damage is an internal indicator, so it is an indicator.', 'impairment-indicators'),
  ('A decrease in market interest rates', 'Not an indicator: lower rates raise value in use. An increase in rates would be an indicator.', None),
  ('The carrying amount of the entity’s net assets exceeds its market capitalisation', 'This is an external indicator listed in IAS 36.', 'impairment-indicators'),
  ('A significant decline in the asset’s market value', 'This is an external indicator.', 'impairment-indicators')], 'b',
 'An increase in market interest rates is an external indicator because it lowers value in use. A decrease is not.', ev='impairment')

c11, f11, v11 = 120_000, 85_000, 92_000
loss11 = c11 - max(f11, v11)
add('1-11', '11', FR, 'Impairment', 2, 'A machine has a carrying amount of CHF 120,000. Due to a new competitor technology, management estimates the fair value less costs of disposal at CHF 85,000 and the value in use at CHF 92,000. What is the impairment loss?',
 [('No impairment loss is recognised.', 'The carrying amount of 120,000 exceeds the recoverable amount of 92,000.', 'impairment-no-loss'),
  ('CHF 35,000', 'Uses fair value less costs of disposal, but the recoverable amount is the higher of the two values.', 'impairment-fvlcd-only'),
  ('CHF 7,000', 'This is the gap between the two measures, not the loss.', 'impairment-wrong-difference'),
  ('CHF 28,000', 'Recoverable amount = max(85,000; 92,000) = 92,000; loss = 120,000 − 92,000.', None)], 'd',
 'Impairment loss = carrying amount − recoverable amount, where recoverable amount = max(fair value less costs of disposal, value in use).', ev='impairment',
 calc=f'Recoverable amount = max(85,000; 92,000) = 92,000. Impairment = 120,000 − 92,000 = {chf(loss11)}.',
 check={'f': 'c - max(f, v)', 'v': {'c': c11, 'f': f11, 'v': v11}, 'x': loss11})

KAPPA = ('On 1st January 2025, Kappa AG entered into a lease for a production machine. The lease runs for 4 years, with annual payments of CHF 10,000 due every 31st December. '
         'The interest rate implicit in the lease is 8% p.a. The right-of-use asset is depreciated on a straight-line basis over the lease term. Kappa AG reports under IFRS. '
         'Use two decimal places during calculations and choose the answer closest to your result.')
p12, i12 = 10_000, D('0.08')
pv12 = p12 * (1 - (1 + i12) ** -4) / i12
bal12 = pv12 * (1 + i12) ** 2 - p12 * (1 + i12) - p12
add('1-12', '12', FR, 'Leases', 3, 'What is the carrying amount of the lease liability on 31.12.2026 (end of the second year)?',
 [('CHF 25,771', 'This is the liability at 31.12.2025, after one year.', 'lease-wrong-year'),
  ('CHF 17,833', 'After two years of interest and repayments the liability is 17,832.65.', None),
  ('CHF 16,561', 'This is the right-of-use asset after two years (33,121 × 2/4), not the liability.', 'lease-liability-as-asset'),
  ('CHF 20,000', 'Deducts two payments from the undiscounted 40,000 and ignores discounting and interest.', 'lease-undiscounted')], 'b',
 'The liability starts at the present value of the payments and grows by interest, less each payment.', scenario=KAPPA, ev='lease',
 calc='PV at 1.1.2025 = 10,000 × 3.31213 = 33,121.27. Year 1: interest 2,649.70, repayment 7,350.30 → 25,770.97. Year 2: interest 2,061.68, repayment 7,938.32 → 17,832.65.',
 check={'f': 'p*(1 - (1 + i)**-4)/i*(1 + i)**2 - p*(1 + i) - p', 'v': {'p': p12, 'i': i12}, 'x': bal12})

exp13 = pv12 / 4 + pv12 * i12
add('1-13', '13', FR, 'Leases', 2, 'What is the total lease-related expense in Kappa AG’s income statement for 2025?',
 [('CHF 2,650', 'Interest only; the right-of-use asset is also depreciated.', 'lease-no-depreciation'),
  ('CHF 10,000', 'The cash payment is not the IFRS 16 expense; the expense is depreciation plus interest.', 'lease-payment-as-expense'),
  ('CHF 10,930', 'Depreciation 8,280.32 + interest 2,649.70 = 10,930.02.', None),
  ('CHF 8,280', 'Depreciation only; the interest expense is missing.', 'lease-interest-omitted')], 'c',
 'Under IFRS 16 the expense is depreciation plus interest, and it is front-loaded (above the payment of 10,000 in the early years).', scenario=KAPPA, ev='lease',
 calc='Depreciation 33,121.27 / 4 = 8,280.32; interest 33,121.27 × 8% = 2,649.70; total 10,930.02.',
 check={'f': 'p*(1 - (1 + i)**-4)/i/4 + p*(1 - (1 + i)**-4)/i*i', 'v': {'p': p12, 'i': i12}, 'x': exp13})

add('1-14', '14', FR, 'Pensions', 1, 'In a defined benefit pension plan, who bears the actuarial and investment risk?',
 [('The state', 'The state is not a party to the employer’s pension promise.', 'pension-risk'),
  ('The employee', 'The employee bears the risk in a defined contribution plan, not in a defined benefit plan.', 'pension-db-dc'),
  ('The employing entity', 'The entity promises agreed benefits, so it bears the actuarial and investment risk.', None),
  ('The pension fund’s auditor', 'The auditor checks the accounts and bears no plan risk.', 'pension-risk')], 'c',
 'In a defined benefit plan the entity promises agreed benefits and bears the risk; in a defined contribution plan the employee does.', ev='pensions')

add('1-15', '15', FR, 'Presentation (IFRS 18)', 1, 'According to IFRS 18, where is the share of profit or loss of equity-accounted investees presented in the income statement (for a company without specified main business activities)?',
 [('In other comprehensive income', 'The share of profit of equity-accounted investees goes through profit or loss, not OCI.', 'ifrs18-categories'),
  ('In the financing category', 'The financing category covers how the entity raises funds, e.g. interest on borrowings.', 'ifrs18-categories'),
  ('In the investing category', 'IFRS 18 places these results in the investing category, outside operating profit.', None),
  ('In the operating category', 'IFRS 18 moved results of equity-accounted investees out of operating profit.', 'ifrs18-categories')], 'c',
 'IFRS 18 introduces the operating, investing and financing categories. Results of equity-accounted investees are always shown in the investing category.', ev='pe-ifrs18')

f16, c16, m16 = 50, D('1.5'), D('0.04')
issue16 = c16 * (1 - (1 + m16) ** -4) / m16 + f16 / (1 + m16) ** 4
end16 = issue16 * (1 + m16) - c16
add('1-16', '16', FR, 'Financial instruments', 2, 'Helvetia Bank AG issues bonds with a face value of CHF 50 million, a term of 4 years and an annual coupon of 3%. At issuance, the market interest rate is 4%. Using the effective interest method, what is the carrying amount of the bonds at the end of the first year (in CHF million)?',
 [('48.61', 'Issue price 48.185 + interest 1.927 − coupon 1.5 = 48.61.', None),
  ('48.19', 'This is the issue price, before the discount is amortised for the year.', 'bond-issue-price'),
  ('50.00', 'This is the face value. The bond is issued at a discount because the coupon (3%) is below the market rate (4%).', 'bond-face-value'),
  ('47.76', 'Amortises the discount in the wrong direction (48.19 − 0.43). The carrying amount moves towards face value.', 'bond-amortisation-direction')], 'a',
 'With the effective interest method, interest expense = carrying amount × market rate; the excess over the coupon is added to the carrying amount.', ev='pe-bonds',
 calc='Issue price = 1.5 × 3.6299 + 50 / 1.04⁴ = 48.185. Interest year 1 = 48.185 × 4% = 1.927; coupon = 1.5. Carrying amount = 48.185 + (1.927 − 1.5) = 48.61.',
 check={'f': '(c*(1 - (1 + m)**-4)/m + f/(1 + m)**4)*(1 + m) - c', 'v': {'c': c16, 'm': m16, 'f': f16}, 'x': end16, 'dp': 2, 'unit': 'MCHF'})

b17, t17 = 800_000, D('0.2')
add('1-17', '17', FR, 'Deferred taxes', 2, 'In its IFRS consolidated financial statements, Müller AG recognises a provision for litigation risks of CHF 800,000. For tax purposes, the expense is only deductible when the payment is made, so no provision is recognised in the tax balance sheet. The tax rate is 20%. Which statement is correct?',
 [('Temporary difference; deferred tax asset of CHF 800,000', 'Forgets the tax rate: the deferred tax is the difference × 20%.', 'tax-rate-omitted'),
  ('Temporary difference; deferred tax liability of CHF 160,000', 'Direction reversed: a liability carried above its tax value gives a deferred tax asset.', 'tax-direction'),
  ('Temporary difference; deferred tax asset of CHF 160,000', 'Group value 800,000 > tax value 0 on a liability → deductible difference → DTA of 800,000 × 20%.', None),
  ('Permanent difference; no deferred taxes', 'The expense becomes deductible when paid, so the difference reverses: it is temporary.', 'tax-permanent-vs-temporary')], 'c',
 'A liability with a higher group value than tax value creates a deductible temporary difference and a deferred tax asset.', ev='tax',
 calc='(800,000 − 0) × 20% = 160,000 deferred tax asset.', check={'f': 'b*t', 'v': {'b': b17, 't': t17}, 'x': b17 * t17, 'same': 'b'})

# ---------- Topic 3: Auditing ----------
add('1-18', '18', AU, 'Three Lines Model', 1, 'According to the Three Lines Model, which function provides independent and objective assurance to the governing body?',
 [('Risk management and compliance (second line)', 'The second line supports and monitors management through policies and compliance; it is not independent of management.', 'three-lines'),
  ('The external auditor as part of the second line', 'The external auditor sits outside the three lines.', 'three-lines'),
  ('Operational management (first line)', 'The first line owns and manages risk; it does not give independent assurance.', 'three-lines'),
  ('Internal audit (third line)', 'Internal audit is the third line and provides independent assurance.', None)], 'd',
 'Internal audit (third line) provides independent assurance. The second line supports management through policies, monitoring and compliance.', ev='lines')

add('1-19', '19', AU, 'Audit scope', 2, 'Which of the following Swiss companies (unlisted, no bonds outstanding, not required to prepare consolidated accounts) is subject to an Ordinary Audit?',
 [('Company C: total assets CHF 15 m, revenue CHF 30 m, 120 FTE in 2024; total assets CHF 21 m, revenue CHF 42 m, 150 FTE in 2025', 'C exceeds two thresholds only in 2025, not in two consecutive years.', 'audit-scope-thresholds'),
  ('Company D: total assets CHF 3 m, revenue CHF 6 m, 9 FTE; all shareholders agreed to opt out', 'D is far below the thresholds and has validly opted out of the audit.', 'audit-scope-thresholds'),
  ('Company B: total assets CHF 22 m, revenue CHF 45 m, 180 FTE in 2024 and in 2025', 'B exceeds two of three thresholds (assets and revenue) in both years.', None),
  ('Company A: total assets CHF 25 m, revenue CHF 35 m, 200 FTE in 2024 and in 2025', 'A exceeds only one threshold (total assets); revenue and FTE are below.', 'audit-scope-thresholds')], 'c',
 'Ordinary audit if 2 of 3 thresholds (total assets > CHF 20 m, revenue > CHF 40 m, > 250 FTE) are exceeded in two consecutive years.', ev='legal')

add('1-20', '20', AU, 'Audit scope', 1, 'A company with 8 full-time positions may opt out of the limited audit if the board of directors decides so.',
 [('True', 'A board decision is not enough: opting out needs the consent of all shareholders.', 'opting-out'),
  ('False', 'Opting out requires at most 10 FTE (annual average) and the consent of all shareholders.', None)], 'b',
 'Opting out requires not more than 10 FTE and the consent of all shareholders. A board decision alone is not sufficient.', ev='legal')

add('1-21', '21', AU, 'Assurance', 1, 'Which of the following is a characteristic of a limited audit compared to an ordinary audit?',
 [('The lead auditor must rotate after 7 years', 'Lead-auditor rotation applies to the ordinary audit.', 'limited-vs-ordinary'),
  ('Third-party confirmations are mandatory', 'Third-party confirmations belong to the ordinary audit.', 'limited-vs-ordinary'),
  ('Attendance at the inventory count is required', 'Attending the inventory count belongs to the ordinary audit.', 'limited-vs-ordinary'),
  ('The audit opinion is formulated negatively (limited assurance)', 'A limited audit gives limited assurance: “nothing has come to our attention…”.', None)], 'd',
 'A limited audit gives limited assurance with a negatively formulated opinion. The other features belong to the ordinary audit.', ev='audit')

add('1-22', '22', AU, 'Independence', 1, 'Under Swiss law (ordinary audit), which rotation requirement applies?',
 [('Rotation of the lead auditor after 7 years', 'CO Art. 730a: the person leading the audit rotates after 7 years.', None),
  ('There is no rotation requirement in Switzerland', 'Swiss law requires lead-auditor rotation after 7 years.', 'auditor-rotation'),
  ('Rotation of the audit firm after 7 years', 'Only the person leading the audit rotates; the firm may stay.', 'auditor-rotation'),
  ('Mandatory audit firm rotation after 10 years', 'Mandatory firm rotation is the EU approach, not Swiss law.', 'auditor-rotation')], 'a',
 'CO Art. 730a: the person leading the audit must rotate after 7 years, but the firm does not have to (unlike EU audit firm rotation).', ev='legal')

add('1-23', '23', AU, 'Audit opinions', 1, 'Which audit opinion is issued when the auditor concludes that the financial statements contain misstatements that are both material and pervasive?',
 [('Unmodified opinion', 'An unmodified opinion means there is no material misstatement.', 'opinion-type'),
  ('Disclaimer of opinion', 'A disclaimer is for when the auditor cannot obtain sufficient evidence, not when misstatements are found.', 'opinion-type'),
  ('Qualified opinion', 'A qualified opinion is for material but not pervasive misstatements.', 'opinion-type'),
  ('Adverse opinion', 'Material and pervasive misstatements mean the statements are not fairly presented.', None)], 'd',
 'Material and pervasive misstatements result in an adverse opinion (e.g. BDO / LumX 2019).', ev='opinion')

add('1-24', '24', AU, 'Audit market', 1, 'Which audit firm has the greatest number of audit clients overall in the Swiss market (all firms, not only public companies)?',
 [('PwC', 'PwC is second, with about 5,100 clients.', 'audit-market'),
  ('BDO', 'BDO has the most clients across all firms, about 6,400.', None),
  ('KPMG', 'Not the largest by client count; BDO leads with about 6,400 clients.', 'audit-market'),
  ('Deloitte', 'Not the largest by client count; BDO leads with about 6,400 clients.', 'audit-market')], 'b',
 'Across all firms in Switzerland, BDO has the most clients (about 6,400), followed by PwC (about 5,100).', ev='legal')

add('1-25', '25', AU, 'Audit procedures', 1, 'Which of the following is a test of controls?',
 [('Comparing the gross margin with the prior year', 'This is an analytical (substantive) procedure.', 'controls-vs-substantive'),
  ('Observing whether supplier invoices are approved by a second person before payment', 'Observation checks whether an internal control works, so it is a test of controls.', None),
  ('Sending confirmation letters to selected customers', 'Confirmations are a substantive test of details.', 'controls-vs-substantive'),
  ('Recalculating the depreciation expense for the year', 'Recalculating an amount is a substantive test of details.', 'controls-vs-substantive')], 'b',
 'Tests of controls check whether internal controls work (inquiry, inspection, observation, re-performance). The other options are substantive procedures.', ev='procedures')

add('1-26', '26', AU, 'Audit fees', 1, 'Which of the following factors tends to decrease audit fees?',
 [('A high share of inventory and receivables in total assets', 'These balances are riskier and need more work, so fees rise.', 'audit-fee-drivers'),
  ('A large number of foreign subsidiaries', 'Foreign subsidiaries add complexity and raise fees.', 'audit-fee-drivers'),
  ('Application of IFRS or US GAAP', 'IFRS or US GAAP are more demanding than Swiss CO and raise fees.', 'audit-fee-drivers'),
  ('A change of auditor', 'A new auditor often discounts the fee (“lowballing”).', None)], 'd',
 'Empirically, a change of auditor is associated with lower fees (fee discounting / lowballing). All other factors increase fees.', ev='audit')

add('1-27', '27', AU, 'Sustainability assurance', 1, 'Based on the trends in Switzerland (2020–2024), which statement about sustainability assurance is correct?',
 [('Fewer than 10% of sustainability reports are assured', 'About 45% of reports (89 of 177) are assured.', 'sustainability-assurance'),
  ('Reasonable assurance is the most common form', 'Almost all assurance is limited, not reasonable.', 'sustainability-assurance'),
  ('Larger companies are more likely to obtain external assurance', 'Firm size is a key determinant of obtaining assurance.', None),
  ('Mid-tier audit firms dominate the market for sustainability assurance', 'The Big Four hold about 85% of the market.', 'sustainability-assurance')], 'c',
 'About 45% of reports are assured (89 of 177), almost all with limited assurance. The Big Four hold about 85% of the market, and firm size is a key determinant.', ev='audit')

RHEIN = ('Rhein Logistik AG (unlisted, stable and profitable) is subject to an Ordinary Audit of its 2025 financial statements. The audit firm uses the following rules of thumb: '
         '5% of EBT, 0.5% of revenue, 1% of total assets or 2% of equity, and selects the benchmark most commonly applied for a stable, profit-oriented company.\n\n'
         + table(['Key figures 2025 (CHF)', 'Amount'], [['Revenue', '60,000,000'], ['Earnings before Tax (EBT)', '2,400,000'], ['Total Assets', '45,000,000'], ['Equity', '18,000,000']]))
add('1-28', '28', AU, 'Materiality', 2, 'Which overall materiality should the auditor most likely apply?',
 [('CHF 450,000', '1% of total assets; total assets is not the usual benchmark for a stable, profitable company.', 'materiality-benchmark'),
  ('CHF 120,000', '5% × 2,400,000 = 120,000.', None),
  ('CHF 300,000', '0.5% of revenue; revenue is used when profit is volatile or low.', 'materiality-benchmark'),
  ('CHF 360,000', '2% of equity; equity is not the usual benchmark here.', 'materiality-benchmark')], 'b',
 'For a stable, profit-oriented company, EBT is the usual benchmark.', scenario=RHEIN, ev='materiality',
 calc='5% × 2,400,000 = 120,000.', check={'f': '0.05*e', 'v': {'e': 2_400_000}, 'x': D('0.05') * 2_400_000})

add('1-29', '29', AU, 'Audit opinions', 2, 'During the audit, two uncorrected misstatements are identified: (i) inventory is overstated by CHF 50,000, and (ii) a provision of CHF 95,000 for a probable lawsuit was not recorded. Management refuses to correct them. The misstatements are not pervasive. Which audit opinion is appropriate?',
 [('Disclaimer of opinion', 'A disclaimer applies when evidence is missing, not when misstatements are known.', 'opinion-type'),
  ('Unmodified opinion, since each misstatement is individually below materiality', 'Misstatements are judged in aggregate: 50,000 + 95,000 = 145,000 exceeds 120,000.', 'materiality-aggregation'),
  ('Adverse opinion, since materiality is exceeded', 'An adverse opinion requires the misstatement to be pervasive, which it is not.', 'opinion-type'),
  ('Qualified opinion', 'Material in aggregate but not pervasive, so the opinion is qualified (“except for”).', None)], 'd',
 'Each item is below 120,000, but together they reduce EBT by 145,000, above materiality. Material but not pervasive → qualified opinion.', scenario=RHEIN, ev='opinion')


# ============================ PART 2 – CONTROLLING ============================
MA, BU, VA, CB, CP = 'Management Accounting', 'Budgeting', 'Variances', 'Capital Budgeting', 'Cost and Performance Management'

ALBIS = table(['Albis Manufacturing, 2025', 'CHF'],
              [['Beginning inventory of direct materials, Jan 1, 2025', '30,000'], ['Purchases of direct materials', '250,000'],
               ['Ending inventory of direct materials, Dec 31, 2025', '40,000'], ['Direct manufacturing labor', '90,000'], ['Indirect manufacturing costs', '150,000'],
               ['Beginning work-in-process inventory', '20,000'], ['Ending work-in-process inventory', '25,000'], ['Beginning inventory of finished goods', '120,000'],
               ['Ending inventory of finished goods', '95,000'], ['Marketing and administrative costs', '180,000']])
cogs = 30_000 + 250_000 - 40_000 + 90_000 + 150_000 + 20_000 - 25_000 + 120_000 - 95_000
add('2-1-1', '1.1', MA, 'Manufacturing cost flows', 2, 'Albis Manufacturing reported the following for 2025. What is Albis’ cost of goods sold?',
 [('CHF 500,000', 'COGS = 120,000 + 475,000 − 95,000 = 500,000.', None),
  ('CHF 475,000', 'This is cost of goods manufactured; the change in finished goods is missing.', 'cogm-vs-cogs'),
  ('CHF 680,000', 'Adds marketing and administrative costs, which are period costs.', 'period-costs-inventoriable'),
  ('CHF 505,000', 'Ignores the change in work-in-process inventory.', 'wip-change-omitted'),
  none_wrong('a')], 'a',
 'Direct materials used → cost of goods manufactured → cost of goods sold. Marketing and administrative costs are period costs.', scenario=ALBIS, ev='ma-flow',
 calc='DM used = 30,000 + 250,000 − 40,000 = 240,000. COGM = 240,000 + 90,000 + 150,000 + 20,000 − 25,000 = 475,000. COGS = 120,000 + 475,000 − 95,000 = 500,000.',
 check={'f': 'bm + p - em + dl + oh + bw - ew + bf - ef', 'v': {'bm': 30_000, 'p': 250_000, 'em': 40_000, 'dl': 90_000, 'oh': 150_000, 'bw': 20_000, 'ew': 25_000, 'bf': 120_000, 'ef': 95_000}, 'x': cogs})

add('2-1-2', '1.2', MA, 'Cost concepts', 1, 'Which of the following is a characteristic of management accounting (as opposed to financial accounting)?',
 [('It is primarily past-oriented', 'Financial accounting is past-oriented; management accounting looks ahead.', 'ma-vs-fa'),
  ('It is mainly aimed at external investors and regulators', 'External investors and regulators are the audience of financial accounting.', 'ma-vs-fa'),
  ('It must comply with IFRS/GAAP', 'Management accounting does not need to follow IFRS/GAAP.', 'ma-vs-fa'),
  ('It is future-oriented and based on a cost-benefit approach', 'Management accounting serves internal managers and looks ahead.', None),
  none_wrong('d')], 'd',
 'Management accounting serves internal managers, is future-oriented, and does not need to follow IFRS/GAAP (cost-benefit approach).', ev='ma-costs')

u13 = D(270_000 + 60_000) / (80 - 50)
add('2-1-3', '1.3', MA, 'CVP analysis', 2, 'Nordwind AG sells a product at CHF 80 per unit. Variable costs are CHF 50 per unit and annual fixed costs are CHF 270,000. How many units must Nordwind sell to achieve a target operating income of CHF 60,000?',
 [('11,000 units', '(270,000 + 60,000) / 30 = 11,000.', None),
  ('9,000 units', 'This is the breakeven point; the target income is missing.', 'cvp-target-omitted'),
  ('4,125 units', 'Divides by the price (80) instead of the contribution margin per unit (30).', 'cvp-price-not-cm'),
  ('6,600 units', 'Divides by the variable cost (50) instead of the contribution margin per unit (30).', 'cvp-price-not-cm'),
  none_wrong('a')], 'a',
 'Target units = (fixed costs + target operating income) / contribution margin per unit.', ev='ma-cvp',
 calc='Contribution margin per unit = 80 − 50 = 30. Units = (270,000 + 60,000) / 30 = 11,000.',
 check={'f': '(f + t)/(p - v)', 'v': {'f': 270_000, 't': 60_000, 'p': 80, 'v': 50}, 'x': u13, 'unit': 'units'})

job = 12_000 + 200 * 35 + 200 * D(600_000) / 40_000
add('2-2-1', '2.1', MA, 'Job costing', 2, 'Precision Works applies manufacturing overhead using a budgeted rate based on direct manufacturing labor-hours. Budgeted manufacturing overhead is CHF 600,000 and budgeted direct labor-hours are 40,000. Job #417 requires direct materials of CHF 12,000 and 200 direct labor-hours at CHF 35 per hour. What is the total manufacturing cost of Job #417?',
 [('CHF 19,000', 'Materials and labor only; the allocated overhead of 3,000 is missing.', 'job-overhead-omitted'),
  ('CHF 15,000', 'Materials and overhead only; direct labor of 7,000 is missing.', 'job-labor-omitted'),
  ('CHF 25,000', 'Overhead is overstated: the rate is 600,000 / 40,000 = CHF 15 per labor-hour, so overhead is 3,000.', 'job-overhead-rate'),
  ('CHF 22,000', '12,000 + 7,000 + 3,000 = 22,000.', None),
  none_wrong('d')], 'd',
 'Job cost = direct materials + direct labor + allocated overhead (budgeted rate × actual labor-hours).', ev='ma-job',
 calc='Overhead rate = 600,000 / 40,000 = 15 per DLH. Cost = 12,000 + 200 × 35 + 200 × 15 = 12,000 + 7,000 + 3,000 = 22,000.',
 check={'f': 'm + h*w + h*o/b', 'v': {'m': 12_000, 'h': 200, 'w': 35, 'o': 600_000, 'b': 40_000}, 'x': job})

KESSLER = ('Kessler AG produces two products, Alpha and Beta, and uses an activity-based costing (ABC) system. The following data apply:\n\n'
           + table(['Activity', 'Overhead costs', 'Activity level'], [['Setups', 'CHF 240,000', '400 setups'], ['Machine maintenance', 'CHF 360,000', '12,000 machine-hours'],
                                                                   ['Inspections', 'CHF 90,000', '1,500 inspections'], ['Total', 'CHF 690,000', '']])
           + '\n\n' + table(['', 'Alpha', 'Beta'], [['Production units', '10,000', '40,000'], ['Setups', '120', '280'], ['Machine-hours', '3,000', '9,000'], ['Inspections', '500', '1,000']]))
abc = (120 * D(240_000) / 400 + 3_000 * D(360_000) / 12_000 + 500 * D(90_000) / 1_500) / 10_000
add('2-2-2', '2.2', MA, 'Activity-based costing', 4, 'Using ABC, what are the estimated overhead costs per unit of Alpha?',
 [('CHF 19.20', '(72,000 + 90,000 + 30,000) / 10,000 = 19.20.', None),
  ('CHF 13.80', 'Spreads total overhead evenly over all 50,000 units (690,000 / 50,000).', 'abc-plantwide-units'),
  ('CHF 12.45', 'This is Beta’s ABC overhead per unit.', 'abc-wrong-product'),
  ('CHF 17.25', 'Traditional costing with one machine-hour rate (57.50 × 3,000 / 10,000), not ABC.', 'abc-single-rate'),
  none_wrong('a')], 'a',
 'ABC: one rate per activity, then charge each product by its use of each activity.', scenario=KESSLER, ev='ma-job',
 calc='Rates: setups 240,000 / 400 = 600; maintenance 360,000 / 12,000 = 30 per MH; inspections 90,000 / 1,500 = 60. '
      'Alpha: 120 × 600 + 3,000 × 30 + 500 × 60 = 192,000 → 192,000 / 10,000 = 19.20.',
 check={'f': '(a*s/sa + b*m/ma + c*i/ia)/u', 'v': {'a': 120, 's': 240_000, 'sa': 400, 'b': 3_000, 'm': 360_000, 'ma': 12_000, 'c': 500, 'i': 90_000, 'ia': 1_500, 'u': 10_000}, 'x': abc, 'dp': 2})

mk = 100 * D('0.12') * 4_000_000 / (12_000 * 225)
add('2-3-1', '3.1', MA, 'Pricing and target costing', 2, 'Velo AG has invested CHF 4,000,000 in a plant to produce e-bike frames. The target return on investment is 12%. Velo plans to sell 12,000 frames per year; the full cost per frame is CHF 225. What is the markup as a percentage of full cost? (Round to one decimal.)',
 [('17.8%', 'Target income 480,000 / total full cost 2,700,000 = 17.8%.', None),
  ('21.3%', 'Too high: the markup is target income (480,000) over total full cost (2,700,000).', 'markup-base'),
  ('12.0%', 'This is the target return on investment, not the markup on cost.', 'markup-roi-confusion'),
  ('15.1%', '480,000 / (2,700,000 + 480,000) is the margin on the target price, not the markup on cost.', 'markup-on-price'),
  none_wrong('a')], 'a',
 'Markup on full cost = target operating income / total full cost.', ev='ma-price',
 calc='Target operating income = 12% × 4,000,000 = 480,000. Total cost = 12,000 × 225 = 2,700,000. Markup = 480,000 / 2,700,000 = 17.8% (target price 265).',
 check={'f': '100*r*i/(q*c)', 'v': {'r': D('0.12'), 'i': 4_000_000, 'q': 12_000, 'c': 225}, 'x': mk, 'dp': 1, 'unit': 'percent'})

tc = 108 * D('0.85')
add('2-3-2', '3.2', MA, 'Pricing and target costing', 2, 'Glacier Gear currently sells a backpack for CHF 120. A competitor launches a similar product at CHF 105. Management decides to lower the price to CHF 108 and expects sales to rise by 10% from the current 15,000 units. What is the target cost per unit if the target operating income is 15% of sales? (Round to two decimals.)',
 [('CHF 89.25', 'Uses the competitor’s price of 105 instead of the new price of 108.', 'target-price-wrong'),
  ('CHF 91.80', '108 × (1 − 15%) = 91.80.', None),
  ('CHF 102.00', 'Uses the old price of 120.', 'target-price-wrong'),
  ('CHF 93.00', 'Subtracts CHF 15 instead of 15% of the price.', 'target-margin-absolute'),
  none_wrong('b')], 'b',
 'Target cost per unit = target price × (1 − target margin). The volume information is not needed for the per-unit target cost.', ev='ma-price',
 calc='Target cost = 108 × 0.85 = 91.80.', check={'f': 'p*(1 - m)', 'v': {'p': 108, 'm': D('0.15')}, 'x': tc, 'dp': 2})

pur = ((50_000 + 8_000 - 5_500) * 3 + 15_000 - 12_000) * 4
add('2-4-1', '4.1', BU, 'Purchases budget', 3, 'Bergkristall AG expects to sell 50,000 units next year. It targets an ending finished goods inventory of 8,000 units; the beginning inventory is 5,500 units. Each unit requires 3 kg of direct material at CHF 4 per kg. The beginning direct materials inventory is 12,000 kg, and the targeted ending inventory is 15,000 kg. What is the budgeted cost of direct material purchases?',
 [('CHF 660,000', 'Bases materials on sales units (50,000), not production, and leaves out the opening material inventory.', 'purchases-production-base'),
  ('CHF 630,000', 'This is the material used in production (157,500 kg × 4); the material inventory change is missing.', 'purchases-inventory-omitted'),
  ('CHF 642,000', '160,500 kg × CHF 4 = 642,000.', None),
  ('CHF 612,000', 'Uses sales units (50,000) instead of production units (52,500).', 'purchases-production-base'),
  none_wrong('c')], 'c',
 'Production = sales + ending FG − beginning FG; purchases = material needed + ending material − beginning material.', ev='budget',
 calc='Production = 50,000 + 8,000 − 5,500 = 52,500 units. Material needed = 157,500 kg. Purchases = 157,500 + 15,000 − 12,000 = 160,500 kg × 4 = 642,000.',
 check={'f': '((s + fe - fb)*k + me - mb)*c', 'v': {'s': 50_000, 'fe': 8_000, 'fb': 5_500, 'k': 3, 'me': 15_000, 'mb': 12_000, 'c': 4}, 'x': pur})

col = D('0.4') * 260_000 + D('0.5') * 240_000 + D('0.1') * 200_000
add('2-4-2', '4.2', BU, 'Cash collections', 2, 'Lindt Trading has budgeted sales of CHF 200,000 (September), CHF 240,000 (October) and CHF 260,000 (November). Customers pay 40% in the month of sale, 50% in the following month and 10% in the second month after the sale. How much cash will be collected from customers in November?',
 [('CHF 240,000', 'This is October sales, not November collections.', 'cash-collections-timing'),
  ('CHF 224,000', 'Leaves out the 10% still due from September (20,000).', 'cash-collections-timing'),
  ('CHF 260,000', 'This is November sales; only 40% of it is collected in November.', 'cash-collections-timing'),
  ('CHF 252,000', 'Does not match 40% × 260,000 + 50% × 240,000 + 10% × 200,000.', 'cash-collections-timing'),
  none_right('November = 104,000 + 120,000 + 20,000 = 244,000, which is not listed.')], 'e',
 'Cash collected in a month = 40% of that month’s sales + 50% of last month’s + 10% of the month before.', ev='budget',
 calc='40% × 260,000 + 50% × 240,000 + 10% × 200,000 = 104,000 + 120,000 + 20,000 = 244,000.',
 check={'f': 'a*n + b*o + c*s', 'v': {'a': D('0.4'), 'n': 260_000, 'b': D('0.5'), 'o': 240_000, 'c': D('0.1'), 's': 200_000}, 'x': col})

SIMM = ('Simmental AG reports the following data for the period:\n\n'
        + table(['', 'Actual', 'Static budget'], [['Units sold', '18,000', '20,000'], ['Selling price per unit', 'CHF 52', 'CHF 50'],
                                                  ['Variable costs (total)', 'CHF 558,000', 'CHF 30 per unit'], ['Fixed costs', 'CHF 155,000', 'CHF 150,000']]))
sv = (18_000 - 20_000) * (50 - 30)
add('2-5-1', '5.1', VA, 'Flexible-budget variance', 2, 'What is the sales-volume variance of the operating income?',
 [('CHF 13,000 favorable', 'This is the flexible-budget variance (223,000 vs 210,000).', 'variance-type'),
  ('CHF 40,000 unfavorable', '(18,000 − 20,000) × (50 − 30) = −40,000 → 40,000 U.', None),
  ('CHF 27,000 unfavorable', 'This is the static-budget variance (223,000 vs 250,000).', 'variance-type'),
  ('CHF 40,000 favorable', 'Right size, wrong direction: selling fewer units than budgeted lowers income.', 'variance-direction'),
  none_wrong('b')], 'b',
 'Sales-volume variance = (actual units − budgeted units) × budgeted contribution margin per unit.', scenario=SIMM, ev='variance',
 calc='(18,000 − 20,000) × (50 − 30) = −40,000 → 40,000 U. Static-budget variance = 27,000 U; flexible-budget variance = 13,000 F.',
 check={'f': '(a - b)*(p - v)', 'v': {'a': 18_000, 'b': 20_000, 'p': 50, 'v': 30}, 'x': sv, 'same': 'd'})

ev52 = (37_800 - 18_000 * 2) * 6
add('2-5-2', '5.2', VA, 'Direct material variances', 3, 'Bodensee Paper AG has a standard of 2 kg of direct materials per unit at CHF 6.00 per kg. In March, it produced 18,000 units and used 37,800 kg of material, which it purchased at CHF 5.80 per kg. What is the direct material efficiency variance?',
 [('CHF 10,440 unfavorable', 'Uses the actual price of 5.80 instead of the budgeted price of 6.00.', 'efficiency-actual-price'),
  ('CHF 10,800 unfavorable', '(37,800 − 36,000) × 6.00 = 10,800 U.', None),
  ('CHF 7,560 favorable', 'This is the price variance: (5.80 − 6.00) × 37,800.', 'variance-type'),
  ('CHF 10,800 favorable', 'Using more material than the standard allows is unfavorable.', 'variance-direction'),
  none_wrong('b')], 'b',
 'Efficiency variance = (actual quantity − budgeted quantity for actual output) × budgeted price.', ev='variance',
 calc='Budgeted quantity = 18,000 × 2 = 36,000 kg. (37,800 − 36,000) × 6.00 = 10,800 U. (Price variance = (5.80 − 6.00) × 37,800 = 7,560 F.)',
 check={'f': '(a - u*s)*p', 'v': {'a': 37_800, 'u': 18_000, 's': 2, 'p': 6}, 'x': ev52, 'same': 'd'})

add('2-5-3', '5.3', VA, 'Direct material variances', 1, 'Which of the following is the most likely cause of an unfavorable direct material efficiency variance combined with a favorable price variance?',
 [('Wage rates were higher than budgeted', 'Wage rates affect labor variances, not material variances.', 'variance-cause'),
  ('The budgeted selling price was set too low', 'The selling price affects the sales variances, not material variances.', 'variance-cause'),
  ('Fixed overhead costs increased', 'Fixed overhead has nothing to do with material price or usage.', 'variance-cause'),
  ('The purchasing manager bought lower-quality material at a discount', 'Cheaper material gives a favorable price variance, but more scrap and rework raise usage.', None),
  none_wrong('d')], 'd',
 'Cheaper, lower-quality material leads to a favorable price variance but more scrap and rework, and therefore an unfavorable efficiency variance.', ev='variance')

sp = (D(115_200) / 4_800 - 25) * 4_800
add('2-6-1', '6.1', VA, 'Variable-overhead variances', 3, 'Säntis Tools allocates variable manufacturing overhead using machine-hours. The budgeted rate is CHF 25 per machine-hour, and the standard is 0.5 machine-hours per unit. Actual output was 9,000 units, using 4,800 machine-hours. Actual variable manufacturing overhead costs were CHF 115,200. What is the variable overhead spending variance?',
 [('CHF 4,800 unfavorable', 'Right size, wrong direction: the actual rate (24) is below the budgeted rate (25).', 'variance-direction'),
  ('CHF 7,500 unfavorable', 'This is the efficiency variance: (4,800 − 4,500) × 25.', 'variance-type'),
  ('CHF 2,700 unfavorable', 'This is the total flexible-budget variance.', 'variance-type'),
  ('CHF 4,800 favorable', '(24 − 25) × 4,800 = −4,800 → 4,800 F.', None),
  none_wrong('d')], 'd',
 'Spending variance = (actual rate − budgeted rate) × actual machine-hours.', ev='variance',
 calc='Actual rate = 115,200 / 4,800 = 24. Spending variance = (24 − 25) × 4,800 = −4,800 → 4,800 F. (Efficiency variance = 7,500 U; total = 2,700 U.)',
 check={'f': '(c/h - r)*h', 'v': {'c': 115_200, 'h': 4_800, 'r': 25}, 'x': sp, 'same': 'a'})

add('2-6-2', '6.2', VA, 'Fixed-overhead variances', 1, 'Which statement about fixed manufacturing overhead variances is correct?',
 [('Fixed overhead has a price and an efficiency variance like direct materials', 'Fixed overhead has a spending and a production-volume variance, not an efficiency variance.', 'fixed-overhead-variances'),
  ('There is no efficiency variance for fixed overhead costs', 'Fixed costs do not change with output, so there is no efficiency variance.', None),
  ('The production-volume variance measures the difference between actual and budgeted fixed costs', 'That is the spending variance. The production-volume variance compares budgeted and allocated fixed overhead.', 'fixed-overhead-variances'),
  ('The flexible-budget amount for fixed overhead changes with actual output', 'For fixed overhead the flexible budget equals the static budget.', 'fixed-overhead-variances'),
  none_wrong('b')], 'b',
 'Fixed costs do not vary with output: spending variance = actual − budgeted fixed costs; production-volume variance = budgeted − allocated fixed overhead.', ev='variance')

RHONE = ('Rhône Energy considers an investment with the following cash flows (no disposal value, no taxes). The required rate of return is 12%.\n\n'
         + table(['Year', '0', '1', '2', '3'], [['Cash flow (CHF)', '−200,000', '70,000', '80,000', '90,000'], ['PV factor (12%)', '1.000', '0.893', '0.797', '0.712']]))
npv = 70_000 * D('0.893') + 80_000 * D('0.797') + 90_000 * D('0.712') - 200_000
add('2-7-1', '7.1', CB, 'Net present value', 3, 'What is the net present value of the investment?',
 [('CHF 40,000', 'Undiscounted: 240,000 − 200,000.', 'npv-no-discounting'),
  ('CHF 9,650', 'Right size, wrong sign: the PV of the inflows (190,350) is below the outlay.', 'npv-sign'),
  ('CHF −12,480', 'Does not match 190,350 − 200,000.', 'npv-calculation'),
  ('CHF −9,650', '190,350 − 200,000 = −9,650 → reject.', None),
  none_wrong('d')], 'd',
 'NPV = present value of the inflows − initial investment.', scenario=RHONE, ev='capital',
 calc='PV of inflows = 70,000 × 0.893 + 80,000 × 0.797 + 90,000 × 0.712 = 62,510 + 63,760 + 64,080 = 190,350. NPV = 190,350 − 200,000 = −9,650.',
 check={'f': 'a*fa + b*fb + c*fc - i', 'v': {'a': 70_000, 'fa': D('0.893'), 'b': 80_000, 'fb': D('0.797'), 'c': 90_000, 'fc': D('0.712'), 'i': 200_000}, 'x': npv, 'same': 'b'})

pb = 2 + D(200_000 - 70_000 - 80_000) / 90_000
add('2-7-2', '7.2', CB, 'Payback period', 2, 'What is the (static) payback period? (Round to one decimal.)',
 [('2.3 years', 'Too short: after two years 50,000 is still open, and 50,000 / 90,000 = 0.56 of year 3.', 'payback-calculation'),
  ('3.0 years', 'Counts full years only; the remaining 50,000 is recovered part-way through year 3.', 'payback-whole-years'),
  ('2.9 years', 'Too long: 50,000 / 90,000 = 0.56 of year 3, so payback is 2.6 years.', 'payback-calculation'),
  ('2.6 years', '2 + 50,000 / 90,000 = 2.56 → 2.6 years.', None),
  none_wrong('d')], 'd',
 'Static payback = full years until the outlay is almost recovered + the remaining amount / next year’s cash flow.', scenario=RHONE, ev='capital',
 calc='Cumulative: 70,000 (year 1), 150,000 (year 2). Remaining 50,000 / 90,000 = 0.56 → 2.6 years.',
 check={'f': '2 + (i - a - b)/c', 'v': {'i': 200_000, 'a': 70_000, 'b': 80_000, 'c': 90_000}, 'x': pb, 'dp': 1, 'unit': 'years'})

aarr = 100 * (D(70_000 + 80_000 + 90_000) / 3 - D(200_000) / 3) / 200_000
add('2-7-3', '7.3', CB, 'Accounting rate of return', 2, 'Compute the accrual accounting rate of return (AARR) based on the net initial investment (straight-line depreciation). (Round to one decimal.)',
 [('6.7%', '13,333 / 200,000 = 6.7%.', None),
  ('40.0%', 'Uses the average cash inflow (80,000) and ignores depreciation.', 'aarr-cash-flow'),
  ('4.4%', 'Too low: average net income is 80,000 − 66,667 = 13,333, divided by 200,000.', 'aarr-calculation'),
  ('13.3%', 'Based on the average investment of 100,000, not the net initial investment.', 'aarr-average-investment'),
  none_wrong('a')], 'a',
 'AARR = average annual net income / net initial investment, where net income = cash inflow − depreciation.', scenario=RHONE, ev='capital',
 calc='Average annual cash inflow = 240,000 / 3 = 80,000; depreciation = 200,000 / 3 = 66,667. Average net income = 13,333. AARR = 13,333 / 200,000 = 6.7%.',
 check={'f': '100*((a + b + c)/3 - i/3)/i', 'v': {'a': 70_000, 'b': 80_000, 'c': 90_000, 'i': 200_000}, 'x': aarr, 'dp': 1, 'unit': 'percent'})

add('2-7-4', '7.4', CB, 'AARR and IRR', 1, 'Which statement about the internal rate of return (IRR) is correct?',
 [('The IRR ignores the time value of money', 'IRR is a discounted cash flow method.', 'irr-concept'),
  ('The IRR is the discount rate at which the NPV of the project equals zero', 'That is the definition of the IRR.', None),
  ('The IRR is expressed as an absolute amount in CHF', 'The IRR is a percentage rate.', 'irr-concept'),
  ('A project is acceptable if its IRR is below the required rate of return', 'A project is acceptable if IRR ≥ the required rate of return.', 'irr-concept'),
  none_wrong('b')], 'b',
 'IRR = discount rate at which NPV = 0. A project is acceptable if IRR ≥ required rate of return.', ev='capital')

add('2-8-1', '8.1', CP, 'Balanced scorecard perspectives', 1, 'Which of the following is a measure of the balanced scorecard’s internal business process perspective?',
 [('Return on investment', 'ROI belongs to the financial perspective.', 'bsc-perspective'),
  ('Customer retention rate', 'Customer retention belongs to the customer perspective.', 'bsc-perspective'),
  ('Manufacturing cycle time / defect rate', 'Quality, cycle time and productivity are process measures.', None),
  ('Employee satisfaction', 'Employee satisfaction belongs to the learning and growth perspective.', 'bsc-perspective'),
  none_wrong('c')], 'c',
 'Process perspective: quality, cycle time and productivity.', ev='cpm')

add('2-8-2', '8.2', CP, 'Balanced scorecard purpose', 1, 'Which statement about the balanced scorecard is correct?',
 [('It should be kept secret from employees', 'The BSC should be communicated broadly so employees can act on it.', 'bsc-purpose'),
  ('It focuses exclusively on financial measures', 'It combines financial and non-financial measures.', 'bsc-purpose'),
  ('It combines financial and non-financial as well as leading and lagging measures', 'The BSC links the strategy to measures across four perspectives.', None),
  ('It should be designed only by external consultants', 'The BSC translates the company’s own strategy, so management owns it.', 'bsc-purpose'),
  none_wrong('c')], 'c',
 'The BSC translates the strategy into objectives and measures across four perspectives and combines financial and non-financial, leading and lagging indicators.', ev='cpm')

ic = D(8_000_000) * D('0.09') / D('0.18')
add('2-9-1', '9.1', CP, 'Return on investment', 2, 'The Outdoor division of Alpinco has revenues of CHF 8,000,000, an EBIT-based return on sales (ROS) of 9% and an EBIT-based return on investment (ROI) of 18%. What are the division’s operating assets (invested capital)?',
 [('CHF 16,000,000', 'Multiplies revenue by the asset turnover of 2 instead of dividing by it.', 'roi-dupont'),
  ('CHF 1,440,000', 'Applies the ROI to revenue (8,000,000 × 18%).', 'roi-dupont'),
  ('CHF 4,000,000', 'EBIT 720,000 / 18% = 4,000,000.', None),
  ('CHF 8,000,000', 'This is revenue, not invested capital.', 'roi-dupont'),
  none_wrong('c')], 'c',
 'Invested capital = EBIT / ROI, with EBIT = ROS × revenue.', ev='cpm',
 calc='EBIT = 9% × 8,000,000 = 720,000. Invested capital = 720,000 / 18% = 4,000,000 (asset turnover 2.0; DuPont: 9% × 2.0 = 18%).',
 check={'f': 's*r/i', 'v': {'s': 8_000_000, 'r': D('0.09'), 'i': D('0.18')}, 'x': ic})

HELIX = ('Helix Group has two sources of funds: long-term debt with a market and book value of CHF 6,000,000 at an interest rate of 6%, and equity with a market value of CHF 9,000,000 '
         '(book value CHF 5,000,000). The cost of equity is 12% and the tax rate is 25%. The divisions report the following:\n\n'
         + table(['Division', 'EBIT', 'Total assets', 'Current liabilities'], [['Zurich', 'CHF 1,200,000', 'CHF 8,000,000', 'CHF 1,000,000'], ['Basel', 'CHF 900,000', 'CHF 5,000,000', 'CHF 600,000']]))
wacc = (6_000_000 * D('0.06') * D('0.75') + 9_000_000 * D('0.12')) / 15_000_000
eva = 1_200_000 * D('0.75') - wacc * (8_000_000 - 1_000_000)
add('2-9-2', '9.2', CP, 'Economic value added', 3, 'What is the EVA of the Zurich division? (Round interim results to four decimals.)',
 [('CHF 570,000', 'Uses pre-tax EBIT: 1,200,000 − 630,000.', 'eva-pretax'),
  ('CHF 270,000', '900,000 − 9% × 7,000,000 = 270,000.', None),
  ('CHF 180,000', 'Charges capital on total assets (8,000,000) instead of total assets minus current liabilities.', 'eva-capital-base'),
  ('CHF 345,000', 'Weights the WACC with the book value of equity (about 7.9%) instead of market values.', 'wacc-book-values'),
  none_wrong('b')], 'b',
 'EVA = EBIT × (1 − t) − WACC × (total assets − current liabilities), with the WACC weighted at market values.', scenario=HELIX, ev='cpm',
 calc='WACC = (6 m × 6% × (1 − 25%) + 9 m × 12%) / 15 m = (270,000 + 1,080,000) / 15,000,000 = 9%. EVA = 1,200,000 × 0.75 − 9% × 7,000,000 = 900,000 − 630,000 = 270,000.',
 check={'f': 'e*(1 - t) - (a - l)*(d*rd*(1 - t) + q*re)/(d + q)', 'v': {'e': 1_200_000, 't': D('0.25'), 'a': 8_000_000, 'l': 1_000_000, 'd': 6_000_000, 'rd': D('0.06'), 'q': 9_000_000, 're': D('0.12')}, 'x': eva})
