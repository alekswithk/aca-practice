"""20 AI-generated Capital Budgeting questions."""
from ai_common import add, D, r, chf, n, pct, table, none_wrong, none_right
T = 'Capital Budgeting'
MIS = 'capital budgeting-calculation'
f3 = lambda rate, t: r(1 / (1 + D(rate)) ** t, 3)   # discount factor rounded to three decimals, as in the past exams

# Scenario A: Lagona Druck AG
cost, flows, rate = 480_000, [140_000, 150_000, 130_000, 120_000, 100_000], D('0.10')
cum, pb = 0, None
for i, f in enumerate(flows):
 if cum + f >= cost: pb = i + D(cost - cum) / f; break
 cum += f
aarr = 100 * (D(sum(flows)) - cost) / len(flows) / cost
pv = sum(f * f3(rate, t) for t, f in enumerate(flows, 1)); npv = pv - cost
LAG = ('Lagona Druck AG considers a new digital printing press. It costs CHF 480,000, has a five-year life and no terminal value. Depreciation is straight-line. Expected cash savings:\n\n'
       + table(['End of year', 'Cash savings (CHF)'], [[str(t), n(f)] for t, f in enumerate(flows, 1)]) +
       '\n\nThe required rate of return is 10%. Ignore taxes. Where discounting is needed, use discount factors rounded to three decimals.')
G = 'Lagona Druck press'
add('ai-cap-01', T, 'Payback period', 'Medium', '(2 marks) What is the payback period? Round to one decimal place.',
 [(f'{n(D(cost)*5/sum(flows),1)} years', 'Uses the average saving. With uneven cash flows, accumulate the actual savings year by year.', MIS),
  (f'{n(pb,1)} years', f'After three years 420,000 is recovered; 60,000 of the 120,000 in year 4 is needed: 3 + 0.5 = {n(pb,1)} years.', None),
  ('3.0 years', 'Stops after three years, but only CHF 420,000 has been recovered by then.', MIS),
  ('4.0 years', 'Counts all of year 4, although payback is reached halfway through it.', MIS), none_wrong('b')],
 'b', 'With uneven cash flows, payback = years before full recovery + unrecovered amount / cash flow of the recovery year.', scenario=LAG, ev='capital', group=G,
 calc=f'Cumulative: 140,000; 290,000; 420,000; 540,000. Payback = 3 + 60,000/120,000 = {n(pb,1)} years.', check={'f': '3 + (c - a - b - d)/e', 'v': {'c': cost, 'a': 140_000, 'b': 150_000, 'd': 130_000, 'e': 120_000}, 'x': pb, 'dp': 1, 'unit': 'years'})
add('ai-cap-02', T, 'Accounting rate of return', 'Medium', '(2 marks) What is the accounting rate of return on the initial investment? Round to one decimal.',
 [(pct(100 * D(sum(flows)) / 5 / cost), 'Uses average cash savings and forgets depreciation.', MIS), (pct(aarr), f'Average income = (640,000 − 480,000) / 5 = 32,000; 32,000 / 480,000 = {pct(aarr)}.', None),
  (pct(100 * (D(sum(flows)) - cost) / cost), 'Uses total income over five years instead of the annual average.', MIS), (pct(2 * aarr), 'Divides by the average investment (half the cost). The question asks for the initial investment.', MIS), none_wrong('b')],
 'b', 'AARR = average annual operating income / initial investment. Operating income = cash savings − depreciation.', scenario=LAG, ev='capital', group=G,
 calc=f'Depreciation 96,000 per year. Average income = 128,000 − 96,000 = 32,000. AARR = {pct(aarr)}.', check={'f': '100*(s - c)/5/c', 'v': {'s': sum(flows), 'c': cost}, 'x': aarr, 'dp': 1, 'unit': 'percent'})
add('ai-cap-03', T, 'Net present value', 'Hard', '(4 marks) Calculate the NPV of the press and decide whether Lagona should buy it on financial grounds.',
 [(f'{chf(npv)}; yes', f'PV of savings = {n(pv)}; NPV = {n(pv)} − 480,000 = {chf(npv)} > 0, so buy.', None),
  (f'{chf(sum(flows) - cost)}; yes', 'Ignores the time value of money.', MIS),
  (f'{chf(npv - flows[-1]*f3(rate,5))}; no', 'Leaves out the year-5 saving.', MIS),
  (f'{chf(sum(f * f3(rate, t + 1) for t, f in enumerate(flows, 1)) - cost)}; no', 'Discounts every flow one year too far.', MIS), none_wrong('a')],
 'a', 'NPV = present value of future cash flows − initial investment. Accept if NPV > 0.', scenario=LAG, ev='capital', group=G,
 calc='Factors 0.909, 0.826, 0.751, 0.683, 0.621. PV = ' + ' + '.join(n(f * f3(rate, t)) for t, f in enumerate(flows, 1)) + f' = {n(pv)}. NPV = {chf(npv)}.',
 check={'f': 'a*0.909 + b*0.826 + c*0.751 + d*0.683 + e*0.621 - i', 'v': {'a': 140_000, 'b': 150_000, 'c': 130_000, 'd': 120_000, 'e': 100_000, 'i': cost}, 'x': npv})
add('ai-cap-04', T, 'AARR and IRR', 'Medium', '(1 mark) Without calculating it, what can you say about the press’s internal rate of return?',
 [('It is below 10%, because the AARR is below 10%.', 'AARR uses accounting income and ignores timing; it does not bound the IRR.', MIS),
  ('It is exactly 10%.', 'At the IRR, NPV is zero. Here NPV at 10% is positive.', MIS),
  ('It is above 10%, because the NPV at 10% is positive.', 'NPV falls as the rate rises; a positive NPV at 10% means the zero point lies above 10%.', None),
  ('It cannot be judged without the tax rate.', 'Taxes are ignored in this question.', MIS), none_wrong('c')],
 'c', 'For a conventional project, NPV > 0 at the required rate means IRR > required rate.', scenario=LAG, ev='capital', group=G)

# Scenario B: Velox Kurier AG
vc, vf, vy, vr, wc = 236_000, 59_000, 6, D('0.08'), 30_000
vpv = sum(vf * f3(vr, t) for t in range(1, vy + 1)); vnpv = vpv - vc; vnpw = vnpv - wc + wc * f3(vr, vy)
VEL = ('Velox Kurier AG plans to buy electric delivery vans for CHF 236,000. They generate additional cash inflows of CHF 59,000 per year for six years and have no terminal value. '
       'The required rate of return is 8%. Ignore taxes. Use discount factors rounded to three decimals: 0.926, 0.857, 0.794, 0.735, 0.681, 0.630.')
G = 'Velox Kurier vans'
add('ai-cap-05', T, 'Static payback period', 'Easy', '(2 marks) Calculate the static payback period.',
 [(f'{n(D(vc)/vf,1)} years', f'236,000 / 59,000 = {n(D(vc)/vf,1)} years.', None), ('5.0 years', 'This is roughly the discounted payback. The question asks for static payback, without discounting.', MIS),
  (f'{n(D(vc)/(vf*vy),2)} years', 'Divides by total inflows over six years.', MIS), (f'{n(D(vc)/(vf - D(vc)/vy),1)} years', 'Uses accounting income (cash flow minus depreciation). Payback uses cash flows.', MIS), none_wrong('a')],
 'a', 'With equal annual cash flows, payback = investment / annual cash flow.', scenario=VEL, ev='capital', group=G,
 calc=f'236,000 / 59,000 = {n(D(vc)/vf,1)} years.', check={'f': 'c/f', 'v': {'c': vc, 'f': vf}, 'x': D(vc) / vf, 'dp': 1, 'unit': 'years'})
add('ai-cap-06', T, 'Net present value', 'Medium', '(3 marks) Calculate the NPV of the vans.',
 [(chf(vf * vy - vc), 'Ignores discounting.', MIS), (chf(vpv), 'This is the present value of the inflows, before deducting the investment.', MIS),
  (chf(vnpv), f'59,000 × (sum of factors 4.623) = {n(vpv)}; − 236,000 = {chf(vnpv)}.', None), (chf(vf * f3(vr, 6) * vy - vc), 'Discounts every inflow with the year-6 factor.', MIS), none_wrong('c')],
 'c', 'NPV = Σ cash flow × discount factor − investment.', scenario=VEL, ev='capital', group=G,
 calc=f'Sum of factors = 4.623. PV = 59,000 × 4.623 = {n(vpv)}. NPV = {chf(vnpv)}.', check={'f': 'f*(0.926 + 0.857 + 0.794 + 0.735 + 0.681 + 0.630) - c', 'v': {'f': vf, 'c': vc}, 'x': vnpv})
add('ai-cap-07', T, 'Net present value and working capital', 'Hard', '(4 marks) The vans also need CHF 30,000 of extra working capital (spare batteries and parts) at the start, fully released at the end of year 6. What is the NPV including working capital?',
 [(chf(vnpv - wc), 'Deducts the working capital but forgets that it comes back in year 6.', MIS), (chf(vnpv), 'Ignores the working capital.', MIS),
  (chf(vnpv - wc * f3(vr, vy) + wc), 'Swaps the timing: discounts the outlay as if it were in year 6 and treats the release as immediate.', MIS), (chf(vnpw), f'{n(vnpv)} − 30,000 + 30,000 × 0.630 = {chf(vnpw)}.', None), none_wrong('d')],
 'd', 'Working capital is an outflow at the start and an inflow when released; only its timing cost affects NPV.', scenario=VEL, ev='capital', group=G,
 calc=f'Working capital effect = −30,000 + 18,900 = −11,100. NPV = {n(vnpv)} − 11,100 = {chf(vnpw)}.', check={'f': 'f*(0.926 + 0.857 + 0.794 + 0.735 + 0.681 + 0.630) - c - w + w*0.630', 'v': {'f': vf, 'c': vc, 'w': wc}, 'x': vnpw})

add('ai-cap-08', T, 'Accounting rate of return limitations', 'Easy', '(1 mark) Which of the following is a limitation of the accounting rate of return?',
 [('It ignores the time value of money.', 'AARR averages accounting income without discounting.', None), ('It needs a discount rate.', 'AARR does not use a discount rate.', MIS),
  ('It ignores depreciation.', 'AARR uses operating income, which includes depreciation.', MIS), ('It can only be used for projects with equal cash flows.', 'AARR works with uneven income too.', MIS), none_wrong('a')],
 'a', 'AARR is simple but ignores the timing of cash flows.', ev='capital')
add('ai-cap-09', T, 'Capital budgeting process', 'Easy', '(1 mark) Which stage comes directly after identifying potential investments in the capital budgeting process?',
 [('Implementing the project and tracking its performance', 'This comes last.', MIS), ('Making predictions: estimating the costs and benefits of each option', 'After identification, managers gather information and forecast the cash flows.', None),
  ('Choosing the project with the best financial result', 'You can only choose after forecasting.', MIS), ('Obtaining funding', 'Funding follows the decision.', MIS), none_wrong('b')],
 'b', 'Stages: identify projects, obtain information and make predictions, choose, obtain funding, implement and control.', ev='capital')
add('ai-cap-10', T, 'AARR and IRR', 'Medium', '(1 mark) Two projects are mutually exclusive. Project X has the higher IRR, Project Y the higher NPV at the required rate. Which project maximizes shareholder value?',
 [('Project X, because a higher IRR always means more value', 'IRR is a percentage and ignores project size.', MIS), ('Project Y, because NPV measures the value added in francs', 'NPV shows the absolute value created at the required rate.', None),
  ('Neither, because the two methods disagree', 'When they disagree, NPV decides.', MIS), ('The project with the shorter payback', 'Payback ignores cash flows after recovery and the time value of money.', MIS), none_wrong('b')],
 'b', 'NPV is the preferred criterion for mutually exclusive projects.', ev='capital')
add('ai-cap-11', T, 'Payback period', 'Easy', '(1 mark) Which statement about the payback method is correct?',
 [('It accounts for all cash flows over the project’s life.', 'It ignores cash flows after the payback point.', MIS), ('It ignores cash flows that occur after the investment has been recovered.', 'That is its main weakness for profitability.', None),
  ('It discounts cash flows at the required rate.', 'Static payback does not discount.', MIS), ('It measures the value a project adds to the firm.', 'That is NPV.', MIS), none_wrong('b')],
 'b', 'Payback measures how fast money comes back, not how much value is created.', ev='capital')
add('ai-cap-12', T, 'Net present value', 'Easy', '(1 mark) Which rate should be used to discount the cash flows of an average-risk project?',
 [('The company’s required rate of return (cost of capital)', 'It reflects what investors require for this level of risk.', None), ('The current inflation rate', 'Inflation alone does not reflect investors’ required return.', MIS),
  ('The project’s accounting rate of return', 'AARR is a result, not a discount rate.', MIS), ('The interest rate on a savings account', 'This is too low for the risk of a business project.', MIS), none_wrong('a')],
 'a', 'Discount at the required rate of return, which reflects the opportunity cost of capital.', ev='capital')

# Scenario C: Mühlebach Wäscherei replacement
nm, old, sav, disp, mr = 350_000, 40_000, 95_000, 25_000, D('0.09')
fac = [f3(mr, t) for t in range(1, 6)]
mpv = sav * sum(fac) + disp * fac[-1]; mnpv = mpv - (nm - old)
MUE = ('Mühlebach Wäscherei AG can replace its old washing machine. The new machine costs CHF 350,000 now. The old machine can be sold now for CHF 40,000. The new machine saves CHF 95,000 in operating costs each year for five years '
       'and can be sold for CHF 25,000 at the end of year 5. Required rate of return 9%. No taxes. Use discount factors rounded to three decimals: 0.917, 0.842, 0.772, 0.708, 0.650.')
G = 'Mühlebach replacement'
add('ai-cap-13', T, 'Net present value', 'Hard', '(4 marks) Calculate the NPV of the replacement and decide whether to buy the new machine.',
 [(f'{chf(mnpv - old)}; yes', 'Forgets the CHF 40,000 from selling the old machine today.', MIS), (f'{chf(mnpv)}; yes', f'PV savings {n(sav*sum(fac))} + PV disposal {n(disp*fac[-1])} − net investment 310,000 = {chf(mnpv)}.', None),
  (f'{chf(mnpv - disp*fac[-1])}; yes', 'Leaves out the CHF 25,000 disposal value in year 5.', MIS), (f'{chf(sav*5 + disp - nm + old)}; yes', 'Ignores discounting.', MIS), none_wrong('b')],
 'b', 'Relevant cash flows: new machine cost, old machine proceeds, savings and terminal disposal value.', scenario=MUE, ev='capital', group=G,
 calc=f'Sum of factors = {n(sum(fac),3)}. PV savings = 95,000 × {n(sum(fac),3)} = {n(sav*sum(fac))}. PV disposal = 25,000 × 0.650 = 16,250. NPV = {n(mpv)} − 310,000 = {chf(mnpv)}.',
 check={'f': 's*(0.917 + 0.842 + 0.772 + 0.708 + 0.650) + d*0.650 - n + o', 'v': {'s': sav, 'd': disp, 'n': nm, 'o': old}, 'x': mnpv})
add('ai-cap-14', T, 'Net present value', 'Easy', '(1 mark) What is the net initial investment at time 0?',
 [(chf(nm), 'Ignores the sale of the old machine.', MIS), (chf(nm + old), 'Adds the sale proceeds instead of deducting them.', MIS),
  (chf(nm - old), '350,000 − 40,000 = 310,000.', None), (chf(nm - old - disp), 'Deducts the year-5 disposal value now.', MIS), none_wrong('c')],
 'c', 'Net initial investment = purchase price − proceeds from disposing of the old asset now.', scenario=MUE, ev='capital', group=G,
 calc='350,000 − 40,000 = CHF 310,000.', check={'f': 'n - o', 'v': {'n': nm, 'o': old}, 'x': nm - old})
add('ai-cap-15', T, 'Static payback period', 'Medium', '(2 marks) What is the static payback period of the replacement, based on the net initial investment? Round to one decimal.',
 [(f'{n(D(nm)/sav,1)} years', 'Uses the gross price of CHF 350,000.', MIS), (f'{n(D(nm-old)/sav,1)} years', f'310,000 / 95,000 = {n(D(nm-old)/sav,1)} years.', None),
  (f'{n(D(nm-old-disp)/sav,1)} years', 'Deducts the year-5 disposal value from the investment.', MIS), (f'{n(D(nm-old)*5/(sav*5+disp),1)} years', 'Spreads the year-5 disposal value over the five years as extra savings.', MIS), none_wrong('b')],
 'b', 'Payback = net investment / annual cash saving.', scenario=MUE, ev='capital', group=G,
 calc=f'310,000 / 95,000 = {n(D(nm-old)/sav,2)} → {n(D(nm-old)/sav,1)} years.', check={'f': '(n - o)/s', 'v': {'n': nm, 'o': old, 's': sav}, 'x': D(nm - old) / sav, 'dp': 1, 'unit': 'years'})

pi, pl, pt, pf = 600_000, 8, 40_000, 120_000
pa = 100 * (pf - D(pi - pt) / pl) / pi
add('ai-cap-16', T, 'Accounting rate of return', 'Medium', '(2 marks) Primo Solar AG invests CHF 600,000 in a rooftop installation with an eight-year life and a terminal value of CHF 40,000. Annual cash inflows are CHF 120,000. Depreciation is straight-line. What is the accounting rate of return on the initial investment? Round to one decimal.',
 [(pct(100 * D(pf) / pi), 'Uses cash inflows and forgets depreciation.', MIS), (pct(100 * (pf - D(pi) / pl) / pi), 'Ignores the terminal value when computing depreciation.', MIS),
  (pct(pa), f'Depreciation = (600,000 − 40,000) / 8 = 70,000. Income = 50,000. 50,000 / 600,000 = {pct(pa)}.', None), (pct(100 * (pf - D(pi - pt) / pl) / (D(pi + pt) / 2)), 'Divides by the average investment.', MIS), none_wrong('c')],
 'c', 'AARR = (cash inflow − depreciation) / initial investment.', ev='capital',
 calc=f'(120,000 − 70,000) / 600,000 = {pct(pa)}.', check={'f': '100*(f - (i - t)/l)/i', 'v': {'f': pf, 'i': pi, 't': pt, 'l': pl}, 'x': pa, 'dp': 1, 'unit': 'percent'})
add('ai-cap-17', T, 'Net present value', 'Easy', '(1 mark) Which statement about the NPV method is correct?',
 [('A project with NPV = 0 earns exactly the required rate of return.', 'At NPV = 0, the project just covers the cost of capital.', None), ('NPV ignores cash flows after the payback period.', 'That is the payback method.', MIS),
  ('NPV is based on accrual accounting income.', 'NPV uses cash flows.', MIS), ('A higher discount rate increases NPV.', 'A higher rate lowers the present value of future inflows.', MIS), none_wrong('a')],
 'a', 'NPV discounts all cash flows at the required rate.', ev='capital')
add('ai-cap-18', T, 'Net present value', 'Medium', '(1 mark) Lagona’s required rate of return rises from 10% to 14%. What happens to the press’s NPV and IRR?',
 [('NPV falls; IRR is unchanged.', 'The IRR depends only on the project’s cash flows; NPV falls because the inflows are discounted more heavily.', None),
  ('Both fall.', 'The IRR does not depend on the required rate.', MIS), ('NPV rises; IRR falls.', 'Directions are wrong.', MIS), ('Both are unchanged.', 'NPV depends on the discount rate.', MIS), none_wrong('a')],
 'a', 'The required rate affects NPV, not IRR.', ev='capital')
add('ai-cap-19', T, 'AARR and IRR', 'Easy', '(1 mark) What is the internal rate of return?',
 [('The discount rate at which the NPV of a project equals zero', 'That is the definition.', None), ('The average accounting income divided by the investment', 'That is the AARR.', MIS),
  ('The rate set by the board as the minimum return', 'That is the required rate (hurdle rate).', MIS), ('The time needed to recover the investment', 'That is payback.', MIS), none_wrong('a')],
 'a', 'IRR solves NPV = 0.', ev='capital')
irr_c, irr_f = 100_000, 115_500
add('ai-cap-20', T, 'AARR and IRR', 'Medium', '(2 marks) A one-year project costs CHF 100,000 today and returns CHF 115,500 at the end of the year. What is its IRR?',
 [(pct(D(irr_f - irr_c) / irr_c * 100), '115,500 / 100,000 − 1 = 15.5%.', None), (pct(D(irr_f) / irr_c * 100), 'This is the gross return factor, not the rate.', MIS),
  (pct(D(irr_f - irr_c) / irr_f * 100), 'Divides the gain by the year-end amount instead of the investment.', MIS), ('10.0%', 'Assumes a typical required rate; the IRR comes from the project’s own cash flows.', MIS), none_wrong('a')],
 'a', 'IRR solves −100,000 + 115,500 / (1 + IRR) = 0.', ev='capital',
 calc='1 + IRR = 115,500 / 100,000 = 1.155 → IRR = 15.5%.', check={'f': '100*(f/c - 1)', 'v': {'f': irr_f, 'c': irr_c}, 'x': D(irr_f - irr_c) / irr_c * 100, 'dp': 1, 'unit': 'percent'})
