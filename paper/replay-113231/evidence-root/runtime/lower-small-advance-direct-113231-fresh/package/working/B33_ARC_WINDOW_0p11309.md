# Necessary positive arc window at radius .11309

In the B33 branch at R=11309/100000, every complete assigned boundary arc
has angle strictly greater than1787/20000=.08935. Thus every half-arc is
strictly greater than1787/40000=.044675. This excludes zero/tiny-arc examples
from the necessary domain of a potential covering, without assuming equal
gaps or an actual covering construction.

Indeed the original necessary area inequality uses center/anchor allowance
[(198-B)A+B kappa]R^2 plus sum H_R(theta_i). Concavity of H_R shows that if
one arc is at most L<2pi/B, its complete boundary sum is at most

H_R(L)+(B-1)H_R((2pi-L)/(B-1)).

The grouped upper bound increases with L below the equal allocation, by
the monotonic derivative of a concave function. At B33,L=1787/20000 the
sum of this bound and the center/anchor allowance is below pi by more than
1/500000, as exact Fraction arithmetic checks. The mean complementary arc
lies within H_R's disk-coverage domain. Therefore an arc of size<=L is
impossible. The ordinary upper endpoint theta<=2asin(R) still applies.

Run `verify_B33_arc_window_0p11309.py` for all exact non-symbolic comparisons.
This is a necessary domain lemma only, and does not close a radius lower
bound by itself.
