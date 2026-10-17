"""B35 exact full-gap degree and marked-count profile reduction."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations_with_replacement
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if not __debug__:raise RuntimeError('Assertions must remain enabled')
 dp=ROOT/'verify/out/n100-B35-full-gaps-190.json';data=json.loads(dp.read_text(encoding='utf-8'));assert data['status']=='PASS_PREMISES';R=F(data['radius']);assert R==F(2831,25000)
 for rel,h in data['bindings'].items():assert sha(ROOT/rel)==h
 rows=data['replay']['result']['branches'];assert len(rows)==5
 assert F(rows[1]['any_low_degree_margin'])>0
 evidence=[]
 for row,excess in ((rows[3],4),(rows[4],3)):
  M=row['M'];assert row['restricted'];base=F(row['ordinary_margin']);g={(p,d):F(v) for p,d,v in row['full_vertex_gaps']};assert len(g)==row['vertices']
  assert set(g)=={(p,d) for p in range(5) for d in range(max(6,p+(4 if M==25 else 3)),100)}
  d8=min(v for (p,d),v in g.items() if d>=8);d8margin=base+R*R*d8;assert d8margin>0
  ear=base-R*R*F(row['shifted_ear_upper']);bad=base-R*R*F(row['bad_q1_upper']);assert min(ear,bad)>0
  # e=b0, all6/7 and Euler: exactly excess many degree7 points.
  survivors=[];excluded=[];pdomain=[p for p in range(5) if (p,7) in g]
  for ps in combinations_with_replacement(pdomain,excess):
   if M==26 and ps.count(4)>1:continue # at most one core-degree2 point
   margin=base+R*R*sum((g[p,7] for p in ps),F(0))
   (excluded if margin>0 else survivors).append({'high7_marked_counts':list(ps),'area_margin':str(margin)})
  assert [x['high7_marked_counts'] for x in survivors]==([[2,3,3,3],[3,3,3,3]] if M==25 else [[3,3,3],[3,3,4]])
  evidence.append({'M':M,'degree8_and_higher_exclusion_margin':str(d8margin),'one_ear_exclusion_margin':str(ear),'one_bad_q1_exclusion_margin':str(bad),'positive_degree_excess':excess,'degree_window':[6,7],'high7_profile_survivors':survivors,'excluded_high7_profiles':excluded,'minimum_degree8_vertex_slack':str(d8)})
 # Low original row: all M<=23 have one extra positive M shift versus flaggedM24.
 low=rows[0];base=F(low['M_le24_flagged_margin']);shift=base+R*R*F(low['M_slope'][0]);assert shift>0
 out=ROOT/'verify/out/n100-B35-profile-reduction-191.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-B35-full-profile-reduction/v1','status':'PASS_REDUCTION','radius':str(R),'B':35,'required_center_norm_squared_upper':str(1-R*R),'M_le23_closed':True,'M_le23_flagged_margin':str(shift),'M25_any_low_degree_closed':True,'M25_any_low_degree_margin':rows[1]['any_low_degree_margin'],'M_ge27_closed':True,'M_ge27_margin':rows[2]['M_ge27_margin'],'high_profiles':evidence,'remaining':['M24 compulsory unmarked low degree witness','M25 no low, e=b0, four7 with p counts2333 or3333','M26 no low, e=b0, three7 with p counts333 or334'],'topology_dependencies':'M25 simple chordlessP25/F103; M26 simpleP26/F102 with at most one core degree2; same-radius source checks in diagnostic190. Distinct conditional row contradictions do not add scalar payments.','B35_closed':False,'global_bound_improved':False,'bindings':{p.relative_to(ROOT).as_posix():sha(p) for p in (Path(__file__),dp)}},indent=2)+'\n',encoding='utf-8');print('B35 PROFILE REDUCTION PASS: M<=23 closed; M25 two profiles; M26 two profiles',flush=True)
if __name__=='__main__':main()
