# Auxiliary JSON serialization corrections

The inherited .11317 and .11318 standalone B33 arc-bootstrap result files
each contain eight large integers rounded during a JavaScript parse/write
round trip, confined to branches[i].M_coefficient endpoint numerator and
denominator metadata. Their original bytes remain in this package and
all earlier published archives remain unchanged.

The exact Python-generated sidecars are in metadata_corrections_20261004:
- B33_arc_bootstrap_0p11317_result_exact_python.json
- B33_arc_bootstrap_0p11318_result_exact_python.json

The new .11319 primary result was regenerated directly from Python before
publication; its earlier diagnostic bytes and correction note are also
preserved in that metadata folder. No mathematical verifier, rational
coefficient input, proved sign or radius bound was changed by this fix.
No Python acceptor reads the affected auxiliary result files. Every
authoritative integrated replay uses fresh component.verify() calls and
preserves exact Python integer tokens.

The included upper_configuration/verification_result.json already has
exact integer serialization. A separate older standalone upper report
outside these package entries had the same reporting-only issue.
