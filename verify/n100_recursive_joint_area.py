"""Apply existing joint triangle-anchor area criterion recursively to the inner disk."""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import json,hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working/lower_bounds_extension_20261004/verify_extension.py'
sys.path.insert(0,str(P.parent))
import verify_extension as E
E.trig=lru_cache(None)(E.trig)
def main():
 U=F(1154469548855829,10**16);s=1-2*U;t=U/s;E.need(0<t<F(1,5),'inner criterion range');q=1/t**2;start=(q.numerator+q.denominator-1)//q.denominator;rows=[];first=None
 for n in range(start,66):
  cases=[E.classify(n,B,t) for B in range(3,n)];alive=[c['B'] for c in cases if c['status']=='not excluded'];rows.append({'disk_count':n,'cases':cases,'not_excluded_B':alive});
  if alive:first=n;break
 E.need(first is not None and first>=56,'first surviving count');E.check_kappa();E.check_concavity_factorization();original=ROOT/'verify/out/n100-vonequinox-count-domain-bound.json';family=json.loads(original.read_text(encoding='utf-8'))['surviving_m_B_families'];prior=json.loads((ROOT/'verify/out/n100-recursive-inner-envelope.json').read_text(encoding='utf-8'));old=set(map(tuple,prior['remaining_triples']));kept=sorted((m,B,k) for m,B,k in old if m-k>=first);newF=sorted({(m,B) for m,B,k in kept});out=ROOT/'verify/out/n100-recursive-joint-area.json';E.need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-recursive-joint-area/v1','radius_upper':str(U),'inner_radius':str(s),'normalized_radius':str(t),'minimum_m_from_union_area':start,'minimum_non_circle_serving_disks':first,'largest_fully_excluded_disk_count':first-1,'count_rows':rows,'kappa_margins':E.check_kappa(),'prior_triple_count':len(old),'remaining_triples':kept,'removed_triples':sorted(old-set(kept)),'remaining_triple_count':len(kept),'remaining_families':newF,'remaining_family_count':len(newF),'removed_families':sorted({(m,B) for m,B,k in old}-set(newF)),'analytic_dependencies':['outer-circle-serving disks cannot enter open disk of radius1-2U, remaining closed disks cover its closure','same-radius inner-cover norm-cap normalization, irredundant generic/limit diagram reduction','joint center/anchor triangle bound with kappa; boundary functional concavity','B distinct boundary cells in inner normalized diagram; outer family B is a separate count'],'scope':'necessary recursive inner count; first surviving n is not an inner covering construction or optimal radius; geometry inherited, independent arithmetic replay pending separate certificate','global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [P,original,ROOT/'verify/out/n100-recursive-inner-envelope.json']},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS recursive joint area; nonserving >=',first,'triples',len(old),'->',len(kept),'families',len({(m,B) for m,B,k in old}),'->',len(newF),'inner first unexcluded',rows[-1]['not_excluded_B'])
if __name__=='__main__':main()
