"""Universal annular center-count cuts and rejection of a radial budget witness."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(c,m):
 if not c:raise ValueError(m)
def main():
 source=ROOT/'verify/out/n100-multiradius-capacity.json';z=json.loads(source.read_text(encoding='utf-8'));r=F(z['radius']);a=F(1,5);b=F(3,4);types=[(t['kind'],F(t['distance']),33 if t['kind']=='near' else 21) for t in z['types']]+[('central',F(0),46)];separations=[]
 for name,d,n in types:
  gap=a-d if d<a else d-b if d>b else F(0);need(gap>r,'strict annular separation');separations.append({'type':name,'distance':str(d),'count':n,'radial_distance_from_annulus':str(gap),'strict_gap_over_radius':str(gap-r)})
 cuts=[]
 for inner,outer in [(F(0),F(3,4)),(F(1,5),F(3,4)),(F(1,4),F(3,4)),(F(1,3),F(3,4)),(F(1,2),F(3,4)),(F(1,5),F(2,3))]:
  ratio=(outer*outer-inner*inner)/(r*r);lower=-((-ratio.numerator)//ratio.denominator);lo=max(F(0),inner-r);hi=outer+r;need((lower-1)*r*r<outer*outer-inner*inner<=lower*r*r,'integer area threshold');cuts.append({'annulus_inner':str(inner),'annulus_outer':str(outer),'center_norm_lower':str(lo),'center_norm_upper':str(hi),'minimum_centers':lower,'area_ratio':str(ratio),'strict_exclusion_margin_for_one_less':str(outer*outer-inner*inner-(lower-1)*r*r),'all_counted_centers_non_circle_serving':hi<1-r})
 out=ROOT/'verify/out/n100-annular-center-cuts.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-annular-center-cuts/v1','radius_upper':str(r),'rejected_specific_radial_multiset':{'counts':[33,21,46],'empty_open_annulus':[str(a),str(b)],'separations':separations},'universal_cuts':cuts,'analytic_dependencies':['if a radius-r disk meets a<|x|<b then its center satisfies max(0,a-r)<=|c|<=b+r by reverse triangle inequality','annulus area pi*(b^2-a^2), per disk contribution <=pi*r^2, area subadditivity','if b+r<1-r then every center counted for this annulus cannot serve unit circle','for smaller covering radius, enlarge every disk to radius_upper first'],'scope':'necessary radial center-distribution cuts for arbitrary centers, no fixed core assumption; rejection applies only to saved radial type multiset; not rejection of k54 generally','global_optimality':False,'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS universal annular cuts',[(c['annulus_inner'],c['annulus_outer'],c['minimum_centers']) for c in cuts],'saved witness rejected',True)
if __name__=='__main__':main()
