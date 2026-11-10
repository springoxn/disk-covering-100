# No high neighbor of the deep five in B34,M24

Assume m=100,B=34,M=24, exactly one original interior degree-five vertex,
and all other original interior degrees at least six. The five is the
strict-interior witness in a face-bearing induced-core block. Ears and
bad marked faces are allowed. We prove every neighbor of the five has
degree six, so its only centered-potential face pattern is (P,0,0) when
the positive label P is placed on that witness and high vertices alone
receive the negative high label.

First, the induced-core identities with I=66 give

    b=24-4(c-1)-n3,     F=106+2(c-1)+n3.

The strict positive curvature is at most one, so blockwise F<=b^2/5.
If c>=2 then F>=108,b<=20, impossible. If n3>=1 then F>=107,b<=23,
also impossible. A bridge would leave cyclic perimeter at most22, and
two face-bearing blocks have total squared perimeter at most3^2+21^2.
Both are too small for106 faces. Thus the core is a simple P24/F106 disk.

Apply the chord-aware first peel. Two strict high-degree excess units
would give D>=1,L<=17 and F<=24+17+17^2/5=494/5<106. Thus there is at
most one strict seven and no strict degree-eight or higher vertex. If
the five touched the core boundary, all strict vertices after peeling
would have nonnegative curvature, giving
F<=24+19+19^2/6=619/6<106. Hence every neighbor of the five is strict.

Suppose now that the five has a high neighbor. It must be the sole strict
seven. The strict excess is exactly D=0. If there were a boundary chord,
the sharper first-peel bound would give at most24+17+17^2/5<106 faces.
There are therefore no chords. The first peel has exactly perimeter18
and64 faces. It is connected by the chordless frontier-walk argument in
GENERAL_FIRST_BOUNDARY_PEEL_CHORDS.md, not by an unstated assumption about
isolated or tree components. A bridge leaves cyclic perimeter at most16;
two cyclic blocks have squared perimeter at most3^2+15^2. The /5 bounds
are both below64. Thus this inner complex is one simple P18/F64 disk.

The five is still strict, since its full original star survived the first
peel. If the seven were also strict, D>=0 would give

    F_inner<=18+12+12^2/5=294/5<64.

So the seven is on the boundary of the inner disk. But if the five touched
that boundary, the next peel would remove its positive curvature from all
strict block interiors, and the /6 bound would give

    F_inner<=18+13+13^2/6=355/6<64.

This final contradiction rules out the alleged high neighbor. The argument
restricts face-label incidences and spends no additional metric deficit.
The main independent auditor checked this two-step argument before its
reconstruction after the workspace reset; the recovered chain must still
be freshly replayed before use in a new global checkpoint.
