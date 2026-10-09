"""Independent numeric recomputation and content-integrity gate. No dependencies."""
import json, re
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING
from pathlib import Path
D=lambda x: Decimal(str(x))
CENT=Decimal('.01')
def cents(x): return x.quantize(CENT,rounding=ROUND_HALF_UP)
def up(x): return int(cents(x).to_integral_value(rounding=ROUND_CEILING))
def solve(c):
 x={k:D(v) if type(v) in (int,float) else v for k,v in c['inputs'].items()}
 k=c['kind']
 if k=='equity': return x['opening']+x['share']*(x['profit']-x['dividends']-x['uplift']/x['life'])
 if k in ('goodwill','nci'):
  net=x['equity']+x['uplift']*(1-x.get('taxRate',D(0)))
  return x['cost']-x['share']*net if k=='goodwill' else (1-x['share'])*net
 if k=='parent-equity': return x['parentEquity']
 if k.startswith('lease-'):
  n=int(x['term']); y=int(x['year']); p=x['payment']; r=x['rate']
  pv=cents(sum(p/(1+r)**t for t in range(1,n+1)))
  bal=pv
  for _ in range(y):
   interest=cents(bal*r); principal=cents(p-interest); bal=cents(bal-principal)
  rou=up(pv*D(n-y)/D(n))
  return {'lease-rou':rou,'lease-interest':up(interest),'lease-principal':up(principal),'lease-pair':[rou,up(bal)]}[k]
 if k=='depreciation-tax':
  year=x['year']; book=x['cost']*(1-year/x['life']); base=x['cost']*(1-x['taxDepreciation'])**int(year)
  return (book-base)*x['rate']
 if k=='inventory-tax': return (x['cost']*(1-x['taxWriteDown'])-x['book'])*x['rate']
 if k=='asset-tax': return (x['book']-x['base'])*x['rate']
 if k=='impairment':
  carrying=x.get('carrying',x.get('cost',D(0))*(1-x.get('years',D(0))/x.get('life',D(1))))
  ra=max(x['viu'],x['fairValue']-x['disposal'])
  return {'recoverable':ra,'loss':max(D(0),carrying-ra),'closing':min(carrying,ra)}[x['measure']]
 if k=='sum': return sum(D(v) for v in x['values'])
 if k=='vases':
  variable=x['material']+x['wage']/x['productivity']
  cogm=variable*x['quantity']+x['fixedManufacturing']
  if x['measure']=='cogm': return cogm
  if x['measure']=='unit': return (cogm+x['fixedOther'])/x['quantity']
  return x['price']*x['quantity']-cogm-x['fixedOther']
 if k=='cvp':
  contribution=x['price']-x['variable']; ratio=contribution/x['price']
  profit=x.get('target',D(0))/(1-x.get('tax',D(0)))
  measure=x['measure']
  if measure=='variable-ratio': return 100*(1-ratio)
  if measure=='contribution': return x['fixed']+profit
  if measure=='revenue': return (x['fixed']+profit)*x['price']/contribution
  if measure=='income': return (x['quantity']*contribution-x['fixed'])*(1-x.get('tax',D(0)))
  quantity=(x['fixed']+profit)/contribution
  if x.get('whole'):
   quantity=quantity.to_integral_value(rounding=ROUND_CEILING)
   assert (quantity*contribution-x['fixed'])*(1-x.get('tax',D(0)))>=x.get('target',D(0))
   assert ((quantity-1)*contribution-x['fixed'])*(1-x.get('tax',D(0)))<x.get('target',D(0))
  return quantity
 if k=='job-cost':
  rate=x['overhead']/x['base']
  labor=sum(D(wage)*D(hours) for wage,hours in zip(x['rates'],x['hours']))
  if x['measure']=='rate': return 100*rate
  result=labor*rate if x['measure']=='overhead' else labor*(1+rate)/(1-x['margin'])
  return result.quantize(D(1),rounding=ROUND_HALF_UP)
 if k=='inventory-flow':
  materials=x['beginMaterials']+x['purchases']-x['endMaterials']
  if x['measure']=='materials': return materials
  if x['measure']=='other': return x['manufacturing']-materials-x['directLabor']-x['indirectLabor']
  if x['measure']=='cogs': return x['manufacturing']+x['beginWip']-x['endWip']+x['beginFinished']-x['endFinished']
  return x['income']+x['period']+x['salesSalaries']
 if k=='fixed-cost': return x['revenue']*x['ratio']-x['income']
 if k=='full-cost-price':
  total=x['quantity']*x['material']+x['laborHours']*x['wage']+sum(D(v) for v in x['otherCosts'])
  return cents(total*(1+x['markup'])/x['quantity'])
 if k=='markup': return (100*x['profit']/(x['quantity']*x['price']-x['profit'])).quantize(D('.1'),rounding=ROUND_HALF_UP)
 if k=='target-cost': return cents(x['price']*(1-x['margin'])*(x['quantity'] if x['measure']=='total' else 1))
 if k=='break-even-revenue': return x['fixed']/(1-x['variableTotal']/x['revenue'])
 if k=='variable-markup':
  return (100*(sum(D(v) for v in x['fixedCosts'])+x['profit'])/sum(D(v) for v in x['variableCosts'])).quantize(D('.1'),rounding=ROUND_HALF_UP)
 if k=='unit-cost-base': return x['price']-x['profit']/x['quantity']
 if k=='finished-goods': return x['beginning']+x['cogm']-x['ending']
 if k=='price-reduction': return x['quantity']*(x['price']*(1-x['reduction'])-sum(D(v) for v in x['variableCosts']))-x['fixed']
 raise AssertionError(k)

def run():
 path=Path(__file__).with_name('questions.json'); bank=json.loads(path.read_text()); qs=bank['questions']
 assert len({q['id'] for q in qs})==len(qs)
 assert len([q for q in qs if q['origin']=='generated'])>=30
 numeric=0
 missing_sources=set()
 for q in qs:
  ids=[o['id'] for o in q['options']]
  assert len(set(ids))==len(ids) and len(ids)>=2,q['id']
  assert q['difficulty'] in ('Easy','Medium','Hard'),q['id']
  assert q['evidence'] and q['source']['path'] and q['prompt'],q['id']
  if q['origin']=='original':
   source_path=path.parents[2]/q['source']['path']
   if source_path.exists():
    assert q['original']['raw'] in source_path.read_text(),q['id']
   else:
    missing_sources.add(q['source']['path'])
   for o in q['original']['options']:
    assert any(f"- {letter}{delimiter} {o['text']}" in q['original']['raw'] for letter in (o['id'],o['id'].upper()) for delimiter in ('.',')')),q['id']
  if q['status']=='review':
   assert q['reviewReason'] and q['correctOptionId'] is None,q['id'];continue
  assert sum(o['id']==q['correctOptionId'] for o in q['options'])==1,q['id']
  assert len({o['text'] for o in q['options']})==len(q['options']),q['id']
  assert q['explanation'],q['id']
  for o in q['options']:
   assert o['explanation'],q['id']
   assert (o['misconception'] is None)==(o['id']==q['correctOptionId']),q['id']
  if 'calculationCheck' in q:
   check=q['calculationCheck']; actual=solve(check);expected=check['expected']
   expected_decimal=[D(v) for v in expected] if isinstance(expected,list) else D(expected)
   assert actual==expected_decimal,(q['id'],actual,expected)
   assert q['workedCalculation'] and check['unit'] in ('CHF','MCHF','units','percent','currency units'),q['id']
   correct=next(o for o in q['options'] if o['id']==q['correctOptionId'])
   numbers=re.findall(r'(?<!\w)(\d{1,3}(?:[,’]\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)(?!\w)',correct['text'])
   if numbers:
    values={D(v.replace(',','').replace('’','')) for v in numbers}
    expected_values=expected_decimal if isinstance(expected_decimal,list) else [abs(expected_decimal)]
    assert all(v in values for v in expected_values),(q['id'],correct['text'],expected)
   if q['id'].startswith('ma-'):
    matches=[]
    for option in q['options']:
     match=re.search(r'[−-]?\d+(?:[’]\d{3})*(?:\.\d+)?',option['text'])
     if match and D(match.group().replace('’','').replace('−','-'))==expected_decimal: matches.append(option['id'])
    assert matches==([q['correctOptionId']] if q['correctOptionId']!='e' else []),(q['id'],matches)
   numeric+=1
 counts=Counter(q['status'] for q in qs); origins=Counter(q['origin'] for q in qs)
 assert sum(item['count'] for item in bank['sourceInventory'])==origins['original']
 print(f"PASS: {len(qs)} records; {origins['original']} source imports; {origins['generated']} generated; {numeric} independent numeric recomputations; {counts['validated']} scored; {counts['review']} excluded.")
 if missing_sources: print(f"Source excerpt comparisons skipped: {len(missing_sources)} original files are outside this standalone repository.")
 return bank,numeric

if __name__=='__main__': run()
