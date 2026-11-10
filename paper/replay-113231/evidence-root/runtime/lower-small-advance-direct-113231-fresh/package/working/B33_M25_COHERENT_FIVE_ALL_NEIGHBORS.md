# Eight-pattern extension: no bound on high neighbours is needed

This extends B33_M25_COHERENT_FIVE_REPLACEMENT.md without changing its
six-pattern sources. Use verify_B33_M25_coherent_five_all.py and
B33_M25_coherent_five_all_proposal.json for this version.

Assign the positive P label only to one selected deep degree-five site.
All its neighbours may be labelled H or O, in any pattern; any additional
low-degree sites can retain the ordinary O label in the global row. No
uniqueness of the global degree-five site and no bound on the number of
high-degree sites is required by this local theorem.

The six old adjacent-pair patterns are supplemented by
  (k;n0,n1,n2)=(4;0,2,3),(5;0,0,5).
These are the entire remaining possibilities among all32 binary five-cycles.
The exact verifier regenerates the full set and checks all eight patterns.

All20 outside signatures were already retained, including HHH. Therefore
the outside bounds, H-B credits, signed physical edge cancellation and the
no-double-counting argument are unchanged. Three new residual central face
supports are added, for16 total residual supports. Both new patterns have
larger gains than the previous minimum.

Consequently the same coherent row improvement remains rigorously valid:
  17237402312060949175547/250000000000000000000000
  > .06894960924.
The positive label occurs only at the selected center, so it cannot occur
in an outside triangle. Global radius use still requires a valid same-radius
global face/vertex row and the existence of this deep degree-five site.
The local theorem does not supply those premises.

