# Coherent degree-five face-row replacement for B33 M25

This is a local replacement for the exact frozen M25 face row in
hinge_B33_lowM_0p11322_proposals.json. It has no radius parameter: all areas
are divided by the proposed squared disk radius. A global application must
first prove the following premises in its own diagram.

There is one selected deep interior vertex P of degree5. Its five neighbors
are interior, with at most three high-labelled neighbors H; all others are
ordinary-labelled O. No other positively labelled P site occurs in the
outside faces. A unique global degree5 together with the relevant Euler
profile is one sufficient way to obtain these premises.

Use exactly the original potentials and corner allowances:
  H=-.33285141, B=-.27065539, O=0, P=.30011312;
  cH=.0242021094, cB=.0138623045, cO=.00000005, cP=.0343633517.
Every H-B edge in a q0 face retains credit t=.0195349539. Its old allowance is
  U(f)=A+sum c(label)-t*(number of H-B edges), A=3sqrt(3)/4.
The checker verifies all16 original complete-face inequalities, including
the retained H-B credits, before calculating the replacement.

## The selected region and all its signatures
The five neighbors of P form one simple cycle. There are five central
triangles. The six possible cyclic adjacent-pair count patterns with at
most three H neighbors are
  (k;n0,n1,n2)=(0;5,0,0),(1;3,2,0),(2;2,2,1),
               (2;1,4,0),(3;1,2,2),(3;0,4,1).
Here nh counts central triangles whose two other corners contain h H sites.
The checker regenerates these patterns from all binary five-cycles.

Each opposite neighbor-cycle edge has one outside incident triangle. It is
q0 because both endpoints are interior. It differs from every central
triangle. An outside triangle can contain one or two selected cycle edges,
never three: the five-cycle contains no triangle. Thus if j outside faces
contain two selected edges, j=0,1,2 and the other5-2j contain one.

For one selected edge, its endpoints are H/O and its third corner is H/O/B:
all12 ordered signatures are retained, including HHH. For two selected
edges, all three corners belong to the neighbor cycle, so all8 H/O
signatures are retained. Relabelling the triangle handles every placement
of the selected edge(s). This proof does not discard H-B interface credits.

## One coherent area/perimeter decomposition
Set epsilon=3/10, tau=13/10 and kappa=epsilon*tau=39/100.
Reserve epsilon times the area of the actual five-star and give its
neighbor-cycle perimeter the negative coefficient-kappa/(2R). The audited
polygon-star theorem bounds this part by
  Pstar=support(5,epsilon,-epsilon*tau).
This is an actual shared-coordinate polygon inequality, not the sum of five
independently optimized triangles.

The remaining area coefficient in each central triangle is w=7/10.
Retain the original neighbor potentials. Replace the center potential LP
temporarily by a freely chosen rational y. The full star's central
angles sum to2pi, so their centered sum ispi/3. Consequently the exact
correction is -(y-LP)*pi/3. For pattern(k;nh), the joint central upper is
  Jcentral=Pstar-(y-LP)*pi/3
             +sum_h nh*w*FaceSupport((y,H repeated h,O repeated2-h)/w;0).
Every residual face checks range(potentials)<w, and all closed-simplex
boundary caps remain included. The rational y and angle-sum multipliers are
only proposals; exact outward interval acceptance verifies each support.

The matching outside selected sides receive+kappa*L/(2R). Their signs
cancel the actual star perimeter exactly, even if neighboring circumradii
differ. For each outside signature the full generic signed-sine support,
including all three simplex-edge caps, is compared with its SAME old U(f).
Let D1,D2 be the maximum excess for one and two selected sides. The total
outside increase is at most
  Joutside=max over j=0,1,2 of (5-2j)*D1+j*D2.
No outside face is counted twice: a face with two selected sides uses its
joint two-side support once.

The old five central allowances total
  5A+5cP+2k*cH+(10-2k)*cO.
Subtract Jcentral and Joutside. Every one of the six patterns has gain at
least
  17237402312060949175547/250000000000000000000000
  > .06894960924.

## Compatibility with the global row
The sum of the new local scores has exactly the original corner-potential
terms: the center adjustment is an exact identity, and the signed physical
edge terms cancel. All outside old allowances, including their H-B credits,
are subtracted before computing their excess. Unselected q0 face bounds
and all marked-face, boundary, hinge and vertex-dual terms remain as in the
original coherent row. Thus this number is a reduction of that row's q0
total, not an extra unweighted area defect appended after those faces have
already been spent.

Run python -B -S verify_B33_M25_coherent_five.py. It uses exact integer
intervals and rational proposal coefficients. The numerical screening script
is not an acceptance dependency. The local theorem does not by itself prove
the unique-five premises or a universal radius bound.

