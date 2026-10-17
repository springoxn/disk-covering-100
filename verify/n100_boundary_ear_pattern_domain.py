"""Complete count of relaxed cyclic boundary-ear words modulo rotations."""
from pathlib import Path
from math import comb,gcd
from fractions import Fraction as F
import json,hashlib
R=Path(__file__).resolve().parents[1]
def fixed_weight_words(n,e):
 if e<0 or 2*e>n:return 0
 return int(F(n,n-e)*comb(n-e,e))
def counts(n,allowed):
 labelled=sum(fixed_weight_words(n,e) for e in allowed);fixed=[]
 for shift in range(n):
  d=gcd(n,shift);rep=n//d;v=sum(fixed_weight_words(d,e//rep) for e in allowed if e%rep==0);fixed.append(v)
 assert sum(fixed)%n==0
 return labelled,sum(fixed)//n,fixed

def main():
 p=R/'verify/out/n100-ear-marked-joint-cuts.json';z=json.loads(p.read_text(encoding='utf-8'));rows=[]
 for r in z['family_rows']:
  m,B,allowed=r['m'],r['B'],r['remaining_ear_counts'];labelled,orbits,fixed=counts(B,allowed);rows.append({'m':m,'B':B,'allowed_ear_counts':allowed,'labelled_cyclic_words':labelled,'rotation_orbits':orbits,'fixed_counts_by_rotation_shift':fixed})
 out=R/'verify/out/n100-boundary-ear-pattern-domain.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-boundary-ear-pattern-domain/v1','radius_upper_inclusive':z['radius_upper_inclusive'],'families':rows,'scope':'complete integer counts of relaxed binary cyclic boundary-tip words with nonadjacent1s and allowed total ear counts; quotient by rotations only, reflections kept; not all words realizable, no interior triangulation enumeration or geometric feasibility','analytic_combinatorial_dependencies':['nonadjacent ear tips in actual diagrams from stage113','number of n-cycle nonadjacent binary words of weight e equals n/(n-e)*binom(n-e,e), including zero word and n1/2 conventions','rotation by s fixes repetition n/gcd(n,s) of fundamental block, weight scales by repetition; Burnside average counts rotation orbits'],'global_optimality':False,'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS17 ear-pattern domains; m99',[(r['B'],r['rotation_orbits']) for r in rows if r['m']==99],'m100B32',next(r['rotation_orbits'] for r in rows if r['m']==100 and r['B']==32))
if __name__=='__main__':main()
