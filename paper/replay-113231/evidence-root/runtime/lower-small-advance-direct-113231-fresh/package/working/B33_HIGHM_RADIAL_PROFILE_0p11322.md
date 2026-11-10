# A complete necessary high-M profile and arc domain at R=.11322

This is a necessary-condition theorem for the normalized B33 branch,
not an exclusion of its remaining profiles or an all-count radius bound.
Set R=5661/50000. Normalize every center before constructing and counting
the diagram. Assume the resulting m100/B33 diagram has M=U-2e>=26.

## 1. Independent starting domain

verify_B33_highM_unpenalized_arc_0p11322.py first invokes the same-radius
global angular bootstrap. It proves m100, the complete possible count
list B31,...,39, absence of bad q0/q1 faces, and q<=3 with all boundary
neighbors in a four-consecutive-cell window. The q<=3 deduction begins
with a paid q4 relaxation, so it is not assumed in its own proof.

Two additional unpenalized full-face rows, using 32 face and780 vertex
supports, prove center cap229.177 throughout M>=26 and arbitrary ears.
The M26 row is used only at that integer; the M>=27 row has negative
M slope. Both shifted-ear coefficients are negative. Concavity of the
unpenalized boundary H then gives every full arc>.0597 and x>.2636,
where x=sin(halfarc)/R. No radial or variance premise is used here.

## 2. Three successive unspent-variance implications

Every radial instance uses the exact reflected endpoint-lens maximum,
the sign-aware cyclic displacement-energy inequality, and its complete
same-radius node guards and exhaustive pair proof. These are the
SignAwareQuadraticRadialStability instances, not a substitution of new
constants into an unchecked geometric domain.

The first instance uses lambda=.04 and gamma=3/2 on x>=.2636. Its1255
boxes pass. The separate full-face row checks16 faces and390 vertex
types, with no fan deduction, and has negative M and shifted-ear slopes.
Its raw area excess is at most889990550547204254307/(2*10^23).
Cauchy for one short arc and the other32 proves full arc>.0825,
x>.3642, with gap52348332762766409031/10^24.

The second instance uses lambda=.08 and gamma=23/20 on x>=.3642.
Its1255 boxes pass. The next independent16/390 row gives excess at most
2048258920144808230901/10^24. It proves full arc>.1072 and x>.4731,
with gap405511414744741987/10^23.

The third instance needs only the weaker input full arc>.1065 and
x>.470, supplied by the previous result. It uses lambda=.11 and
gamma=27/20 and passes1433 boxes. Its newly rationalized16/390 row
gives excess at most8527389428064349363/(8*10^21). It proves full
arc>.134 and x>.591, with gap41182029196166026381/10^24.

Each Cauchy step uses

    sum_i(a_i-pi/33)^2 >= (33/32)*(pi/33-a_cut)^2

if some half-arc is at most a_cut<pi/33. Each stage reserves its entire
gamma coefficient for that one implication. The earlier inequality
establishes an actual domain for the next one; their area or variance
budgets are never added together.

## 3. The final Q premise is discharged

On the established full arc>.134 domain, the final instance uses
lambda=7/50 and gamma=33/20. Its1637 exact boxes prove

    Qactual <= Qupper-(33/20)*sum_i(a_i-pi/33)^2,
    Qupper=89384917857293177360127/(25*10^22)<.35754.

Here Qactual is exactly the signed outer/segment sum plus lambda times
the sum of squared actual marked-base lengths. It contains no
independent-anchor slack J-A.

Discarding, not spending, the nonnegative variance term supplies the
previously separate Q<=.35754 premise of the16-face/390-vertex profile
checker. Its exact negative M and ear coefficients and integer reduced
costs force e0,M26,66 degree-six vertices and one degree-seven vertex
whose marked incidence is two or three. All other high-M cases are
excluded at this step. No graph catalog or local actual-anchor fee is
used in this reduction.

## 4. A stronger actual arc domain for the remaining profile

The same final row has conservative raw excess at most
799847568053744389853/10^24. Keeping the still-unspent33/20 variance
term and applying the one-arc Cauchy inequality at full cutoff .147
gives positive gap692378883496257457/(5*10^23). Hence every actual
full arc exceeds147/1000, and x>1297/2000=.6485.

This is another domain implication, not a new deficit to add to a later
covering bound. A subsequently certified support on this stronger domain
may be used as a new final inequality with its variance reserved afresh.

## 5. Reproducible complete entry

verify_B33_highM_profile_arc_0p11322.py invokes the three-stage domain
chain, the final pair and the exact profile checker in fresh processes,
checks the Q comparison and profile, and proves the last arc comparison.
The nested domain stages recheck their own original-domain and local
support dependencies. Assertions must remain enabled. Actual reports
are saved as B33_highM_*_0p11322_result.json.

The remaining q2/q3 profile still needs an exclusion, for example a
separately certified regional metric support. Whole-cover genericity
and closed endpoint passage retain the same strict-margin normalization
ordering as the completed .11321 checkpoint.
