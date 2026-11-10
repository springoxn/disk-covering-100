# A uniquely curved M24 core has an isolated degree-five witness

Assume a100-center diagram with B32 or33 and M=U-2e=24. Define deep
interior vertices as those with no boundary-center neighbor. Suppose
their total positive curvature sum max(6-d,0) equals1. The general
core obstruction guarantees a strict block-interior low-degree vertex,
so it is a unique deep degree-five vertex v. Every other strict interior
vertex of every face-bearing core block has degree at least6.

The conclusion is that v has no neighbor on the core boundary and no
high-degree neighbor. Its five incident q0 faces all have the corner
label pattern(P,0,0) if only v receives a distinguished label P and
ordinary degree-six interior vertices receive0. This conclusion is
about the actual combinatorial diagram, not a lattice approximation.

## 1. One simple chordless core

Let c count induced-interior components and n3 count q0 faces with three
boundary vertices. The general identities give

    b=24-4(c-1)-n3,
    Fcore=2I-2-24+2(c-1)+n3,

where I=100-B is67 or68. Hence Fcore>=108. The total positive strict-
interior curvature in the face-bearing blocks is at most1. The theorem
F<=b^2/5 therefore applies blockwise.

If c>=2, then b<=20 and Fcore>=110, contradicting Fcore<=20^2/5.
Thus c1. If n3>=1, b<=23 and Fcore>=109, contradicting23^2/5<109.
Thus n3=0, and the total frontier length is24. The exact core area is
108 for B33 or110 for B32.

Multiple face-bearing blocks would have total area at most
(3^2+21^2)/5=90. A bridge outside the sole face-bearing block would leave
that block perimeter at most22, allowing area at most22^2/5. Both bounds
are below108. Therefore the induced interior graph is one triangulated
disk with a simple boundary cycle of length24.

A boundary chord splits it into two disks with lengths summing26.
Both inherit positive-curvature budget at most1. Their total area is at
most(3^2+23^2)/5=107.6, again too small. The core is chordless.

## 2. No other strict interior vertex has degree above six

If another strict core-interior vertex had degree at least7, it would
cancel the unique5's one unit of positive curvature in the net sum.
The chordless first-peeling identity would then give exposed inner
frontier length U1<=24-6=18. The surviving face-bearing blocks retain
positive-curvature budget at most1, so

    Fcore <=24+U1+U1^2/5 <=24+18+18^2/5=106.8.

This contradicts Fcore>=108. All strict core-interior vertices except
v therefore have degree6, and the net interior curvature is exactly1.

## 3. The degree-five vertex does not touch the core boundary

Suppose v had a core-boundary neighbor. Deleting the outer boundary
would expose part of v's star, so v would lie on an exterior frontier
and would not be strictly inside any surviving face-bearing block.
Every strict vertex of those blocks would retain full degree at least6.

The first frontier now has U1=24-6+1=19. Applying the zero-positive-
curvature theorem with denominator6 to the inner blocks gives

    Fcore <=24+19+19^2/6=619/6<108,

a contradiction. Thus all five neighbors of v are strict core-interior
vertices. They have degree6 by section2. Since v is deep, it has no
original boundary-center neighbors either. Every one of its five faces
therefore has exactly one P corner and two ordinary zero corners.

This argument uses only the general induced-core identities and the
two audited disk isoperimetric theorems. It does not require ears or
bad marked faces to be absent in advance; their contributions are
already included in M and the general identities. The unique-curvature
hypothesis must be proved separately before using the special face list.
