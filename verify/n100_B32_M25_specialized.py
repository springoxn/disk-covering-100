"""Exact73+8 M25 profile partition using original coherent support checker.
Every final positivity assertion is retained; profile domains checked independently.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,itertools,builtins
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'verify'))
import n100_B32_M25_hinge_retuned as base

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def key(r):return (r['ears'],tuple(r['high_degrees']),tuple(r['high_marked']),r['star_pattern'])
def universe():
 return {(e,tuple(degrees),ps,si) for e,degrees in [(0,[7,7]),(0,[8]),(1,[7]),(2,[])] for ps in itertools.product(range(4),repeat=len(degrees)) for si,k in enumerate((0,1,2,2)) if k<=len(degrees)}
def run(allowed,candidate):
 original=builtins.compile;transforms=[]
 def change(text,filename,*args,**kw):
  if str(filename).endswith('verify_B32_M25_direct_interface_0p11323.py'):
   assert isinstance(text,str);needle='center=constant-5*A+star_caps[si]+q(J)';assert text.count(needle)==1;text=text.replace(needle,f'if (e,tuple(degrees),tuple(ps),si) not in {allowed!r}:continue\n     '+needle);assert text.count('assert len(rows)==81')==1;text=text.replace('assert len(rows)==81',f'assert len(rows)=={len(allowed)}')
   if candidate is not None:
    eps=F(*candidate['epsilon']);tau=F(*candidate['perimeter_penalty']);rules=[('data=json.loads(p.read_text())',f'data={candidate!r}'),("assert data['epsilon']==[1,2] and data['perimeter_penalty']==[13,10]",f"assert data['epsilon']=={candidate['epsilon']!r} and data['perimeter_penalty']=={candidate['perimeter_penalty']!r}"),('eps=F(1,2);weight=1-eps;tau=F(13,10);kappa=eps*tau',f'eps=F({eps.numerator},{eps.denominator});weight=1-eps;tau=F({tau.numerator},{tau.denominator});kappa=eps*tau')]
    for old,new in rules:assert text.count(old)==1;text=text.replace(old,new)
   transforms.append(hashlib.sha256(text.encode()).hexdigest())
  return original(text,filename,*args,**kw)
 builtins.compile=change
 try:result=base.worker(F(1189,20000))
 finally:builtins.compile=original
 assert len(transforms)==1;result['adapted_filtered_source_sha256']=transforms[0];result['expected_profile_count']=len(allowed)
 if result['status']=='ARITHMETIC_PASS':
  rows=result['result']['rows'];assert len(rows)==len(allowed) and {key(r) for r in rows}==allowed and all(F(r['area_margin_lower'])>0 for r in rows);result['result']['scope']='Exact filtered subset only; complete profile partition audited separately';result['result']['integer_profile_cases']=len(allowed)
 return result

def main():
 diagnostic=ROOT/'verify/out/n100-B32-M25-all-profile-diagnostic-144.json';old=json.loads(diagnostic.read_text(encoding='utf-8'));total=universe();assert len(total)==81 and {key(r) for r in old['result']['rows']}==total;bad={key(r) for r in old['nonpositive_profiles']};assert len(bad)==8;good=total-bad;assert len(good)==73 and not good&bad;candidatepath=ROOT/'runtime/B32-M25-specialized-discovery-144/proposal.json';candidate=json.loads(candidatepath.read_text(encoding='utf-8'));assert candidate['radius']=='2831/25000';runs=[]
 for label,domain,data in [('baseline73',good,None),('specialized8',bad,candidate)]:
  row=run(domain,data);row['label']=label
  if data is not None and row['status']=='ARITHMETIC_PASS':row['result']['proposal_sha256']=sha(candidatepath)
  runs.append(row);print(label,row['status'],row['result'].get('minimum_area_margin',row['result'].get('error')),flush=True)
 closed=all(r['status']=='ARITHMETIC_PASS' for r in runs);out=ROOT/'verify/out/n100-B32-M25-specialized-144.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-M25-specialized-profile-partition/v1','radius':'2831/25000','status':'PASS' if closed else 'NOT_CLOSED','full_M25_arithmetic_closed':closed,'partition_counts':[73,8],'complete_integer_profiles':81,'profile_partition_disjoint_exhaustive':True,'all_final_margin_assertions_retained':True,'runs':runs,'geometry_dependencies':'exact same selected deep5, at most2 high sites, four cyclic star patterns, physical edge cancellation and unique boundary bank as original M25 proof; numerical coefficients may vary by already fixed integer profile','full_B32_closed':False,'global_bound_improved':False,'bindings':{p.relative_to(ROOT).as_posix():sha(p) for p in (Path(__file__),diagnostic,candidatepath,ROOT/'verify/n100_B32_M25_hinge_retuned.py',ROOT/'verify/n100_B32_low_coherent.py')}},indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
