"""Independent transformation checks and negative controls for direct .113231."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,re,ast,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
folder=ROOT/'runtime/lower-small-advance-direct-113231-fresh';package=folder/'package'
source=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323'
manifest=json.loads((folder/'transformation.json').read_text(encoding='utf-8'))
radius=F(113231,1000000)
assert F(manifest['radius'])==radius
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
asserts=0;checked=0
for rel,oldhash in manifest['source_snapshot'].items():
    original=source/rel;target=package/rel
    assert sha(original)==oldhash and sha(target)==manifest['copy_snapshot'][rel],rel
    if target.suffix not in ('.py','.json'):
        assert original.read_bytes()==target.read_bytes();continue
    text=original.read_text(encoding='utf-8')
    expected=re.sub(r'F\(\s*11323\s*,\s*100000\s*\)',f'F({radius.numerator},{radius.denominator})',text).replace('11323/100000',str(radius))
    assert target.read_text(encoding='utf-8')==expected,rel
    if target.suffix=='.py':
        oldast=ast.parse(text);newast=ast.parse(expected)
        a=sum(isinstance(x,ast.Assert) for x in ast.walk(oldast));b=sum(isinstance(x,ast.Assert) for x in ast.walk(newast))
        assert a==b,rel
        asserts+=a;checked+=1
# The used entry is working/verify_all_11323.py, not package/run_certificates.py.
# The unused old combined lower/upper wrapper retains a Fraction(...) LOW literal
# and release integrity metadata. It is not an entry for the new lower bound.
controls=[]
commands=[('assertions_disabled',[sys.executable,'-B','-S','-O','working/verify_all_11323.py'],package,'Assertions must remain enabled'),('wrong_radius',[sys.executable,'-B','-S','-c',"from fractions import Fraction as F\nimport verify_B31_global_low_degree_0p11323 as m\nm.R=F(11323,100000)\nm.verify()"],package/'working','AssertionError')]
for name,cmd,cwd,message in commands:
    result=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,encoding='utf-8')
    assert result.returncode!=0 and message in result.stderr,(name,result.stdout,result.stderr)
    controls.append({'name':name,'expected_rejection':True,'exit_code':result.returncode,'stderr':result.stderr})
report={'status':'PASS_TRANSFORMATION_AND_NEGATIVE_CONTROLS','radius':str(radius),'snapshot_files':len(manifest['source_snapshot']),'python_sources_parsed':checked,'assertions_preserved':asserts,'all_changes_reconstructed_from_exact_radius_rule':True,'source_and_copy_hashes_match':True,'controls':controls,'new_lower_bound_entry':'working/verify_all_11323.py','unused_original_combined_wrapper_is_not_a_new_radius_entry':True,'geometry_independently_reproved':False,'bindings':{str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in [Path(__file__),folder/'transformation.json']}}
out=ROOT/'verify/out/n100-direct-113231-controls.json'
assert not out.exists();out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ['controls','bindings']},indent=2))
