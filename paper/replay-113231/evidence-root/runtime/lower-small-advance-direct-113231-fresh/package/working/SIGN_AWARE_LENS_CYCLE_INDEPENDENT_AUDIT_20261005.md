# Independent audit of the sign-aware lens-cycle energy

2026-10-05 UTC. PASS for the stated continuous energy lemma and its scalar checker. This is a reusable geometric inequality, not an additional covering-radius exclusion.

Reviewed immutable files:

- `SIGN_AWARE_LENS_CYCLE_ENERGY.md`: SHA-256 `eaaf1bcf672256b59a58147862ec56eca98e97dd09c518c7758ea498608dc8ef`
- `sign_aware_lens_cycle_energy.py`: SHA-256 `ecc14faca3cc8bca56bd14988b96c5a746311eff001462d15ff6984abc32213e`

Fresh `python -B -S sign_aware_lens_cycle_energy.py` passed all 21 scalar cases, including the positive-part radical identities, cutoff guards and the strict rational upper K < 127742/50000 at R=11321/100000, x0=3/5. The scalar samples supplement the continuous proof; they do not replace it.

## Continuous argument independently checked

Endpoint constraints imply Delta>=0 and s*|t|<=h*Delta. Each nonzero displacement therefore has direction theta+sigma*phi, where sigma is its tangential sign and 0<=phi<=beta=acos(s/R). Choose a sign arbitrarily for a zero tangential component, consistently for that vertex; zero displacements do not matter. Unwrap consecutive radial midpoint directions so their difference is a_i+a_{i+1}.

For equal signs, the stated cutoff x0>=2R*sqrt(1-R^2) gives beta0+2asin R<=pi/2, so the neighboring dot product is nonnegative. For a negative-to-positive edge, the worst negative part is at most cA=max(0,cos(2eta0)), with eta0=asin x0-a0. For the reverse orientation it is at most cB=max(0,cos(2xi0)), with xi0=asin x0+a0. The alternate reverse endpoint a_i+a_j is less than pi/2 because R<1/2. Eta and xi are increasing in a because their derivatives are cos(a)/h-1>0 and cos(a)/h+1>0.

There is no spurious second positive-cosine branch in cB: xi0<=pi/2+asin R<2pi/3<3pi/4. If xi0>=pi/4, the reverse orientation cannot have a negative dot product and cos(2xi0)<=0; if xi0<pi/4 the displayed cap is positive and valid.

Every vertex has at most one incident negative-to-positive edge and one incident positive-to-negative edge. Applying 2d_i*d_j<=d_i^2+d_j^2 therefore proves

    sum |delta_i-delta_next|^2 <= (2+cA+cB) sum |delta_i|^2.

This remains valid on odd cycles, at cone endpoints, with arbitrary magnitudes, and with arbitrary permitted half-arcs. No simultaneous attainment of edgewise extremizers is assumed. Reflection normalization is not needed for this energy inequality itself.

The radical identities sin eta0=x0*(c0-h0) and sin xi0=x0*(c0+h0) give the implemented cA/cB. When both are positive, their sum is exactly 2(1-2x0^2)(1-2R^2*x0^2). A downstream backend must replace its older cone-factor guard explicitly before using this smaller energy constant.

## Additional analytic extension: no cutoff required when R<=1/5

The same-sign dot products are in fact nonnegative whenever eta0>=A=asin R: their adverse angular difference is at most A+pi/2-eta0. Consider the remaining case eta0<A. Since rho0=c0-h0>=1-R,

    x0*rho0=sin eta0<R,
    x0<R/(1-R)<=1/4.

Then xi0<pi/2 and sin xi0=x0*(c0+h0)<=x0*(1+R)<=3/10. Hence cA>=cB>=41/50. The negative part of every same-sign dot product is bounded by s*=sin(A-eta0)<=R<=1/5. At each vertex the incoming/outgoing sign cases yield an adverse row sum among cA+cB, cA+s*, cB+s*, or 2s*. All are at most cA+cB. The same quadratic charging thus proves K=2+cA+cB for every cutoff x0 in [0,1] when 0<R<=1/5.

This extension is analytically checked here. The reviewed scalar helper still intentionally enforces its original stronger cutoff, so it must not be described as already implementing the extension.

## Optional odd-cycle spectral refinement

Only in the same-sign-nonnegative regime, the opposite-sign edges of a 33-cycle form alternating-weight paths: at least one edge joins equal signs. Every such path embeds into the 33-vertex alternating cA/cB path, up to reversal. Its bipartite incidence block is 17 by 16. The 16 by 16 Gram matrix has diagonal cA^2+cB^2 and adjacent off-diagonal cA*cB, so its largest eigenvalue is cA^2+cB^2+2cA*cB*cos(pi/17). Thus a valid sharper energy coefficient there is

    2+sqrt(cA^2+cB^2+2cA*cB*cos(pi/17)).

This spectral extension has not been inserted in a reviewed backend or radius certificate. It is not automatically applicable in the weak-cutoff case where same-sign products can be negative.
