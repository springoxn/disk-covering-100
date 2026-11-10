# Conditional q2/q3 boundary-weight window at R=.11322

This is a same-radius geometric supplement to the R22 profile. It assumes
that the profile's complete boundary inequality with required Q=17877/50000
has been established, and that every actual full assigned arc exceeds.147.
The checker recomputes the profile. It does not establish either assumption.

The profile has66 degree-six interior sites and one degree-seven site with
marked incidence2 or3, no ears and M26. Its two marked-apex conjugate tilts
are exactly .40712065 and .05359415. The entire unexcluded area surplus is
recomputed; no earlier-radius surplus is reused.

For a short marked base L<=.9R, put x=L/(2R)<=.45. The previously proved
fixed-base convexity reduction bounds its marked score by the larger of
  x*(1+2*sqrt(1-x*x))-4*lambda*x*x+s*asin(x)
and
  x-4*lambda*x*x+s*(pi-asin(x)),
with lambda=.14. Each is increasing on[0,.45]: the acute derivative is at
least1+2h-2x*x/h-8lambda*x, and the obtuse derivative is
1-8lambda*x-s/h. These displayed lower bounds decrease as x increases,
and both are exactly positive at.45 for each allowed tilt.
The exact conjugate minus this cap, multiplied by R^2, exceeds the
profile's entire surplus for both site types. Every other retained local
dual slack is nonnegative. Thus each actual marked base is greater than.9R.

The independent full-arc premise gives half-arc>.0735 and
sin(half-arc)/R>.6485. Each inner radial reference tip has radius at least
1-R, so a reference edge exceeds2*.6485*(1-R)*R>1.15R.
The existing lifted-angle error lemma therefore permits constant13/(8R),
since pi^2<4*(.9)*(1.15)*(13/8)^2. For adjacent boundary weights differing
by at most1/8, the outer-area loss absorbs the error because
  .6485^2-2*(13/8)*(1/8)>0.
The same actual-base>.9R bound preserves the unequal-base marked support's
25/16 square charge.

These arguments support only the scalar boundary functional comparison.
They do not move the original covering or preserve its graph under a move.
They use one outer-loss budget and the same physical half-edge units as the
existing boundary metric method. No local fan fee or final variance is added
to the new graph dual. The earlier .11321 checker is unchanged.

