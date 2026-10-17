"""Complete new high-M reduction allowing the unique5 to be marked.
The former marked-low exclusion is replaced by an exhaustive B-neighbor split.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,importlib.util,subprocess,traceback
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323';W=P/'working';S=P/'lower_staging';sys.path[:0]=[str(S),str(W),str(W/'lower_bounds_extension_20261004')];R=F(11324,100000)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def component(name):
 path=S/'verify_B32_highM_complete_0p11323.py';before=path.read_bytes();text=before.decode('utf-8');rules=[('geometry.cluster_exclusion(B,5,F(1733,2500),3,F(1,1000))','geometry.cluster_exclusion(B,5,F(17331,25000),3,F(1,1000))'),('marked_margin=raw+rr.sq()*q(marked);assert marked_margin.l>0','marked_margin=raw+rr.sq()*q(marked) # not an exclusion: marked unique5 retained'),('unique_degree5_marked_incidence=0','unique_degree5_marked_incidence=list(range(4))')]
 for a,b in rules:assert text.count(a)==1;text=text.replace(a,b)
 spec=importlib.util.spec_from_file_location('highM_expanded_148',path);m=importlib.util.module_from_spec(spec);exec(compile(text,str(path),'exec'),m.__dict__);m.R=R;functions={'profiles':m.reduce_profiles,'topology':m.topology_checks,'deep_five':m.direct_deep_five,'four_face':m.four_face_metric};assert name in functions
 try:result=functions[name]();assert result['status']=='PASS';status='PASS'
 except Exception as e:status='NOT_CLOSED';result={'error_type':type(e).__name__,'error':str(e),'traceback':traceback.format_exc()}
 assert path.read_bytes()==before;return {'component':name,'status':status,'radius':str(R),'result':result,'source_sha256':sha(path),'adapted_source_sha256':hashlib.sha256(text.encode()).hexdigest()}
def main():
 if len(sys.argv)==3 and sys.argv[1]=='--component':print(json.dumps(component(sys.argv[2])),flush=True);return
 assert len(sys.argv)==1 and __debug__;runs=[]
 for name in ('profiles','topology','deep_five','four_face'):
  done=subprocess.run([sys.executable,'-B','-S',str(Path(__file__).resolve()),'--component',name],cwd=ROOT,text=True,capture_output=True);assert done.returncode==0,done.stderr;row=json.loads(done.stdout);runs.append(row);print(name,row['status'],row['result'].get('minimum_area_margin',row['result'].get('marked_low_margin',row['result'].get('error',''))),flush=True)
 closed=all(x['status']=='PASS' for x in runs);minimum=None
 if closed:
  reduction,topology,deep,metric=[x['result'] for x in runs];assert reduction['M_domain']=='M>=26' and reduction['remaining_profiles'][1]['unique_degree5_marked_incidence']==list(range(4));assert F(reduction['two_curvature_margin'])>0 and all(F(x)>0 for x in reduction['low_case_shift_margins'].values());assert deep['integer_profile_cases']==8 and topology['core_boundary']==26 and topology['deep_vertices']==42;assert [x['deep_degree_excess'] for x in metric['rows']]==[0,1]
  for x in (reduction,deep,metric):assert F(x['radius'])==R and F(x['required_center_norm_squared_upper'])==1-R*R
  minimum=str(min([F(deep['minimum_area_margin']),F(metric['minimum_area_margin']),F(reduction['two_curvature_margin']),*map(F,reduction['low_case_shift_margins'].values())]));assert F(minimum)>0
 out=ROOT/'verify/out/n100-B32-high-expanded-148.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-highM-expanded-marked-core-split/v1','status':'PASS' if closed else 'NOT_CLOSED','radius':str(R),'B':32,'M_domain':'M>=26','high_M_closed':closed,'minimum_positive_closure_margin':minimum,'fresh_process_components':4,'runs':runs,'replacement_of_old_obligation':'Marked-low margin is not asserted positive; retain any p in0..3 for unique5. All other row assertions, two-curvature exclusion and shifted cases checked. Split on actual original-B neighbor: no neighbor forces p0 and uses original8 direct-star cases; any neighbor places the5 outside every strict core-block interior. Original /6 topology and h0/h1 metric proof only use deep degrees>=6 and ring degrees unrestricted, so cover marked5 as well.','coverage_cases':['all-six: core metric h0','unique5 without original-B neighbor: original direct star, low p0','unique5 with original-B neighbor, low p0/1/2/3: core metric h0/h1'],'geometry_review_pending':True,'full_B32_closed':False,'global_bound_improved':False,'bindings':{p.relative_to(ROOT).as_posix():sha(p) for p in (Path(__file__),S/'verify_B32_highM_complete_0p11323.py',S/'B32_HIGHM_CATALOG_FREE_COMPLETE_0p11323.md')}},indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
