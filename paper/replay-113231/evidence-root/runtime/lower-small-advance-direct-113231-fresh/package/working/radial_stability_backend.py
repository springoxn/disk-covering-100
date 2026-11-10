"""Instance-based exact radial/stability support for future covering proofs.

No completed checkpoint constants are changed by importing this module.
"""
from fractions import Fraction as F
import time
from verify_star_lp_duals import I, q, S, PI
from verify_potential_star_duals import sine
from verify_radial_boundary_support_0p11309 import arcsine, absolute


class RadialStability:
    def __init__(self, radius, penalty, sine_lower, slope, intercept, stability, B=33):
        self.radius = F(radius)
        self.penalty = F(penalty)
        self.sine_lower = F(sine_lower)
        self.slope = F(slope)
        self.intercept = F(intercept)
        self.stability = F(stability)
        self.B = B
        assert 0 < self.radius < F(1, 2)
        assert self.penalty >= 0 and self.stability >= 0
        self.R = q(self.radius)
        self.LAM = q(self.penalty)
        self.MU = q(self.slope)
        self.TARGET = q(self.intercept)
        self.GAMMA = q(self.stability)
        self.XLOW = q(self.sine_lower).l
        self.CENTER = PI / B

    def site(self, raw):
        x = I(*raw)
        s = self.R * x
        c = (1 - s.sq()).sqrt()
        h = self.R * (1 - x.sq()).sqrt()
        return s, c, h, c - h

    def node_guard(self, half_arc_lower):
        x = I(self.XLOW)
        assert x.l > q(F(1, 3)).u
        assert sine(q(F(half_arc_lower))).l > (self.R * x).u
        wr = 4 * self.LAM * (1 + self.R * (1 - x.sq()).sqrt()
              - (1 - self.R) * (1 - 2 * self.R.sq())) - self.R * x
        assert wr.u < 0
        return {'status': 'PASS', 'radial_normal_margin': str(F(-wr.u, S)),
                'half_arc_lower': str(F(half_arc_lower))}

    def natural_upper(self, box):
        sa, ca, ha, pa = self.site(box[0:2])
        sb, cb, hb, pb = self.site(box[2:4])
        a, b = arcsine(sa), arcsine(sb)
        edge = (pa-pb).sq() + 2*pa*pb*(sa+sb).sq()/(1+ca*cb+sa*sb)
        score = (a-sa*pa+b-sb*pb)/2 + self.LAM*edge - self.MU*(a+b)
        score += self.GAMMA*((a-self.CENTER).sq()+(b-self.CENTER).sq())/2
        return score.u

    def upper(self, box):
        natural = self.natural_upper(box)
        if natural <= self.TARGET.l:
            return natural
        sa, ca, ha, pa = self.site(box[0:2])
        sb, cb, hb, pb = self.site(box[2:4])
        if min(ha.l, hb.l) <= 0:
            return natural
        a, b = arcsine(sa), arcsine(sb)
        cosine_sum = ca*cb-sa*sb
        sine_sum = sa*cb+ca*sb
        pa_prime, pb_prime = sa*pa/ha, sb*pb/hb
        da = (1-ca*pa-sa*pa_prime)/2
        da += 2*self.LAM*(pa_prime*(pa-pb*cosine_sum)+pa*pb*sine_sum)
        da += self.GAMMA*(a-self.CENTER)-self.MU
        db = (1-cb*pb-sb*pb_prime)/2
        db += 2*self.LAM*(pb_prime*(pb-pa*cosine_sum)+pa*pb*sine_sum)
        db += self.GAMMA*(b-self.CENTER)-self.MU
        dx, dy = da*self.R/ca, db*self.R/cb
        mx, my = (box[0]+box[1])//2, (box[2]+box[3])//2
        point = I(self.natural_upper((mx,mx,my,my)))
        rx = q(F(max(mx-box[0],box[1]-mx),S))
        ry = q(F(max(my-box[2],box[3]-my),S))
        mean_value = point+absolute(dx)*rx+absolute(dy)*ry
        return min(natural, mean_value.u)

    def exhaustive_pair(self, seconds=7200):
        todo = [(self.XLOW,S,self.XLOW,S)]
        visited = accepted = skipped = 0
        largest = None
        start = time.time()
        while todo:
            box = todo.pop()
            visited += 1
            if box[0] > box[3]:
                skipped += 1
                continue
            value = self.upper(box)
            if value <= self.TARGET.l:
                accepted += 1
                largest = value if largest is None else max(largest,value)
                continue
            axis = 0 if box[1]-box[0] >= box[3]-box[2] else 2
            mid = (box[axis]+box[axis+1])//2
            assert box[axis] < mid < box[axis+1], ('unresolved box',box)
            left, right = list(box), list(box)
            left[axis+1], right[axis] = mid, mid
            todo.extend([tuple(left),tuple(right)])
            if time.time()-start > seconds:
                return {'status':'PENDING','visited':visited,'pending':len(todo)}
        return {'status':'PASS','visited':visited,'accepted':accepted,
                'symmetry_skips':skipped,'largest_accepted_upper':str(F(largest,S)),
                'seconds_reporting_only':time.time()-start}
