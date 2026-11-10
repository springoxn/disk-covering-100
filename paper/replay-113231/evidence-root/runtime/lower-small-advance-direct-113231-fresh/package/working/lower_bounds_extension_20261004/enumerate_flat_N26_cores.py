#!/usr/bin/env python3
"""Exhaustive outside-connected face deletions for all flat N26 cores.

The six containing regions follow from LATTICE_CORE_ISOPERIMETRY.md.
No corner-cut characterization is assumed by this enumeration.
"""
from collections import defaultdict,Counter
import json
import sys
from check_lattice_width_cases import verify as width_cases


def det(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def region_faces(row):
    xw,yw,zw=row['widths']
    L=row['lower_diagonal_offset']
    points={(x,y) for x in range(xw+1) for y in range(yw+1) if L<=x+y<=L+zw}
    faces=[]
    for x in range(-1,xw+1):
        for y in range(-1,yw+1):
            for tri in (((x,y),(x+1,y),(x,y+1)),((x+1,y),(x+1,y+1),(x,y+1))):
                if set(tri)<=points:
                    assert det(*tri)==1
                    faces.append(tri)
    assert len(faces)==row['triangle_count']
    edges=defaultdict(list)
    for i,tri in enumerate(faces):
        for j in range(3):
            edges[tuple(sorted((tri[j],tri[(j+1)%3])))].append(i)
    neighbors=[0]*len(faces)
    boundary_counts=[0]*len(faces)
    for edge,fs in edges.items():
        assert len(fs) in (1,2)
        if len(fs)==1:
            boundary_counts[fs[0]]+=1
        else:
            a,b=fs
            neighbors[a]|=1<<b
            neighbors[b]|=1<<a
    assert sum(boundary_counts)==26
    boundary_mask=sum(1<<i for i,b in enumerate(boundary_counts) if b)
    return faces,neighbors,boundary_counts,boundary_mask


def removed_candidates(neighbors,boundary_counts,boundary_mask,k):
    if k==0:
        return {0},[1]
    # q counts removed/removed edges plus removed original-boundary edges.
    # Remaining perimeter is 26+3k-2q, so the terminal target is q=3k/2.
    assert k%2==0
    target=3*k//2
    states={0:0}
    levels=[1]
    for depth in range(1,k+1):
        nxt={}
        for mask,q in states.items():
            available=boundary_mask
            scan=mask
            while scan:
                bit=scan&-scan
                scan-=bit
                available|=neighbors[bit.bit_length()-1]
            available&=~mask
            while available:
                bit=available&-available
                available-=bit
                i=bit.bit_length()-1
                qq=q+boundary_counts[i]+(neighbors[i]&mask).bit_count()
                # The added triangle has only three edges, so q rises by at most3.
                if qq>target or qq+3*(k-depth)<target:
                    continue
                newmask=mask|bit
                if newmask in nxt:
                    assert nxt[newmask]==qq
                else:
                    nxt[newmask]=qq
        states=nxt
        levels.append(len(states))
        print('deletion depth',depth,'of',k,'states',len(states),file=sys.stderr,flush=True)
    assert all(q==target for q in states.values())
    return set(states),levels


def mesh(faces,expected_widths=None):
    points=sorted({p for tri in faces for p in tri})
    if len(points)!=67 or len(faces)!=106:
        return None
    if expected_widths is not None:
        actual=(max(p[0] for p in points)-min(p[0] for p in points),
                max(p[1] for p in points)-min(p[1] for p in points),
                max(sum(p) for p in points)-min(sum(p) for p in points))
        if tuple(expected_widths)!=actual:
            return None
    edges=defaultdict(list)
    incidence=Counter()
    for fi,tri in enumerate(faces):
        assert det(*tri)==1
        for p in tri:
            incidence[p]+=1
        for j in range(3):
            a,b=tri[j],tri[(j+1)%3]
            edges[tuple(sorted((a,b)))].append((fi,a,b))
    if len(edges)!=172:
        return None
    boundary=[]
    next_vertex={}
    previous={}
    for fs in edges.values():
        if len(fs)==1:
            fi,a,b=fs[0]
            if a in next_vertex or b in previous:
                return None
            next_vertex[a]=b
            previous[b]=a
        elif len(fs)==2:
            if fs[0][1:]!=tuple(reversed(fs[1][1:])):
                return None
        else:
            return None
    if len(next_vertex)!=26 or set(next_vertex)!=set(previous):
        return None
    start=min(next_vertex)
    v=start
    for unused in range(26):
        if v in boundary:
            return None
        boundary.append(v)
        v=next_vertex[v]
    if v!=start or set(boundary)!=set(next_vertex):
        return None
    bs=set(boundary)
    boundary_edges={tuple(sorted((p,next_vertex[p]))) for p in boundary}
    # Core chordlessness follows independently from general triangulation isoperimetry.
    if any(a in bs and b in bs and (a,b) not in boundary_edges for a,b in edges):
        return None
    if any(incidence[p]!=6 for p in points if p not in bs):
        return None
    # Check face connectivity; the one boundary cycle and Euler then give a disk.
    face_neighbors=[set() for unused in faces]
    for fs in edges.values():
        if len(fs)==2:
            a,b=fs[0][0],fs[1][0]
            face_neighbors[a].add(b)
            face_neighbors[b].add(a)
    reached={0}
    todo=[0]
    while todo:
        f=todo.pop()
        for q in face_neighbors[f]-reached:
            reached.add(q)
            todo.append(q)
    if len(reached)!=106:
        return None
    ids={p:i for i,p in enumerate(points)}
    return {'axial_vertices':[list(p) for p in points],
            'triangles':[[ids[p] for p in tri] for tri in faces],
            'boundary_ids':[ids[p] for p in boundary],
            'boundary_face_incidences':[incidence[p] for p in boundary],
            'boundary_incidence_histogram':dict(sorted(Counter(incidence[p] for p in boundary).items())),
            'verified_counts':{'vertices':67,'edges':172,'faces':106,'boundary':26},
            'chordless':True,'interior_degrees_all_six':True}


def canonical(faces):
    candidates=[]
    for reflected in (False,True):
        for rotation in range(6):
            def transform(p):
                x,y=p
                if reflected:
                    x,y=y,x
                for unused in range(rotation):
                    x,y=-y,x+y
                return x,y
            transformed=[tuple(transform(p) for p in tri) for tri in faces]
            xmin=min(p[0] for tri in transformed for p in tri)
            ymin=min(p[1] for tri in transformed for p in tri)
            key=tuple(sorted(tuple(sorted((x-xmin,y-ymin) for x,y in tri)) for tri in transformed))
            candidates.append(key)
    key=min(candidates)
    oriented=[]
    for tri in key:
        a,b,c=tri
        oriented.append((a,b,c) if det(a,b,c)>0 else (a,c,b))
    return key,oriented


def enumerate_all():
    regions=width_cases()['N26_containing_regions']
    distinct={}
    statistics=[]
    for ri,row in enumerate(regions):
        print('region',ri,row,file=sys.stderr,flush=True)
        faces,neighbors,bc,bmask=region_faces(row)
        candidates,levels=removed_candidates(neighbors,bc,bmask,row['triangles_to_delete'])
        accepted=0
        for mask in candidates:
            remaining=[tri for i,tri in enumerate(faces) if not (mask>>i)&1]
            data=mesh(remaining,row['widths'])
            if data is None:
                continue
            accepted+=1
            key,oriented=canonical(remaining)
            if key not in distinct:
                normalized=mesh(oriented)
                assert normalized is not None
                normalized['source_region']=ri
                normalized['removed_face_indices']=[i for i in range(len(faces)) if (mask>>i)&1]
                distinct[key]=normalized
        statistics.append({'region':ri,'levels':levels,'perimeter_candidates':len(candidates),
                           'valid_disks':accepted,'cumulative_dihedral_classes':len(distinct)})
    patches=[]
    for i,key in enumerate(sorted(distinct)):
        row=distinct[key]
        row['core_id']='flat_N26_'+str(i).zfill(3)
        patches.append(row)
    return {'status':'PASS','scope':'All conditional flat N26/F106 chordless core patches, not all 100-disk covering graphs',
            'coordinate_warning':'Axial coordinates are combinatorial unit-triangle labels, not covering centers',
            'containing_regions':regions,'statistics':statistics,'core_count':len(patches),'cores':patches}


if __name__=='__main__':
    print(json.dumps(enumerate_all(),separators=(',',':')))
