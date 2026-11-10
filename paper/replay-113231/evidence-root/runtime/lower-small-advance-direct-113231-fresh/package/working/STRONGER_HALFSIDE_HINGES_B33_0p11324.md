# Further scalar tradeoffs at R=.11324

These two exact normalized boundary supports use the same geometry,
interval enclosure and accounting as HIGHER_HALFSIDE_HINGES_B33_0p11324.md.
They are separate alternatives, not extra losses to add to its boundary
functional. They establish no center-face or universal radius exclusion.

| k | T | c | Exact minimum hinge margin |
|---:|---:|---:|---:|
| 13/25=.52 | 187/2000=.0935 | 7/400=.0175 | 1702194556662030629/(5*10^23) |
| 27/50=.54 | 47/500=.094 | 129/10000=.0129 | 121410954603402859/(25*10^22) |

Each proves global delta>=0 and delta>=c*(T-t)_+ with no variance spent,
using1000 whole-envelope boxes and1000 hinge boxes at the same radius
R=2831/25000 and B=33. Whole-cover normalization remains required.

Executable: verify_stronger_halfside_hinges_B33_0p11324.py. The complete
dual must select one coherent half-side multiplier, its own marked
conjugate, and its own ownership charge. Recompute radius-dependent
footprint spans and all structural/count premises before application.
