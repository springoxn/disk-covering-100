# Independent review of the Jensen-slab actual-ear support

Date: 2026-10-04. Result: PASS for the stated continuous local theorem and fresh exact `verify_jensen_slab_ear_support.py` replay.

I independently derived the complete scalar reduction. With t=z1+z2, actual area is simultaneously at most t by the two-side area/AM-GM inequality and at most w by the boundary-annulus slab. The joint anchor-minus-linear-halfside function h_k is concave for0<=k<=1; Jensen therefore yields sqrt(2t-t^2)-k*sqrt(2t). This is a joint support and does not incorrectly assume an independently lower halfside sum equal to its balanced value.

The left branch derivative decreases and remains strictly positive at w. The right branch decreases because w>1. Thus the cusp t=w is the global maximum on[0,2]. The exact uniform derivative comparisons and radius/width identity are valid. The squared-edge variant has the same argument for0<=lambda<=1/5 and retains exactly the corresponding two penalties.

The fresh exact replay passes both uniform derivative margins, 24 linear-support instances and12 squared-support instances. The proof correctly restricts application to actual all-boundary ears; the slab cap is unavailable for a general two-marked triangle. It also correctly requires the complete downstream score to be recomputed before replacing an older cap.

Frozen SHA-256:
- JENSEN_SLAB_EAR_SUPPORT.md: a8ab214fcfda4aee12bbc7af0f23a3777cef89095df78f8dd18c2d282d2b4fd2
- verify_jensen_slab_ear_support.py: 1c8d46f5e08714519e1545199fdd6edebe7b1defec0df3b693649be0ad6c4e4b

This supplies local ear score bounds only. It does not establish a universal radius exclusion, certify a downstream loss allocation or modify any frozen checkpoint. Exact arithmetic determines acceptance; no numerical optimizer is used.
