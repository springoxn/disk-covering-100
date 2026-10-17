"""Full fixed-core circle propagation scan and separate independent replay.
Result hashes include every final box; exclude only strict interval failures.
"""
from pathlib import Path
from collections import Counter
import json,hashlib,argparse,time
ROOT=Path(__file__).resolve().parents[1]
def need(x,m):
 if not x:raise ValueError(m)
def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--independent',action='store_true');ap.add_argument('--out');args=ap.parse_args()
 if args.independent:
  from n100_boundary_circle_independent import replay
 else:
  from n100_boundary_circle_propagation import run
 cp=ROOT/'verify/out/n100-cubic-core-roundtrip.json';bp=ROOT/'verify/out/n100-axis-coupled-boxes.json';apath=ROOT/'verify/out/n100-axis-subdivision-pruning.json';pp=ROOT/'verify/out/n100-axis-dual-chain-pruning.json';sp=ROOT/'verify/out/n100-boundary-circle-full.json'
 load=lambda p:json.loads(p.read_text(encoding='utf-8'));core=load(cp)['core'];prior=load(bp);candidate=load(apath)['candidate_axis_edge_indices'];expected=set(map(tuple,load(pp)['retained_axis_edge_placements']));need(len(expected)==4776 and expected=={tuple(row['placement']) for row in prior['retained']},'complete4776 domain')
 primary=load(sp) if args.independent else None;reference={tuple(r['placement']):r for r in primary['results']} if primary else {};records=[];hist=Counter();retained=[];excluded=[];capped=0;start=time.monotonic()
 for num,row in enumerate(prior['retained'],1):
  p=row['placement']
  if args.independent:r,w=replay(core,p,row['boxes'])
  else:r=run(core,p,row['boxes']);w=None
  record={'placement':p,'excluded':r['excluded'],'sweeps':r['sweeps'],'full_result_sha256':digest(r)}
  if r['excluded']:
   record['failure']=r['failure'];excluded.append(p)
   if r['failure'][0]=='distance':
    a,b=r['failure'][1:];record['failure_boxes']=[r['boxes'][a],r['boxes'][b]]
  else:record['fixed']=r['fixed'];retained.append(p);capped+=not r['fixed']
  if primary:need(record==reference[tuple(p)],'independent full result mismatch '+str(p))
  records.append(record);hist['excluded' if r['excluded'] else 'fixed' if r['fixed'] else 'capped']+=1
  if num%256==0:print('progress',num,dict(hist),'elapsed',round(time.monotonic()-start),flush=True)
 need(candidate in retained,'actual candidate retained');need(len(records)==4776 and len(excluded)+len(retained)==4776,'partition')
 sources=[cp,bp,apath,pp,ROOT/'verify/n100_boundary_circle_independent.py' if args.independent else ROOT/'verify/n100_boundary_circle_propagation.py',ROOT/'verify/n100_axis_coupled_boxes_independent.py' if args.independent else ROOT/'verify/n100_axis_coupled_boxes.py']
 if primary:sources.append(sp)
 output={'schema':'n100-boundary-circle-full-independent/v1' if primary else 'n100-boundary-circle-full/v1','verified_integer_scan':True,'independent_replay':args.independent,'input_placements':4776,'excluded_count':len(excluded),'retained_count':len(retained),'retained_capped':capped,'candidate_retained':True,'boundary_vertices_per_case':32,'incidences_per_case':562,'max_sweeps':40,'results':records,'retained_axis_edge_placements':retained,'histogram':dict(hist),'result_digest_encoding':'SHA256 of full result with sorted JSON keys and compact separators; includes all boxes and counters; replay required to reconstruct','scope':'one fixed core, full stage42 domain; necessary boundary-circle/quadrant/shared-vertex relaxation; capped and fixed boxes unresolved; no full core enumeration','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 out=ROOT/(args.out or ('verify/out/n100-boundary-circle-full-independent.json' if primary else 'verify/out/n100-boundary-circle-full.json'));need(not out.exists(),'overwrite');out.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8');print('PASS full circle',args.independent,dict(hist),'candidate retained',flush=True)
if __name__=='__main__':main()
