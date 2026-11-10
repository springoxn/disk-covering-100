# Conditional stronger boundary weights, B33 q3-corner profile

Assume the separately verified high-M arc bootstrap gives sin(t_i)/R>.6
at R=.11321, and the q3-profile proof's boundary-Q inequality is valid in
the same diagram. Its remaining degree-six and degree-seven marked
apices have tilted penalty multipliers .40712065 and .05359415, with
squared-base penalty lambda=.14. Every individual marked conjugate gap
is one nonnegative term in the profile's total-slack decomposition.

For L=2Rx, x<=.45, fixed-base convexity in the apex angle bounds its score
by the larger of

    x(1+2sqrt(1-x^2))-4lambda*x^2+s*asin x,
    x-4lambda*x^2+s*(pi-asin x).

For both multipliers the checker proves these branches increase on
[0,.45]. Their endpoint upper bounds are below the exact conjugates by
more than the entire profile surplus. The short-edge contradiction
margins exceed .00428779 and .00369406. Hence L>.9R for every marked edge.

Each radial lens tip has norm at least1-R. Adjacent midpoint directions
differ by t_i+t_(i+1), so the actual half-sine premise gives reference
edge length>1.2(1-R)R>1.06R. The already proved consistent angle lifts
and principal-angle inequality imply

    |e_i| <= [13/(8R)](d_i+d_(i+1)),

since pi^2<4*.9*1.06*(13/8)^2. Summation by parts for the boundary weights
w_i gives an angular-error cost at most
2*(13/8)*max|w_(i+1)-w_i|*R*sum d_i. At maximum difference .11 this is
.3575R*sum d_i, strictly less than the genuine outer displacement loss
R*sum[(sin(t_i)/R)^2*d_i]>.36R*sum d_i. Thus .11 is admissible; the
constructor's smaller .079 choice is contained.

The actual-edge guard remains .9R, so the unequal-base square-completion
charge remains25/16. Scalar arc supports must use their corresponding
actual half-arc domain. The reference-lens angle reduction spends the
outer displacement loss once; earlier radial inequalities are independent
bootstrap proofs of the domain, not extra losses added to this functional.

The checker is a conditional geometry theorem. It does not by itself
prove the required Q inequality, the initial arc bootstrap, graph
completeness, or the final graph metric exclusions.
