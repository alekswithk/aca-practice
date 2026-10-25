"""Captured Capital Budgeting and Cost and Performance Management questions."""
import re

CAP = 'Exam by topic/Capital Budgeting/Capital Budgeting Exam Bank.md'
CPM = 'Exam by topic/Cost and Performance Management/Cost and Performance Management Exam Bank.md'
SOURCES = {'capital-budgeting': CAP, 'cost-performance': CPM}


def _q(ident, topic, source, exam, number, marks, subtopic, scenario, prompt, choices, key, explanation, calculation=''):
    options = []
    for i, text in enumerate(choices):
        oid = 'abcde'[i]
        options.append(dict(id=oid, text=text,
                            explanation=explanation if oid == key else 'This does not match the source data or accounting method.',
                            misconception=None if oid == key else f'{topic.lower()}-calculation'))
    raw = prompt + '\n' + '\n'.join(f"- {o['id'].upper()}) {o['text']}" for o in options)
    return dict(id=ident, origin='original', topic=topic, subtopic=subtopic,
                difficulty='Medium', type='single-choice', marks=marks, prompt=prompt,
                scenario=scenario, assumptions=[], options=options, correctOptionId=key,
                explanation=explanation, workedCalculation=calculation,
                evidence=[dict(path=source, section=f'{exam}, Question {number}; expanded solution in Dia')],
                status='validated', reviewReason='', changes=[],
                targets=sorted({o['misconception'] for o in options if o['misconception']}),
                source=dict(path=source, heading=exam, number=number, line=None),
                original=dict(wording=prompt, options=[dict(id=o['id'], text=o['text']) for o in options],
                              raw=raw, scenario=scenario, recordedStudentAnswer=None,
                              answerProvenance='Answer checked against the expanded Ecoreps solution in Dia.'))


def import_capital_performance(root):
    q = []
    add = lambda *a: q.append(_q(*a))
    none = 'None of the answers A)–D) is correct.'
    add('cap-ss26-7.1', 'Capital Budgeting', CAP, 'SS26 Question 7', '7.1', 2, 'Accounting rate of return',
        'Proposal A costs CHF 90,000, lasts three years, has no terminal value, and generates cash-flow increases of CHF 80,000, CHF 10,000 and CHF 45,000. Straight-line depreciation applies.',
        'Compute the accounting rate of return on initial investment.', ['25.7%', '9.4%', '15.3%', '16.7%', none], 'd',
        'Average annual accounting income divided by the initial investment gives 16.7%.',
        'Depreciation = 90,000/3 = 30,000. Average cash flow = (80,000+10,000+45,000)/3 = 45,000. Average income = 45,000−30,000 = 15,000. ARR = 15,000/90,000 = 16.7%.')
    add('cap-ss26-7.2', 'Capital Budgeting', CAP, 'SS26 Question 7', '7.2', 2, 'Static payback period',
        'Net investment CHF 3,100,000; annual cash inflows CHF 500,000; useful life 10 years.',
        'Calculate the static payback period, rounded to one decimal place.', ['5.8 years', '10.0 years', '7.4 years', '6.2 years', none], 'd',
        'Divide the net investment by annual cash inflows. The useful life is not needed for static payback.',
        '3,100,000/500,000 = 6.2 years.')
    add('cap-ss26-7.3', 'Capital Budgeting', CAP, 'SS26 Question 7', '7.3', 1, 'Accounting rate of return limitations', '',
        'Which of the following is a limitation of the AARR method?',
        ['It does not consider the time value of money.', 'It is difficult to compare projects as AARR is expressed in dollars and not percentage terms.', 'It does not track initial investment.', 'It does not consider income earned throughout a project’s expected useful life.', none], 'a',
        'The expanded solution confirms A: AARR uses average annual net income without discounting, so it ignores time value of money.')
    add('cap-as25-7.1', 'Capital Budgeting', CAP, 'AS25 Question 7', '7.1', 2, 'Static payback period',
        'A machine costs CHF 340,480 and saves CHF 89,600 annually for six years, with no terminal value or tax.',
        'Calculate the static payback period.', ['3.8 years', '4.7 years', '5.0 years', '3.1 years', none], 'a',
        'The net investment is recovered in 3.8 years at the stated annual savings.',
        '340,480/89,600 = 3.8 years.')
    add('cpm-ss26-8.1', 'Cost and Performance Management', CPM, 'SS26 Question 8', '8.1', 1, 'Balanced scorecard', '',
        'Which question belongs to the learning-and-growth perspective?',
        ['How can employees be enabled to develop and contribute?', 'How can the company increase profit?', 'Which processes create customer value?', 'How can costs be reduced?', none], 'a',
        'Learning and growth concerns employee development and organizational capability.')
    add('cpm-ss26-8.2', 'Cost and Performance Management', CPM, 'SS26 Question 8', '8.2', 1, 'Balanced scorecard implementation', '',
        'Which statement about implementing a balanced scorecard is correct?',
        ['Management accountants should have no role in choosing measures.', 'External auditors should design and implement the scorecard.', 'The scorecard should be withheld from employees.', 'Only top management should form the scorecard.', none], 'e',
        'The expanded solution states that the listed A–D claims are incorrect; scorecard development involves internal stakeholders and communication.')
    add('cpm-ss26-9.1', 'Cost and Performance Management', CPM, 'SS26 Question 9', '9.1', 2, 'Weighted average cost of capital',
        'Debt market value CHF 32m at 10%; equity market value CHF 18m at a 15% required return; tax rate 30%.',
        'Calculate WACC using market-value weights.', ['8.60%', '12.12%', '9.88%', '9.22%', none], 'c',
        'Apply the after-tax cost of debt and market-value capital weights.',
        '(32/50×10%×(1−30%)) + (18/50×15%) = 9.88%.')
    add('cpm-ss26-9.2', 'Cost and Performance Management', CPM, 'SS26 Question 9', '9.2', 2, 'Return on sales',
        'The Acoustic division reports EBIT CHF 7,930,800 and return on sales of 15%.',
        'Calculate the division’s revenue.', ['CHF 43,254,600', 'CHF 65,500,789', 'CHF 52,872,000', 'CHF 49,567,500', none], 'c',
        'Revenue equals EBIT divided by return on sales.', '7,930,800/0.15 = CHF 52,872,000.')
    add('cpm-as25-8.1', 'Cost and Performance Management', CPM, 'AS25 Question 8', '8.1', 1, 'Balanced scorecard measures', '',
        'Which is a customer-perspective performance measure?',
        ['Process-improvement rate', 'Number of new customers acquired', 'Defect rate', 'Customer complaints', none], 'd',
        'Customer complaints measure customer experience; customer acquisition is a strategic objective rather than a customer-outcome measure.')
    add('cpm-as25-9.1', 'Cost and Performance Management', CPM, 'AS25 Question 9', '9.1', 2, 'Return on sales',
        'A division earns EBIT CHF 4,800,000 at a return on sales of 12%.',
        'Calculate its revenue.', ['CHF 65,000,000', 'CHF 12,500,564', 'CHF 31,733,333', 'CHF 51,500,923', none], 'e',
        'Revenue is CHF 40,000,000, which is not among A–D.', '4,800,000/0.12 = CHF 40,000,000; select E.')
    add('cpm-as25-9.2', 'Cost and Performance Management', CPM, 'AS25 Question 9', '9.2', 3, 'Economic value added',
        'Debt CHF 4m at 5%, market equity CHF 8m at 15%, tax 25%; division EBIT CHF 480,000, assets CHF 2m and current liabilities CHF 140,000.',
        'Calculate EVA.', ['CHF 150,750', 'CHF 191,580', 'CHF 175,116', 'CHF 360,000', none], 'a',
        'EVA equals NOPAT less the capital charge on invested capital.',
        'WACC = (8/12×15%) + (4/12×5%×(1−25%)) = 11.25%. Invested capital = 2,000,000−140,000 = 1,860,000. NOPAT = 480,000×75% = 360,000. EVA = 360,000−1,860,000×11.25% = CHF 150,750.')
    add('cpm-as24-8.1', 'Cost and Performance Management', CPM, 'AS24 Question 8', '8.1', 1, 'Balanced scorecard purpose', '',
        'Which statement best describes the balanced scorecard’s effect on performance management?',
        ['It prioritizes short-run nonfinancial results.', 'It weakens attention to long-run financial performance.', 'It prioritizes short-run financial results.', 'It reduces an exclusive focus on short-run financial performance.', none], 'd',
        'The balanced scorecard adds nonfinancial perspectives and counterbalances an exclusive short-run financial focus.')
    add('cpm-as24-8.2', 'Cost and Performance Management', CPM, 'AS24 Question 8', '8.2', 1, 'Balanced scorecard implementation', '',
        'Which statement about implementing a balanced scorecard is correct?',
        ['External auditors should design and implement it.', 'Management accountants should determine measures alone.', 'Only top management should develop it.', 'It should never be communicated to employees.', none], 'e',
        'The displayed A–D choices are inconsistent with shared internal development and communication; none is correct.')
    add('cap-screen-a-7.2', 'Capital Budgeting', CAP, 'Additional screenshot set A', '7.2', 1, 'Accounting rate of return limitations', '',
        'Which of the following is a limitation of the AARR method?',
        ['It does not consider time value of money.', 'It is difficult to compare projects because its result is expressed in dollars and not in percentage terms.', 'It does not track initial investment.', 'It does not consider income earned throughout a project’s expected useful life.', none], 'a',
        'AARR uses average annual net income without discounting it, so it does not account for time value of money.')
    add('cap-screen-a-7.3', 'Capital Budgeting', CAP, 'Additional screenshot set A', '7.3', 3, 'Net present value',
        'TechFlow proposal B requires CHF 60,000 initially. Cash inflows are CHF 45,000 in each of years 1 and 2, zero in year 3, and no disposal value. Required return is 20%; round present-value factors to three decimals.',
        'Calculate the net present value of Proposal B.', ['CHF 18,225', 'CHF 8,715', 'CHF 11,700', 'CHF 20,945', none], 'b',
        'Using the specified rounded discount factors, the NPV is CHF 8,715.',
        '−60,000 + 45,000×0.833 + 45,000×0.694 = CHF 8,715.')
    add('cap-mississippi-7.1', 'Capital Budgeting', CAP, 'Mississippi Company screenshot', '7.1', 2, 'Payback period',
        'A specially equipped van costs CHF 146,800 and generates additional annual cash inflows of CHF 44,400 for six years.',
        'Calculate the payback period, rounded to one decimal place.', ['2.0 years', '1.8 years', '3.3 years', '5.6 years', none], 'c',
        'Divide investment by annual cash inflow and round to one decimal.', '146,800/44,400 = 3.306… = 3.3 years.')
    add('cap-flexxon-7.2', 'Capital Budgeting', CAP, 'Flexxon Corp. screenshot', '7.2', 3, 'Net present value',
        'Machine cost CHF 280,000; annual savings CHF 165,000 for three years; terminal disposal value CHF 35,000; no tax effects; required return 14%.',
        'Calculate the project NPV.', ['CHF 190,880', 'CHF 87,750', 'CHF 103,130', 'CHF 126,693', none], 'd',
        'Discount each annual saving and the disposal proceeds in year 3.',
        'NPV = −280,000 + 165,000/1.14 + 165,000/1.14² + (165,000+35,000)/1.14³ = CHF 126,693 rounded.')
    add('cap-process-4.1', 'Capital Budgeting', CAP, 'Capital budgeting process screenshot', '4.1', 1, 'Capital budgeting process', '',
        'Which option describes the first stage in the capital budgeting process?',
        ['Forecasting cash flows for alternative projects.', 'Selecting the investment with greatest benefit and least cost.', 'Obtaining financing and making selected investments.', 'Identifying potential capital investments consistent with organizational strategy.', none], 'd',
        'The process begins by identifying potential investments that agree with organizational strategy.')
    add('cap-cleansvc-4.2', 'Capital Budgeting', CAP, 'Clean Service screenshot', '4.2', 4, 'Net present value',
        'Sell the current machine now for CHF 120,000. New machine costs CHF 580,000 and produces additional inflows CHF 200,000 in year 1 and CHF 280,000 in years 2 and 3. Three-year life, no terminal value or tax, required return 10%; source choice uses discount factors rounded to three decimals.',
        'Calculate NPV and decide whether to buy on financial grounds.', ['CHF 163,360; yes', 'CHF 210,368; yes', '−CHF 210,368; no', '−CHF 163,360; no', none], 'a',
        'Net initial outlay is CHF 460,000. Rounded factors give a positive NPV, so the investment is desirable.',
        '−460,000 + 200,000×0.909 + 280,000×0.826 + 280,000×0.751 = CHF 163,360. Exact factors give CHF 163,591; the source keys the rounded-factor answer A.')
    add('cap-aar-irr-4.3', 'Capital Budgeting', CAP, 'Capital budgeting methods screenshot', '4.3', 1, 'AARR and IRR', '',
        'Which statement about Accrual Accounting Rate of Return (AARR) and Internal Rate of Return (IRR) is true?',
        ['AARR gives absolute amounts while IRR gives percentages.', 'AARR uses operating income after accruals and taxes; IRR uses after-tax cash flows and time value of money.', 'AARR accounts for time value of money but IRR does not.', 'AARR uses cash flows while IRR uses operating income.', none], 'b',
        'AARR is based on accrual accounting income; IRR is a discounted cash-flow measure.')
    add('cap-qilti-7.1', 'Capital Budgeting', CAP, 'Qilti Corp. screenshot', '7.1', 2, 'Payback period',
        'Investment CHF 159,000; annual savings CHF 55,000; six-year life; zero terminal value; no tax effects.',
        'What is the payback period, rounded to one decimal place?', ['1.9 years', '2.9 years', '5.8 years', '6.0 years', none], 'b',
        'Payback is investment divided by annual cost savings.', '159,000/55,000 = 2.8909… = 2.9 years.')
    add('cap-difiend-6.1', 'Capital Budgeting', CAP, 'Difiend Cleaners screenshot', '6.1', 4, 'Net present value and working capital',
        'New machine CHF 430,000; working capital CHF 100,000 required and not recovered; old machine sale proceeds CHF 100,000 now. Additional cash inflows CHF 140,000 in year 1 and CHF 270,000 in years 2 and 3; no terminal value or taxes; return 9%.',
        'Calculate NPV and decide whether to buy. The source solution rounds discount factors to three decimals.',
        ['CHF −208,440; yes', 'CHF −134,160; no', 'CHF 134,160; yes', 'CHF 208,440; no', none], 'c',
        'The net initial investment is CHF 430,000 after including working capital and sale proceeds. Rounded discount factors yield positive NPV.',
        'Initial = 430,000+100,000−100,000 = CHF 430,000. NPV using .917, .842 and .772 = −430,000 + 140,000×.917 + 270,000×.842 + 270,000×.772 = CHF 134,160. Exact-factor NPV is CHF 134,183.50.')
    add('cap-malive-6.2', 'Capital Budgeting', CAP, 'Malive Park screenshot', '6.2', 2, 'Payback period',
        'Machine costs CHF 179,000 and saves CHF 35,000 annually; ten-year life, no terminal value or tax consequences.',
        'What is the payback period?', ['4.1 years', '5.1 years', '10.0 years', '10.2 years', none], 'b',
        'Payback is initial investment divided by annual savings.', '179,000/35,000 = 5.1143… = 5.1 years.')
    add('cpm-screen-3.4', 'Cost and Performance Management', CPM, 'Screenshot batch, Question 3', '3.4', 1, 'Balanced scorecard perspectives', '',
        'Which option is a performance measure of the financial perspective of the Balanced Scorecard?',
        ['Operating income', 'Service response time', 'Defect rates', 'Number of new patents', none], 'a',
        'Operating income is financial; service response time, defect rates and new patents represent internal-process measures.')
    add('cpm-screen-3.5', 'Cost and Performance Management', CPM, 'Screenshot batch, Question 3', '3.5', 1, 'Balanced scorecard perspectives', '',
        'Which question best describes the learning-and-growth perspective of the Balanced Scorecard?',
        ['How do we reduce costs?', 'How do we empower our employees?', 'Which processes will increase value for customers?', 'How can we achieve higher profits?', none], 'b',
        'Learning and growth focuses on employee learning, capability and empowerment.')
    add('cpm-screen-8.1', 'Cost and Performance Management', CPM, 'Screenshot batch, Question 8', '8.1', 1, 'Balanced scorecard purpose', '',
        'Which statement about the Balanced Scorecard is true?',
        ['Its primary goal is to sustain short-run nonfinancial performance.', 'It reduces managers’ emphasis on long-run financial performance.', 'Its primary goal is to sustain short-run financial performance.', 'It reduces managers’ emphasis on short-run financial performance.', none], 'd',
        'The scorecard broadens attention across financial and nonfinancial measures and reduces exclusive focus on short-run financial results.')
    add('cpm-screen-8.2', 'Cost and Performance Management', CPM, 'Screenshot batch, Question 8', '8.2', 1, 'Balanced scorecard perspectives', '',
        'Which option measures the customer perspective of the Balanced Scorecard?',
        ['Number of process improvements', 'Revenue growth', 'Defect rates', 'Number of client complaints', none], 'd',
        'Client complaints directly measure customer experience; the other choices are process or financial measures.')
    add('cpm-mike-9.1', 'Cost and Performance Management', CPM, 'Mike Inc. screenshot', '9.1', 3, 'Return on sales',
        'The Clothing division reports EBIT CHF 1,600,000 and EBIT-based return on sales of 12%.',
        'What were Clothing division revenues? Round to a whole CHF.', ['CHF 13,333,333', 'CHF 12,307,692', 'CHF 1,733,333', 'CHF 1,476,923', none], 'a',
        'Return on sales = EBIT/revenue, so revenue = EBIT/return on sales.', '1,600,000/0.12 = CHF 13,333,333.33 ≈ CHF 13,333,333.')
    add('cpm-fritz-9.1', 'Cost and Performance Management', CPM, 'Fritz Arlton screenshot', '9.1', 3, 'Economic value added',
        'Debt CHF 5.5m at 12%; market equity CHF 4.2m (book CHF 2.5m) with 12% cost of equity; tax 25%. Profit centers (EBIT/assets/current liabilities): San Francisco CHF 480,000/2,000,000/140,000; Geneva CHF 600,000/4,000,000/300,000; Bali CHF 1,020,000/6,000,000/600,000.',
        'Calculate San Francisco EVA. Round interim ratios to four decimals and final value to a whole CHF.', ['CHF 168,420', 'CHF 191,580', 'CHF 175,116', 'CHF 360,000', none], 'a',
        'First calculate WACC, after-tax operating income and invested capital, then subtract the capital charge.',
        'WACC = [4.2m×.12 + 5.5m×.12×(1−.25)]/9.7m = .1030. NOPAT = 480,000×.75 = 360,000. Capital = 2,000,000−140,000 = 1,860,000. EVA = 360,000−.1030×1,860,000 = CHF 168,420.')
    add('cpm-fritz-9.2', 'Cost and Performance Management', CPM, 'Fritz Arlton screenshot', '9.2', 3, 'Economic value added',
        'Debt CHF 5.5m at 12%; market equity CHF 4.2m (book CHF 2.5m) with 12% cost of equity; tax 25%. Profit centers (EBIT/assets/current liabilities): San Francisco CHF 480,000/2,000,000/140,000; Geneva CHF 600,000/4,000,000/300,000; Bali CHF 1,020,000/5,000,000/600,000.',
        'Calculate San Francisco EVA. Round interim ratios to four decimals and final value to a whole CHF.', ['CHF 168,420', 'CHF 191,580', 'CHF 175,116', 'CHF 360,000', none], 'a',
        'First calculate WACC, after-tax operating income and invested capital, then subtract the capital charge.',
        'WACC = [4.2m×.12 + 5.5m×.12×(1−.25)]/9.7m = .1030. NOPAT = 480,000×.75 = 360,000. Capital = 2,000,000−140,000 = 1,860,000. EVA = 360,000−.1030×1,860,000 = CHF 168,420.')
    by_id = {item['id']: item for item in q}
    for source in SOURCES.values():
        text = (root / source).read_text()
        sections = []
        for section in re.finditer(r'^### (.+)\n([\s\S]*?)(?=^#{2,3} |\Z)', text, re.M):
            options = [dict(id=m[1].lower(), text=m[2])
                       for m in re.finditer(r'^- ([A-E])\) (.+)$', section[2], re.M)]
            if options:
                sections.append((section, options))
        imported = [item for item in q if item['source']['path'] == source]
        assert len(imported) == len(sections), source
        for item, (section, options) in zip(imported, sections):
            number = re.search(r'\d+\.\d+', section[1])[0]
            assert item['source']['number'] == number, item['id']
            assert [o['id'] for o in item['options']] == [o['id'] for o in options], item['id']
            wording = section[2].split('\n- A)', 1)[0].strip()
            item['marks'] = int(re.search(r'\((\d+) points?\)', section[1])[1])
            item['source'].update(heading=section[1], line=text[:section.start()].count('\n') + 1)
            item['original'].update(wording=wording, options=options, raw=section[0].strip(), scenario='')
            for option, original in zip(item['options'], options):
                option['text'] = original['text']
            item['changes'].append('Shortened the exercise wording for practice; the full source exercise and options are preserved.')
            item['evidence'] = [dict(path=source, section='Answer key and worked solutions; ' + section[1])]
            if '| Location |' in wording:
                item['scenario'] = wording[:wording.index('\n\nCalculate')]

    # Cash-flow timing stays visible while working on the question.
    by_id['cap-ss26-7.1']['scenario'] = '''Proposal A costs CHF 90,000, lasts three years and has no terminal value. Straight-line depreciation applies.

| Year | Cash-flow increase (CHF) |
|---|---:|
| 1 | 80,000 |
| 2 | 10,000 |
| 3 | 45,000 |'''
    by_id['cap-screen-a-7.3']['scenario'] = '''TechFlow Proposal B has no disposal value. Required return is 20%; round present-value factors to three decimals.

| Time | Cash flow (CHF) |
|---|---:|
| Initial investment | −60,000 |
| End of year 1 | 45,000 |
| End of year 2 | 45,000 |
| End of year 3 | 0 |'''
    for ident, investment, sale, working, flows, rate in [
        ('cap-flexxon-7.2', 280000, 0, 0, (165000, 165000, 200000), 14),
        ('cap-cleansvc-4.2', 580000, 120000, 0, (200000, 280000, 280000), 10),
        ('cap-difiend-6.1', 430000, 100000, 100000, (140000, 270000, 270000), 9),
    ]:
        item = by_id[ident]
        rows = [f'| New machine, now | −{investment:,} |']
        if working:
            rows.append(f'| Working capital, now (not recovered) | −{working:,} |')
        if sale:
            rows.append(f'| Old machine sale, now | {sale:,} |')
        rows += [f'| End of year {year}' + (' (including CHF 35,000 disposal proceeds)' if ident == 'cap-flexxon-7.2' and year == 3 else '') + f' | {flow:,} |'
                 for year, flow in enumerate(flows, 1)]
        item['scenario'] = (f'Required return {rate}%. No tax effects. ' +
            ('Year 3 includes the terminal disposal proceeds. Round interim present values to cents and the final NPV to a whole CHF.'
             if ident == 'cap-flexxon-7.2' else 'No terminal value. Use discount factors rounded to three decimals.') +
            '\n\n| Time / cash flow | Amount (CHF) |\n|---|---:|\n' + '\n'.join(rows))
    for item in q:
        if '|' in item['scenario'] and '|' not in item['original']['wording']:
            item['changes'].append('Presented the supplied exercise data as a table; cash-flow amounts and timing are unchanged.')

    checks = {
        'cap-ss26-7.1': ('arr', 16.7, 'percent', dict(cost=90000, flows=[80000,10000,45000], residual=0)),
        'cap-ss26-7.2': ('payback', 6.2, 'years', dict(cost=3100000, annual=500000)),
        'cap-as25-7.1': ('payback', 3.8, 'years', dict(cost=340480, annual=89600)),
        'cap-screen-a-7.3': ('npv', 8715, 'CHF', dict(initial=60000, flows=[45000,45000,0], rate=.2, roundedFactors=True)),
        'cap-mississippi-7.1': ('payback', 3.3, 'years', dict(cost=146800, annual=44400)),
        'cap-flexxon-7.2': ('npv', 126693, 'CHF', dict(initial=280000, flows=[165000,165000,200000], rate=.14, roundInterim=True)),
        'cap-cleansvc-4.2': ('npv', 163360, 'CHF', dict(initial=460000, flows=[200000,280000,280000], rate=.1, roundedFactors=True)),
        'cap-qilti-7.1': ('payback', 2.9, 'years', dict(cost=159000, annual=55000)),
        'cap-difiend-6.1': ('npv', 134160, 'CHF', dict(initial=430000, flows=[140000,270000,270000], rate=.09, roundedFactors=True)),
        'cap-malive-6.2': ('payback', 5.1, 'years', dict(cost=179000, annual=35000)),
        'cpm-ss26-9.1': ('wacc', 9.88, 'percent', dict(debt=32000000, equity=18000000, debtRate=.1, equityRate=.15, tax=.3)),
        'cpm-ss26-9.2': ('ros', 52872000, 'CHF', dict(ebit=7930800, ros=.15)),
        'cpm-as25-9.1': ('ros', 40000000, 'CHF', dict(ebit=4800000, ros=.12)),
        'cpm-as25-9.2': ('eva', 150750, 'CHF', dict(debt=4000000, equity=8000000, debtRate=.05, equityRate=.15, tax=.25, ebit=480000, assets=2000000, liabilities=140000)),
        'cpm-mike-9.1': ('ros', 13333333, 'CHF', dict(ebit=1600000, ros=.12)),
    }
    for ident in ('cpm-fritz-9.1', 'cpm-fritz-9.2'):
        checks[ident] = ('eva', 168420, 'CHF', dict(debt=5500000, equity=4200000, debtRate=.12, equityRate=.12, tax=.25, ebit=480000, assets=2000000, liabilities=140000, roundedWacc=True))
    for ident, (kind, expected, unit, inputs) in checks.items():
        by_id[ident]['calculationCheck'] = dict(kind=kind, expected=expected, unit=unit, inputs=inputs)
    return q
