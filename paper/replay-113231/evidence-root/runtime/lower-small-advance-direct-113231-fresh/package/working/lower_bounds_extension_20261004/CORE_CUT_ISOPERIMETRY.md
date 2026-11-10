# Core-cut isoperimetry and the count U>=22+2e

Assume a generic straight center triangulation has m=100, B=33, and no q0
or q1 face with three boundary vertices. Let e be its number of q2 ears.
Suppose the original sum of nonnegative normalized center-face/anchor
losses is below d<1. The following restrictions are independent of actual
angle acuteness, interior degrees, the number of marked incidences at an
apex, and any flat-core or lattice-development assumption.

There are 33-2e ordinary q1 faces and132+e q0 faces. Write F0,F1,F2 for
the numbers of q0 faces with respectively zero, one and two boundary
vertices. Thus U=F1+2F2 counts q0 boundary-angle occurrences, and

    F0=132+e-U+F2.

Call a q0 face with a boundary vertex a ring face, and call an F0 face a
core face. These are face classes, not assumptions that the ring or core
is connected or simple.

## 1. Exact cut counts

Each F1 face has one II edge opposite its boundary vertex. An F2 face has
no II edge. Every II edge has two q0 incident faces, because ordinary q1
and q2 faces have at most one interior vertex. Let a count II edges with
two ring incident faces, and h count ring/core shared edges. Double counting
the F1 II-edge incidences gives

    h=F1-2a=U-2F2-2a.                       (1)

In particular h and U have the same parity. Each cut edge contributes one
opposite boundary-angle occurrence on its ring side and one opposite
interior-angle occurrence on its core side. There are exactly h distinct
ring faces incident to cuts, since an F1 face has only one II edge. Core
faces can have zero, one, two or three cut edges; their total is h.

Let c be the number of boundary chords. Each F2 face has exactly one chord;
each ear also has exactly one chord, its unmarked side. No other face type
has a chord, so

    2c=F2+e.                                (2)

No chord can have ears on both sides: the union would have four marked
boundary edges forming the complete outer cycle, forcing B=4, contrary to
B=33. Consequently each ear has an F2 face across its chord, and these
F2 faces are distinct because each has only one chord. Therefore

    F2>=e, and F2-e is even.                 (3)

This argument does not require ears or their boundary footprints to be
separated.

## 2. Geometric area and perimeter of the actual core union

Let Omega be the union of all F0 actual center triangles. Their interiors
are disjoint in the straight triangulation. Each has normalized area at
most A=3sqrt(3)/4, and its deficit A-area/R^2 is one of the nonnegative
old face losses. The complete loss budget therefore gives

    area(Omega)>=R^2*(F0*A-d).               (4)

The exposed edges of Omega are exactly the h ring/core cuts, each of
length at most2R. Hence its total exposed perimeter P is at most2Rh.
The usual planar isoperimetric inequality holds also for disconnected
polygonal regions and regions with holes: apply it to each component,
including its whole boundary, and sum, using sum P_i^2<=P^2. Thus

    area(Omega)<=P^2/(4pi)<=R^2*h^2/pi,
    h^2>=pi*(F0*A-d).                        (5)

No convexity, connectivity, injective equilateral development, or minimum
interior curvature is assumed. Ring/ring II edges do not belong to the
core perimeter and are correctly absent from P.

## 3. The universal shifted count

Put M=U-2e and x=F2-e. By(1) and(3), x is a nonnegative even integer,

    h=M-2x-2a<=M,  F0=132-M+x>=132-M.

If M<=21, then h<=21 while F0>=111. Exact arithmetic proves

    pi*(111*A-1)>21^2,

with excess greater than8.85. This contradicts(5). Therefore

    U>=22+2e.                               (6)

In particular, the e=0,1,2 branches start at U=22,24,26 respectively.
For the currently certified B33 budgets through .11315, all d are below1.
This strengthens the earlier fan-only lower ranges without spending any
new angular or radial loss budget in a later score bound.

## 4. Near-minimal counts and the requested U24 cut

If M<=25 and x>=2, then h<=21 and F0>=109. But

    pi*(109*A-1)>21^2

by more than .69. Thus x=0: F2=e and every boundary chord is the base of
an ear. In the no-ear case there are no boundary chords at all.

The remaining integer a is restricted by(5):

- M=22: a=0 and h=22
- M=23: a=0 and h=23
- M=24: a=0 or1, hence h=24 or22
- M=25: a=0,1 or2, hence h=25,23 or21

The exact comparisons for each forbidden next value are recorded by the
checker. In particular, the constructor's no-ear U24 branch is chordless,
has F0=108 and F1=24, and its ring/core cut has exactly22 or24 edges.
If h=22, precisely two ring faces share one II edge with each other; the
other22 ring faces meet the core. If h=24, every ring face meets the core.

`check_core_cut_isoperimetry.py` proves every non-symbolic numerical
comparison using rational intervals. It is a conditional structural lemma,
not a radius exclusion by itself. Generic covers give the exact face
counts and polygonal union; the inherited finite-type limiting argument
extends the strict contradictions to degenerate covers.
