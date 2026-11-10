# Exact pointwise boundary loss gives a stronger B34 arc cutoff

This is a conditional implication at R=.11322,B34. Its initial face/star
row must independently prove that the total raw area upper bound exceeds
pi by at most1/2500=.0004. The row uses half-side multiplier k=.5 and must
not already spend the boundary tangent deficits on a fan/count charge.
Any positive boundary-loss allowances in a prior relaxation must be
restored when computing this raw budget.

Let delta(t)=F(mu)+F'(mu)(t-mu)-F(t)-P(t), using the exact normalized lens
support at k=.5 and mu=pi/34. The global scalar proof gives
delta(t)>=.03*(t-mu)^2>=0. More importantly, direct1000-box verification
on0<=t<=.078 gives delta(t)>.000418018, without subtracting the quadratic
term. The complete cover inequality therefore gives

    sum_i delta(t_i)<=raw surplus<=.0004.

No individual t_i can be at most.078. Thus every assigned full boundary
arc is greater than.156. This uses the initial bound only to establish a
domain; a new final dual may then use the outer-area loss afresh, provided
the two scores are not added together.

Three boundary sites of a center face have their assigned arcs inside a
radius2R disk about that face's circumcenter. Such a disk cuts at most an
arc of length2asin(2R) from the unit circle. But three assigned arcs would
have total length>.468, and the exact check sin(.234)>2R rules this out.
Thus there are no all-boundary q0/q1 faces and no q2 ears.

Likewise every site adjacent to an interior apex has its assigned boundary
arc inside the radius3R disk about that apex. Five cells, including any
intervening complete cells between its extreme neighbors, would contribute
more than.78 of arc. The exact guard sin(.39)>3R excludes this. Every apex
therefore has neighbors within at most four consecutive boundary cells,
and ordinary marked incidence at most three.

The separately checked final envelope with k=.6 and variance.03 is valid
whenever t>=.065. The newly established stronger t>.078 domain supplies
that premise. No equal-arc, chordlessness or unchanged-graph assumption
is introduced by the scalar bootstrap itself. Its initial raw budget,
topological generic reduction and final face supports remain separate
requirements of a covering-radius theorem.
