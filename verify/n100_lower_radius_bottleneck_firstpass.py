"""Exact first-pass radius sensitivity along the upstream global skeleton.
B31 fixed-row final margins and generic count bridge are recomputed.
Tail scalar margins alone do NOT validate its radius-dependent pair envelope.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,ast
R=Path(__file__).resolve().parents[1];P=R/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323';W=P/'working'
sys.path[:0]=[str(W),str(W/'lower_bounds_extension_20261004')]
import verify_B31_global_low_degree_0p11323 as b31
import verify_extension as g
from verify_star_lp_duals import q,S,PI
from verify_potential_star_duals import sine,cosine
from exact_quadratic_marked_conjugate import conjugate
from verify_jensen_slab_ear_support import quadratic_cap
ENTRIES={'B31':W/'verify_B31_global_low_degree_0p11323.py','B32':P/'lower_staging/verify_B32_complete_0p11323_v2.py','B33':W/'verify_B33_hinge_metric_complete_0p11323.py','B34':P/'lower_staging/B34_0p11323/verify_hinge_B34_complete_0p11323.py','B35':W/'lower_staging/B35_0p11323/check_B35_complete_0p11323_v2.py','B36plus':W/'verify_capped_pair_B36plus_0p11323.py'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def interval(z):return [str(F(z.l,S)),str(F(z.u,S))]
def main():
 assert __debug__;g.check_kappa();g.check_concavity_factorization();baseline=b31.verify();rows=json.loads((W/'B31_global_low_degree_0p11323_proposals.json').read_text(encoding='utf-8'))['rows'];A=3*q(3).sqrt()/4;ANG=PI/3;C0=conjugate(F(0),F(0));samples=[]
 for radius in map(F,('0.11323','0.113231','0.113235','0.11324','0.11325','0.1133')):
  g.R=radius;count_rows=[g.classify(100,b,radius) for b in range(3,100)];survivors=[b for b,row in zip(range(3,100),count_rows) if row['status']=='not excluded']
  try:n99={'status':'PASS','receipt':g.exclude_all(99,radius)}
  except (ValueError,AssertionError) as e:n99={'status':'NOT_CLOSED','reason':str(e)}
  B=31;mu=PI/B;s=sine(mu);Q=B*(mu-s*(cosine(mu)-(q(radius).sq()-s.sq()).sqrt()));reports=[]
  for row in rows:
   M=row['M'];required=row['required_degree_five_count'];D=row['denominator'];pd=row['potential_denominator'];charges=[F(row[k],D) for k in ('charge_a','charge_b','charge_0','charge_low')];lb=-F(row['boundary_potential'],pd);u0,beta,eta,apex,flag=[q(F(row[k],D)) for k in ('u0','beta','eta','apex','flag')];slope=-eta+apex+q(charges[1])-q(lb)*ANG;ear=A-2*C0+quadratic_cap(radius,F(0))-2*beta+eta+q(lb)*PI+2*slope;width=q(2)/(q(1)+(q(1)-2*q(radius)).sqrt());bad=width+q(F(1,2))-C0-beta-eta;center=(198-2*B)*A+B*C0+69*u0+B*beta+(B-6-M)*eta+M*apex+M*q(charges[1])-required*flag-q(lb)*(2*PI+M*ANG);margin=PI-q(radius).sq()*center-Q;reports.append({'M_endpoint':M,'area_margin_interval':interval(margin),'area_positive':margin.l>0,'shifted_ear_upper':str(F(ear.u,S)),'ear_sign_pass':ear.u<0,'bad_q1_upper':str(F(bad.u,S)),'bad_sign_pass':bad.u<0})
  if radius==F(11323,100000):assert min(F(z['area_margin_interval'][0]) for z in reports)==F(baseline['minimum_area_margin'])
  old=((198-31)*g.AH+31*g.KAPPA)*radius*radius+31*g.H_upper(radius,2*g.PL/31,2*g.PH/31);degree_loss=F(b31.check_window()['degree4_loss_lower']);degree_margin=degree_loss-(old-g.PL)/(radius*radius)
  try:fan={'status':'PASS','receipt':g.cluster_exclusion(31,5,F(6933,10000),3,F(1,1000))}
  except (ValueError,AssertionError) as e:fan={'status':'NOT_CLOSED','reason':str(e)}
  # Exact scalar budget with old MU/L/K, conditional on their NEW-radius supports.
  mu_tail=F(92531,10**7);L=F(751,100000);K=F(3892,12500);tail=(1-mu_tail)*g.PL-((198-36)*g.AH+36*K)*radius*radius-36*L;gain=(g.AH-K)*radius*radius-L
  samples.append({'radius':str(radius),'n99_exclusion':n99,'m100_surviving_B':survivors,'B31_fixed_rows':reports,'B31_degree_window_margin_lower':str(degree_margin),'B31_fan':fan,'B31_radius_independent_face_vertex_supports':'replayed once at baseline; coefficients and dimensionless supports unchanged','B36plus_old_coefficients_scalar_margin':str(tail),'B36plus_per_B_gain':str(gain),'B36plus_pair_envelope_replayed_at_new_radius':False,'new_global_bound_certified':False})
 closure=[];allpy=list(P.rglob('*.py'));lookup={}
 for p in allpy:lookup.setdefault(p.name,[]).append(p)
 for name,entry in ENTRIES.items():
  queue=[entry];seen=set();nodes=[]
  while queue:
   p=queue.pop()
   if p in seen:continue
   seen.add(p);text=p.read_text(encoding='utf-8-sig');tree=ast.parse(text);radius_sites=[];links=[]
   for n in ast.walk(tree):
    if isinstance(n,(ast.Assign,ast.AnnAssign)):
     targets=n.targets if isinstance(n,ast.Assign) else [n.target]
     if any(isinstance(t,ast.Name) and t.id in ('R','RADIUS','NORM','CURVATURE','B','K') for t in targets):radius_sites.append({'line':n.lineno,'expression':ast.get_source_segment(text,n)})
    mods=[a.name for a in n.names] if isinstance(n,ast.Import) else [n.module] if isinstance(n,ast.ImportFrom) and n.module else []
    refs=[m+'.py' for m in mods]
    if isinstance(n,ast.Constant) and isinstance(n.value,str) and n.value.endswith('.py') and '\n' not in n.value:refs.append(Path(n.value).name)
    for ref in refs:
     candidates=lookup.get(ref,[])
     if candidates:
      # Keep ambiguous locators explicit, not silent import resolution.
      for c in candidates:links.append(c.relative_to(P).as_posix());queue.append(c)
   nodes.append({'path':p.relative_to(P).as_posix(),'sha256':sha(p),'radius_and_support_assignments':radius_sites,'static_candidate_dependencies':sorted(set(links))})
  closure.append({'branch':name,'entry':entry.relative_to(P).as_posix(),'candidate_source_count':len(nodes),'candidate_sources':nodes,'closure_is_execution_trace':False})
 out=R/'verify/out/n100-lower-radius-bottleneck-firstpass.json';assert not out.exists();paths=[Path(__file__),W/'B31_global_low_degree_0p11323_proposals.json']+list(ENTRIES.values());out.write_text(json.dumps({'schema':'n100-lower-radius-bottleneck-firstpass/v1','baseline_B31_full_checker_passed':True,'baseline_B31_recomputed_margin_matches':True,'radius_samples':samples,'six_branch_static_dependency_locator':closure,'scope':'exact radius-sensitive count/B31 final-row/conditional tail-budget diagnostics; B32-B35 and new-radius continuous support replays still pending','global_lower_bound_improved':False,'bindings':{p.relative_to(R).as_posix():sha(p) for p in paths}},indent=2)+'\n',encoding='utf-8');print('PASS exact first-pass radius diagnostics')
 for row in samples:print(row['radius'],'n99',row['n99_exclusion']['status'],'B',row['m100_surviving_B'],'B31 margin',min(float(F(z['area_margin_interval'][0])) for z in row['B31_fixed_rows']),'tail scalar',float(F(row['B36plus_old_coefficients_scalar_margin'])))
if __name__=='__main__':main()
