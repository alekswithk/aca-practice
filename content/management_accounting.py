"""Management accounting source import and reviewed teaching feedback."""
import re

SOURCE = 'Exam by topic/Management Accounting/Management Accounting Exam Bank.md'
LESSON = 'ACA Course Materials/Week 4/W4 Lecture Summary.md'


def import_management(root):
    text = (root / SOURCE).read_text()
    questions = []
    batches = list(re.finditer(r'^## Batch (\d+) — (.+)$', text, re.M))
    for i, batch in enumerate(batches):
        start = batch.end()
        block = text[start:batches[i + 1].start() if i + 1 < len(batches) else len(text)]
        headers = list(re.finditer(r'^### (\d+\.\d+) — (.+?) \((\d+) (?:marks?|points?)\)$', block, re.M))
        shared = re.search(r'^### (?:Scenario: .+|Given information|Shared scenario)\n([\s\S]+)', block[:headers[0].start()], re.M)
        scenario = shared.group(1).strip() if shared else ''
        for j, header in enumerate(headers):
            section = block[header.start():headers[j + 1].start() if j + 1 < len(headers) else len(block)]
            stop = re.search(r'^### (?:Answer key|Worked solutions|Common mistakes)', section, re.M)
            raw = section[:stop.start() if stop else len(section)].strip()
            option_start = re.search(r'^- [A-E]\) ', raw, re.M)
            assert option_start, (batch.group(1), header.group(1))
            wording = raw[raw.index('\n') + 1:option_start.start()].strip()
            options = [{'id': m.group(1).lower(), 'text': m.group(2)} for m in re.finditer(r'^- ([A-E])\) (.+)$', raw, re.M)]
            ident = f'ma-{int(batch.group(1)):02}-{header.group(1)}'
            questions.append(dict(id=ident, origin='original', topic='Management Accounting',
                subtopic='Pending review', difficulty='Medium', type='single-choice', marks=int(header.group(3)),
                prompt=wording, scenario=scenario, assumptions=[], options=options, correctOptionId=None,
                explanation='', workedCalculation='', evidence=[], status='review', reviewReason='', changes=[], targets=[],
                source=dict(path=SOURCE, heading=f'Batch {batch.group(1)} — {batch.group(2)}',
                            number=header.group(1), line=text[:start + header.start()].count('\n') + 1),
                original=dict(wording=wording, options=[dict(o) for o in options], raw=raw, scenario=scenario,
                              recordedStudentAnswer=None, answerProvenance='The source includes supplied answers and displayed solutions; these were checked independently.')))
    assert len(questions) == 51
    by_id = {q['id']: q for q in questions}

    def check(kind, expected, unit='CHF', **inputs):
        return dict(kind=kind, expected=expected, unit=unit, inputs=inputs)

    def add(batch, num, key, subtopic, rule, calculation='', numeric=None, wrong=None, assumptions=(), difficulty='Medium'):
        q = by_id[f'ma-{batch:02}-{num}']
        q.update(correctOptionId=key, subtopic=subtopic, explanation=rule, workedCalculation=calculation,
                 status='validated', difficulty=difficulty, assumptions=list(assumptions),
                 evidence=[dict(path=LESSON, section={'Manufacturing cost flows':'2: cost classification and manufacturing cost flow',
                    'Cost concepts':'1–2: internal reporting, cost behavior and classification',
                    'CVP analysis':'3: contribution margin, break-even and target profit',
                    'Job costing':'4: overhead rates and assignment; 6: pricing',
                    'Pricing and target costing':'6: target costing and cost-plus pricing'}[subtopic])])
        if assumptions:
            q['changes'].append('Added explicit study assumptions: ' + ' '.join(assumptions))
        if numeric:
            q['calculationCheck'] = numeric
        assert set(wrong or {}) == {o['id'] for o in q['options'] if o['id'] != key}, q['id']
        for option in q['options']:
            if option['id'] == key:
                option.update(explanation='This is the one option consistent with the rule and calculation above.', misconception=None)
            else:
                reason, tag = wrong[option['id']].rsplit('|', 1)
                option.update(explanation=reason, misconception=tag)
        q['targets'] = sorted({o['misconception'] for o in q['options'] if o['misconception']})
        return q

    def exclude(batch, num, subtopic, reason):
        q = by_id[f'ma-{batch:02}-{num}']
        q.update(subtopic=subtopic, reviewReason=reason, evidence=[dict(path=LESSON, section='2–6: cost flows, allocation and pricing')])

    cvp = ('Use the course linear CVP model within the relevant range: unchanged unit variable cost and total fixed cost, production equals sales, and no inventory changes.',)
    pretax = cvp + ('No interest or other non-operating items; operating income equals earnings before income tax. Tax is proportional to positive profit; no minimum or turnover tax.',)
    cost = 'Manufacturing cost flows'
    pricing = 'Pricing and target costing'
    vases = dict(material=1, wage=28, productivity=10, fixedManufacturing=28000, fixedOther=10000)
    add(1,'1.1','c',cost,'COGM includes material, production labor and manufacturing overhead. Selling and administrative costs are period costs.',
        'Labor/unit = 28 / 10 = 2.80; COGM = 5,000 × (1 + 2.80) + 28,000 = CHF 47,000.',
        check('vases',47000,quantity=5000,measure='cogm',**vases),
        {'a':'49,000 exceeds the 47,000 manufacturing total by 2,000; convert the hourly wage to 2.80 per vase.|labor-productivity',
         'b':'71,000 exceeds manufacturing cost by 24,000; neither period costs nor the full hourly wage belong in each vase.|manufacturing-cost-boundary',
         'd':'64,000 exceeds manufacturing cost by 17,000; 500 labor hours cost 14,000, not 31,000.|labor-productivity',
         'e':'C gives the computed manufacturing cost of 47,000.|none-of-the-above'},cvp)
    add(1,'1.2','b',cost,'Total unit cost includes both manufacturing and non-manufacturing costs divided by output.',
        '(5,000 × 3.80 + 28,000 + 10,000) / 5,000 = CHF 11.40 per vase.',
        check('vases',11.4,quantity=5000,measure='unit',**vases),
        {'a':'14.30 implies total cost 71,500, rather than the 57,000 supported by the inputs.|total-versus-unit-cost',
         'c':'17.50 implies total cost 87,500; labor per vase is 2.80 and fixed costs total 38,000.|labor-productivity',
         'd':'9.30 implies 46,500 total cost and does not cover the 57,000 manufacturing and period costs.|period-cost-omitted',
         'e':'B gives 57,000 / 5,000 = 11.40.|none-of-the-above'},cvp)
    for num, qty, key, result, wrong in [
        ('1.3',5000,'c',-7000,{'a':'A profit of 2,300 understates the 57,000 total costs at revenue 50,000.|fixed-cost-omitted','b':'A profit of 2,700 understates the 57,000 total costs at revenue 50,000.|fixed-cost-omitted','d':'A loss of 1,560 is too small: total costs exceed revenue by 7,000.|total-cost-reconciliation','e':'C gives the actual loss of 7,000.|none-of-the-above'}),
        ('1.4',10000,'d',24000,{'a':'23,000 implies costs of 77,000; variable costs are 38,000 and fixed costs 38,000.|cvp-cost-reconciliation','b':'27,000 implies costs of 73,000, understating the stated total cost by 3,000.|fixed-cost-omitted','c':'26,600 implies costs of 73,400, understating total costs by 2,600.|cvp-cost-reconciliation','e':'D gives revenue 100,000 less total costs 76,000.|none-of-the-above'})]:
        add(1,num,key,'CVP analysis','Operating income equals revenue less variable costs and all fixed operating costs.',
            f'{qty:,} × (10 − 3.80) − 28,000 − 10,000 = CHF {result:,}.',
            check('vases',result,quantity=qty,price=10,measure='income',**vases),wrong,cvp)

    for batch in (2,6):
        q=add(batch,'2.1','c','CVP analysis','Break-even quantity is fixed cost divided by contribution per unit.',
            'CM/unit = 68 − 60 = CHF 8; 1,640,000 / 8 = 205,000 collars.',
            check('cvp',205000,'units',price=68,variable=60,fixed=1640000,measure='quantity'),
            {'a':'240,000 collars produce 280,000 operating profit, above break-even.|cvp-break-even-profit',
             'b':'440,000 collars produce 1,880,000 operating profit, above break-even.|cvp-break-even-profit',
             'd':'210,000 collars produce 40,000 operating profit, above break-even.|cvp-break-even-profit',
             'e':'C produces zero operating profit.|none-of-the-above'},pretax)
        q['options'][-1]['text']='None of the answers A)–D) is correct.'
        q['changes'].append('Corrected option E range A)–C) to A)–D); original option is preserved.')
        add(batch,'2.2','d','CVP analysis','Operating income equals total contribution margin less fixed costs.',
            '410,000 × (68 − 60) − 1,640,000 = CHF 1,640,000.',
            check('cvp',1640000,price=68,variable=60,fixed=1640000,quantity=410000,measure='income'),
            {'a':'1,203,000 leaves 2,077,000 fixed costs after the actual 3,280,000 contribution, exceeding the stated 1,640,000.|cvp-cost-reconciliation',
             'b':'1,270,000 implies fixed costs of 2,010,000 rather than 1,640,000.|cvp-cost-reconciliation',
             'c':'2,260,600 implies fixed costs of 1,019,400, understating the stated fixed costs.|fixed-cost-omitted',
             'e':'D equals the actual operating profit; its equality with fixed costs is coincidental.|none-of-the-above'},pretax)
        add(batch,'2.3','c','CVP analysis','Target revenue equals (fixed costs + pre-tax target profit) divided by the contribution margin ratio.',
            '(1,640,000 + 3,128,000) / (8 / 68) = CHF 40,528,000.',
            check('cvp',40528000,price=68,variable=60,fixed=1640000,target=3128000,measure='revenue'),
            {'a':'42,223,000 implies profit of 3,327,411.76, above the requested 3,128,000.|cvp-target-revenue',
             'b':'41,217,000 implies profit of 3,209,058.82, above the target.|cvp-target-revenue',
             'd':'38,236,000 implies profit of 2,858,352.94, below the target.|cvp-target-revenue',
             'e':'C produces precisely the requested pre-tax profit.|none-of-the-above'},pretax)
    add(2,'2.4','a','CVP analysis','Gross up the after-tax target, add fixed costs, then divide by unit contribution. A minimum whole-unit quantity rounds upward.',
        '54,000 / (1 − .068) = 57,939.914…; (1,640,000 + 57,939.914…) / 8 = 212,242.489… → 212,243 collars. At 212,242: net 53,996.352; at 212,243: net 54,003.808.',
        check('cvp',212243,'units',price=68,variable=60,fixed=1640000,target=54000,tax=.068,measure='quantity',whole=True),
        {'b':'323,636 yields after-tax income 884,550.016, well above the minimum target.|cvp-tax-target',
         'c':'227,022 yields after-tax income 164,196.032, exceeding the target and minimum.|cvp-tax-target',
         'd':'276,512 yields after-tax income 533,193.472, exceeding the target and minimum.|cvp-tax-target',
         'e':'A is the smallest integer quantity meeting the after-tax target.|minimum-quantity-rounding'},pretax,difficulty='Hard')

    cafe=dict(price=17,variable=6.8,fixed=918000,tax=.3,target=214200)
    rows=[('2.1','a',40,'percent','variable-ratio','Variable cost ratio = variable cost per customer / revenue per customer.','6.80 / 17 × 100 = 40%.',
           {'b':'30% is the income tax rate, not the variable cost ratio.|tax-rate-versus-cost-ratio','c':'62% is neither the variable cost ratio of 40% nor contribution ratio of 60%.|cvp-cost-ratio','d':'48% would imply variable costs of 8.16 per customer, not 6.80.|cvp-cost-ratio'}),
          ('2.2','d',2040000,'CHF','revenue','Convert after-tax income to pre-tax profit before solving for sales revenue.','214,200 / .70 = 306,000; (918,000 + 306,000) / .60 = CHF 2,040,000.',
           {'a':'3,290,000 produces net income 739,200, above the target.|cvp-tax-target','b':'2,410,000 produces net income 369,600, above the target.|cvp-tax-target','c':'3,070,000 produces net income 646,800, above the target.|cvp-tax-target'}),
          ('2.3','b',1224000,'CHF','contribution','Total contribution at target sales must cover fixed costs plus pre-tax target profit.','918,000 + 214,200 / .70 = CHF 1,224,000.',
           {'a':'1,316,000 leaves net income 278,600 after fixed costs and tax, exceeding the target.|contribution-versus-profit','c':'1,446,000 leaves net income 369,600, exceeding the target.|contribution-versus-profit','d':'1,472,000 leaves net income 387,800, exceeding the target.|contribution-versus-profit'}),
          ('2.4','e',90000,'units','quantity','At break-even, total contribution equals fixed costs and profit is zero.','918,000 / (17 − 6.80) = 90,000 customers.',
           {'a':'111,000 customers generate operating profit 214,200, so this is not break-even.|tax-net-versus-operating','b':'103,000 customers generate operating profit 132,600.|cvp-break-even-profit','c':'46,000 customers leave an operating loss of 448,800.|cvp-break-even-profit','d':'75,000 customers leave an operating loss of 153,000.|cvp-break-even-profit'}),
          ('2.5','a',120000,'units','quantity','Target customers cover both fixed costs and the tax-grossed-up profit.','(918,000 + 214,200 / .70) / 10.20 = 120,000 customers.',
           {'b':'90,000 customers only break even; net income is zero.|target-profit-omitted','c':'110,000 customers generate net income 142,800, below target.|cvp-tax-target','d':'130,000 customers generate net income 285,600, above the required target.|cvp-tax-target'}),
          ('2.6','c',871080,'CHF','income','Apply income tax to operating profit after subtracting all fixed costs.','(212,000 × 10.20 − 918,000) × .70 = CHF 871,080.',
           {'a':'893,340 exceeds net income by 22,260; apply 30% to the full 1,244,400 pre-tax profit.|tax-net-versus-operating','b':'742,090 understates net income by 128,990; income tax is 373,320.|cvp-cost-reconciliation','d':'964,216 exceeds net income by 93,136; the after-tax factor is .70.|tax-gross-up-direction'})]
    for num,key,expected,unit,measure,rule,calc,wrong in rows:
        inputs={**cafe,'measure':measure}
        if num=='2.4': inputs['target']=0
        if num=='2.6': inputs['quantity']=212000
        if key!='e': wrong['e']='The stated calculation matches one of A)–D).|none-of-the-above'
        assumptions=pretax + (('Contribution margin means the total at the sales level required for the CHF 214,200 after-tax target in the shared scenario.',) if num=='2.3' else ())
        add(3,num,key,'CVP analysis',rule,calc,check('cvp',expected,unit,**inputs),wrong,assumptions)

    job=dict(overhead=27200000,base=10625000,rates=[396,202,98,72],hours=[4,42,22,86],margin=.11)
    add(4,'3.1','b','Job costing','Budgeted overhead rate is budgeted indirect costs divided by budgeted direct labor cost.',
        '27,200,000 / 10,625,000 × 100 = 256%.',check('job-cost',256,'percent',measure='rate',**job),
        {'a':'194% allocates only 20,612,500 of the budgeted 27,200,000 overhead.|overhead-allocation-base','c':'174% allocates only 18,487,500 overhead.|overhead-allocation-base','d':'316% allocates 33,575,000, above the overhead budget.|overhead-allocation-base','e':'B uses the stated direct labor cost base.|none-of-the-above'})
    add(4,'3.2','a','Job costing','Apply the budgeted rate to the job’s direct labor cost, retaining precision until the final rounding.',
        '396×4 + 202×42 + 98×22 + 72×86 = 18,416; 18,416 × 2.56 = 47,144.96 → CHF 47,145.',
        check('job-cost',47145,measure='overhead',**job),
        {'b':'19,234 implies a rate of about 104.44%, instead of 256%.|overhead-rate-application','c':'16,948 is below even direct labor cost; overhead alone is 2.56 times labor cost.|direct-versus-indirect-cost','d':'37,612 implies a rate of about 204.24%, instead of 256%.|overhead-rate-application','e':'A is 47,144.96 rounded to a whole franc.|none-of-the-above'},('Round the final result to the nearest whole CHF; retain intermediate precision.',),difficulty='Hard')
    add(4,'3.3','c','Job costing','A margin on revenue requires dividing total job cost by one minus the margin.',
        '(18,416 + 47,144.96) / (1 − .11) = CHF 73,664.',check('job-cost',73664,measure='price',**job),
        {'a':'114,554 implies about 42.77% margin on the 65,560.96 job cost, not 11%.|margin-versus-markup','b':'96,337 implies about 31.95% margin, not 11%.|margin-versus-markup','d':'204,226 implies about 67.90% margin, not 11%.|margin-versus-markup','e':'C gives an 11% margin using unrounded job costs.|none-of-the-above'},('Use unrounded indirect cost; round only the final price to the nearest whole CHF. Margin is operating income / revenue.',),difficulty='Hard')

    inv=dict(purchases=123000,beginMaterials=11000,endMaterials=17000,directLabor=12000,indirectLabor=15000,manufacturing=163000,beginWip=29000,endWip=30000,beginFinished=10000,endFinished=13000,income=-6000,period=26000,salesSalaries=50000)
    for num,key,value,measure,rule,calc,wrong in [
        ('1.1','a',117000,'materials','Materials used equals beginning materials plus purchases less ending materials.','11,000 + 123,000 − 17,000 = 117,000.',{'b':'163,000 is total manufacturing cost, including labor and overhead.|materials-versus-manufacturing','c':'159,000 is COGS after WIP and finished-goods adjustments.|materials-versus-cogs','d':'130,000 exceeds materials used by 13,000; inventory must be adjusted in the right direction.|inventory-flow-direction'}),
        ('1.2','c',19000,'other','Other manufacturing costs are the residual after materials and separately listed direct and indirect labor.','163,000 − 117,000 − 12,000 − 15,000 = 19,000.',{'a':'18,000 is 1,000 too low; WIP changes do not belong in costs incurred.|wip-versus-costs-incurred','b':'13,000 is ending finished goods, an inventory balance rather than other manufacturing cost.|inventory-versus-period-cost','d':'15,000 is the separately stated indirect labor, which must already be deducted.|overhead-double-count'}),
        ('1.3','d',159000,'cogs','Adjust costs incurred for WIP to get COGM, then adjust for finished goods to get COGS.','COGM = 163,000 + 29,000 − 30,000 = 162,000; COGS = 162,000 + 10,000 − 13,000 = 159,000.',{'a':'130,000 is 29,000 too low; beginning WIP is part of goods completed.|beginning-wip-omitted','b':'138,000 is 21,000 below the two-stage cost roll-forward.|inventory-flow-direction','c':'155,000 understates COGS by 4,000; net inventory adjustments are −1,000 and −3,000.|inventory-flow-direction'}),
        ('1.4','a',70000,'gross','Gross profit equals operating income plus non-manufacturing operating expenses.','−6,000 + 26,000 + 50,000 = 70,000.',{'b':'55,000 omits 15,000 of the 76,000 period costs needed to reconcile the operating loss.|gross-versus-operating-profit','c':'84,000 overstates gross profit by 14,000; the 6,000 operating loss must enter with a negative sign.|loss-sign','d':'77,000 overstates gross profit by 7,000; add total period costs 76,000 to the loss of 6,000.|gross-versus-operating-profit'})]:
        wrong['e']='The cost reconciliation matches one of A)–D).|none-of-the-above'
        assumptions=('Amounts are in the source’s unspecified currency units.',)
        if num=='1.2': assumptions+=('“Other manufacturing costs” excludes the separately stated indirect manufacturing labor.',)
        if num=='1.4': assumptions+=('The 26,000 selling and administrative costs exclude the separately listed 50,000 sales salaries, as in the source solution.',)
        add(5,num,key,cost,rule,calc,check('inventory-flow',value,'currency units',measure=measure,**inv),wrong,assumptions)

    add(6,'2.4','d','CVP analysis','At zero pre-tax profit, proportional income tax is zero. Changing its rate alone leaves operating break-even unchanged.',wrong={
        'a':'A positive-profit tax rate changes after-tax profit above break-even, but profit and tax are zero at break-even.|tax-affects-break-even',
        'b':'The model holds selling price and demand assumptions constant; a tax increase does not automatically change price.|tax-changes-price',
        'c':'Income tax affects net income, not operating income or contribution per unit.|tax-net-versus-operating'},assumptions=pretax,difficulty='Easy')
    add(7,'2.1','a','CVP analysis','Convert the after-tax target to pre-tax profit, then round required indivisible units up.',
        '(100,000 + 20,000 / .60) / (1,200 − 700) = 266.666… → 267 hoodies. 266 yields net 19,800; 267 yields net 20,100.',
        check('cvp',267,'units',price=1200,variable=700,fixed=100000,target=20000,tax=.4,whole=True,measure='quantity'),
        {'b':'200 hoodies only break even and produce no target profit.|target-profit-omitted','c':'400 hoodies produce net income 60,000 and are not the minimum required.|cvp-tax-target','d':'240 hoodies produce pre-tax profit 20,000 but net profit only 12,000.|tax-gross-up-omitted','e':'A is the smallest whole quantity achieving at least 20,000 after tax.|minimum-quantity-rounding'},pretax+('Find the minimum whole number of hoodies meeting or exceeding the target.',))
    add(7,'2.2','b','CVP analysis','Fixed costs equal contribution margin less operating income.',
        '.25 × 260,000 − 50,000 = CHF 15,000.',check('fixed-cost',15000,revenue=260000,ratio=.25,income=50000),
        {'a':'157,500 would leave an operating loss of 92,500 at contribution 65,000.|contribution-versus-profit','c':'35,000 would leave operating profit 30,000, not 50,000.|contribution-versus-profit','d':'210,000 subtracts profit directly from revenue and ignores variable costs.|variable-cost-omitted','e':'B reconciles the target contribution and operating income.|none-of-the-above'},cvp+('Sales volume expressed in CHF means revenue.',))
    add(7,'2.3','d','CVP analysis','Pre-tax income equals after-tax income divided by one minus the income tax rate.',wrong={
        'a':'Multiplication by the retention factor converts pre-tax to after-tax income, the opposite direction.|tax-gross-up-direction',
        'b':'Multiplication by the tax rate computes tax on a pre-tax amount, not pre-tax profit.|tax-amount-versus-profit',
        'c':'Divide by the retained share 1 − tax rate, not by the share paid in tax.|tax-rate-versus-retention',
        'e':'D is the rearrangement of net income = pre-tax income × (1 − tax rate).|none-of-the-above'},
        assumptions=pretax+('“Net operating income” means after-tax target net income in this source question.',),difficulty='Easy')

    add(8,'7.1','d',pricing,'Long-run full-cost-plus pricing includes manufacturing and non-manufacturing costs, then applies the markup to that full cost.',
        '50 + 10,000×12/30,000 + (322,500+1,200,000+600,000+1,290,000)/30,000 = 167.75; ×1.20 = CHF 201.30.',
        check('full-cost-price',201.3,quantity=30000,material=50,laborHours=10000,wage=12,otherCosts=[322500,1200000,600000,1290000],markup=.2),
        {'a':'64.75 is variable manufacturing cost per table, excluding fixed and non-manufacturing costs and markup.|long-run-variable-only',
         'b':'103.00 is not full cost: manufacturing alone costs 104.75 per table before design, marketing and markup.|full-cost-boundary',
         'c':'167.75 is full cost before applying the 20% markup.|markup-omitted',
         'e':'D includes all stated full costs and the markup.|none-of-the-above'},('Apply the stated long-run full-cost policy; one product, all listed monthly costs belong to this product. Round price to CHF .01.',),difficulty='Hard')
    for batch,num,key in [(8,'7.2','c'),(9,'3.1','d'),(15,'3.1','d')]:
        profit=350000 if batch==15 else 303000
        value=11.1 if batch==15 else 9.5
        wrong={}
        q=by_id[f'ma-{batch:02}-{num}']
        for o in q['options']:
            if o['id']==key: continue
            number=o['text']
            if number.startswith('13.8'): reason='13.8% approximates 303,000 / 2,200,000, an investment return rather than profit / costs.'
            elif number.startswith('8.7'): reason='8.7% approximates the earlier 303,000 / 3,500,000 margin on sales, not this markup on cost.'
            elif number.startswith('9.5'): reason='9.5% uses the earlier 303,000 profit scenario; the stated 350,000 target requires a new cost denominator.'
            elif number.startswith('0.9'): reason='0.9% understates the markup by a decimal place; convert profit / cost to percent by multiplying by 100.'
            else: reason=f'One of A)–D) matches the computed {value}% markup.'
            wrong[o['id']]=reason+'|'+('none-of-the-above' if o['id']=='e' else 'markup-denominator')
        add(batch,num,key,pricing,'Markup on cost is operating profit / (revenue − operating profit), rather than margin on revenue or return on investment.',
            f'Revenue = 7,000×500 = 3,500,000; cost = 3,500,000 − {profit:,}; markup = {profit:,} / {3500000-profit:,} × 100 → {value}%.',
            check('markup',value,'percent',quantity=7000,price=500,profit=profit),wrong,
            ('Express markup as a percent of cost, rounded to one decimal.',))
    exclude(8,'7.3',pricing,'B and D can both describe profitable incremental supply when willingness to pay is the attainable selling price. No market condition distinguishes B from D. The source solution selects D, but its explanation adds an unstated competition assumption. Needs revised wording before scoring.')
    add(9,'3.2','d',pricing,'Target cost equals revenue less target operating profit. A margin on sales uses revenue as its base.',
        '21,000 × 240 × (1 − .20) = CHF 4,032,000 total annual cost (CHF 192/unit).',
        check('target-cost',4032000,price=240,quantity=21000,margin=.2,measure='total'),
        {'a':'5,040,000 is revenue and leaves no target profit.|target-profit-omitted','b':'1,008,000 is target profit, not allowable cost.|target-profit-versus-cost','c':'6,048,000 adds profit to revenue rather than subtracting it.|target-cost-direction','e':'D leaves exactly a 20% operating margin on sales.|none-of-the-above'},('Target cost means total annual cost, not cost per unit.',))

    add(10,'1.1','d','Cost concepts','Select the incorrect statement: fixed costs are constant with activity within a stated time horizon and relevant range.',wrong={
        'a':'This is a true direct-cost definition in the course model; the task asks for the incorrect statement.|negative-question-stem',
        'b':'This is the source’s simplified shared-cost definition; costs shared across cost objects are allocated rather than directly traced.|negative-question-stem',
        'c':'This is a true variable-cost definition; variable costs change with activity.|negative-question-stem',
        'e':'D is incorrect, so there is an incorrect statement among A)–D).|negative-question-stem'},
        assumptions=('Use the course’s simplified cost classification within a fixed time horizon and relevant activity range.',),difficulty='Easy')
    exclude(10,'1.2','Cost concepts','The source selects B, but the supplied Week 4 lessons do not establish the stated cost-type / cost-center / cost-object accounting sequence or its “why” criterion. Need the corresponding lecture or authoritative solution context to validate every statement; source key alone is insufficient.')
    add(10,'1.3','b','CVP analysis','Select the incorrect statement: contribution margin is revenue minus variable costs, never their sum.',wrong={
        'a':'CVP can support planned volume decisions; this statement is not the false definition sought.|negative-question-stem',
        'c':'Successive contribution levels deduct fixed costs at product-group, division and company levels; they do not add variable costs to revenue.|negative-question-stem',
        'd':'At break-even, contribution covers all fixed costs, leaving zero profit.|negative-question-stem',
        'e':'B incorrectly adds variable costs to revenue.|negative-question-stem'},assumptions=cvp,difficulty='Easy')
    add(10,'1.4','b','Cost concepts','Select the incorrect statement: management accounting supports internal decisions; financial reporting communicates externally.',wrong={
        'a':'In the advisory role described here, accountants inform management decisions; this is not the incorrect statement.|negative-question-stem',
        'c':'Internal reports follow usefulness and cost–benefit rather than a prescribed external reporting framework.|negative-question-stem',
        'd':'Internal information can influence behavior toward organizational goals; this is true in the course model.|negative-question-stem',
        'e':'B assigns the external reporting function to management accounting and is the incorrect statement.|management-versus-financial-reporting'},
        assumptions=('Read the organizational role in the course’s advisory management-accounting model; individuals may hold additional decision-making roles.',),difficulty='Easy')
    for num in ('2.1','2.2','2.3'):
        exclude(11,num,'Job costing','The scenario says 28,000 backpacks were produced, but their direct materials alone would be 28,000 × 3.20 = 89,600, exceeding the 60,000 company total. PCC I backpack wages alone would be 84,000, exceeding that center’s 56,000 total. The displayed overhead-rate calculation ignores these contradictory totals. Production quantity or cost-allocation table needs correction. For 2.3 the administration/distribution allocation base is also unstated.')
    add(11,'2.4','d','CVP analysis','Use the independent revenue/cost data in this question: break-even revenue is fixed cost / contribution ratio.',
        'CM ratio = (500,000 − 125,000) / 500,000 = .75; 180,000 / .75 = CHF 240,000.',
        check('break-even-revenue',240000,revenue=500000,variableTotal=125000,fixed=180000),
        {'a':'1,000,000 produces contribution 750,000 and operating profit 570,000.|cvp-break-even-profit','b':'433,333 produces contribution 324,999.75, above fixed costs 180,000.|cvp-break-even-profit','c':'621,111 produces contribution 465,833.25, above fixed costs.|cvp-break-even-profit','e':'D produces contribution exactly equal to fixed costs.|none-of-the-above'},cvp+('Only the independent CHF revenue, variable-cost and fixed-cost figures in this question are used; the contradictory backpack table is not required.',))
    add(12,'1.1','c',cost,'Manufacturing inventory includes materials, manufacturing labor and both variable and fixed manufacturing overhead.',
        '86 + 24 + 20 + 10 = CHF 140/unit.',check('sum',140,values=[86,24,20,10]),
        {'a':'120 omits 20 of manufacturing costs; fixed and variable manufacturing overhead are both inventoriable.|manufacturing-overhead-omitted','b':'130 excludes the 10 fixed manufacturing overhead.|fixed-overhead-period-cost','d':'196 includes 18 sales commissions and 38 administrative salaries, which are period costs.|period-cost-in-inventory','e':'C includes exactly the manufacturing components.|none-of-the-above'},('Use the course’s manufacturing absorption-cost model; overhead is appropriately allocated at normal capacity and no exceptional waste is present.',),difficulty='Easy')
    add(12,'1.2','a','CVP analysis','With total revenue and variable cost, compute contribution ratio before break-even sales.',
        '(440,000 − 220,000) / 440,000 = .50; 110,000 / .50 = CHF 220,000.',
        check('break-even-revenue',220000,revenue=440000,variableTotal=220000,fixed=110000),
        {'b':'330,000 equals historical variable plus fixed costs; at that revenue profit would be 55,000.|historical-cost-versus-break-even','c':'110,000 is fixed cost, not revenue needed to cover variable costs too.|variable-cost-omitted','d':'440,000 is historical sales and generates profit 110,000.|actual-versus-break-even','e':'A gives revenue whose 50% contribution covers fixed costs.|none-of-the-above'},cvp+('Round the ratio to two decimals and final revenue to a whole CHF; .50 is already exact.',))
    add(12,'1.3','c','CVP analysis','Break-even depends on fixed costs and contribution per procedure, not the planned number of procedures.',
        '36,000 / (1,300 − 500) = 45 procedures.',check('cvp',45,'units',price=1300,variable=500,fixed=36000,measure='quantity'),
        {'a':'19 procedures contribute 15,200, leaving a 20,800 loss.|cvp-break-even-profit','b':'10 procedures contribute 8,000, leaving a 28,000 loss.|cvp-break-even-profit','d':'30 procedures contribute 24,000, leaving a 12,000 loss.|cvp-break-even-profit','e':'C covers fixed costs with 45 × 800 contribution.|none-of-the-above'},cvp)
    q=add(13,'3.1','a',pricing,'Markup on variable cost must recover fixed costs and target operating income, using all variable costs as the base.',
        'Variable cost = 1,150,000 + 785,000 + 870,000 + 370,000 = 3,175,000; (670,000 + 495,000 + 910,000) / 3,175,000 × 100 = 65.354…% → 65.4%.',
        check('variable-markup',65.4,'percent',variableCosts=[1150000,785000,870000,370000],fixedCosts=[670000,495000],profit=910000),
        {'b':'85.7% adds 2,720,975, exceeding the fixed-cost-plus-profit requirement of 2,075,000.|markup-cost-base','c':'96.9% adds 3,076,575, above the amount required to cover fixed costs and target profit.|markup-cost-base','d':'43.1% adds only 1,368,425, below the required 2,075,000.|fixed-cost-in-markup-omitted','e':'A is the required percentage rounded to one decimal.|none-of-the-above'},('The target belongs to Terra Inc.; “Wilde’s” in the source is a company-name typo. Round the ending percentage to one decimal.', 'Use the individual cost components. Their sum is CHF 4,340,000; the source’s CHF 4,335,000 total is an arithmetic inconsistency, corrected in this practice version.'),difficulty='Hard')
    q['prompt']=q['prompt'].replace('Wilde’s annual','Terra Inc.’s annual')
    q['prompt']=q['prompt'].replace('| Total costs | 4’335’000 |','| Total costs | 4’340’000 |')
    q['changes'].append('Changed Wilde’s to Terra Inc.’s in the practice prompt; preserved original wording separately.')
    q['changes'].append('Corrected the displayed total cost from 4,335,000 to the sum of its listed components, 4,340,000. No component was changed.')
    add(13,'3.2','c',pricing,'Full cost per unit equals selling price less target operating income per unit; invested capital is not this cost base.',
        '(1,250 × 2,450 − 1,240,000) / 1,250 = CHF 1,458/unit.',
        check('unit-cost-base',1458,quantity=1250,price=2450,profit=1240000),
        {'a':'1,896 leaves total operating income 692,500, below the target.|total-versus-unit-profit','b':'1,580 leaves operating income 1,087,500, below the target.|total-versus-unit-profit','d':'650 leaves operating income 2,250,000, above the stated target.|investment-versus-cost','e':'C reconciles revenue and the target operating income.|none-of-the-above'})
    add(14,'1.1','d',cost,'COGS is beginning finished goods plus COGM less ending finished goods.',
        '90,000 + 472,000 − 86,000 = CHF 476,000.',check('finished-goods',476000,beginning=90000,cogm=472000,ending=86000),
        {'a':'261,000 understates COGS by 215,000; revenue and operating costs are not terms in this inventory roll-forward.|cogs-versus-profit','b':'567,000 is 91,000 too high; ending finished goods must be subtracted.|inventory-flow-direction','c':'472,000 is COGM before the net 4,000 finished-goods decrease.|finished-goods-adjustment-omitted','e':'D is the finished-goods cost reconciliation.|none-of-the-above'},('Use explicitly provided COGM of CHF 472,000; no WIP roll-forward is supplied or needed.',))
    add(14,'1.2','b','CVP analysis','Break-even revenue is fixed costs divided by the contribution margin ratio.',
        '(250,000 − 150,000) / 250,000 = .40; 45,000 / .40 = CHF 112,500.',
        check('break-even-revenue',112500,revenue=250000,variableTotal=150000,fixed=45000),
        {'a':'163,500 contributes 65,400 and yields profit 20,400, above break-even.|cvp-break-even-profit','c':'1,500,000 contributes 600,000, far above fixed costs.|cvp-ratio-scale','d':'621,000 contributes 248,400, above fixed costs.|cvp-break-even-profit','e':'B contributes exactly 45,000 to fixed costs.|none-of-the-above'},cvp)
    add(14,'1.3','e','CVP analysis','Reduce selling price, retain all variable operating costs, then subtract annual fixed costs.',
        'New price = 35×.85 = 29.75; variable/unit = 7+1.35+.95+2.60 = 11.90; 17,000×(29.75−11.90)−140,000 = CHF 163,450, absent from A–D.',
        check('price-reduction',163450,price=35,reduction=.15,quantity=17000,variableCosts=[7,1.35,.95,2.6],fixed=140000),
        {'a':'109,050 is 54,400 below the profit supported by the new price and stated costs.|price-change-cvp','b':'140,000 is annual fixed cost, not operating income.|fixed-cost-versus-profit','c':'144,750 understates operating income by 18,700; price is reduced, not the cost components.|price-change-cvp','d':'170,025 exceeds operating income by 6,575; both variable selling costs and fixed costs remain.|variable-selling-cost-omitted'},
        cvp+('The stated average price and costs continue to represent the unchanged sales mix after the price reduction.',),difficulty='Hard')
    add(15,'3.2','c',pricing,'When target profit is a percentage of sales, allowable unit cost is target price times one minus the margin.',
        '170 × (1 − .19) = CHF 137.70/unit. Planned 27,966 helmets imply revenue 4,754,220 and target total cost 3,850,918.20; dividing gives the same 137.70.',
        check('target-cost',137.7,price=170,quantity=27966,margin=.19,measure='unit'),
        {'a':'90.05 leaves 79.95 profit per unit, a 47.03% margin rather than 19%.|target-margin-base','b':'102.20 leaves a 39.88% margin rather than 19%.|target-margin-base','d':'112.60 leaves a 33.76% margin rather than 19%.|target-margin-base','e':'C leaves 32.30 profit per helmet, exactly 19% of the new 170 price.|none-of-the-above'},('Use the new target selling price CHF 170 and a 19% margin on revenue. Round the unit cost to CHF .01.',))
    assert sum(q['status']=='review' for q in questions) == 5
    return questions
