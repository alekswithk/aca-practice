"""20 AI-generated Consolidated Statements questions."""
from ai_common import add, D, r, chf, n, table
T = 'Consolidated Statements'
ACQ_ASSUME = ['Course acquisition model: control, partial goodwill, NCI at its share of fair-value net assets, no deferred tax on hidden reserves, no transaction costs or post-acquisition movements.']

# Scenario A: Arvento AG / Kestrel Systems AG
pa = {'ca': 1_850_000, 'nca': 9_600_000, 'ap': 1_150_000, 'ltd': 3_900_000, 'eq': 6_400_000}
sa = {'ca': 980_000, 'nca': 2_640_000, 'ap': 520_000, 'ltd': 1_100_000, 'eq': 2_000_000}
assert pa['ca'] + pa['nca'] == pa['ap'] + pa['ltd'] + pa['eq'] and sa['ca'] + sa['nca'] == sa['ap'] + sa['ltd'] + sa['eq']
price, share, hr = 2_400_000, 0.7, 300_000
fvna = sa['eq'] + hr; gw = price - share * fvna; nci = (1 - share) * fvna
total_assets = pa['ca'] + pa['nca'] - price + sa['ca'] + sa['nca'] + hr + gw
ACQ = ('Arvento AG acquired 70% of Kestrel Systems AG on 31 December 2025 for CHF 2,400,000 in cash. Kestrel owns land with hidden reserves of CHF 300,000 that are not in its balances. '
       'Arvento’s balances already reflect the purchase; the investment in Kestrel (CHF 2,400,000) is included in its non-current assets.\n\n'
       + table(['Balance at 31.12.2025 (CHF)', 'Arvento AG', 'Kestrel Systems AG'],
               [['Current assets', n(pa['ca']), n(sa['ca'])], ['Non-current assets', n(pa['nca']), n(sa['nca'])],
                ['Accounts payable', n(pa['ap']), n(sa['ap'])], ['Long-term debt', n(pa['ltd']), n(sa['ltd'])], ['Equity', n(pa['eq']), n(sa['eq'])]]))
G = 'Arvento/Kestrel acquisition'
add('ai-cs-01', T, 'Acquisition accounting', 'Medium', 'Does goodwill arise in Arvento’s consolidated financial statements? If so, how much under the method learned in class?',
 [(f'Yes; {chf(price - fvna)}', 'Subtracts 100% of the fair-value net assets. Arvento bought only 70%, so only 70% is compared with the price.', 'goodwill-whole-assets'),
  (f'Yes; {chf(price - share*sa["eq"])}', 'Uses book equity and leaves out the CHF 300,000 hidden reserves on the land.', 'goodwill-ignore-reserves'),
  (f'Yes; {chf(gw)}', f'2,400,000 − 70% × (2,000,000 + 300,000) = 2,400,000 − {n(share*fvna)} = {chf(gw)}.', None),
  ('No goodwill is recognized', f'The price is above the acquired share of {chf(share*fvna)}, so goodwill remains.', 'goodwill-zero')],
 'c', 'Partial goodwill = purchase price − acquired share of fair-value net assets (book equity + hidden reserves).', scenario=ACQ, assume=ACQ_ASSUME, ev='acquisition',
 calc=f'FV net assets = 2,000,000 + 300,000 = {n(fvna)}. Goodwill = 2,400,000 − 0.7 × {n(fvna)} = {chf(gw)}.',
 check={'f': 'p - s*(e + h)', 'v': {'p': price, 's': share, 'e': sa['eq'], 'h': hr}, 'x': gw}, group=G)
add('ai-cs-02', T, 'Acquisition accounting', 'Medium', 'What is the value of the non-controlling interest on Arvento’s consolidated balance sheet at 31 December 2025?',
 [(chf((1-share)*sa['eq']), 'Leaves out the minority’s share of the hidden reserves.', 'nci-ignore-reserves'),
  (chf(nci), f'30% × (2,000,000 + 300,000) = {chf(nci)}.', None),
  (chf(share*fvna), 'This is Arvento’s 70% share, not the 30% held by outside shareholders.', 'nci-parent-share'),
  (chf((1-share)*price), 'Bases NCI on the price Arvento paid. Under partial goodwill, NCI is a share of net assets.', 'nci-purchase-price')],
 'b', 'Under partial goodwill, NCI = minority share × fair-value net assets of the subsidiary.', scenario=ACQ, assume=ACQ_ASSUME, ev='acquisition',
 calc=f'NCI = 30% × {n(fvna)} = {chf(nci)}.', check={'f': '(1-s)*(e + h)', 'v': {'s': share, 'e': sa['eq'], 'h': hr}, 'x': nci}, group=G)
add('ai-cs-03', T, 'Acquisition accounting', 'Easy', 'What is the equity attributable to Arvento AG shareholders on the consolidated balance sheet at 31 December 2025?',
 [(chf(pa['eq'] + sa['eq']), 'Adds Kestrel’s equity. Kestrel’s equity is eliminated against the investment at acquisition.', 'equity-add-subsidiary'),
  (chf(pa['eq'] + nci), 'Includes NCI. NCI is shown in equity, but separately from the equity attributable to the parent.', 'parent-equity-includes-nci'),
  (chf(pa['eq'] + gw), 'Adds goodwill to equity. Goodwill replaces part of the investment on the asset side; it does not create equity.', 'goodwill-nci-confusion'),
  (chf(pa['eq']), 'At the acquisition date, equity attributable to the parent equals the parent’s own equity.', None)],
 'd', 'At acquisition, the subsidiary’s equity is fully eliminated, so parent-attributable equity equals the parent’s equity.', scenario=ACQ, assume=ACQ_ASSUME, ev='acquisition',
 calc=f'Equity attributable to Arvento = {chf(pa["eq"])} (Kestrel’s equity is eliminated).', check={'f': 'e', 'v': {'e': pa['eq']}, 'x': pa['eq']}, group=G)
add('ai-cs-04', T, 'Acquisition accounting', 'Hard', 'What are total assets on Arvento’s consolidated balance sheet at 31 December 2025?',
 [(chf(pa['ca']+pa['nca']+sa['ca']+sa['nca']), 'Adds both balance sheets without removing the investment or adding hidden reserves and goodwill.', 'consolidation-parent-only'),
  (chf(total_assets), f'Remove the CHF 2,400,000 investment, add Kestrel’s assets, the CHF 300,000 hidden reserves and goodwill of {chf(gw)}: {chf(total_assets)}.', None),
  (chf(total_assets - hr - gw), 'Removes the investment but forgets the hidden reserves and goodwill that replace it.', 'goodwill-ignore-reserves'),
  (chf(total_assets + price), 'Keeps the investment in Kestrel. It is eliminated against Kestrel’s equity in consolidation.', 'intragroup-not-eliminated')],
 'b', 'Consolidated assets = parent assets − investment + subsidiary assets at fair value (book + hidden reserves) + goodwill.', scenario=ACQ, assume=ACQ_ASSUME, ev='acquisition',
 calc=f'{n(pa["ca"]+pa["nca"])} − 2,400,000 + {n(sa["ca"]+sa["nca"])} + 300,000 + {n(gw)} = {chf(total_assets)}. Check: liabilities {n(pa["ap"]+pa["ltd"]+sa["ap"]+sa["ltd"])} + equity {n(pa["eq"]+nci)} = {n(total_assets)}.',
 check={'f': 'a - p + b + h + p - s*(e + h)', 'v': {'a': pa['ca']+pa['nca'], 'p': price, 'b': sa['ca']+sa['nca'], 'h': hr, 's': share, 'e': sa['eq']}, 'x': total_assets}, group=G)
add('ai-cs-05', T, 'Acquisition accounting', 'Medium', 'What is total equity, including non-controlling interest, on Arvento’s consolidated balance sheet at 31 December 2025?',
 [(chf(pa['eq'] + nci), f'Parent equity {n(pa["eq"])} + NCI {n(nci)} = {chf(pa["eq"]+nci)}.', None),
  (chf(pa['eq']), 'This is only the equity attributable to Arvento. NCI is also part of consolidated equity.', 'nci-balance-sheet-only'),
  (chf(pa['eq'] + sa['eq']), 'Adds all of Kestrel’s book equity instead of the NCI.', 'equity-add-subsidiary'),
  (chf(pa['eq'] + (1-share)*sa['eq']), 'Uses NCI without the minority’s share of the hidden reserves.', 'nci-ignore-reserves')],
 'a', 'Consolidated equity = equity attributable to the parent + non-controlling interest.', scenario=ACQ, assume=ACQ_ASSUME, ev='acquisition',
 calc=f'{n(pa["eq"])} + {n(nci)} = {chf(pa["eq"]+nci)}.', check={'f': 'q + (1-s)*(e+h)', 'v': {'q': pa['eq'], 's': share, 'e': sa['eq'], 'h': hr}, 'x': pa['eq']+nci}, group=G)

# Scenario B: equity method, Polaris AG / Nimbus Foods AG
cost, sh, hr_b, life, profit, div = 4_200_000, 0.35, 900_000, 6, 1_500_000, 400_000
inc = sh * profit - sh * hr_b / life; close = cost + inc - sh * div
EQS = ('On 1 January 2025, Polaris AG buys 35% of Nimbus Foods AG for CHF 4,200,000 and gains significant influence. At that date Nimbus’s production equipment has hidden reserves of CHF 900,000 (for 100% of Nimbus), with a remaining useful life of six years. '
       'In 2025 Nimbus reports a profit of CHF 1,500,000 and pays a dividend of CHF 400,000.')
EQA = ['Equity method; ownership unchanged during 2025; no impairment, no intragroup transactions and no tax effect on the hidden reserves.']
G = 'Polaris/Nimbus equity method'
add('ai-cs-06', T, 'Equity method', 'Hard', 'What is the carrying amount of Polaris’s equity-accounted investment in Nimbus on 31 December 2025?',
 [(chf(cost + sh*profit - sh*div), 'Leaves out the extra depreciation on Polaris’s share of the hidden reserves.', 'equity-ignore-reserves'),
  (chf(cost + sh*profit), 'Ignores the dividend. Dividends received reduce the investment.', 'equity-ignore-dividends'),
  (chf(close), f'4,200,000 + 35% × 1,500,000 − 35% × 150,000 − 35% × 400,000 = {chf(close)}.', None),
  (chf(cost + sh*profit - sh*div - hr_b/life), 'Deducts the full CHF 150,000 depreciation on the hidden reserves instead of Polaris’s 35% share.', 'equity-whole-reserves')],
 'c', 'Investment = cost + share of profit − share of hidden-reserve depreciation − share of dividends.', scenario=EQS, assume=EQA, ev='equity',
 calc=f'Hidden-reserve depreciation = 900,000 / 6 = 150,000 (Polaris share 52,500). Closing = 4,200,000 + 525,000 − 52,500 − 140,000 = {chf(close)}.',
 check={'f': 'c + s*(p - h/l - d)', 'v': {'c': cost, 's': sh, 'p': profit, 'h': hr_b, 'l': life, 'd': div}, 'x': close}, group=G)
add('ai-cs-07', T, 'Equity method', 'Medium', 'How much income from the associate does Polaris report in its 2025 consolidated income statement?',
 [(chf(sh*profit), 'Leaves out Polaris’s share of the extra depreciation on the hidden reserves.', 'equity-ignore-reserves'),
  (chf(inc), f'35% × (1,500,000 − 150,000) = {chf(inc)}.', None),
  (chf(sh*div), 'This is Polaris’s share of the dividend. Dividends are not income under the equity method.', 'equity-dividend-income'),
  (chf(inc - sh*div), 'Deducts the dividend from income. The dividend reduces the investment, not the share of profit.', 'equity-dividend-income')],
 'b', 'Equity-method income = investor’s share of the associate’s profit, adjusted for depreciation of hidden reserves.', scenario=EQS, assume=EQA, ev='equity',
 calc=f'35% × 1,500,000 = 525,000; less 35% × 150,000 = 52,500; income = {chf(inc)}.', check={'f': 's*(p - h/l)', 'v': {'s': sh, 'p': profit, 'h': hr_b, 'l': life}, 'x': inc}, group=G)
add('ai-cs-08', T, 'Equity method', 'Easy', 'How does the dividend Polaris receives from Nimbus affect Polaris’s consolidated accounts?',
 [(f'Income of {chf(sh*div)}; the investment is unchanged', 'Under the equity method the dividend is not income. Polaris already took its share of the profit.', 'equity-dividend-income'),
  (f'Cash rises and the investment falls by {chf(sh*div)}', 'The dividend converts part of the investment into cash.', None),
  (f'Cash rises and the investment falls by {chf(div)}', 'Uses Nimbus’s whole dividend. Polaris receives only 35%.', 'equity-whole-dividend'),
  ('No effect, because Nimbus is not consolidated', 'Cash comes in and the investment goes down, so there is an effect.', 'equity-ignore-dividends')],
 'b', 'Dividends from an associate reduce the carrying amount of the investment.', scenario=EQS, assume=EQA, ev='equity',
 calc=f'35% × 400,000 = {chf(sh*div)}.', check={'f': 's*d', 'v': {'s': sh, 'd': div}, 'x': sh*div, 'same': 'a'}, group=G)
add('ai-cs-09', T, 'Equity method', 'Medium', 'When using the equity method, the equity-accounted investment is NOT affected when …',
 [('the associate reports a loss for the year.', 'A loss reduces the investment by the investor’s share.', 'equity-ignore-profit'),
  ('the associate pays a dividend.', 'A dividend reduces the investment.', 'equity-ignore-dividends'),
  ('the investor guarantees a bank loan taken by the associate.', 'A guarantee is a possible obligation of the investor. It does not change the associate’s net assets or the investment balance.', None),
  ('hidden reserves identified at purchase are depreciated.', 'The investor’s share of that depreciation reduces the investment.', 'equity-ignore-reserves')],
 'c', 'The investment moves with the investor’s share of the associate’s profit, dividends and hidden-reserve depreciation.', ev='equity')
add('ai-cs-10', T, 'Equity method', 'Easy', 'True or false: An investor that holds 20% to 50% of the voting rights is usually presumed to have significant influence and applies the equity method.',
 [('True', '20% to 50% is the usual range for significant influence without control.', None),
  ('False', 'This is the standard presumption for associates.', 'ownership-control')],
 'a', 'Significant influence is usually presumed between 20% and 50% of voting rights.', ev='equity')

# Consolidation concepts
pr, sr, ig = 3_200_000, 1_800_000, 500_000
add('ai-cs-11', T, 'Consolidation concepts', 'Medium', 'Ravello Group consists of Ravello AG and its 100% subsidiary Brisa SA. During 2025 Ravello AG sold goods to Brisa for CHF 500,000; Brisa sold all of them to outside customers before year-end.\n\n'
 + table(['Revenue 2025 (CHF)', 'Amount'], [['Ravello AG (including sales to Brisa)', n(pr)], ['Brisa SA', n(sr)]]) + '\n\nWhat is consolidated revenue for 2025?',
 [(chf(pr + sr), 'Adds both revenues without eliminating the intragroup sale.', 'intragroup-not-eliminated'),
  (chf(pr + sr - 2*ig), 'Eliminates the intragroup amount twice. Only the internal sale of CHF 500,000 is removed.', 'intragroup-not-eliminated'),
  (chf(pr), 'Reports only the parent’s revenue. Consolidated statements include the subsidiary.', 'consolidation-parent-only'),
  (chf(pr + sr - ig), f'3,200,000 + 1,800,000 − 500,000 = {chf(pr+sr-ig)}.', None)],
 'd', 'Intragroup sales are eliminated so that the group only reports sales to outside parties.', ev='acquisition',
 calc=f'{n(pr)} + {n(sr)} − {n(ig)} = {chf(pr+sr-ig)}.', check={'f': 'a + b - c', 'v': {'a': pr, 'b': sr, 'c': ig}, 'x': pr+sr-ig})
add('ai-cs-12', T, 'Consolidation concepts', 'Easy', 'Which statement about non-controlling interests (NCI) is correct?',
 [('NCI are shown as a liability because they belong to outside shareholders.', 'NCI are part of group equity, presented separately from the parent’s equity.', 'nci-balance-sheet-only'),
  ('NCI appear in consolidated equity and as a share of consolidated profit.', 'Both the balance sheet and the income statement show the NCI share.', None),
  ('NCI only arise when the parent owns less than 50%.', 'Below 50% (without other control) there is usually no subsidiary. NCI arise when the parent controls but owns less than 100%.', 'ownership-control'),
  ('NCI are measured at the price the parent paid.', 'Under partial goodwill, NCI are a share of fair-value net assets.', 'nci-purchase-price')],
 'b', 'NCI are the outside shareholders’ share of a subsidiary’s equity and profit.', ev='acquisition')
add('ai-cs-13', T, 'Consolidation concepts', 'Medium', 'Which investment of Tavira Holding AG must be fully consolidated?',
 [('A 30% stake in Orla AG with two of nine board seats', 'This normally gives significant influence, so the equity method applies.', 'ownership-control'),
  ('A 45% stake in Vento SA, where a shareholder agreement gives Tavira the right to appoint the majority of the board', 'Control comes from the right to direct the company, here through the board majority, even below 50% of shares.', None),
  ('A 15% stake in a listed bank held for trading', 'This is a financial investment without control or significant influence.', 'ownership-control'),
  ('A 50% stake in a joint venture with equal joint control', 'Joint control means no single party controls; the joint venture is not fully consolidated.', 'ownership-control')],
 'b', 'Full consolidation follows control, which can exist without a share majority.', ev='acquisition')
add('ai-cs-14', T, 'Consolidation concepts', 'Easy', 'What is the main purpose of consolidated financial statements?',
 [('To replace the individual statutory accounts of each group company', 'Each company still prepares its own statutory accounts.', 'standards-replace-law'),
  ('To present the group as if it were a single economic entity', 'Consolidation shows the group’s assets, liabilities and results as one entity, with intragroup items eliminated.', None),
  ('To calculate the tax payable by the group', 'Tax is assessed on individual companies in Switzerland, not on the consolidated group.', 'consolidation-tax'),
  ('To show each subsidiary’s results in detail', 'Consolidation aggregates; it does not report each subsidiary in detail.', 'consolidation-subsidiary-detail')],
 'b', 'Consolidated statements give a true and fair view of the group as one economic unit.', ev='acquisition')

# Scenario C: acquisition with deferred tax
price_c, share_c, eq_c, hr_c, t_c = 5_600_000, 0.8, 4_500_000, 1_000_000, 0.2
fv_c = eq_c + hr_c * (1 - t_c); gw_c = price_c - share_c * fv_c; nci_c = (1 - share_c) * fv_c
TAXA = ('Corvana AG acquires 80% of Lindt-Schaller Pharma AG on 31 December 2025 for CHF 5,600,000. Lindt-Schaller’s book equity is CHF 4,500,000. Its patents have hidden reserves of CHF 1,000,000. '
        'The patents’ tax base is unchanged, so a deferred tax liability at 20% is recognized on the hidden reserves.')
TAXAS = ['Partial goodwill; NCI at proportionate fair-value net assets; deferred tax recognized on the uplift at 20%; no other adjustments.']
G = 'Corvana/Lindt-Schaller acquisition'
add('ai-cs-15', T, 'Acquisition accounting', 'Hard', 'What goodwill does Corvana recognize?',
 [(chf(price_c - share_c*(eq_c+hr_c)), 'Ignores the deferred tax liability on the hidden reserves, which reduces net assets.', 'acquisition-ignore-tax'),
  (chf(gw_c), f'Net assets = 4,500,000 + 1,000,000 − 200,000 = {n(fv_c)}. Goodwill = 5,600,000 − 80% × {n(fv_c)} = {chf(gw_c)}.', None),
  (chf(price_c - fv_c), 'Compares the price with 100% of net assets. Corvana bought 80%.', 'goodwill-whole-assets'),
  (chf(price_c - share_c*eq_c), 'Uses book equity and leaves out the hidden reserves (net of tax).', 'goodwill-ignore-reserves')],
 'b', 'Deferred tax on hidden reserves reduces the fair-value net assets, which raises goodwill.', scenario=TAXA, assume=TAXAS, ev='acquisition',
 calc=f'DTL = 1,000,000 × 20% = 200,000. FV net assets = {n(fv_c)}. Goodwill = 5,600,000 − {n(share_c*fv_c)} = {chf(gw_c)}.',
 check={'f': 'p - s*(e + h*(1-t))', 'v': {'p': price_c, 's': share_c, 'e': eq_c, 'h': hr_c, 't': t_c}, 'x': gw_c}, group=G)
add('ai-cs-16', T, 'Acquisition accounting', 'Hard', 'What is the non-controlling interest at acquisition?',
 [(chf((1-share_c)*(eq_c+hr_c)), 'Ignores the deferred tax on the hidden reserves.', 'acquisition-ignore-tax'),
  (chf((1-share_c)*eq_c), 'Uses book equity only.', 'nci-ignore-reserves'),
  (chf(nci_c), f'20% × {n(fv_c)} = {chf(nci_c)}.', None),
  (chf(share_c*fv_c), 'This is Corvana’s 80% share, not the outside shareholders’ 20%.', 'nci-parent-share')],
 'c', 'NCI = minority share of fair-value net assets after deferred tax.', scenario=TAXA, assume=TAXAS, ev='acquisition',
 calc=f'NCI = 20% × {n(fv_c)} = {chf(nci_c)}.', check={'f': '(1-s)*(e + h*(1-t))', 'v': {'s': share_c, 'e': eq_c, 'h': hr_c, 't': t_c}, 'x': nci_c}, group=G)
price_d, share_d, eq_d, hr_d = 1_150_000, 0.75, 1_400_000, 260_000
add('ai-cs-17', T, 'Acquisition accounting', 'Medium', 'Ostara AG acquires 75% of Pellmann AG for CHF 1,150,000. Pellmann’s book equity is CHF 1,400,000 and it has hidden reserves of CHF 260,000 on its warehouse. Does goodwill arise under the method learned in class? If so, how much?',
 [(f'Yes; {chf(price_d - share_d*eq_d)}', 'Ignores the hidden reserves. With them, the acquired share is worth more than the price.', 'goodwill-ignore-reserves'),
  (f'Yes; {chf(share_d*(eq_d+hr_d) - price_d)}', 'This is the amount by which the acquired share exceeds the price. A shortfall like this is not goodwill.', 'goodwill-zero'),
  ('No goodwill is recognized', f'The acquired share of {chf(share_d*(eq_d+hr_d))} exceeds the price of CHF 1,150,000, so no goodwill arises.', None),
  (f'Yes; {chf(price_d)}', 'The whole price is not goodwill; most of it pays for identifiable net assets.', 'goodwill-net-assets')],
 'c', 'Goodwill only arises when the price exceeds the acquired share of fair-value net assets. Under IFRS 3 a shortfall, after reassessment, is a bargain-purchase gain.', assume=ACQ_ASSUME, ev='acquisition',
 calc=f'Acquired share = 75% × (1,400,000 + 260,000) = {n(share_d*(eq_d+hr_d))}, above the price of 1,150,000. No goodwill.')

add('ai-cs-18', T, 'Accounting frameworks', 'Easy', 'Helvetra Group is listed on SIX and prepares its consolidated statements under Swiss GAAP FER. Which statement is correct?',
 [('Helvetra AG does not need statutory accounts under the CO because it applies FER.', 'FER is applied on top of the CO. The statutory accounts under the CO are still required.', 'standards-replace-law'),
  ('Helvetra AG still prepares statutory individual accounts under the Code of Obligations.', 'The CO is binding law for every Swiss company; FER is an additional standard.', None),
  ('FER follows prudence, so it allows hidden reserves in the consolidated statements.', 'FER aims at a true and fair view; hidden reserves are a feature of CO accounts.', 'framework-objective'),
  ('FER is a rule-based standard like US GAAP.', 'FER is principle-based.', 'framework-classification')],
 'b', 'Swiss companies always follow the CO; FER or IFRS add a true-and-fair-view reporting layer.', ev='frameworks')
add('ai-cs-19', T, 'Accounting frameworks', 'Easy', 'Select the response that best fills in the blanks: IFRS are ___-based, the CO follows the principle of ___, and Swiss GAAP FER aims at a ___.',
 [('rule; true and fair view; prudence', 'Mixes up the CO and FER, and labels IFRS rule-based.', 'framework-classification'),
  ('principle; prudence; true and fair view', 'IFRS are principle-based; the CO follows prudence; FER aims at a true and fair view.', None),
  ('principle; true and fair view; prudence', 'Swaps the objectives of the CO and FER.', 'framework-objective'),
  ('rule; prudence; true and fair view', 'IFRS are principle-based, not rule-based.', 'framework-classification')],
 'b', 'IFRS and FER: principle-based, true and fair view. CO: prudence. US GAAP: rule-based.', ev='frameworks')
add('ai-cs-20', T, 'Consolidation concepts', 'Medium', 'Saltera AG owns 80% of Ferrolux AG and controls it. How does Saltera present Ferrolux in its consolidated statements?',
 [('Equity method, with 80% of Ferrolux’s profit added to the investment', 'The equity method is for associates. A controlled subsidiary is fully consolidated.', 'ownership-control'),
  ('Full consolidation of 80% of Ferrolux’s assets and liabilities', 'Full consolidation includes 100% of the assets and liabilities; the outside 20% is shown as NCI.', 'nci-zero'),
  ('Full consolidation of 100% of Ferrolux’s assets and liabilities, with a 20% non-controlling interest', 'Control means 100% consolidation, with the minority’s share presented as NCI.', None),
  ('At cost, because Saltera does not own 100%', 'Ownership below 100% does not prevent consolidation when there is control.', 'ownership-control')],
 'c', 'Control leads to full consolidation of all assets and liabilities, with NCI for the outside share.', ev='acquisition')
