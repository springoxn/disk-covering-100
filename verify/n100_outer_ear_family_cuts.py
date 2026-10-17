"""Original-disk ear obstruction at the tightest saved radius layer."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
from n100_recursive_ear_obstruction import E,H_upper,ROOT

def main():
 p=ROOT/'verify/out/n100-radius-local-joint-domain.json';z=json.loads(p.read_text(encoding='utf-8'));layer=z['layers'][0];r=F(layer['radius_upper']);families=sorted({tuple(t[:2]) for t in layer['remaining_triples']});x=2*r;coef=F(1);v=F(0)
 for j in range(30):v+=coef*x**(2*j+1);coef*=F((2*j+1)**2,2*(j+1)*(2*j+3))
 a=2*(v+coef*x**61/(1-x*x));S=10**30;gamma=F(a.numerator*S//a.denominator+1,S);rows=[]
 for m,B in families:
  E.need(B>3 and B*gamma<6*E.PL,'Jensen concentration domain');small=gamma/3;lo=(2*E.PL-gamma)/(B-3);hi=(2*E.PH-gamma)/(B-3)
  if E.sin_at(hi/2)[1]>=r:
   rows.append({'m':m,'B':B,'status':'ear excluded by remaining arc capacity'});continue
  hs=3*H_upper(r,small,small)+(B-3)*H_upper(r,lo,hi);base=((2*m-B-2)*E.AH+B*E.KAPPA)*r*r;gap=E.PL-base-hs;rows.append({'m':m,'B':B,'status':'ear excluded by area' if gap>0 else 'not excluded','boundary_H_sum_upper':str(hs),'triangle_base_upper':str(base),'strict_area_deficit':str(gap)})
 noear=[(c['m'],c['B']) for c in rows if c['status'].startswith('ear excluded')];out=ROOT/'verify/out/n100-outer-ear-family-cuts.json';E.need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-outer-ear-family-cuts/v1','radius':str(r),'three_arc_sum_upper':str(gamma),'family_rows':rows,'no_ear_families':noear,'family_count':len(rows),'no_ear_count':len(noear),'prior_triple_count':len(layer['remaining_triples']),'analytic_dependencies':['same-radius normalized common-diagram and joint triangle area as original family domain','ear face with two boundary edges forces three consecutive assigned arcs into one radius2r disk','ear three-arc sum <=2asin(2r); H concavity and grouped Jensen','proof here at fixed saved radius, no independent proof of radius-uniform ear flag below it'],'scope':'fixed-radius ear prohibition for original disk families, not exclusion of families, not automatic geometry classification at all smaller radii','global_optimality':False,'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS outer ear cuts at',r,'families',len(rows),'noear',len(noear),'unresolved',[(c['m'],c['B']) for c in rows if c['status']=='not excluded'])
if __name__=='__main__':main()
