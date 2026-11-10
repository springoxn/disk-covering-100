"""Exact lattice mesh helpers, generalized without changing the frozen N26 checker."""
from collections import defaultdict,Counter


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
    assert sum(boundary_counts)==sum(row['widths'])
    boundary_mask=sum(1<<i for i,b in enumerate(boundary_counts) if b)
    return faces,neighbors,boundary_counts,boundary_mask

def mesh(faces,expected_widths=None,vertex_count=67,face_count=106,boundary_count=26,allowed_boundary_incidences=None):
    points=sorted({p for tri in faces for p in tri})
    if len(points)!=vertex_count or len(faces)!=face_count:
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
    if len(edges)!=vertex_count+face_count-1:
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
    if len(next_vertex)!=boundary_count or set(next_vertex)!=set(previous):
        return None
    start=min(next_vertex)
    v=start
    for unused in range(boundary_count):
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
    if len(reached)!=face_count:
        return None
    if allowed_boundary_incidences is not None and any(incidence[p] not in allowed_boundary_incidences for p in boundary):
        return None
    ids={p:i for i,p in enumerate(points)}
    return {'axial_vertices':[list(p) for p in points],
            'triangles':[[ids[p] for p in tri] for tri in faces],
            'boundary_ids':[ids[p] for p in boundary],
            'boundary_face_incidences':[incidence[p] for p in boundary],
            'boundary_incidence_histogram':dict(sorted(Counter(incidence[p] for p in boundary).items())),
            'verified_counts':{'vertices':vertex_count,'edges':len(edges),'faces':face_count,'boundary':boundary_count},
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
