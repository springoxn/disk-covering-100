"""Project all learned finite supports back into their inherited continuous parent."""
from pathlib import Path
import json,hashlib
from n100_arc_nogood_state_dp import ROOT,load,need,labels
from n100_arc_nogood_reinjection import setup,build,intersect,independent_tile,coupled,independent

def width(B):return sum(b[1]-b[0]+b[3]-b[2] for b in B)
def main():
 source='verify/out/n100-arc-ranked-witnesses.json';z=load(source);learned=z['learned'];need(learned and learned['proof']['excluded'],'certified range nogood');p=z['placement'];node=z['source_node'];base=next(c['result']['boxes'] for c in load('verify/out/n100-arc-center-projection.json')['cases'] if c['placement']==p and c['source_node']==node);core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior=next(c['boxes'] for c in load('verify/out/n100-axis-coupled-boxes.json')['retained'] if c['placement']==p);_,E,q=setup(core,p,prior);_,IE,Iq=independent.setup(core,p,prior);_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});signs={(1,1):0,(-1,1):1,(-1,-1):2,(1,-1):3};B=[b[:] for b in base];hulls=[]
 for raw,bits in learned['supported_domains'].items():
  v=int(raw);parts=[]
  for j in labels(bits):
   b=intersect(base[v],independent_tile(j,256,signs[q[v-100]]))
   if b is not None:parts.append(b)
  need(parts,'nonempty support hull');h=[min(b[0] for b in parts),max(b[1] for b in parts),min(b[2] for b in parts),max(b[3] for b in parts)];B[v]=h;hulls.append({'vertex':v,'support_count':bits.bit_count(),'old_box':base[v],'new_box':h})
 a=coupled(B,E,q,pairs,limit=160);b=coupled(B,IE,Iq,pairs,alt=True,limit=160);need(a==b,'projected continuous propagation alternate');summary={'parent_width':width(base),'projected_width':width(B),'width_removed_by_projection':width(base)-width(B),'projected_changed_vertices':sum(r['old_box']!=r['new_box'] for r in hulls),'excluded':a['excluded']}
 if not a['excluded']:
  need(all(base[i][0]<=x[0]<=x[1]<=base[i][1] and base[i][2]<=x[2]<=x[3]<=base[i][3] for i,x in enumerate(a['boxes'])),'continuous subset');summary.update({'final_width':width(a['boxes']),'total_width_removed':width(base)-width(a['boxes']),'fixed':a['fixed'],'sweeps':a['sweeps']})
 out=ROOT/'verify/out/n100-arc-ranked-projection.json';need(not out.exists(),'overwrite');paths=[source,'verify/out/n100-arc-center-projection.json','verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_arc_ranked_witnesses.py','verify/n100_circle_center_alternating.py','verify/n100_boundary_arc_tiles_audit.py','verify/n100_axis_coupled_boxes.py','verify/n100_axis_coupled_boxes_independent.py','verify/n100_boundary_circle_branch_tree.py','verify/n100_boundary_circle_branch_tree_independent_full.py'];out.write_text(json.dumps({'schema':'n100-arc-ranked-projection/v1','verified_integer_support_hulls':True,'all_alternate_geometry_results_equal':True,'placement':p,'source_node':node,'summary':summary,'vertex_projections':hulls,'result':a,'scope':'necessary support hull projection for one inherited parent; hull loses label correlations; nonempty result does not prove coverage','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS ranked projection',summary)
if __name__=='__main__':main()
