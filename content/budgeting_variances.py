"""Reviewed Budgeting and Variances questions transcribed from Ecoreps."""

SOURCE = 'Ecoreps ACA / Exams by Topic / Budgeting and Variances'


def _q(ident, topic, exam, number, marks, subtopic, scenario, prompt, choices, key,
       explanation, calculation, difficulty='Medium', changes=()):
    ids = 'abcde'[:len(choices)]
    options = []
    for oid, text in zip(ids, choices):
        correct = oid == key
        options.append(dict(
            id=oid, text=text,
            explanation=('This matches the expanded source solution and the calculation shown.' if correct
                         else 'This does not follow the stated budget or variance calculation.'),
            misconception=None if correct else f'{topic.lower()}-calculation'))
    return dict(
        id=ident, origin='original', topic=topic, subtopic=subtopic,
        difficulty=difficulty, type='single-choice', marks=marks, prompt=prompt,
        scenario=scenario, assumptions=[], options=options, correctOptionId=key,
        explanation=explanation, workedCalculation=calculation,
        evidence=[dict(path=SOURCE, section=f'{exam}, Question {number}; expanded solution')],
        status='validated', reviewReason='', changes=list(changes),
        targets=sorted({o['misconception'] for o in options if o['misconception']}),
        source=dict(path=SOURCE, heading=exam, number=number, line=None),
        original=dict(wording=prompt, options=[dict(id=o['id'], text=o['text']) for o in options],
                      raw=prompt + '\n' + '\n'.join(f"- {o['id'].upper()}) {o['text']}" for o in options),
                      scenario=scenario, recordedStudentAnswer=None,
                      answerProvenance='Verified from the expanded Ecoreps solution in Dia.'))


def import_budgeting_variances(root=None):
    q = []
    add = lambda *a, **k: q.append(_q(*a, **k))
    none = 'None of the answers A)–D) is correct.'

    s = ('Bob’s grocery store budgets ordering at CHF 90/order, delivery at CHF 82/delivery, '
         'restocking at CHF 21/hour, and customer service at CHF 0.18/item. Beverages use '
         '14 orders, 12 deliveries, 16 hours and 4,600 items; fresh food 24, 62, 172 and '
         '34,200; packaged food 14, 19, 94 and 10,750.')
    add('bud-ss16-5.1','Budgeting','SS16 Mock Question 5','5.1',2,'Activity-based budgeting',s,
        'What is the total budgeted delivery cost for all product categories?',
        ['CHF 4,120','CHF 7,626','CHF 3,580','CHF 3,740',none],'b',
        'Multiply the delivery rate by total planned deliveries.','Total deliveries = 12 + 62 + 19 = 93; 93 × CHF 82 = CHF 7,626.')
    add('bud-ss16-5.2','Budgeting','SS16 Mock Question 5','5.2',2,'Activity-based budgeting',s,
        'What are total budgeted activity costs for beverages?',
        ['CHF 3,408','CHF 2,290','CHF 7,440','CHF 2,400',none],'a',
        'Budget each activity separately and add the four costs.','90×14 + 82×12 + 21×16 + 0.18×4,600 = 1,260 + 984 + 336 + 828 = CHF 3,408.')
    add('bud-ss16-5.3','Budgeting','SS16 Mock Question 5','5.3',2,'Activity-based budgeting',s,
        'What are total budgeted activity costs for packaged food?',
        ['CHF 7,332','CHF 6,874','CHF 6,727','CHF 9,229',none],'c',
        'Apply every driver rate to the packaged-food activity level.','90×14 + 82×19 + 21×94 + 0.18×10,750 = 1,260 + 1,558 + 1,974 + 1,935 = CHF 6,727.')

    s = ('Elody forecasts bicycle sales/service revenue: April CHF 5,500/1,000; May CHF 6,200/1,400; '
         'June CHF 9,700/2,600. Service is paid by card. Bicycle sales are 50% card, 10% cash and '
         '40% on account. Card fees are 3%; account sales collect 90% next month and 8% two months later.')
    add('bud-ss17-5.1','Budgeting','SS17 Question 5','5.1',2,'Cash collections',s,
        'How much cash is collected from May and June service revenue?',
        ['CHF 4,970','CHF 3,880','CHF 1,358','CHF 2,007',none],'b','Deduct the card fee from service receipts.','(1,400 + 2,600) × 97% = CHF 3,880.')
    add('bud-ss17-5.2','Budgeting','SS17 Question 5','5.2',2,'Cash collections',s,
        'How much June bicycle-sales revenue is received by credit card, excluding account collections?',
        ['CHF 620','CHF 970','CHF 853','CHF 2,980',none],'e','Half of June bicycle sales is paid by card and incurs the fee.','9,700 × 50% × 97% = CHF 4,704.50; none of A–D.')
    add('bud-ss17-5.3','Budgeting','SS17 Question 5','5.3',2,'Cash collections',s,
        'How much cash from bicycle sales on account is collected in June?',
        ['CHF 2,524','CHF 2,408','CHF 2,232','CHF 2,907',none],'b','June collections combine May’s 90% tranche and April’s 8% tranche.','6,200×40%×90% + 5,500×40%×8% = 2,232 + 176 = CHF 2,408.')

    s = 'Bär AG plans average monthly sales of 7,500 summer shoes at CHF 220 and 4,500 winter shoes at CHF 390.'
    add('bud-ss19-5.1','Budgeting','SS19 Mock Question 5','5.1',2,'Sales budget',s,'What is planned annual revenue?',
        ['CHF 46,780,000','CHF 41,440,000','CHF 40,860,000','CHF 49,140,000',none],'c','Annualize both monthly product revenues.','12 × (7,500×220 + 4,500×390) = CHF 40,860,000.')
    add('bud-ss19-5.2','Budgeting','SS19 Mock Question 5','5.2',2,'Production budget',s + ' Annual summer sales are 90,000; beginning inventory is 14,000 and minimum ending inventory 9,500.','What is minimum summer-shoe production?',
        ['85,500','86,600','81,000','82,400',none],'a','Production equals sales plus desired ending inventory less beginning inventory.','90,000 + 9,500 − 14,000 = 85,500 pairs.')
    add('bud-ss19-5.3','Budgeting','SS19 Mock Question 5','5.3',2,'Production budget',s + ' Annual winter sales are 54,000, planned production 30,000 and ending inventory 2,500.','What beginning winter-shoe inventory is required?',
        ['24,550','28,450','27,320','26,500',none],'d','Rearrange production = sales + ending − beginning.','Beginning inventory = 54,000 + 2,500 − 30,000 = 26,500 pairs.')

    add('bud-ss20-4.1','Budgeting','SS20 Question 4','4.1',2,'Master budget','', 'A master budget _____.',
        ['is the initial plan of what a company intends to accomplish and evolves from operating and financing decisions','is prepared only for manufacturing companies','improves market capitalization by definition','is another term for the financial budget',none],'a','The master budget integrates operating and financing plans.','Conceptual question; no calculation is required.','Easy')
    s = ('Moe Co forecasts sales/purchases: Jan CHF 67,000/32,000; Feb 88,000/45,000; Mar 100,000/58,000. '
         'Thirty percent of sales is collected in-month and 70% next month.')
    add('bud-ss20-4.2','Budgeting','SS20 Question 4','4.2',3,'Cash collections',s,'What cash is collected in March?',
        ['CHF 91,600','CHF 118,000','CHF 96,400','CHF 100,000',none],'a','March collections include 30% of March sales and 70% of February sales.','0.30×100,000 + 0.70×88,000 = 30,000 + 61,600 = CHF 91,600.','Hard')
    s = ('Frucci budgets 67,000 pairs of socks and 20,000 ties. Sock direct material rises from CHF 2.00 to 3.50 per unit; '
         'tie labor rises from CHF 8.20 to 14.00 per unit; all other data are unchanged.')
    add('bud-ss20-4.3','Budgeting','SS20 Question 4','4.3',2,'Profit planning',s,'By how much does budgeted operating income decrease?',
        ['CHF 116,000','CHF 514,500','CHF 216,500','CHF 100,500',none],'c','The profit decrease equals the two unit-cost increases at planned volumes.','(3.50−2.00)×67,000 + (14.00−8.20)×20,000 = 100,500 + 116,000 = CHF 216,500.')

    add('bud-as20-4.1','Budgeting','AS20 Question 4','4.1',2,'Production budget','Lime plans sales of 22,000 units, ending finished goods of 9,000 and beginning finished goods of 5,000.','How many units must be produced?',
        ['31,000','26,000','22,000','36,000',none],'b','Use the finished-goods inventory roll-forward.','22,000 + 9,000 − 5,000 = 26,000 units.')
    add('bud-as20-4.2','Budgeting','AS20 Question 4','4.2',2,'Income statement budget','Migos forecasts January revenue of CHF 203,000 and COGS of 68% of revenue.','What is budgeted gross margin?',
        ['CHF 101,500','CHF 64,960','CHF 48,000','CHF 138,040',none],'b','Gross-margin ratio is 32%.','203,000 × (1−0.68) = CHF 64,960.')

    s = 'Stellar’s 2020 results: sales CHF 962,000 on 160,250 units; COGS CHF 641,000; operating expenses CHF 269,000; operating income CHF 52,000.'
    add('bud-ss21-5.1','Budgeting','SS21 Question 5','5.1',3,'Sensitivity analysis',s + ' For 2021, price rises 13.5%, volume falls 11%, COGS is variable and operating expense fixed.','Should Stellar implement the price increase?',
        ['Yes, because sales revenue decreases','No, because volume decreases','No, because gross margin decreases','Yes, because operating income increases',none],'d','Compare the revised operating income with the current CHF 52,000.','Revenue = 962,000×1.135×0.89 = 971,902.30; COGS = 641,000×0.89 = 570,490; OI = 971,902.30−570,490−269,000 = CHF 132,412.30.')
    add('bud-ss21-5.2','Budgeting','SS21 Question 5','5.2',3,'Purchases budget','Revolution forecasts sales Jan–Apr of CHF 124,000, 111,000, 136,000 and 147,000. Gross margin is 25%; ending inventory is 10% of next month’s sales at cost.','What are February purchases?',
        ['CHF 103,200','CHF 85,125','CHF 83,250','CHF 30,600',none],'b','Purchases equal February COGS plus desired ending inventory less beginning inventory.','COGS Feb = 111,000×75%=83,250; end =136,000×75%×10%=10,200; begin=111,000×75%×10%=8,325; purchases=CHF 85,125.')

    add('bud-as24-4.1','Budgeting','AS24 Question 4','4.1',3,'Purchases budget','Doyo forecasts sales Jan–Apr of CHF 124,000, 111,000, 136,000 and 147,000. Gross margin is 25%; ending inventory is 20% of next month’s sales at cost.','What are February purchases?',
        ['CHF 103,200','CHF 87,000','CHF 83,250','CHF 30,600',none],'b','Adjust February COGS for the 20% inventory policy.','83,250 + (136,000×75%×20%) − (111,000×75%×20%) = 83,250 +20,400−16,650 = CHF 87,000.')
    add('bud-as24-4.2','Budgeting','AS24 Question 4','4.2',2,'Income statement budget','GroceryNow forecasts January revenue CHF 203,000 and COGS at 58% of revenue.','What is gross profit?',
        ['CHF 101,500','CHF 85,260','CHF 64,960','CHF 138,040',none],'b','Gross-profit ratio is 42%.','203,000×42% = CHF 85,260.')

    add('bud-as25-4.1','Budgeting','AS25 Question 4','4.1',3,'Sales budget','Tsinghue’s 2025 sales were CHF 961,000 on 161,000 units. For 2026 price rises 13.5% and volume falls 9%.','What is budgeted 2026 sales revenue, rounded to a whole CHF?',
        ['CHF 992,569','CHF 961,000','CHF 874,510','CHF 1,090,735',none],'a','Apply both price and volume changes.','961,000×1.135×0.91 = CHF 992,568.85 → CHF 992,569.')
    add('bud-as25-4.2','Budgeting','AS25 Question 4','4.2',3,'Direct labor budget','Rollx AP362 plans sales of 20,000 units, ending finished goods 5,000 and beginning finished goods 1,100. Each unit requires 2 assembly and 3 polishing hours.','What direct labor hours are budgeted?',
        ['48,300 assembly; 32,200 polishing','47,800 assembly; 71,700 polishing','71,700 assembly; 47,800 polishing','32,200 assembly; 48,300 polishing',none],'b','Compute production first, then multiply by hours per unit.','Production = 20,000+5,000−1,100=23,900; assembly=23,900×2=47,800; polishing=23,900×3=71,700.')

    # Variances
    s = 'Dave AG budgets price CHF 1,326, variable cost CHF 504, fixed overhead CHF 4,400,000 and 8,800 units; actual production and sales are 10,400 units.'
    add('var-ss16-6.1','Variances','SS16 Mock Question 6','6.1',2,'Flexible budgets',s,'What is flexible-budget operating income?',
        ['CHF 4,210,800','CHF 4,148,800','CHF 3,247,400','CHF 4,560,300',none],'b','Use actual volume with budgeted price and cost.','10,400×(1,326−504)−4,400,000 = CHF 4,148,800.')
    add('var-ss16-6.2','Variances','SS16 Mock Question 6','6.2',3,'Sales-volume variance',s,'What is the sales-volume variance in operating income?',
        ['CHF 1,315,200 U','CHF 1,212,700 U','CHF 1,212,700 F','CHF 1,315,200 F',none],'d','Multiply the volume difference by budgeted contribution per unit.','(10,400−8,800)×(1,326−504) = 1,600×822 = CHF 1,315,200 favorable.')
    add('var-ss16-6.3','Variances','SS16 Mock Question 6','6.3',3,'Fixed-overhead variance',s,'What is the fixed-overhead production-volume variance?',
        ['CHF 500,000','CHF 960,000','CHF 800,000','CHF 470,000',none],'c','Compare budgeted fixed overhead with overhead allocated at actual output.','Rate = 4,400,000/8,800 = 500 per unit; allocated = 10,400×500=5,200,000; variance = 4,400,000−5,200,000 = CHF 800,000 favorable.')

    s = 'Flick budgets 200 car inspections and CHF 30,000 revenue; actual inspections are 225 and actual revenue CHF 39,375. Budgeted contribution margin is CHF 22,900.'
    add('var-ss17-6.1','Variances','SS17 Question 6','6.1',2,'Flexible-budget variance',s,'What is the revenue flexible-budget variance?',
        ['CHF 5,625 F','CHF 5,625 U','CHF 4,750 F','CHF 4,750 U',none],'a','Restate budgeted revenue at actual volume, then compare with actual.','Flexible revenue = 30,000/200×225=33,750; 39,375−33,750 = CHF 5,625 favorable.')
    add('var-ss17-6.2','Variances','SS17 Question 6','6.2',2,'Sales-volume variance',s,'What is the sales-volume variance in contribution margin?',
        ['CHF 4,363 F','CHF 4,363 U','CHF 2,862 U','CHF 2,862 F',none],'e','The exact calculation is CHF 2,862.50 favorable; none of the printed choices states it exactly.','22,900/200×(225−200) = CHF 2,862.50 favorable; therefore E.',changes=('Preserved the source rounding inconsistency and selected E for the exact result.',))

    s = 'Daniels: actual price CHF 18, budget CHF 19; actual units 280,000, budget 278,000; actual/budget variable costs CHF 960,000/886,000; fixed costs CHF 60,000/51,000.'
    add('var-ss20-5.1','Variances','SS20 Question 5','5.1',2,'Static-budget variance',s,'What is the static-budget variance in operating income?',
        ['CHF 325,000 U','CHF 316,000 F','CHF 325,000 F','CHF 316,000 U',none],'a','Compare actual operating income with static-budget operating income.','Actual OI=280,000×18−960,000−60,000=4,020,000; budget OI=278,000×19−886,000−51,000=4,345,000; variance=CHF 325,000 U.')
    add('var-ss20-5.2','Variances','SS20 Question 5','5.2',2,'Flexible budgets','Great Cabinets budgets variable cost CHF 463,910 at 23,000 units; actual volume is 18,000.','What variable cost appears in the flexible budget?',
        ['CHF 592,774','CHF 363,060','CHF 463,910','CHF 460,000',none],'b','Scale budgeted variable cost to actual volume.','463,910/23,000×18,000 = CHF 363,060.')
    add('var-ss20-5.3','Variances','SS20 Question 5','5.3',2,'Direct labor price variance','Genent produced 4,000 units. Actual labor was 1,290 hours at CHF 18.40; standard rate is CHF 18.00.','What is the direct labor price variance?',
        ['CHF 3,600 U','CHF 1,620 U','CHF 516 F','CHF 3,600 F',none],'e','The calculated CHF 516 is unfavorable, while option C labels it favorable.','1,290×(18.40−18.00) = CHF 516 unfavorable; therefore E.',changes=('Preserved the source sign inconsistency and selected E.',))
    add('var-ss20-5.4','Variances','SS20 Question 5','5.4',1,'Fixed-overhead variances','', 'For fixed manufacturing overhead there is no ____ variance.',
        ['production-volume','efficiency','spending','flexible-budget',none],'b','Fixed overhead has spending/flexible-budget and production-volume variances, but no efficiency variance.','Conceptual question; no calculation is required.','Easy')

    add('var-as20-5.1','Variances','AS20 Question 5','5.1',2,'Flexible budgets','Tenindo budgets variable cost CHF 377,550 at 15,000 units; actual volume is 12,000.','What variable cost appears in the flexible budget?',
        ['CHF 302,040','CHF 377,550','CHF 471,938','CHF 375,000',none],'a','Scale variable cost to actual volume.','377,550/15,000×12,000 = CHF 302,040.')
    add('var-as20-5.2','Variances','AS20 Question 5','5.2',2,'Static-budget variance','Michaelsoft price is CHF 21. Actual/budget units are 177,000/185,000; variable costs CHF 1,088,000/1,289,000; fixed costs CHF 805,000/777,000.','What is the static-budget variance in operating income?',
        ['CHF 8,000 U','CHF 173,000 U','CHF 5,000 F','CHF 33,000 F',none],'c','Compute both operating-income amounts.','Actual=177,000×21−1,088,000−805,000=1,824,000; budget=185,000×21−1,289,000−777,000=1,819,000; CHF 5,000 F.')
    add('var-as20-5.3','Variances','AS20 Question 5','5.3',2,'Direct material price variance','MultiMix standard material is 1 kg at CHF 3.25. Actual production is 1,000 units using 1,400 kg at CHF 3.00.','What is the direct material price variance?',
        ['CHF 950 U','CHF 350 U','CHF 950 F','CHF 350 F',none],'d','Price variance uses actual input quantity.','1,400×(3.00−3.25) = −CHF 350 = CHF 350 favorable.')
    add('var-as20-6.1','Variances','AS20 Question 6','6.1',2,'Fixed-overhead variances','', 'Which expression calculates the fixed-overhead spending variance?',
        ['Actual costs incurred − flexible-budget amount','Static-budget amount − fixed overhead allocated for actual output','Static-budget amount − flexible-budget amount','Flexible-budget amount − fixed overhead allocated for actual output',none],'a','For fixed overhead, the flexible-budget amount equals budgeted fixed overhead; compare actual with that amount.','Fixed-OH spending variance = actual fixed OH − budgeted (flexible-budget) fixed OH.','Easy')

    add('var-ss21-6.1','Variances','SS21 Question 6','6.1',2,'Flexible budgets','AlphaProdukte budgets variable cost CHF 180,000 at 12,000 units; actual volume is 16,000.','What variable cost appears in the flexible budget?',
        ['CHF 180,000','CHF 126,000','CHF 12,000','CHF 240,000',none],'d','Scale budgeted variable cost to actual volume.','180,000/12,000×16,000 = CHF 240,000.')
    add('var-ss21-6.2','Variances','SS21 Question 6','6.2',2,'Direct material variances','Materials flexible-budget variance is CHF 7,000 U and material price variance CHF 33,000 F.','What is the material efficiency variance?',
        ['CHF 15,000 U','CHF 1,000 F','CHF 40,000 F','CHF 30,000 U',none],'e','Efficiency must offset the favorable price variance and leave CHF 7,000 unfavorable overall.','7,000 U = efficiency + 33,000 F; efficiency = CHF 40,000 U, which is not A–D.',changes=('Selected E because option C has the correct magnitude but wrong direction.',))
    add('var-ss21-6.3','Variances','SS21 Question 6','6.3',2,'Flexible budgets','Actual revenue is CHF 21,690,000; revenue flexible-budget variance is CHF 1,110,000 F. Actual quantity is 49,000 and budget quantity 44,600.','What are flexible-budget revenue A and static-budget revenue B?',
        ['CHF 22,800,000; CHF 20,952,000','CHF 23,500,490; CHF 18,832,510','CHF 20,580,000; CHF 18,732,000','CHF 19,850,000; CHF 20,560,190',none],'c','Remove the favorable variance, then scale to budget quantity.','A=21,690,000−1,110,000=20,580,000; B=20,580,000/49,000×44,600=CHF 18,732,000.')

    add('var-as24-5.1','Variances','AS24 Question 5','5.1',2,'Flexible budgets','Pearl’s static budget has 20,500 units and CHF 615,000 revenue; actual volume is 19,000.','What sales revenue appears in the flexible budget?',
        ['CHF 615,040','CHF 510,000','CHF 635,500','CHF 570,000',none],'d','Use the static price per unit at actual volume.','615,000/20,500×19,000 = CHF 570,000.')
    add('var-as24-5.2','Variances','AS24 Question 5','5.2',2,'Direct material standards','Nunangat uses a standard 2 m² of wool per coat at CHF 45/m². Actual input is 1.70 m² at CHF 36/m².','What is the budgeted wool cost per unit of output?',
        ['CHF 61.20','CHF 72.00','CHF 76.50','CHF 90.00',none],'d','Budgeted cost per output uses standard quantity and standard price.','2.00×CHF 45 = CHF 90 per coat.')
    add('var-as24-5.4','Variances','AS24 Question 5','5.4',1,'Variance diagram','A diagram shows planned and actual price and volume; the marked area uses planned price and planned quantity.','What does the marked area denote?',
        ['the flexible budget','the static budget','the flexible-input budget','the contribution margin',none],'b','Planned quantity at planned price is the static-budget amount.','Conceptual diagram: static budget = planned input quantity × planned input price.','Easy')

    add('var-as24-6.1','Variances','AS24 Question 6','6.1',2,'Variable-overhead variances','', 'Which expression calculates the variable-overhead flexible-budget variance?',
        ['Actual variable overhead incurred − flexible-budget variable overhead','Static budget − fixed overhead allocated for actual output','Static variable overhead − flexible-budget variable overhead','Flexible-budget variable overhead − fixed overhead allocated for actual output',none],'a','Flexible-budget variance compares actual cost with flexible-budget cost.','Variable-OH flexible-budget variance = actual variable OH − flexible-budget variable OH.','Easy')
    add('var-as24-6.2','Variances','AS24 Question 6','6.2',3,'Variable-overhead budgets','Gilletson budgets 2,400 units, 14,400 machine-hours and CHF 158,400 variable overhead. Actual output is 3,330 units, actual hours 18,900 and actual variable overhead CHF 138,400.','What is the flexible-budget variable-overhead amount?',
        ['CHF 207,900','CHF 219,780','CHF 132,300','CHF 234,960',none],'b','A flexible budget uses budgeted hours per unit and budgeted rate at actual output.','158,400/2,400×3,330 = CHF 219,780.')

    s = 'LocaTea actual/flexible/static data include actual operating income CHF 17,740, flexible-budget operating income CHF 16,080 and static operating income CHF 15,140.'
    add('var-as25-5.1','Variances','AS25 Question 5','5.1',2,'Flexible-budget variance',s,'What is the operating-income flexible-budget variance?',
        ['CHF 1,660 F','CHF 1,660 U','CHF 340 U','CHF 340 F',none],'a','Higher actual income is favorable.','17,740−16,080 = CHF 1,660 favorable.')
    add('var-as25-5.2','Variances','AS25 Question 5','5.2',2,'Flexible budgets','Stellar budgets variable cost CHF 360,000 at 24,000 units; actual volume is 32,000.','What variable cost appears in the flexible budget?',
        ['CHF 120,000','CHF 690,000','CHF 480,000','CHF 320,000',none],'c','Scale budgeted variable cost to actual volume.','360,000/24,000×32,000 = CHF 480,000.')
    add('var-as25-5.3','Variances','AS25 Question 5','5.3',2,'Direct material variances','Materials flexible-budget variance is CHF 6,000 U and material price variance CHF 29,000 F.','What is the material efficiency variance?',
        ['CHF 25,000 U','CHF 1,000 F','CHF 40,000 F','CHF 40,000 U',none],'e','The exact result is CHF 35,000 U, absent from A–D.','Efficiency = 6,000 U − (29,000 F) = CHF 35,000 U; therefore E.')
    add('var-as25-6.1','Variances','AS25 Question 6','6.1',4,'Variable-overhead budgets','Djoker budgets 8,000 units, 24,000 machine-hours and CHF 288,000 variable overhead. Actual output is 8,500 units, actual hours 25,500 and actual variable overhead CHF 250,000.','What is the flexible-input-budget amount for variable manufacturing overhead?',
        ['CHF 306,000','CHF 312,000','CHF 288,500','CHF 250,000',none],'a','Apply the budgeted variable-overhead rate per machine-hour to actual machine-hours.','Budgeted rate=288,000/24,000=CHF 12/hour; flexible-input budget=25,500×12=CHF 306,000.','Hard')
    assert len(q) == 45
    return q
