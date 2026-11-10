# A single hinge budget pays ordinary apices and ears jointly

The boundary polygon is a simple cycle. Each boundary edge has exactly one
incident center face, so its owner is either an ordinary interior apex, a
q2 ear, or a bad q1 face. An ordinary apex owning p edges uses at least p+1
distinct endpoint cells, since p is a proper subset of the cycle. Select
any p+1 of those endpoint cells. Their assigned half-arcs have sum at most
asin(3R), because every selected boundary site is joined to the apex by an
edge of length at most2R. A q2 ear owns two consecutive edges and exactly
three endpoint cells; its circumcenter is within R of all three sites, so
those cells' half-arcs have sum at most asin(2R).

Every boundary cell belongs to at most two of these selected owner sets.
Indeed, it has only two incident cycle edges. Distinct owner memberships
require distinct incident edges. At the middle vertex of an ear both edges
have the same owner, which only decreases the membership count. Split
ordinary fans and adjacency between different ears do not change this
argument. Bad q1 owners are simply left uncharged.

Suppose the same pointwise boundary deficit satisfies

    delta(t)>=c*(T-t)_+.

Then its one global sum pays, simultaneously,

    c/2 * sum_apices ((p+1)T-asin(3R))_+
    + c/2 * e*(3T-asin(2R))_+.

The factor one half is essential. This is one joint allocation, not the
addition of two independent uses of the deficit. Each owner inequality
follows from sum(T-t_i)_+ >= (number*T-sum t_i)_+.

At R=5661/50000, B33, k=11/25, the exact normalized-lens checker verifies
c=7/200 and T=23/250 on1000 interval boxes, along with the previously
verified global nonnegative deficit. The earlier high-M face row used
only c=3/100 for ordinary apex charges. It can therefore retain all of its
ordinary charges while also using the c=7/200 ear charge from this joint
allocation. No coefficient in that row is changed.

The exact sine comparison sin(457/2000)>2R gives an ear area charge at
least133/160000. Combining it with the old paid shifted-ear coefficient
and raw M26 margin leaves the strict contradiction margin

    16207322954835285460093029103 / (5*10^32).

Thus the one-ear all-degree-six high-M profile is excluded. The complete
structural survivors of this lemma are M26/e0 with one degree7, and M27/e0
with all degrees6. This is not yet a covering-radius exclusion.

Executable: verify_B33_highM_no_ears_0p11322.py. It replays the entire
previous minimum-degree theorem and the stronger scalar hinge; no rounded
numeric acceptance is used.
