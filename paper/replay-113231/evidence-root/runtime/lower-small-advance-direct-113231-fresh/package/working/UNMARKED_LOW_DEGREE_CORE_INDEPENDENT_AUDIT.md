# Independent induced-core low-degree obstruction audit

Date: 2026-10-04. Result: PASS for the final general shifted theorem and exact integer checker.

I independently reconstructed the induced-interior graph, its filled bounded faces, exterior walk length and block decomposition. Strict interior vertices of a face-bearing core block have no original boundary neighbor by planarity; they are p=0 and retain their full original degree. Thus if all p=0 vertices have degree at least six, the previously independently proved disk isoperimetry applies blockwise, even with disconnected cores, chords, articulation points, bridges and isolated vertices.

Writing I=m-B>0 and c for the induced-interior component count, Euler and incidence give Fcore=E-I+c and2E=3Fcore+n1. Combined with the full q0-tag count these yield

n2+n3=e+2(c-1),
b=n1=M-4(c-1)-n3<=M,
Fcore=2I-2-M+2(c-1)+n3>=2I-2-M,

where M=U-2e. This remains valid with all-boundary q0 or q1 faces. Since b>=0, M>=0 follows. Summing the block face bounds gives Fcore<=b^2/6. The resulting strict integer contradictions force a p0 degree3,4 or5 vertex for B32/B33/B34,M<=25 and B35 throughB38,M<=24 at m=100.

The fresh checker passes all stated integer margins. The minimum margin for B34,M25 is5. If a separate degree-five lower bound is available, the forced type is specifically(p0,d5). A downstream proof may use one positive reduced-cost slack of the forced type, but must verify that deduction in its own local-slack decomposition; this lemma alone supplies no numerical area deficit or radius exclusion.

Frozen SHA-256:
- UNMARKED_LOW_DEGREE_CORE_OBSTRUCTION.md: 79372435a76d0b935a41ce3b003d4a96d39f44b172bdccb5c2f426dc0039ae5e
- verify_unmarked_low_degree_core_obstruction.py: ea4639cd3bb6955d4df1a12b473a65053200e335c899c844d104078880fa45bb
- General disk isoperimetry proof: 3dd646f173e5b840370d725260d98500d7c2e1b6b7ce87feecbfaf7e8a92de38

This is a conditional combinatorial theorem under the inherited simple center-triangulation reduction. It neither assumes actual angle acuteness nor certifies a graph catalog or exact optimum.
