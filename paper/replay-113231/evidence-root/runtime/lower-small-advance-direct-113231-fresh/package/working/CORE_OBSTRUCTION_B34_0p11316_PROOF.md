# B34 at .11316 by an induced-core obstruction

`verify_core_obstruction_B34_0p11316.py` excludes the B34 branch at the exact radius R=2829/25000=.11316. It does not establish a universal .11316 lower bound or the exact optimum.

Its minimum exact area margin is

`1510229773586609225176079071773/50000000000000000000000000000000000`,

approximately .00003020459547. The remaining three branch margins exceed .0012.

## 1. Dependencies and fresh geometry

The unchanged `.11315` mixed-face/fan verifier is replayed first. Its complete triangle supports, marked supports and vertex reduced costs are dimensionless and do not depend on the covering radius. They remain the same exact rational inequalities here.

Every radius-dependent item is then recomputed at R: the old count criterion excludes at most 99 effective centers; K4 at span .4566 excludes all-boundary q0/q1 faces; K6 at span .693 gives q<=4 and five-neighbor windows; the individual-arc/endpoint-union argument gives at most five q4 fans; the complete `.29` boundary-variance support and the sharper Jensen-slab ear cap pass again.

The actual count is therefore m=100. This is essential to the core obstruction below; the proof does not silently replace a smaller actual count by 100 in a topological equality.

All radius-dependent fan-budget constants are recomputed by taking the maximum over the same 52 exact integer fan-count inequalities. The preceding radius's positive area margins are not used as a larger-radius conclusion.

## 2. A small core forces an unmarked low-degree vertex

Write e for the ear count and U for q0 boundary-angle occurrences. Define the integer M=U-2e. The combinatorial theorem is `UNMARKED_LOW_DEGREE_CORE_OBSTRUCTION.md`, using blockwise `GENERAL_DISK_ISOPERIMETRY.md` and the induced-core frontier identities.

For clarity, under the no-all-boundary-q0/q1 hypothesis already established here, let n2 count q0 faces with two boundary vertices. Deleting all boundary vertices leaves only filled triangular core blocks, together with possible bridges and isolated vertices. Its total exterior walk length is

`b=U-2n2<=M`,

because n2>=e. Its core triangle count satisfies

`F_core>=130-M`.

A vertex strictly inside a face-bearing core block has no original boundary neighbor, is an unmarked p=0 vertex, and retains its entire original degree. If all p=0 vertices had degree at least six, every core block would satisfy `F<=b_block^2/6`. Summing over blocks gives

`130-M<=F_core<=b^2/6<=M^2/6`.

For every M<=25 this is impossible: at M=25 the integer comparison is `6*(130-25)-25^2=5>0`, and smaller M are worse. Therefore M<=25 forces at least one unmarked interior vertex of degree 3,4 or5.

No global minimum-degree-six assertion is made. Marked low-degree vertices may remain. Boundary chords, disconnected cores, articulation points and bridges do not invalidate the blockwise argument. The accompanying exact integer checker is replayed.

## 3. Use the compulsory vertex's existing reduced cost

In each of the inherited three-label rows, an unmarked vertex of degree d<=5 has label zero and exact score d*p0. Its vertex dual allowance is `u0+eta*(d-6)`. Thus the minimum slack over d=3,4,5 is

`sigma=min_d[u0+eta*(d-6)-d*p0]>0`.

The three exact sigma values are approximately .11690758, .13170560 and .14593601. When M<=25 the compulsory low-degree vertex allows sigma to be subtracted once from that row's normalized global upper bound.

This is a reduced-cost deduction inside the same nonnegative local-slack decomposition. It does not subtract an unrelated second area deficit from the same triangle.

## 4. Shift the ear accounting to M

For a fixed rational row, let c be the coefficient of U in its total normalized correction G(U), and E its per-ear coefficient. Since U=M+2e,

`G(U)+eE=G(M)+e(E+2c)`.

The new-radius verifier proves E+2c<0 for every row. Consequently arbitrary allowed ear counts can be discarded conservatively after this change of variable.

There are four exhaustive integer-M branches:

- M<=23: use the row with positive c, evaluated at23, and subtract its sigma
- M=24: use the middle row and subtract its sigma
- M=25: use the last row and subtract its sigma
- M>=26: use the last row's negative c, evaluated at26, without any compulsory-vertex deduction

The refreshed fan budget and boundary support are included in each case. All four exact final areas are strictly below pi. The last branch is the weakest and gives the margin stated above.

## Scope and limiting configurations

Run the checker in a fresh Python process with assertions enabled. It imports no numerical optimizer. Its proof dependencies are the unchanged mixed-face/fan certificate, the combinatorial core-block theorem and the exact new-radius comparisons recorded in its output.

The positive-margin fixed-finite-type limiting argument includes degenerate configurations. The result closes B34 at .11316; other boundary counts and a matching exact optimum remain separate obligations.
