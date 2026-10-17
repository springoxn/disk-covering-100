"""Exact free-intercept affine support optimized over certified arc/lens rectangles."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(x,m):
 if not x:raise ValueError(m)
def main():
 src=ROOT/'verify/out/n100-arc-lens-support.json';z=json.loads(src.read_text(encoding='utf-8'));pl,ph=map(F,z['pi_interval']);r=F(z['radius']);delta=F(z['delta']);M=F(z['maximum_half_arc_upper']);lines=[(F(s['arc_half_upper']),F(s['lens_area_upper']),i) for i,s in enumerate(z['steps'])]+[(M,F(0),'tail')];unique={}
 for p,C,i in lines:
  if p not in unique or C>unique[p][0]:unique[p]=(C,i)
 hull=[];starts=[]
 for p,(C,i) in sorted(unique.items()):
  while hull:
   crossing=(hull[-1][1]-C)/(p-hull[-1][0])
   if len(hull)==1 or crossing>starts[-1]:break
   hull.pop();starts.pop()
  starts.append(None if not hull else crossing);hull.append((p,C,i))
 candidates={F(0)}|{a for a in starts if a is not None and a>=0};k=54
 def eval_at(a):
  b=max(C+a*p for p,C,i in lines);return k*b-a*pl,b
 a=min(candidates,key=lambda a:(eval_at(a)[0],a));objective,b=eval_at(a);active=[i for p,C,i in lines if C+a*p==b];margin=pl*(1-2*r+delta)**2-46*ph*r*r-objective;old_a=F(z['slope']);old_obj=54*old_a*M-old_a*pl;need(objective<=old_obj,'free intercept improves or matches old feasible line');support=[{'source':i,'p':str(p),'C':str(C),'slack':str(b-a*p-C)} for p,C,i in lines];need(all(F(s['slack'])>=0 for s in support),'all affine constraints')
 # Subgradient at a>0 brackets zero; at a=0 right derivative nonnegative.
 active_p=[p for p,C,i in lines if C+a*p==b];need((min(active_p)*k<=pl<=max(active_p)*k) if a>0 else max(active_p)*k>=pl,'exact convex optimality witness');families=json.loads((ROOT/'verify/out/n100-vonequinox-count-domain-bound.json').read_text(encoding='utf-8'))['surviving_m_B_families'];triples=[[m,B,k] for m,B in families for k in range(B,m+1) if pl*(1-2*r+delta)**2-(m-k)*ph*r*r-k*b+a*pl<=0];old=set(map(tuple,z['old_count_domain_intersection']));joint=old&set(map(tuple,triples));out=ROOT/'verify/out/n100-arc-lens-free-intercept.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-arc-lens-free-intercept/v1','radius':str(r),'delta':str(delta),'slope':str(a),'intercept':str(b),'k54_objective':str(objective),'old_constrained_objective':str(old_obj),'objective_improvement':str(old_obj-objective),'k54_margin':str(margin),'k54_excluded':margin>0,'active_constraints':active,'active_p_min':str(min(active_p)),'active_p_max':str(max(active_p)),'support':support,'upper_hull':[{'p':str(p),'C':str(C),'source':i,'start':None if start is None else str(start)} for (p,C,i),start in zip(hull,starts)],'compatible_triples':triples,'joint_triples':sorted(joint),'additional_triples_removed':sorted(old-joint),'scope':'exact optimum for fixed certified rectangular arc/lens envelopes and delta; not exact geometric attainable envelope or global best radius','global_optimality':False,'input_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS free intercept','active',active,'k54 excluded',margin>0,'removed',len(old-joint),'strict improvement',old_obj>objective)
if __name__=='__main__':main()
