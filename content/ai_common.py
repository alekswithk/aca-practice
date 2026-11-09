"""Shared builder for AI-generated questions.

Every numeric question carries two separate calculations:
1. the Python arithmetic written next to the question, which produces the option texts;
2. a formula string, evaluated here and again in validate_bank.py with Decimal.
The builder refuses a question when the two disagree, when the correct option does not
show the computed value, or when a wrong option shows it.
"""
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING, ROUND_FLOOR
import re

D = lambda x: Decimal(str(x))
QUESTIONS = []
SOURCE = 'AI-generated study question'
NONE_TEXT = 'None of the answers A)–D) is correct.'
AI_NOTE = 'AI-generated practice question. Figures were recomputed by script; wording is not from an official exam.'

EV = {
 'frameworks': {'path':'ACA Course Materials/Week 1/Module 1 — Transcript Summary.md','section':'Sections 2–4: principles and Swiss reporting'},
 'equity': {'path':'ACA Course Materials/Week 1/Module 1 — Transcript Summary.md','section':'Section 7: initial cost, profit, dividends and hidden-reserve depreciation'},
 'acquisition': {'path':'ACA Course Materials/Week 1/Module 1 — Transcript Summary.md','section':'Section 6.2: partial goodwill and NCI'},
 'goodwill': {'path':'ACA Course Materials/Week 1/Lecture/Session1_Students.md','section':'Goodwill policy choices under IFRS and Swiss GAAP FER'},
 'lease': {'path':'ACA Course Materials/Week 2/Session2_Students.md','section':'Lease example: present value, interest and depreciation'},
 'impairment': {'path':'ACA Course Materials/Week 2/Session2_Students.md','section':'Impairment, slide 22: recoverable amount = max(FVLCD, VIU)'},
 'pensions': {'path':'ACA Course Materials/Week 2/Module 2 — Transcript Summary.md','section':'Section 7: defined benefit obligations and investment risk'},
 'tax': {'path':'ACA Course Materials/Week 2/Module 2 — Transcript Summary.md','section':'Sections 9.5–9.9: temporary differences, direction and tax rate'},
 'audit': {'path':'ACA Course Materials/Week 3/Module 3 — Transcript Summary.md','section':'Sections 1, 4–6: audit purpose, reasonable assurance and evidence'},
 'legal': {'path':'ACA Course Materials/Week 3/HS26_Session3_Students.md','section':'Slides 24 and 28: legal audit requirements and independence; course context'},
 'procedures': {'path':'ACA Course Materials/Week 3/HS26_Session3_Students.md','section':'Slide 50: analytical procedures and tests of details'},
 'materiality': {'path':'ACA Course Materials/Week 3/HS26_Tutorial_3_Auditing_student.md','section':'Task 3: materiality benchmark and misstatement effects; explicit study thresholds where added'},
 'opinion': {'path':'ACA Course Materials/Week 3/HS26_Session3_Students.md','section':'Slide 52: qualified, adverse and disclaimer opinions'},
 'kam': {'path':'ACA Course Materials/Week 3/HS26_Session3_Students.md','section':'Audit reports: significant audit judgments and Key Audit Matters'},
 'going': {'path':'ACA Course Materials/Week 3/HS26_Session3_Students.md','section':'Slide 51: management and auditor going-concern responsibilities'},
 'lines': {'path':'ACA Course Materials/Week 3/HS26_Session3_Students.md','section':'Slide 14: Three Lines Model'},
 'gap': {'path':'ACA Course Materials/Week 3/HS26_Session3_Students.md','section':'The Audit Expectations Gap, ACCA source'},
 'ma-costs': {'path':'ACA Course Materials/Week 4/W4 Lecture Summary.md','section':'1–2: internal reporting, cost behavior and classification'},
 'ma-flow': {'path':'ACA Course Materials/Week 4/W4 Lecture Summary.md','section':'2: cost classification and manufacturing cost flow'},
 'ma-cvp': {'path':'ACA Course Materials/Week 4/W4 Lecture Summary.md','section':'3: contribution margin, break-even and target profit'},
 'ma-job': {'path':'ACA Course Materials/Week 4/W4 Lecture Summary.md','section':'4: overhead rates and assignment; 6: pricing'},
 'ma-price': {'path':'ACA Course Materials/Week 4/W4 Lecture Summary.md','section':'6: target costing and cost-plus pricing'},
 'budget': {'path':'Ecoreps ACA / Exams by Topic / Budgeting and Variances','section':'Budgeting methods used in the past-exam solutions (sales, production, purchases, cash, ABB)'},
 'variance': {'path':'Ecoreps ACA / Exams by Topic / Budgeting and Variances','section':'Variance methods used in the past-exam solutions (static, flexible, price, efficiency, overhead)'},
 'capital': {'path':'Exam by topic/Capital Budgeting/Capital Budgeting Exam Bank.md','section':'Methods used in the answer key: payback, AARR, NPV, IRR and process'},
 'cpm': {'path':'Exam by topic/Cost and Performance Management/Cost and Performance Management Exam Bank.md','section':'Methods used in the answer key: balanced scorecard, ROS, ROI, WACC and EVA'},
}

def r(x, dp=0, mode='half'):
 x = D(x); quantum = Decimal(1).scaleb(-dp)
 return x.quantize(quantum, rounding={'half':ROUND_HALF_UP,'up':ROUND_CEILING,'down':ROUND_FLOOR}[mode])

def n(x, dp=0, sep=',', mode='half'):
 v = r(x, dp, mode); body = f'{abs(v):,.{dp}f}'.replace(',', sep)
 return ('−' if v < 0 else '') + body

def chf(x, dp=0, sep=',', mode='half'):
 v = r(x, dp, mode)
 return ('CHF −' if v < 0 else 'CHF ') + n(abs(v), dp, sep)

def pct(x, dp=1):
 return n(x, dp) + '%'

def table(header, rows, numeric_from=1):
 align = ['---' if i < numeric_from else '---:' for i in range(len(header))]
 lines = ['| ' + ' | '.join(header) + ' |', '|' + '|'.join(align) + '|']
 lines += ['| ' + ' | '.join(str(c) for c in row) + ' |' for row in rows]
 return '\n'.join(lines)

def evaluate(formula, inputs):
 env = {k: ([D(i) for i in v] if isinstance(v, list) else D(v)) for k, v in inputs.items()}
 env.update({'max': max, 'min': min, 'sum': sum, 'abs': abs, 'D': D})
 formula = re.sub(r'(?<![\w.])(\d+\.\d+)', r"D('\1')", formula)
 return eval(formula, {'__builtins__': {}}, env)

NUM = re.compile(r'(?<![\w.])(\d{1,3}(?:[,’]\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)(?![\w])')
def numbers(text):
 return {D(m.replace(',', '').replace('’', '')) for m in NUM.findall(text)}

def to_json(v):
 v = D(v)
 return int(v) if v == v.to_integral_value() else float(v)

LETTERS = 'abcde'

def none_wrong(key):
 # The letter is filled in later from the correct option's text, because options are shuffled on screen.
 return (NONE_TEXT, '__NONE_WRONG__', 'none-of-the-above')

def none_right(why):
 return (NONE_TEXT, 'Correct answer. ' + why, None)

def add(ident, topic, subtopic, difficulty, prompt, opts, key, explanation, *, scenario='', assume=(), calc='',
        check=None, ev='', marks=None, bank_set='bank', group=None):
 assert difficulty in ('Easy','Medium','Hard'), ident
 m = re.match(r'\((\d+) marks?\)\s*', prompt)
 if m:
  assert marks in (None, int(m.group(1))), (ident, 'marks mismatch')
  marks, prompt = int(m.group(1)), prompt[m.end():]
 assert ident not in {q['id'] for q in QUESTIONS}, ident
 if len(opts) == 2 and opts[0][0] == 'True': qtype = 'true-false'
 else: qtype = 'single-choice'
 options = []
 for letter, (text, why, mis) in zip(LETTERS, opts):
  if letter == key:
   assert mis is None, (ident, letter)
   why = why if why.startswith('Correct answer.') else 'Correct answer. ' + why
  else:
   assert mis, (ident, letter, 'wrong option needs a misconception tag')
  options.append({'id': letter, 'text': text, 'explanation': why, 'misconception': mis})
 assert key in [o['id'] for o in options], ident
 for o in options:
  if o['explanation'] == '__NONE_WRONG__':
   right = next(x['text'] for x in options if x['id'] == key)
   o['explanation'] = f'Wrong, because one of the listed answers is correct: {right}'.rstrip('.') + '.'
 assert len({o['text'] for o in options}) == len(options), (ident, 'duplicate option text')
 q = {'id': ident, 'origin': 'generated', 'aiGenerated': True, 'set': bank_set, 'topic': topic, 'subtopic': subtopic,
      'difficulty': difficulty, 'type': qtype, 'marks': marks, 'prompt': prompt, 'scenario': scenario,
      'assumptions': list(assume), 'options': options, 'correctOptionId': key, 'explanation': explanation,
      'workedCalculation': calc, 'evidence': [EV[ev]], 'status': 'validated', 'reviewReason': '', 'changes': [],
      'source': {'path': SOURCE, 'heading': group or subtopic, 'number': ident, 'line': None}, 'original': None,
      'targets': sorted({o['misconception'] for o in options if o['misconception']})}
 if check:
  formula, inputs, python_value = check['f'], check['v'], check['x']
  dp, mode = check.get('dp', 0), check.get('mode', 'half')
  got = evaluate(formula, inputs)
  if isinstance(python_value, (tuple, list)):
   expected = [r(v, dp, mode) for v in python_value]; recomputed = [r(v, dp, mode) for v in got]
  else:
   expected = r(python_value, dp, mode); recomputed = r(got, dp, mode)
  assert expected == recomputed, (ident, 'formula and inline arithmetic disagree', expected, recomputed)
  targets = expected if isinstance(expected, list) else [abs(expected)]
  correct = next(o for o in options if o['id'] == key)
  if correct['text'] == NONE_TEXT:
   for o in options:
    assert not all(t in numbers(o['text']) for t in targets), (ident, 'a listed option shows the true value', o['text'])
  else:
   assert all(t in numbers(correct['text']) for t in targets), (ident, 'correct option does not show the value', correct['text'], targets)
   for o in options:
    if o['id'] != key and o['id'] not in check.get('same', '') and numbers(o['text']):
     assert not all(t in numbers(o['text']) for t in targets), (ident, 'wrong option shows the value', o['text'])
  assert check.get('unit', 'CHF') in ('CHF','MCHF','units','percent','currency units','years'), ident
  assert calc, (ident, 'numeric question needs a worked calculation')
  clean = {k: ([to_json(i) for i in v] if isinstance(v, list) else to_json(v)) for k, v in inputs.items()}
  assert r(evaluate(formula, clean) if not isinstance(python_value, (tuple, list)) else 0, dp, mode) == (expected if not isinstance(expected, list) else 0), (ident, 'JSON inputs change the result')
  q['calculationCheck'] = {'kind': 'formula', 'formula': formula, 'inputs': clean, 'round': dp, 'rounding': mode,
                           'expected': [to_json(v) for v in expected] if isinstance(expected, list) else to_json(expected),
                           'unit': check.get('unit', 'CHF')}
 QUESTIONS.append(q)
 return q
