"""Independent source-bound replay of the four radius count strata."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
R=Path(__file__).resolve().parents[1]
def load(name):return json.loads((R/'verify/out'/name).read_text(encoding='utf-8'))
def main():
 z=load('n100-radius-count-strata.json');front=load('n100-recursive-radius-frontier.json');audit=load('n100-recursive-radius-frontier-independent.json');base=load('n100-recursive-joint-area.json');ba=load('n100-recursive-joint-area-independent.json')
 for name,a in [('n100-recursive-radius-frontier.json',audit),('n100-recursive-joint-area.json',ba)]:
  assert a['input_sha256']==hashlib.sha256((R/'verify/out'/name).read_bytes()).hexdigest()
 sources={F(c['radius_cut']):c for c in front['cuts'] if c['excluded_at_current_lower']};sources[F(base['radius_upper'])]={'minimum_nonserving_count':58,'remaining_triples':base['remaining_triples']}
 layers=z['layers'];assert len(layers)==4;prev=F(z['radius_lower_global']);domains=[];report=[]
 for layer in layers:
  lo,hi=map(F,[layer['radius_lower'],layer['radius_upper']]);assert lo==prev<hi;prev=hi;src=sources[hi];assert layer['minimum_nonserving']==src['minimum_nonserving_count'];expected=sorted(map(tuple,src['remaining_triples']));actual=sorted(map(tuple,layer['triples']));assert actual==expected and len(actual)==layer['triple_count'];families=sorted({t[:2] for t in actual});assert families==list(map(tuple,layer['families'])) and len(families)==layer['family_count'];assert (100,32,32) in actual;domains.append(set(actual));report.append({'upper':str(hi),'count':len(actual),'families':len(families)})
 assert prev==F(z['radius_upper_global']);assert all(a<=b for a,b in zip(domains,domains[1:]));assert z['monotone_inclusion_checked']
 # For a radius at a shared endpoint, prefer earlier/stronger layer.
 endpoints=[F(l['radius_upper']) for l in layers];assert [next(i for i,l in enumerate(layers) if r<=F(l['radius_upper'])) for r in endpoints]==list(range(4))
 out=R/'verify/out/n100-radius-count-strata-independent.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-radius-count-strata-independent/v1','verified_source_bound_domains':True,'verified_gap_free_reference_intervals':True,'verified_nested_domains':True,'verified_shared_endpoint_stronger_layer_selection':True,'candidate_count_tuple_retained_all_layers':True,'layers':report,'scope':'independent exact source-bound domain interface replay; no new geometry or radius exclusion; candidate integer tuple survival does not certify a covering at smaller radii','global_optimality':False,'input_sha256':hashlib.sha256((R/'verify/out/n100-radius-count-strata.json').read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent four strata; counts245/294/347/404; endpoints and source hashes')
if __name__=='__main__':main()
