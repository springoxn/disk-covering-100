#!/usr/bin/env python3
"""Complete P26/F108 flat-core enumeration for the reduced B32 branch.

Only combinatorial unit-lattice labels are exported, not covering centers.
No Young-diagram characterization is needed: deletions are enumerated by
outside-connected triangle subsets and checked as complete meshes.
"""
from contextlib import redirect_stderr
from io import StringIO
import json
from check_lattice_width_cases import verify as width_cases
from enumerate_flat_N26_cores import removed_candidates
from lattice_mesh_utils import region_faces,mesh,canonical


def check_mesh(faces,widths=None):
    return mesh(faces,widths,vertex_count=68,face_count=108,boundary_count=26,
                allowed_boundary_incidences={2,3,4})


def enumerate_all():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    regions=[]
    for old in width_cases()['N26_containing_regions']:
        if old['triangle_count']>=108:
            row=dict(old);row['triangles_to_delete']=row['triangle_count']-108
            regions.append(row)
    assert [r['triangle_count'] for r in regions]==[108,108,110,110,112]
    distinct={};stats=[]
    for ri,row in enumerate(regions):
        faces,neighbors,bc,bmask=region_faces(row)
        with redirect_stderr(StringIO()):
            candidates,levels=removed_candidates(neighbors,bc,bmask,row['triangles_to_delete'])
        accepted=0
        for mask in sorted(candidates):
            remaining=[tri for i,tri in enumerate(faces) if not (mask>>i)&1]
            data=check_mesh(remaining,row['widths'])
            if data is None:continue
            accepted+=1
            key,oriented=canonical(remaining)
            if key not in distinct:
                normalized=check_mesh(oriented)
                assert normalized is not None
                normalized['source_region']=ri
                normalized['removed_face_indices']=[i for i in range(len(faces)) if (mask>>i)&1]
                distinct[key]=normalized
        stats.append({'region':ri,'deletion_levels':levels,'perimeter_candidates':len(candidates),
                      'valid_meshes':accepted,'cumulative_dihedral_classes':len(distinct)})
    assert [s['perimeter_candidates'] for s in stats]==[1,1,6,6,27]
    assert sum(s['perimeter_candidates'] for s in stats)==41
    cores=[]
    for i,key in enumerate(sorted(distinct)):
        row=distinct[key];row['core_id']='B32_P26_F108_'+str(i).zfill(3)
        assert sum(4-h for h in row['boundary_face_incidences'])==32
        cores.append(row)
    return {'status':'PASS','scope':'Complete conditional B32 all-degree-six P26/F108 core catalog; metric exclusion remains separate',
            'coordinate_warning':'Axial coordinates describe abstract unit-triangle development, not actual disk centers',
            'target_counts':{'vertices':68,'edges':175,'faces':108,'boundary':26},
            'containing_regions':regions,'statistics':stats,'raw_perimeter_candidates':41,
            'core_count':len(cores),'cores':cores}


if __name__=='__main__':print(json.dumps(enumerate_all(),separators=(',',':')))
