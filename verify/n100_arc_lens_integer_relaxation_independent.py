"""Independent audit of integer aggregate witness and two rejected corruptions."""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(x,m):
 if not x:raise ValueError(m)
def check(z,base):
 r=F(z['radius']);d=F(z['delta']);need(r==F(base['radius']) and d==F(base['delta']),'same geometry parameters');pl,ph=map(F,z['pi_interval']);need(z['pi_interval']==base['pi_interval'],'same pi');arc=F(0);capacity=F(0);total=0
 for row in z['types']:
  n=row['multiplicity'];need(type(n) is int and n>=0,'nonnegative integer multiplicity');p=F(row['half_arc']);C=F(row['inner_area_capacity']);total+=n
  if row['kind']=='near':
   src=base['steps'][row['source_radial_interval']];need(0<=p<=F(src['arc_half_upper']) and 0<=C<=F(src['lens_area_upper']),'inside source rectangle')
  else:need(row['kind']=='tail' and C==0 and 0<=p<=F(base['maximum_half_arc_upper']),'tail rectangle')
  arc+=n*p;capacity+=n*C
 need(total==z['serving_disks']==54 and z['total_disks']==100 and z['nonserving_disks']==46,'all counts');capacity+=46*pl*r*r;target=ph*(1-2*r+d)**2;need(arc>=ph and capacity>target,'aggregate coverage inequalities');need(str(arc)==z['arc_sum'] and str(capacity)==z['inner_capacity_sum'] and str(target)==z['inner_target_area_upper'],'saved sums');need(str(arc-ph)==z['arc_surplus_over_pi_upper'] and str(capacity-target)==z['capacity_surplus'],'saved surplus');return arc-ph,capacity-target

def main():
 path=ROOT/'verify/out/n100-arc-lens-integer-relaxation.json';basepath=ROOT/'verify/out/n100-arc-lens-support.json';z=json.loads(path.read_text(encoding='utf-8'));base=json.loads(basepath.read_text(encoding='utf-8'));need(hashlib.sha256(basepath.read_bytes()).hexdigest()==z['input_sha256'],'bound input');arc,area=check(z,base);bad=[]
 for name in ('fractional_count','exceeds_source_capacity'):
  altered=deepcopy(z)
  if name=='fractional_count':altered['types'][0]['multiplicity']='34/1'
  else:altered['types'][0]['inner_area_capacity']='1'
  try:check(altered,base)
  except ValueError:bad.append(name)
  else:raise ValueError('corruption accepted')
 out=ROOT/'verify/out/n100-arc-lens-integer-relaxation-independent.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-arc-lens-integer-relaxation-independent/v1','verified_integer_rectangular_relaxation_witness':True,'near_disk_count':34,'tail_disk_count':20,'nonserving_disk_count':46,'arc_surplus':str(arc),'capacity_surplus':str(area),'negative_controls_rejected':bad,'scope':'independent membership and sum arithmetic; shares prior certified rectangles; no centers, no arrangement, no actual target coverage or optimal-radius proof','global_optimality':False,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent aggregate witness','counts 34+20+46','corruptions rejected',len(bad))
if __name__=='__main__':main()
