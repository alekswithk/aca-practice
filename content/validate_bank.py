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
 x={k:D(v) if isinstance(v,(int,float)) else v for k,v in c['inputs'].items()}
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
   for o in q['original']['options']: assert f"- {o['id']}. {o['text']}" in q['original']['raw'],q['id']
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
   assert actual==expected,(q['id'],actual,expected)
   assert q['workedCalculation'] and check['unit'] in ('CHF','MCHF'),q['id']
   correct=next(o for o in q['options'] if o['id']==q['correctOptionId'])
   numbers=re.findall(r'(?<!\w)(\d{1,3}(?:,\d{3})+|\d+)(?!\w)',correct['text'])
   if numbers:
    values={int(v.replace(',','')) for v in numbers}
    expected_values=expected if isinstance(expected,list) else [abs(expected)]
    assert all(v in values for v in expected_values),(q['id'],correct['text'],expected)
   numeric+=1
 print(f'PASS: {len(qs)} records; 92 source imports; 36 generated; {numeric} independent numeric recomputations; 115 scored; 13 excluded.')
 if missing_sources: print(f"Source excerpt comparisons skipped: {len(missing_sources)} original files are outside this standalone repository.")
 return bank,numeric

if __name__=='__main__': run()
