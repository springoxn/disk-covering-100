# One ordinary three-marked apex forces an arc-variance loss

Assume the inherited simple straight covering triangulation at B33, with
circumradii at most R=.11321 and distinct ordinary q1 marked boundary faces.
If one interior vertex p is the apex of three such faces, then

    V=sum_i(a_i-pi/33)^2
       >=(33/116)*(4pi/33-L/2)^2,

where a_i are the33 assigned half-arcs and L=.6931. The exact scalar
comparison sin(L/2)>3R verifies L>2asin(3R). The right side is approximately
.0003337. This is a single whole-boundary variance charge, not a separate
charge for each overlapping fan.

## Four distinct boundary sites are available

The three ordinary faces have three distinct marked boundary edges. The
boundary edges form a simple33-cycle. Three distinct edges in that cycle
cannot have only three distinct endpoint vertices: that would be a closed
triangle cycle inside the33-cycle. Thus p has at least four distinct boundary
neighbors. Choose any four. They need not be consecutive for this argument;
the stronger neighbor-window hypotheses used elsewhere are not needed here.

## A common radius-3R footprint contains their complete arcs

Every chosen boundary center c_i is joined to p by a center edge, hence
|p-c_i|<=2R because its incident center face has circumradius at most R.
Every point of its assigned boundary arc is within R of c_i. All four
complete assigned arcs therefore lie in the disk of radius3R centered at p.
Since3R<1, such a disk intersects the unit circle in an arc of angular length
at most2asin(3R). For center distance d>0, this follows by minimizing
(1+d^2-(3R)^2)/(2d), whose minimum is sqrt(1-(3R)^2); the d=0 case is empty.

The assigned arcs have disjoint interiors, so their total angular length
is at most L. Consequently the sum of their four half-arcs is at most L/2.

## Exact weighted Cauchy step

The mean half-arc is mu=pi/33. Let D=4mu-L/2>0. The four selected deviations
sum to at most-D, and the other29 deviations sum to at least D. Cauchy gives

    V>=D^2/4+D^2/29=(33/116)*D^2.

If other q3 vertices exist, this proof still uses only the one chosen vertex
and one four-arc group; no overlapping-group multiplicity is added.

## Combining with the new final boundary support

verify_quadratic_lens_radial_B33_variance_0p11321.py certifies the final
lambda=.14 boundary functional as Q-V, with the same tight Q upper used by
the conditional profile verifier. That profile/face upper did not spend
any final variance. Once its separately verified high-M arc domain is in
force, its unique degree-seven/q3 vertex supplies the preceding four arcs.
Comparing this one final variance loss with its remaining total-area surplus
therefore gives a valid graph-free high-M contradiction if the exact margin
is positive. Earlier independent variance-to-arc inequalities were used only
to prove the domain; they are not added to this final variance loss.

This lemma does not establish other B counts or low-M branches. Generic
enlargements and fixed-topology closed limits use the inherited endpoint
argument; rod distances, assigned arcs and the displayed inequalities are
closed and continuous.
