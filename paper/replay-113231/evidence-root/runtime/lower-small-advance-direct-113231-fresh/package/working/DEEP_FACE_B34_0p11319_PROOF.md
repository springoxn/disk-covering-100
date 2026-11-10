# B34 exclusion at .11319 with deep curvature labels

Set R=11319/100000. Normalize ALL centers of the hypothetical cover by
the proved norm reflection before forming its diagram. This component
treats B34 of that normalized diagram. Reflection can change the original
boundary count, so this is not an isolated claim that the original B34
label is preserved, nor an all-count radius theorem.

## 1. Independent unpenalized arc and core-size bootstrap

`verify_B34_arc_bootstrap_0p11319.py` freshly proves m100 and the global
surviving count list[31,...,38]. For B34 it excludes all-boundary q0/q1
faces using span.4568 and bounds ordinary marked incidence by4 using
the six-arc span.693. The smaller new K4 margin is checked explicitly.

Three unpenalized full-face rows cover M=U-2e<=25, M26, and M>=27.
They include the compulsory low-degree flag where required, and all
their shifted-ear coefficients are negative. Complete face and vertex
replays prove normalized center/anchor cap228.352 for arbitrary ears.
No radial, variance, or minimum-arc premise is used for this cap.

Constrained H concavity then shows that a full assigned arc at most.0482
would give area below pi by4036411118475250323/(25*10^22).
Thus every full arc exceeds.0482, and sin(half arc)/R>.2128.
The slightly larger cutoff.2129 is not used, since it would exceed what
this exact full-arc comparison proves.

The same bootstrap checks the old normalized loss budget below1.
If M<=21, the core has at least109 q0 faces and perimeter at most42R.
Its area is at leastR^2(109A-1). Euclidean isoperimetry would require
pi(109A-1)<=21^2, contradicted by the exact positive gap. Hence M>=22.

## 2. Retaining the tangential residual explicitly

At this smaller sine cutoff the previous zero-tangent guard is not
assumed. RADIAL_TANGENTIAL_REMAINDER.md bounds the already combined
node displacement score by

    P(a)=(C-rho)*max(F_K(a),0)+(R-s)*k(a),
    k(a)=2lambda*max(D_T(a)-K*s,0),
    C=sqrt(1-R^2), s=sin(a).

Reflection gives0<=Delta<=C-rho; the endpoint lens gives|t|<=R-s.
The two coordinate bounds enlarge the same combined residual functional,
not two independent area budgets. Positive-part derivative crossings
and the h=0 endpoint use the proved safe interval branches.

`verify_general_reflected_B34_0p11319.py` verifies two complete paired
supports on x>=.2128, both with zero variance charge and cone factor3.85682:

* low: lambda=.06, Q upper141819558744279137634931/(5*10^23),783 boxes;
* high: lambda=.07, Q upper293656842385045313715191/10^24,831 boxes.

Each says outer+lambda*sum(marked base length)^2<=Q. The low support is
used only for M<=25 and the high support only for M>=26; they are never
added together.

## 3. Deep witnesses and complete four-label face supports

The general core theorem forces one deep degree-at-most-five vertex
when M<=25, and the denominator-five theorem forces two weighted units
of deep positive curvature when M<=23. A deep vertex has no original
boundary-center neighbor, as proved in DEEP_CORE_CURVATURE_WITNESSES.md.

Assign four potential classes: high-degree interior, boundary, ordinary
interior, and distinguished deep low-degree. A q0 triangle cannot contain
both the distinguished and boundary classes. All16 remaining unordered
triples are checked with the range-below-one full-simplex support,
including the mandatory degenerate-vertex cap. No actual-angle acuteness
is assumed.

Nonnegative terminal BI credits are reserved independently for marked
high-degree and marked ordinary vertices. The deep class has no BI
edge. For p0,d3/4/5, both the deep and nondeep vertex types are checked;
the compulsory flag applies only to the deep type. All other p=0,...,4
and d=max(3,p+1),...,99 types are included. Each row has485 types.

The marked support is the global two-branch squared-base conjugate at
the row's own lambda. Its negative edge squares cancel the selected
radial bound. Each row also checks the joint Jensen/slab ear cap at R.

## 4. Three ranges and arbitrary ears

The exact rows cover:

* M22..23: low support, weighted deep-curvature flag2, endpoint M22;
* M24..25: low support, one deep-vertex flag, endpoint M24;
* M>=26: high support, no flag, endpoint M26.

All three M slopes and all shifted-ear coefficients are strictly
negative. Evaluation at e0 therefore bounds every e>=0 at fixed M.
No fan variance, finite graph list, or ear-count restriction is used
in this final stage.

`verify_deep_face_B34_0p11319.py` replays the independent bootstrap,
both complete reflected pairs,48 face supports,1455 vertex supports,
and all three final area bounds. The minimum strict gap is

    203266614227238135699/(5*10^23) >.0004065332284,

in the M24/25 range. The high-M gap exceeds.0010026703.
Numerical proposals are stored separately from exact acceptance.

## 5. Scope and closure

Whole-cover normalization precedes every count and case split. Slight
enlargement, normalization, an inward movement off the norm boundary,
and a generic perturbation within the strict coverage margin give the
inherited constant finite-type limiting argument. All final gaps are
strict. Other boundary counts at .11319 must be excluded separately
before announcing a universal bound.
