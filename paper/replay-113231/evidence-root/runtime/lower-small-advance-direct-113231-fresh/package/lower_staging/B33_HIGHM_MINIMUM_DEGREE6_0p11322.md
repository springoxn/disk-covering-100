# B33 high-M minimum-degree reduction at R=5661/50000

This is a conditional structural theorem, not a covering-radius exclusion.
Normalize the entire cover before constructing its generic irredundant clipped
Voronoi diagram, so every center has squared norm at most 1-R². Assume B=33
boundary cells and M=U-2e>=26, where U is the number of q0 boundary-angle
occurrences and e is the number of q2 ears. Bad q1 means a triangle with one
marked boundary edge whose third vertex is also a boundary site.

The exact checker first excludes m<=99 and rechecks the global interior
degree window 5..8. It uses the independently checked exact-lens hinge
allocation with k=11/25, c=3/100, T=23/250, and footprint span L=3467/5000:

    gamma(p)=c*((p+1)T-L/2)_+/(2R²).

This allocation needs only p<B and at least two interior sites. It permits
split fans and arbitrary ears and bad faces. No qmax footprint premise or
second expenditure of the boundary deficit is used.

Assign the corner potential -38035915/10^8 to degree7/8 interior sites,
-28793429/10^8 to boundary sites, and zero to degree5/6 interior sites.
All ten three-label multisets are checked with the full-simplex support,
including its degenerate-vertex cap. The q0 face allowance is A plus its
three corner charges, minus 196028847/10^10 on every high/boundary edge.
Here A=3sqrt(3)/4. Every ordinary marked apex has at least two terminal
boundary/interior incidences into q0 faces, so its high/boundary credit is
paid twice. Split fans only increase the available count.

For p marked incidences and degree d, the exact normalized score is

 p(C_k(ell+lb)-C_k(0)) - ell(6-d+p)pi/3
 +(d-p)charge(ell) - 2*tau*[p>0,ell is high] - gamma(p).

All26 types d=5..8, 0<=p<d are bounded by u0+beta*p+eta*(d-6), with
u0=200000/10^10, beta=2616668073/10^10, eta=-1834026504/10^10.
Every degree5 type has excess allowance at least458556001/2500000000.
This is a reduced cost from the same coherent face/vertex accounting, not
an independently subtracted triangle deficit.

The Euler and angle identities retain all exceptional counts:
q0=132+e; good q1=33-2e-b; sum p=33-2e-b;
sum(d-6)=27-M-e-b; U=M+2e; q0 boundary-angle sum=Gamma+(e-2)pi.
The resulting M slope, shifted ear coefficient, and bad-q1 coefficient are
all strictly negative. At M=26, the raw area margin is negative, but adding
the guaranteed slack of one degree5 vertex gives the strictly positive
margin36021926703645063869/(5*10^23). Hence no degree5 vertex exists in
any M>=26 case. The paid bad-q1 coefficient alone gives contradiction
margin417839250329472312641/10^24, so b=0 as well.

Consequently all original interior degrees are at least6. The identity
sum(d-6)=27-M-e-b leaves precisely:

* M26,e0,b0: one degree7, all other interior degrees6
* M26,e1,b0: all interior degrees6
* M27,e0,b0: all interior degrees6

No marked-incidence restriction on the degree7 vertex is concluded here.
These three profiles remain open for this checker. All statements at a
degenerate limit follow from the strict finite margins and the same
generic-perturbation limiting procedure as the baseline proof.

Executable: verify_B33_highM_minimum_degree6_0p11322.py. It embeds rational
coefficients, replays the hinge support, and uses only the standard-library
exact interval backend. Python assertions must remain enabled.
