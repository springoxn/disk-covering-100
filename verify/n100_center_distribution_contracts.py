"""Controls, independent arithmetic and7-process timing of distribution kernels."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,copy,argparse,subprocess,sys,os,time,statistics
import n100_center_distribution_interfaces as C
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inputs():
 z=json.loads((R/'verify/out/n100-annular-center-cuts.json').read_text(encoding='utf-8'));dist=z['rejected_specific_radial_multiset']['separations'];bounds=[]
 for row in dist:bounds += [[row['distance'],row['distance']]]*row['count']
 ann={'target':'closed_unit_disk','radius_units':'radius','radius_upper':z['radius_upper'],'annulus':['1/5','3/4'],'center_norm_bounds':bounds};target={'target':'closed_unit_disk','radius_units':'radius','radius_upper':'1/10','target_center':['1/2','0'],'target_radius':'1/4','center_boxes':[['0','0','0','0']]*100};return [('annular_norm_counts',ann),('translated_target_counts',target)]
def independent(method,p,r):
 U=F(p['radius_upper'])
 if method=='annular_norm_counts':
  a,b=map(F,p['annulus']);selected=[i for i,z in enumerate(p['center_norm_bounds']) if not (F(z[1])<max(F(0),a-U) or F(z[0])>b+U)];area=b*b-a*a
 else:
  q=list(map(F,p['target_center']));s=F(p['target_radius']);selected=[];area=s*s
  for i,z in enumerate(p['center_boxes']):
   x=min(max(q[0],F(z[0])),F(z[1]));y=min(max(q[1],F(z[2])),F(z[3]));
   if (x-q[0])**2+(y-q[1])**2<=(s+U)**2:selected.append(i)
 n=r['required_centers_area_only'];assert (n-1)*U*U<area<=n*U*U and selected==r['possible_center_indices'] and (len(selected)<n)==(r['status']=='EXCLUDED')
def worker(block,folder):
 rows=[]
 for method,p in inputs():
  result=C.run(method,p);independent(method,p,result);assert result['status']=='EXCLUDED';samples=[];C.run(method,p)
  for j in range(5):
   t=time.perf_counter_ns();again=C.run(method,p);samples.append(time.perf_counter_ns()-t);assert again==result
  rows.append({'method':method,'samples_ns':samples,'median_ns':statistics.median(samples),'status':result['status']})
 (folder/('block-'+str(block)+'.json')).write_text(json.dumps({'pid':os.getpid(),'block':block,'timings':rows},indent=2)+'\n',encoding='utf-8');print('PASS distribution block',block,flush=True)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--run-dir',required=True);ap.add_argument('--block',type=int);a=ap.parse_args();folder=Path(a.run_dir).resolve()
 if a.block is not None:worker(a.block,folder);return
 assert not folder.exists();folder.mkdir(parents=True);results=[];controls=[]
 for m,p in inputs():
  r=C.run(m,p);independent(m,p,r);results.append(r)
 m,p=inputs()[1];keep=copy.deepcopy(p);keep['center_boxes'][:7]=[['1/2','1/2','0','0']]*7;assert C.run(m,keep)['status']=='NOT_EXCLUDED';controls.append('sufficient_area_count_not_claimed_cover');tangent=copy.deepcopy(p);tangent['center_boxes']=[['3/20','3/20','0','0']];assert C.run(m,tangent)['possible_center_indices']==[0];controls.append('closed_tangent_retained')
 for label,edit in [('target_outside',lambda x:x.update(target_center=['1','0'])),('float_radius',lambda x:x.update(radius_upper=0.1)),('zero_radius',lambda x:x.update(radius_upper='0')),('reversed_box',lambda x:x['center_boxes'].__setitem__(0,['1','0','0','0']))]:
  bad=copy.deepcopy(p);edit(bad);assert C.run(m,bad)['status']=='PRECONDITION_MISSING';controls.append(label)
 anchor=C.anchor_variance([['0','0'],['1','0'],['0','1']],['1/16']*3,['1']*3);assert anchor['status']=='EXCLUDED';eq=C.anchor_variance([['-1','0'],['1','0']],['1','1'],['1','1']);assert eq['status']=='NOT_EXCLUDED' and eq['gap']=='0';controls.append('anchor_closed_equality_retained')
 import sympy as sp
 x,y=sp.symbols('x y');pts=[(sp.Rational(0),sp.Rational(0)),(sp.Rational(1),sp.Rational(0)),(sp.Rational(0),sp.Rational(1))];mean=[sp.Rational(v) for v in anchor['mean']];lhs=sum((x-a)**2+(y-b)**2 for a,b in pts);rhs=3*((x-mean[0])**2+(y-mean[1])**2)+sp.Rational(anchor['variance']);assert sp.expand(lhs-rhs)==0
 blocks=[]
 for b in range(7):
  result=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--run-dir',str(folder),'--block',str(b)],cwd=R);assert result.returncode==0;blocks.append(json.loads((folder/('block-'+str(b)+'.json')).read_text(encoding='utf-8')))
 assert len({b['pid'] for b in blocks})==7;timings=[]
 for i in range(2):
  values=[b['timings'][i]['median_ns'] for b in blocks];timings.append({'method':blocks[0]['timings'][i]['method'],'block_medians_ns':values,'median_ns':statistics.median(values),'identical_input_1000_calls_seconds':statistics.median(values)/1e6})
 out=R/'verify/out/n100-center-distribution-interface-contracts.json';assert not out.exists();paths=[Path(__file__),R/'verify/n100_center_distribution_interfaces.py',R/'verify/out/n100-annular-center-cuts.json']+[folder/('block-'+str(i)+'.json') for i in range(7)];out.write_text(json.dumps({'schema':'n100-center-distribution-interface-contracts/v1','results':results,'anchor_variance':anchor,'anchor_closed_equality':eq,'sympy_variance_identity_zero':True,'negative_and_closed_controls':controls,'independent_arithmetic_replay':True,'seven_process_timing':timings,'operation_complexity':'annulus O(n) rational comparisons; translated disk O(n) rational squared distances; anchor variance O(k) rational work; intermediary bit growth tracked separately','scope':'universal necessary area cuts on declared center domains; translated target uses area lower count only, not stronger recursive frontier; anchor needs separate map/path geometry lift','global_optimality':False,'bindings':{p.relative_to(R).as_posix():sha(p) for p in paths}},indent=2)+'\n',encoding='utf-8');print('PASS distribution interfaces;controls',len(controls),'timing',json.dumps(timings))
if __name__=='__main__':main()
