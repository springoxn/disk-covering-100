# Complete normalized B33 exclusion at R=.11322

The complete entry is verify_B33_hinge_metric_complete_0p11322.py. Every
component executes in a fresh Python subprocess with assertions enabled.
This theorem concerns the B33 branch of a cover normalized before its
boundary-cell count is chosen. Other B values remain separate branches.

1. HINGE_B33_LOWM_0p11322_PROOF.md and its checker exclude every M<=25,
   retaining arbitrary ears and bad faces. They recheck m100, the global
   degree window5..8, M>=22, and the needed deep-curvature witnesses.
2. B33_HIGHM_MINIMUM_DEGREE6_0p11322.md forces all interior degrees>=6
   and excludes bad q1 for M>=26. No qmax footprint premise is assumed.
3. JOINT_EAR_APEX_HINGE_0p11322.md pays ears and ordinary apices from one
   correctly halved endpoint-owner budget. It removes the sole one-ear
   Euler profile. Only M26/one7 and M27/all6 remain.
4. N26_SEVEN_FACE_METRIC_0p11322.md excludes M26 using one simple chordless
   P26/F106 core and seven exact signed-edge triangle supports.
5. N27_METRIC_CHORD_CASES_0p11322.md excludes M27 using one P27/F105 core
   with at most two chords and seven exact signed-edge supports.

The two metric inequalities cancel signed shared-edge lengths exactly,
use consistent corner potentials, include every full-simplex boundary cap,
and do not spend a second hinge budget. They use only the unconditional
linear-halfside normalized boundary envelope k=11/25. Neither a finite
lattice catalog nor a conditional quadratic radial bootstrap is needed.

All numerical coefficients used in acceptance are rational. Floating-point
optimizers supplied proposals only. The small scalar interval certificates
and the generic signed-sine support backend are replayed or called exactly.
The smallest reported final-profile margin exceeds .0000324, in the ear
exclusion. The preceding minimum-degree reduced-cost margin exceeds
.000072. Strict margins support the established perturbation/limit step.

Independent review is required before incorporating this new branch into
a universal radius theorem. This file does not assert the exact optimum.
