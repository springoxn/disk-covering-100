# A norm-normalized small-arc radial correction

This strengthens the audited soft correction. It does not change any
earlier frozen checkpoint or establish a radius exclusion on its own.

## 1. Reflection preserves the covered subset of the target disk

Let0<R<1 and C=sqrt(1-R^2). If a radius-R disk has center c with
d=|c|>C, replace its center by c'=C^2*c/d^2. Put k=C^2/d^2<1. Direct
expansion gives the exact identity

    |x-c'|^2-R^2
      =k*(|x-c|^2-R^2)+(1-k)*(|x|^2-1).

For every x in the closed unit disk covered by the old disk, both terms
on the right are nonpositive. The new disk therefore covers every such
point and has center norm C^2/d<C. Strict coverage is also preserved,
because k>0. This works even when the old center was outside the target
disk; no prior projection is required. Applying the replacement disk by
disk gives a cover whose centers all have norm at most C.

The subsequent Voronoi topology and assigned arcs must be recomputed for
that cover. One must not retain the original cover's topology after this
replacement. The same-radius geometric and count lemmas apply anew.

For genericity, first enlarge a hypothetical cover slightly. It then has
strict coverage; reflection preserves it. Compactness of the target gives
a uniform strict margin. Move any centers on the norm boundary slightly
inward and perturb generically within that margin. Taking enlarged radii
down to R yields the closed bound |c|<=C. This justifies both generic
reduction and endpoint closure without assuming a same-radius arbitrary
perturbation preserves coverage.

## 2. The improved radial displacement cap

For an assigned half-arc a, use s=sin a, c_a=cos a,
h=sqrt(R^2-s^2), rho=c_a-h. Since s<=R, c_a>=C. If the actual center is
rho*u+Delta*u+t*v, the norm bound implies

    0<=Delta<=C-rho=C-c_a+h<=h.

The lower bound is the original endpoint-lens inequality. Thus the old
safe cap2h can be replaced by D=C-rho, approximately halving the small-arc
correction. An exact stable identity avoids subtracting nearly equal
radicals:

    C^2-rho^2=2h*rho,
    D=2h*rho/(C+rho)>=0.

The lens-cone quadratic bound and all neighbor/tangential guards are
otherwise unchanged. If their remaining radial residual is at most
F_K(a), the node contribution is at most

    P_ref(a)=D*max(F_K(a),0).

This is the same combined displacement support as before, using the
stronger norm cap. It must be included once per node in the pair bound,
not added to a second independent area or variance deduction.

## 3. Exact derivative handling

For h>0, rho'=s*rho/h and D'=-rho'. On the positive residual branch,

    P_ref'=-rho'*F_K+D*F_K'.

On the negative branch it is zero. A crossing of F_K=0 uses the hull of
both branches, and boxes touching h=0 retain the natural value enclosure.
These are the same nonsmooth/end-point safeguards as the original soft
correction. The implementation uses the stable positive radical formula
for D and inherits the audited mean-value pair enclosure.

reflected_radial_stability_backend.py implements the local support. A
separate exact arc-domain bootstrap, pair certificate and full star/face
accounting are required at each radius. No original-center configuration
is claimed to be radial or symmetric.
