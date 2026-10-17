"""Independent exact replay of fixed-core axis insertion filter."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from math import comb
import json,hashlib,argparse,copy
ROOT=Path(__file__).resolve().parents[1]
def need(ok,msg):
    if not ok:raise ValueError(msg)
def audit(z):
    r=F(z['radius']);c=F(z['sqrt_lower']);M=F(z['half_arc_upper']);pl=F(z['pi_lower']);b=z['boundary_core_edges']
    need(0<r<1 and c>0 and c*c<=1-r*r and M*c==r,'arc rational bound')
    def atan(q,n):return sum((F((-1)**j,(2*j+1)*q**(2*j+1)) for j in range(n)),F(0))
    need(pl<16*atan(5,10)-4*atan(239,9),'independent pi bracket')
    need(pl/2-12*M>0 and F(z['six_arc_quadrant_gap'])==pl/2-12*M,'six arcs gap')
    # Independently enumerate only distinct boundary edges; any repeated edge gives
    # consecutive axes separated by no core vertex and hence one arc, impossible.
    kept=set()
    for choice in combinations(range(b),4):
        gaps=[choice[j+1]-choice[j] for j in range(3)]+[b+choice[0]-choice[-1]]
        if min(gaps)<6:continue
        for j in range(4):kept.add(choice[j:]+choice[:j])
    saved=[tuple(row) for row in z['retained_axis_edge_placements']]
    need(len(saved)==len(set(saved)),'duplicate placements')
    # Candidate core has unique outer neighbors (prior separate dual audit);
    # therefore this instance's same-face filter removes none.
    need(z['rejected_by_same_face_filter']==0,'extra face pruning requires separate replay')
    need(set(saved)==kept,'complete placement set')
    need(len(kept)==b*comb(b-21,3)==z['after_arc_budget'],'count formula')
    need(z['all_ordered_four_axis_placements']==4*comb(b+3,4),'unfiltered count')
    candidate=tuple(z['candidate_axis_edge_indices']);need(candidate in kept,'candidate lost')
    return {'retained':len(kept),'discarded':4*comb(b+3,4)-len(kept),'complete_set_equal':True,'candidate_retained':True}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-axis-subdivision-independent.json');args=ap.parse_args()
    p=ROOT/'verify/out/n100-axis-subdivision-pruning.json';z=json.loads(p.read_text(encoding='utf-8'));result=audit(z)
    controls=[]
    for label,change in [('missing_placement',lambda q:q['retained_axis_edge_placements'].pop()),('understated_arc_bound',lambda q:q.__setitem__('half_arc_upper','1/100')),('wrong_count',lambda q:q.__setitem__('after_arc_budget',1))]:
        q=copy.deepcopy(z);change(q)
        try:audit(q)
        except ValueError:controls.append(label)
    need(len(controls)==3,'controls')
    out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-axis-subdivision-independent/v1','verified':True,'result':result,'rejected_controls':controls,'method':'independent distinct-edge combinations versus primary multisets and gap compositions; no primary pruning imports','input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'machine_verified_geometry':False,'global_optimality':False,'scope':'fixed candidate core axis subdivision combinatorics; geometry dependencies inherited; no continuous-domain or complete-core enumeration'},indent=2)+'\n',encoding='utf-8');print('PASS independent distinct-edge placement sets:',result,';3 corruptions rejected')
if __name__=='__main__':main()
