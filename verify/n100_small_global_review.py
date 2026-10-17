"""Review uniform new-radius composition after complete independent replay."""
from pathlib import Path
from fractions import Fraction as F
import ast,json,re,hashlib,argparse
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--tag',default='143');a=ap.parse_args();folder=ROOT/f'runtime/lower-small-advance-{a.tag}';source=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323';package=folder/'package';manifestpath=folder/'transformation.json';manifest=json.loads(manifestpath.read_text(encoding='utf-8'));radius=F(manifest['radius']);firstpath=ROOT/f'verify/out/n100-lower-small-advance-{a.tag}.json';secondpath=ROOT/f'verify/out/n100-radius-dependency-audit-{a.tag}.json';first=json.loads(firstpath.read_text(encoding='utf-8'));second=json.loads(secondpath.read_text(encoding='utf-8'));assert first['exit_code']==second['exit_code']==0 and first['all_six_branch_arithmetic_closed'] and second['all_branches_replayed'];assert first['radius']==second['radius']==str(radius);assert F(11323,100000)<radius
 assert not second['entries_with_other_global_R'],second['entries_with_other_global_R']
 changes=[];proposal_count=0
 for rel,h in manifest['source_snapshot'].items():
  original=source/rel;copy=package/rel;assert sha(original)==h and sha(copy)==manifest['copy_snapshot'][rel]
  if original.suffix not in ('.py','.json'):assert copy.read_bytes()==original.read_bytes();continue
  old=original.read_text(encoding='utf-8');expected=re.sub(r'F\(\s*11323\s*,\s*100000\s*\)',f'F({radius.numerator},{radius.denominator})',old).replace('11323/100000',str(radius));actual=copy.read_text(encoding='utf-8');assert actual==expected
  if original.suffix=='.py':
   before=ast.parse(old);after=ast.parse(actual);n1=sum(isinstance(z,ast.Assert) for z in ast.walk(before));n2=sum(isinstance(z,ast.Assert) for z in ast.walk(after));assert n1==n2
   if old!=actual:changes.append({'source':rel,'assertions_before':n1,'assertions_after':n2,'only_radius_replacements':True})
  else:
   obj1=json.loads(old);obj2=json.loads(actual)
   def check(x,y):
    if isinstance(x,dict):assert x.keys()==y.keys();return all(check(x[k],y[k]) for k in x)
    if isinstance(x,list):assert len(x)==len(y);return all(check(u,v) for u,v in zip(x,y))
    if isinstance(x,str):assert y==x.replace('11323/100000',str(radius));return True
    assert x==y;return True
   check(obj1,obj2);proposal_count+=int('proposal' in rel)
 # Reflect ALL centers before creating a common diagram: rational CAS identity.
 d,T,x,y=sp.symbols('d T x y',nonzero=True);dp=(1-T)/d;left=(x-dp)**2+y*y-T;right=dp/d*((x-d)**2+y*y-T)+(1-dp/d)*(x*x+y*y-1);identity=sp.factor(left-right);assert identity==0
 result=first['result'];audited=json.loads((folder/'audit.stdout.json').read_text(encoding='utf-8'));keys=('B31','B32','B33','B34','B35','B36plus');margins={}
 for branch in keys:
  one=result[branch]['result'];two=audited[branch]['result'];assert one['status']==two['status']=='PASS';assert F(one['radius'])==F(two['radius'])==radius
  key=next(k for k in ('minimum_area_margin','minimum_reported_area_margin','minimum_area_margin_at_B36') if k in one);assert one[key]==two[key] and F(one[key])>0;margins[branch]=one[key]
 assert result['complete_surviving_boundary_counts']==list(range(31,40));bridge=result['common_count_bridge'];assert F(bridge['radius'])==radius and bridge['n']==99 and F(bridge['minimum_area_margin'])>0
 assert result['B32']['result']['direct_M25_cases']==81 and result['B32']['result']['same_radius_components'];assert result['B34']['result']['no_second_deficit_spend'];assert result['B36plus']['result']['complete_capped_pair']['status']=='PASS';assert F(result['B36plus']['result']['additional_margin_per_boundary_cell'])>0
 # Entries and source text reviewed for result-cache consumption; no imported
 # saved result is used as a mathematical assertion by the six live entries.
 loaded=second['loaded_source_sha256'];read_sites=[]
 for rel in loaded:
  text=(package/rel).read_text(encoding='utf-8')
  for i,line in enumerate(text.splitlines(),1):
   if 'read_text(' in line:read_sites.append({'source':rel,'line':i,'text':line.strip()})
  assert not re.search(r"(?:_result\.json|integrated_11323_fresh_result\.json).*read_text",text),rel
 report={'schema':'n100-new-radius-global-composition-review/v1','status':'PASS','radius':str(radius),'theorem':'r_D(100)>'+str(radius),'strict_improvement':str(radius-F(11323,100000)),'norm_squared_upper':str(1-radius*radius),'global_bound_improved':True,'all_six_branches_closed':True,'branch_margins':margins,'common_n99_margin':bridge['minimum_area_margin'],'branches_exhaust_survivors':list(range(31,40)),'actual_process_radius_entries_reviewed':len(second['entries']),'other_global_R_entries':second['entries_with_other_global_R'],'source_transformations_reviewed':changes,'json_proposal_files_numeric_coefficients_unchanged':proposal_count,'loaded_read_sites':read_sites,'CAS_whole_cover_reflection_identity':str(identity),'normalization_and_degeneracy_review':'At this exact R normalize every center by dprime=(1-R²)/d before rebuilding ownership/common diagram. Original exhaustive m/B and M reductions retained. Six branches recompute all finite supports at current R. Upstream continuous geometric/isoperimetric/polygon theorems, signed physical-edge cancellation and single-spend boundary banks inherited unchanged. Strict rational gaps permit the same enlarged-radius finite-type limiting argument; compact projected center space gives attainment and strict lower bound. This is a computer-assisted mathematical proof, not a theorem-prover formalization.','proof_scope':'New universal lower bound under the explicitly reviewed upstream geometric proof; exact optimum/minimal polynomial/optimal configuration remain unresolved.','bindings':{p.relative_to(ROOT).as_posix():sha(p) for p in (Path(__file__),firstpath,secondpath,manifestpath,source/'working/PROOF_11323.md',source/'working/GLOBAL_11323_INDEPENDENT_COMPOSITION_AUDIT.md')}};out=ROOT/f'verify/out/n100-new-lower-bound-{a.tag}.json';assert not out.exists();out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print('PASS NEW LOWER BOUND',str(radius),'improvement',str(radius-F(11323,100000)),'six positive branch margins',flush=True)
if __name__=='__main__':main()
