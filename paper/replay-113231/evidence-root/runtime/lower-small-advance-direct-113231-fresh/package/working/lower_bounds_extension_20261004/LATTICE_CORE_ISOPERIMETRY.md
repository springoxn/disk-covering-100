# Lattice isoperimetry and injectivity of the near-regular core development

This extends the flat-core development argument beyond convex ring boundaries. It is conditional on a simply connected triangulated core whose interior degrees are six and whose boundary unit development has no immediate backtracking. The critical N26/N27 type lists satisfy the latter condition; it must be checked separately for any new type list.

## 1. An elementary unit-triangle area bound

Use axial lattice coordinates (x,y), with z=x+y and unit directions (1,0),(0,1),(-1,1) and their negatives. Let a simple polygon follow P unit edges. Write its coordinate widths as wx,wy,wz and T=wx+wy+wz. Each unit step changes exactly two of x,y,z by one. Each coordinate's total variation on the closed boundary is at least twice its width. Therefore T<=P.

Translate the coordinate minima of x and y to zero. The polygon lies in the rectangle [0,wx] times [0,wy] and in a strip L<=x+y<=L+wz. Put U=wx+wy-L-wz. Its actual coordinate extrema imply 0<=L,U<=min(wx,wy): attaining the x and y minima gives L<=min(wx,wy), while attaining the maxima gives U<=min(wx,wy). Thus the strip intersection removes two right triangles of axial areas L^2/2 and U^2/2 from the rectangle. Since L+U=wx+wy-wz, its area in unit-equilateral-triangle units is

    2wxwy-L^2-U^2
      <= 2wxwy-(wx+wy-wz)^2/2
      = T^2/6-[(wx-wy)^2+(wy-wz)^2+(wz-wx)^2]/3
      <= P^2/6.

The polygon's area cannot exceed the area of its containing strip intersection. This proves the lattice bound without invoking an anisotropic isoperimetric theorem.

For any closed lattice walk, split at repeated vertices until it consists of simple cycles and possible two-edge backtracks. Signed areas add; backtracks have zero area. Applying the bound to each simple cycle and summing squares proves that the absolute signed area of a length-P closed walk is at most P^2/6 as well.

## 2. The N26 and N27 developments cannot overlap

Developing the abstract unit-equilateral core is consistent because every interior degree is six, as proved in FLAT_CORE_HEXAGON_REDUCTION.md. Every oriented face has unit area, so the boundary's signed shoelace area equals the number F of core triangles, even before injectivity is known.

Distinct unit triangular-lattice edges cannot cross away from lattice vertices. Thus a nonsimple developed boundary repeats a vertex. Split it there into closed walks of lengths k and P-k. With no immediate backtracking on the original cyclic boundary, both lengths are at least three. The preceding closed-walk inequality gives

    F <= [k^2+(P-k)^2]/6
      <= [3^2+(P-3)^2]/6.

For P=26 this upper bound is 269/3, strictly below F=106. For P=27 it is 195/2, strictly below F=105. Hence both developed boundaries are simple. Their orientation is positive because F>0. The orientation-preserving local development consequently has boundary winding number one, so each generic interior point has exactly one preimage. The entire core development is injective by continuity. Reflex boundary vertices cause no difficulty in this argument.

The no-backtracking premise matters: a boundary angle of zero or 2pi would create an immediate reversal. The earlier critical ring types have core angles among 2pi/3, pi and 4pi/3, so none does.

## 3. Finite containing hexagons for P26,F106

The widths are positive integers. Since 25^2/6<106 and T<=26, necessarily T=26. The sharper width-difference bound leaves, up to permutation, only

    (wx,wy,wz)=(7,9,10), (8,8,10), (8,9,9).

Permuting these three unoriented lattice coordinate axes is a triangular-lattice symmetry: swapping x,y and the transformation (x,y)->(-x,x+y) generate all such permutations. After sorting the widths, central reflection identifies offsets L and wx+wy-wz-L. The containing strip hexagon's exact triangle count is

    F_hex=2wxwy-L^2-(wx+wy-wz-L)^2.

Requiring F_hex>=106 leaves six representative strip hexagons:

- widths (7,9,10), L=2 or 3, with 106 or 108 triangles
- widths (8,8,10), L=2 or 3, with 108 or 110 triangles
- widths (8,9,9), L=3 or 4, with 110 or 112 triangles

Thus every N26 core is a simple lattice patch inside one of these six regions and differs from it by at most six unit triangles. Its true widths must still equal those of the region, and its final boundary length, manifold condition and prescribed vertex types must be checked. This is a finite reduction, not yet an enumeration of all deletions or marked-fringe assignments.

The integer checker `check_lattice_width_cases.py` independently verifies the constants, the complete width/offset enumeration and the six representatives. It does not replace the geometric proof of development or the future deletion enumeration.
