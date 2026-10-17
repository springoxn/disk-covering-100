"""Orientation-free face-path verification of candidate boundary semantics."""
from pathlib import Path
from collections import defaultdict,Counter
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(c,m):
 if not c:raise ValueError(m)
def main():
 path=ROOT/'verify/out/n100-boundary-count-semantics.json';z=json.loads(path.read_text(encoding='utf-8'));mapfile=ROOT/'verify/out/n100-candidate-clipped-map.json';G=json.loads(mapfile.read_text(encoding='utf-8'));arcs=[e for e in G['edges'] if len(e['faces'])==1];need(len(arcs)==36 and all(e['kind']=='unit_circle_arc' for e in arcs),'boundary definition via face incidence');face_edges=defaultdict(list)
 for e in arcs:face_edges[e['faces'][0]].append(tuple(e['ends']))
 internal=[];endpoints=Counter()
 for face,edges in face_edges.items():
  adj=defaultdict(set)
  for a,b in edges:adj[a].add(b);adj[b].add(a)
  need(sum(len(v)==1 for v in adj.values())==2 and all(1<=len(v)<=2 for v in adj.values()),'face boundary path degrees');seen=set();stack=[next(iter(adj))]
  while stack:
   v=stack.pop()
   if v not in seen:seen.add(v);stack.extend(adj[v]-seen)
  need(len(seen)==len(adj) and len(edges)==len(adj)-1,'connected acyclic face boundary path')
  internal.extend(v for v,nbs in adj.items() if len(nbs)==2)
  endpoints.update(v for v,nbs in adj.items() if len(nbs)==1)
 need(len(face_edges)==32 and len(internal)==4 and all(G['vertices'][v]['type']=='axis' for v in internal),'32 paths and4 internal axes');need(all(n==2 for n in endpoints.values()) and len(endpoints)==32,'32 owner-transition vertices');need(sorted(internal)==sorted(z['same_owner_subdivision_vertices']) and sorted(face_edges)==z['distinct_boundary_owners'],'primary agreement');domain=json.loads((ROOT/'verify/out/n100-recursive-inner-envelope.json').read_text(encoding='utf-8'));T=set(map(tuple,domain['remaining_triples']));need(tuple(z['candidate_count_tuple'])==(100,32,32) and (100,32,32) in T and len(T)==530,'count control and domain size');toy=[0,1,0,2];runs=sum(toy[j]!=toy[j-1] for j in range(len(toy)));need(runs==4>len(set(toy))==3,'repeated-owner semantic negative control');out=ROOT/'verify/out/n100-boundary-count-semantics-independent.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-boundary-count-semantics-independent/v1','verified_orientation_free_candidate_face_paths':True,'boundary_segments':36,'connected_boundary_owner_paths':32,'internal_axis_subdivisions':4,'owner_transition_vertices':32,'candidate_recursive_count_tuple_retained':True,'repeated_owner_toy_runs':4,'repeated_owner_toy_distinct_owners':3,'scope':'independent combinatorial candidate verification and count-domain control, no universal single-arc or normalization proof; repeated-owner word is a semantic control, not a claimed realizable geometric counterexample','global_optimality':False,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent face paths32,axis4; repeated-owner semantic control; candidate retained')
if __name__=='__main__':main()
