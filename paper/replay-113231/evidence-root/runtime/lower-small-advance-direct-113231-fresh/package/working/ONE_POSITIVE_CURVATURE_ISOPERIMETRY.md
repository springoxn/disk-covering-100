# Disk isoperimetry with at most one unit of positive interior curvature

Let a finite simple plane graph triangulate a closed topological disk
with simple boundary length b>=3 and F bounded triangular faces. Put

    K = sum over strict interior vertices max(6-degree,0).

If K<=1, then F<=b^2/5. This is sharp for a degree-five triangular cone.
The claim is purely combinatorial and does not assume a metric embedding
by equal triangles.

## Induction on the number of faces

For b<=4 there are no interior vertices. Otherwise, if every boundary
degree were at least3, the disk curvature identity would give

    6 = sum_boundary(4-degree)+sum_interior(6-degree) <= b+1 <=5,

a contradiction. A degree-two boundary vertex is an ear; remove it,
preserving every interior vertex and its degree, and repeat. At b3 an
interior vertex would again make every boundary degree at least3 and
contradict the same inequality. Therefore F=b-2 for b3 or4, and the
claimed bound holds.

If a boundary chord is present and b>=5, split into disks of lengths
b1,b2>=3, with b1+b2=b+2. Every vertex interior to a subdisk retains its
full original star, so its positive interior curvature budget remains
at most1. Induction gives

    F <= (b1^2+b2^2)/5 <= [9+(b-1)^2]/5 <= b^2/5.

The b4 chord case is already covered by the small-boundary argument.

Now suppose there is no boundary chord and an interior vertex is
present. As in GENERAL_DISK_ISOPERIMETRY.md, let U count triangles with
exactly one boundary vertex. The boundary/interior incidence and
curvature identities give

    U = b-6+sum_interior(6-degree) <= b-5.

Deleting the outer boundary removes exactly b+U faces. The induced
interior graph has only original triangular bounded faces; its total
outer facial-walk length is U, with bridges counted twice. Splitting
it at articulation vertices gives face-bearing blocks with simple
boundary lengths p_i whose sum is at most U. Every strict block interior
vertex retains its full original star. By induction on each block,

    F_core <= sum p_i^2/5 <= U^2/5.

The argument includes disconnected stripped graphs, bridges, and
isolated vertices. Since U>=0 implies b>=5,

    F <= b+U+U^2/5 <= b+(b-5)+(b-5)^2/5 = b^2/5.

This completes the induction.

## Weighted compulsory low stars in a covering core

Use the general induced-core identities of
UNMARKED_LOW_DEGREE_CORE_OBSTRUCTION.md. With I=m-B and M=U-2e,

    F_core >= 2I-2-M,     total core frontier length <= M.

Every vertex strictly inside a face-bearing core block is unmarked and
retains its full degree. If the total unmarked positive curvature

    K0 = sum_(marked incidence q=0) max(6-d,0)

were at most1, each block would obey the theorem above. Thus

    2I-2-M <= F_core <= M^2/5.

For m100 and B33 this is impossible at M<=23: at the endpoint,
5*(132-23)-23^2=16>0. Therefore K0>=2. In particular the M22 and23
branches need two units of unmarked low-degree curvature, not merely
one low-degree vertex. Degrees3,4,5 contribute3,2,1 units respectively.
No minimum-degree-five hypothesis is needed.

For a nonnegative dual flag f, certify a local allowance containing

    -f*max(6-d,0)*1_(q=0).

Its sum permits subtracting2f once in the final bound. This is the
correct weighted negative-indicator direction. The count must not be
replaced by two distinct degree-five vertices unless those additional
degree assumptions have been proved separately.
