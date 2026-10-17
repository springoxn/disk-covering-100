"""Exact four-axis subdivision pruning on the actual n100 cubic core.
All placements counted relative to fixed directed boundary; not quotient by automorphisms.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations_with_replacement,combinations
from math import comb,isqrt
from collections import Counter
import json,hashlib,argparse
from n100_dart_independent_canonicalization import loops,need
from n100_cubic_core_roundtrip import restore
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-axis-subdivision-pruning.json');args=ap.parse_args()
    source=ROOT/'verify/out/n100-cubic-core-roundtrip.json';z=json.loads(source.read_text(encoding='utf-8'));core=z['core'];A=core['alpha'];P=core['phi'];tags=core['core_tags']
    r=F(1154469548855829,10**16);scale=10**24;v=1-r*r;c=F(isqrt(v.numerator*scale**2//v.denominator),scale);M=r/c
    need(c>0 and c*c<=v,'sqrt lower');pl=F(314159,100000)
    def atan(q,n):return sum((F((-1)**j,(2*j+1)*q**(2*j+1)) for j in range(n)),F(0))
    need(pl<16*atan(5,8)-4*atan(239,7),'pi lower')
    need(24*M<pl,'six boundary arcs cannot cover quadrant')
    # phi<=sin(phi)/c<=r/c=M. Six arcs span <=12M<pi/2.
    fc=loops(P);outer=next(row for row in fc if tags[row[0]][0]=='outer')
    boundary=[A[d] for d in reversed(outer)];b=len(boundary);need(b==32,'candidate boundary')
    owner={d:j for j,row in enumerate(fc) for d in row}
    alpha0,phi0,tags0=restore(core)
    candidate={}
    for j,d in enumerate(boundary):
        for original in core['subdivision_paths'][d]:
            mark=tags0[original][1]
            if mark!='':need(mark not in candidate,'axis repeated');candidate[mark]=j
    need(set(candidate)==set('0123'),'axes recovered')
    candidate_edges=[candidate[str(j)] for j in range(4)]
    distances=[(candidate_edges[(i+1)%4]-candidate_edges[i])%b for i in range(4)]
    need(sum(distances)==b and min(distances)>=6,'candidate must survive arc filter')
    need(len({owner[boundary[j]] for j in candidate_edges})==4,'candidate same-face axis filter')
    examined=0;arc_kept=[];face_kept=[];hist=Counter()
    for edges in combinations_with_replacement(range(b),4):
        gaps=[edges[i+1]-edges[i] for i in range(3)]+[b+edges[0]-edges[3]]
        for start in range(4):
            examined+=1
            if min(gaps)<6:continue
            # Axis0 placed at ordered slot start; axis1 follows it on the positive boundary.
            labeled=[edges[(start+i)%4] for i in range(4)];arc_kept.append(labeled)
            if len({owner[boundary[j]] for j in labeled})<4:continue
            face_kept.append(labeled);hist[tuple(sorted(gaps))]+=1
    need(examined==4*comb(b+3,4),'all multiset slots count')
    formula=b*comb(b-24+3,3);need(len(arc_kept)==formula,'stars and bars count')
    need(candidate_edges in face_kept,'actual candidate pruned')
    # Independent generation via positive cyclic gap compositions starting at labeled axis0.
    independent=set()
    for first in range(b):
        for g0 in range(6,b-17):
            for g1 in range(6,b-g0-11):
                for g2 in range(6,b-g0-g1-5):
                    g3=b-g0-g1-g2
                    if g3<6:continue
                    independent.add((first,(first+g0)%b,(first+g0+g1)%b,(first+g0+g1+g2)%b))
    need(independent==set(map(tuple,arc_kept)),'independent composition enumeration')
    out=ROOT/args.out;need(not out.exists(),'overwrite')
    output={'schema':'n100-axis-subdivision-pruning/v1','verified':True,'radius':str(r),'sqrt_lower':str(c),'half_arc_upper':str(M),'pi_lower':str(pl),'six_arc_quadrant_gap':str(pl/2-12*M),'minimum_arcs_per_quadrant':7,'minimum_core_vertices_between_axes':6,
        'boundary_core_edges':b,'all_ordered_four_axis_placements':examined,'after_arc_budget':len(arc_kept),'after_same_face_axis_pair_filter':len(face_kept),'rejected_by_arc_budget':examined-len(arc_kept),'rejected_by_same_face_filter':len(arc_kept)-len(face_kept),
        'independent_gap_composition_sets_equal':True,'arc_budget_count_formula':'b*C(b-21,3) for b>=24; 0 otherwise','candidate_axis_edge_indices':candidate_edges,'candidate_core_gap_counts':distances,'candidate_retained':True,'retained_axis_edge_placements':face_kept,
        'analytic_dependencies':['disk radius U<1 has a single short service arc of half-length phi<=U/sqrt(1-U^2)','ordered quadrant chain covers arc pi/2','each boundary edge is covered by its owner, so its length<=2M','between consecutive axis points there are g core vertices and g+1 arc segments','same face cannot contain two fixed axes at radius U<sqrt(1/2)'],
        'scope':'all four-axis subdivisions of the fixed candidate core with fixed directed boundary; no core enumeration, automorphism quotient or continuous feasibility proof','machine_verified_geometry':False,'n100_count_families_excluded':0,'global_optimality':False,'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print('PASS actual core axis placements:',examined,'->',len(arc_kept),'arc-budget ->',len(face_kept),'same-face; independent composition set equal; actual candidate retained',candidate_edges,distances)
if __name__=='__main__':main()
