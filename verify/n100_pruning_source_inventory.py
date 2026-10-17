"""Inventory n100 verification scripts without treating lexical hints as proven methods."""
from pathlib import Path
import ast,json,hashlib
R=Path(__file__).resolve().parents[1]
def main():
 scripts=sorted(p for p in (R/'verify').glob('*.py') if 'n100' in p.stem);modules={p.stem:p for p in scripts};rows=[]
 for p in scripts:
  text=p.read_text(encoding='utf-8-sig');tree=ast.parse(text,filename=str(p));doc=ast.get_docstring(tree) or '';imports=set();refs=set();functions=[]
  for node in ast.walk(tree):
   if isinstance(node,ast.Import):imports.update(a.name.split('.')[0] for a in node.names)
   elif isinstance(node,ast.ImportFrom) and node.module:imports.add(node.module.split('.')[0])
   elif isinstance(node,ast.Constant) and isinstance(node.value,str) and node.value.endswith('.json') and '\n' not in node.value and len(node.value)<350:refs.add(node.value)
   elif isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)) and node.col_offset==0:functions.append(node.name)
  hints=[word for word in ['hall','capacity','cap','area','arc','local','tree','radial','ear','count','interval','lens','frontier','witness','kkt','map','negative','counterexample','independent','audit'] if word in (p.stem+' '+doc).lower()]
  rows.append({'script':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'docstring':doc,'public_top_level_functions':functions,'local_n100_imports':sorted(m for m in imports if m in modules),'json_literal_candidates':sorted(refs),'lexical_hints_not_verified_classification':hints,'interface_review_status':'unreviewed','eligible_for_composition':False})
 out=R/'verify/out/n100-pruning-source-inventory.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-pruning-source-inventory/v1','script_count':len(rows),'scripts':rows,'scope':'complete current top-level verify/*.py whose filenames contain n100; excludes nested copies and runtime discovery scripts; all method semantics require review, filename hints are not an authority to activate cuts','global_optimality':False,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS source inventory',len(rows),'scripts parsed; all unreviewed interfaces fail closed')
if __name__=='__main__':main()
