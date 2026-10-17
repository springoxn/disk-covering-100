"""Read-only recursive dependency census. Hash consistency is not mathematical proof.

Traverses explicit path->SHA256 bindings and static local Python imports. Unnamed
hashes and dynamic paths remain visible unresolved, never silently accepted.
"""
from pathlib import Path
from collections import Counter
import ast,json,hashlib,re
from n100_pruning_catalogue import WITHDRAWN
R=Path(__file__).resolve().parents[1]
ROOTS=[
 'verify/out/n100-proof-interface-contracts-v2.json',
 'verify/out/n100-proof-interface-batch2.json',
 'verify/out/n100-proof-interface-batch3.json',
 'verify/out/n100-count-proof-interface-contracts.json',
 'verify/out/n100-arc-budget-interface-contracts.json',
 'verify/out/n100-continuous-proof-interface-contracts.json',
 'verify/out/n100-finite-tree-proof-interface-contracts-v2.json',
 'verify/out/n100-algebra-proof-interface-contracts.json']
HEX=re.compile(r'^[0-9a-f]{64}$')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def resolve(raw):
 p=Path(raw)
 if not p.is_absolute():p=R/p
 p=p.resolve();return p if p.is_relative_to(R) else None
def relative(p):return p.relative_to(R).as_posix()
def binding_pairs(value,loc='$'):
 if isinstance(value,dict):
  for k,v in value.items():
   here=loc+'.'+str(k)
   if isinstance(v,str) and HEX.fullmatch(v) and isinstance(k,str) and ('/' in k or '\\' in k) and Path(k).suffix:yield k,v,here
   elif isinstance(v,(dict,list)):yield from binding_pairs(v,here)
 elif isinstance(value,list):
  for i,v in enumerate(value):yield from binding_pairs(v,loc+'['+str(i)+']')
def unnamed_hashes(value,loc='$'):
 if isinstance(value,dict):
  for k,v in value.items():
   here=loc+'.'+str(k)
   if isinstance(v,str) and HEX.fullmatch(v) and 'sha256' in str(k) and not ('/' in str(k) or '\\' in str(k)):yield here,v
   elif isinstance(v,(dict,list)):yield from unnamed_hashes(v,here)
 elif isinstance(value,list):
  for i,v in enumerate(value):yield from unnamed_hashes(v,loc+'['+str(i)+']')
def audit(roots):
 queue=[resolve(p) for p in roots];seen=set();nodes=[];edges=[];issues=[];anonymous=[];withdrawn_hashes={sha(R/p):p for p in WITHDRAWN};hashcache={}
 def cached(p):
  if p not in hashcache:hashcache[p]=sha(p)
  return hashcache[p]
 def edge(source,raw,expected,kind,where):
  p=resolve(raw)
  if p is None:issues.append({'source':source,'target':raw,'kind':'outside_project','location':where});return
  rel=relative(p)
  if not p.is_file():issues.append({'source':source,'target':rel,'kind':'missing','location':where});return
  actual=cached(p);state='MATCH' if expected is None or actual==expected else 'HASH_MISMATCH';edges.append({'source':source,'target':rel,'kind':kind,'state':state,'expected_sha256':expected,'actual_sha256':actual,'location':where})
  if rel in WITHDRAWN or actual in withdrawn_hashes:issues.append({'source':source,'target':rel,'kind':'withdrawn_or_alias','location':where})
  if state!='MATCH':issues.append({'source':source,'target':rel,'kind':state,'location':where})
  queue.append(p)
 while queue:
  p=queue.pop()
  if p is None or p in seen:continue
  seen.add(p)
  if not p.is_file():issues.append({'target':str(p),'kind':'missing_root'});continue
  rel=relative(p);node={'path':rel,'sha256':cached(p),'bytes':p.stat().st_size,'kind':p.suffix};nodes.append(node)
  if rel in WITHDRAWN or cached(p) in withdrawn_hashes:issues.append({'target':rel,'kind':'withdrawn_or_alias'})
  if p.suffix=='.json':
   z=json.loads(p.read_text(encoding='utf-8-sig'))
   for raw,h,where in binding_pairs(z):edge(rel,raw,h,'explicit_hash_binding',where)
   for where,h in unnamed_hashes(z):anonymous.append({'source':rel,'location':where,'sha256':h,'resolution':'UNRESOLVED_UNNAMED_HASH; metadata/model hashes need not denote files'})
  elif p.suffix=='.py':
   tree=ast.parse(p.read_text(encoding='utf-8-sig'));imports=[]
   for n in ast.walk(tree):
    if isinstance(n,ast.Import):imports.extend(a.name for a in n.names)
    elif isinstance(n,ast.ImportFrom) and n.module:imports.append(n.module)
   for module in sorted(set(imports)):
    candidate=p.parent/(module.replace('.','/')+'.py')
    if not candidate.is_file():candidate=R/'verify'/(module.replace('.','/')+'.py')
    if candidate.is_file():edge(rel,str(candidate),None,'static_local_import',module)
   node['dynamic_path_review_required']=any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ('insert','read_text','read_bytes','load','loads','open') for n in ast.walk(tree))
   node['top_level_call_statements']=sum(isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) for n in tree.body)
   node['external_module_names_unresolved']=[m for m in sorted(set(imports)) if not (p.parent/(m.replace('.','/')+'.py')).is_file() and not (R/'verify'/(m.replace('.','/')+'.py')).is_file()]
 paths={n['path'] for n in nodes}
 # An unnamed hash can be matched to already traversed content, but this is only
 # a candidate association; an input/model fingerprint is not assumed a file hash.
 byhash={}
 for n in nodes:byhash.setdefault(n['sha256'],[]).append(n['path'])
 for a in anonymous:
  a['matching_traversed_files']=byhash.get(a['sha256'],[])
  if a['matching_traversed_files']:a['resolution']='CONTENT_MATCH_CANDIDATES_ONLY'
 bysource={}
 for e in edges:bysource.setdefault(e['source'],set()).add(e['target'])
 bad_sources={i.get('source',i.get('target')) for i in issues};root_states=[]
 for root in roots:
  reached=set();pending=[root]
  while pending:
   current=pending.pop()
   if current in reached:continue
   reached.add(current);pending.extend(bysource.get(current,()))
  bad=sorted(reached&bad_sources);root_states.append({'root':root,'transitive_files':len(reached),'known_invalid_dependencies':bad,'binding_gate':'REJECT' if bad else 'NO_KNOWN_EXPLICIT_BINDING_ERROR','complete_proof_dependency_gate':'UNDECIDED: dynamic and analytic dependencies not fully discharged'})
 return {'root_dependency_states':root_states,'roots':roots,'nodes':sorted(nodes,key=lambda n:n['path']),'edges':edges,'issues':issues,'unnamed_hash_fields':anonymous,'summary':{'files':len(nodes),'explicit_hash_edges':sum(e['kind']=='explicit_hash_binding' for e in edges),'static_import_edges':sum(e['kind']=='static_local_import' for e in edges),'issue_counts':dict(Counter(i['kind'] for i in issues)),'unnamed_hash_fields':len(anonymous),'dynamic_python_sources':sum(n.get('dynamic_path_review_required',False) for n in nodes),'nested_files':sum(not n['path'].startswith('verify/') for n in nodes)},'mathematical_verdict':None,'dependency_completeness':'PARTIAL: explicit binding closure plus static local imports; dynamic loads, anonymous hashes, external packages and analytic lemmas require review','global_optimality':False}
def main():
 result=audit(ROOTS);controls=[]
 # Direct scanner controls use tiny in-memory records; no historical files mutate.
 assert list(binding_pairs({'bindings':{'verify/x.json':'a'*64}}))==[('verify/x.json','a'*64,'$.bindings.verify/x.json')];controls.append('explicit_hash_detected')
 assert list(binding_pairs({'rows':[{'bindings':{'verify/x.json':'a'*64}}]}))==[('verify/x.json','a'*64,'$.rows[0].bindings.verify/x.json')]
 controls.append('nested_list_binding_detected')
 assert resolve('../outside.json') is None;controls.append('outside_project_rejected')
 result.update(schema='n100-interface-dependency-audit/v1',controls=controls,script_sha256=sha(Path(__file__)))
 out=R/'verify/out/n100-interface-dependency-audit-v2.json';assert not out.exists();out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print('PASS dependency census',json.dumps(result['summary']));print('ISSUES',json.dumps(result['issues'][:12]))
if __name__=='__main__':main()
