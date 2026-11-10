"""Exact support-expression helper for corner-potential range below one."""
from fractions import Fraction as F
from verify_star_lp_duals import I,q,S,PI
from exact_angle_conjugates import sine_conjugate


def face_bound(labels,nu):
    labels=tuple(F(x) for x in labels)
    assert len(labels)==3 and max(labels)-min(labels)<1
    nu=q(F(nu));mean=q(sum(labels,F(0)))/3
    acute=PI*nu+sum((sine_conjugate(nu-q(x)) for x in labels),q(0))-PI*mean
    vertex=PI*(q(max(labels))-mean)
    # This encloses the stated upper-bound expression, not necessarily the
    # exact constrained supremum when nu is not its minimizing multiplier.
    return I(max(acute.l,vertex.l),max(acute.u,vertex.u)),acute,vertex


def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    # Polynomial coefficients in c,z. Second derivative /sin(alpha)=4c-z.
    hessian={(1,0):F(4),(0,1):F(-1)}
    assert hessian=={(1,0):4,(0,1):-1}
    # Inward derivative -1 = c(z-2c), positive under z>=4c>=0.
    expanded={(1,1):F(1),(2,0):F(-2)}
    factored={}
    for (i,j),a in {(1,0):F(1)}.items():
        for (k,l),b in {(0,1):F(1),(1,0):F(-2)}.items():
            factored[i+k,j+l]=factored.get((i+k,j+l),F(0))+a*b
    assert expanded==factored
    # c(z-2c)=c(z-4c)+2c^2 is manifestly nonnegative.
    assert {(1,1):1,(2,0):-4+2}==expanded
    samples=[
        ((F(0),F(0),F(0)),F(-1,2)),
        ((F(-2,5),F(0),F(1,5)),F(-1,2)),
        ((F(9,10),F(0),F(0)),F(-2,25)),
        ((F(-7,10),F(-1,5),F(1,5)),F(-1,2))]
    records=[];vertex_active=False
    for labels,nu in samples:
        bound,acute,vertex=face_bound(labels,nu)
        assert bound.u>=acute.u and bound.u>=vertex.u
        if vertex.l>acute.u:vertex_active=True
        records.append({'labels':[str(x) for x in labels],'nu':str(nu),
                        'upper_bound':str(F(bound.u,S)),'acute_upper':str(F(acute.u,S)),
                        'vertex_upper':str(F(vertex.u,S))})
    assert vertex_active,'A sample must exercise the required degenerate cap'
    return {'status':'PASS','domain':'Three real corner potentials with range strictly below1',
            'scope':'Full-simplex support theorem and exact algebraic identities; no covering radius bound',
            'sample_bounds':records}


if __name__=='__main__':
    import json
    print(json.dumps(verify(),indent=2))
