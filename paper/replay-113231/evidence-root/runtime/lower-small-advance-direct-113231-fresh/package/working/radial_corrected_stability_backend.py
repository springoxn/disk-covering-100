"""Exact radial-pair support with a lens-cone residual correction.

The local correction spends the same displacement loss as the simultaneous
cycle expansion. It is not an additional independent area allowance.
"""
from fractions import Fraction as F
from verify_star_lp_duals import I, q, S
from verify_potential_star_duals import positive_part, hull
from verify_radial_boundary_support_0p11309 import arcsine, absolute
from radial_stability_backend import RadialStability


class CorrectedRadialStability(RadialStability):
    def __init__(self, *args, quadratic_factor, **kwargs):
        super().__init__(*args, **kwargs)
        self.factor = F(quadratic_factor)
        self.K = q(self.factor)
        self.s0,self.c0,self.h0,self.p0 = self.site((self.XLOW,self.XLOW))

    def node_guard(self, full_arc_lower):
        from verify_potential_star_duals import sine
        x = q(self.sine_lower)
        C = (1-self.R.sq()).sqrt()
        eta_sine = x*self.p0
        margins = {
            'cone_factor':self.K-4*(1-eta_sine.sq()),
            'eta_at_most_pi_over_four':1-2*eta_sine.sq(),
            'neighbor_cosine_monotonicity':x.sq()-4*self.R.sq()*(1-self.R.sq()),
            'normal_monotonicity':1-4*self.LAM*self.p0*self.s0,
            'tangent_spread':self.K*self.s0-C*(self.s0*C+self.c0*self.R)+2*self.p0*self.s0*self.c0,
            'actual_arc_domain':sine(q(F(full_arc_lower))/2)-self.R*x,
        }
        assert self.factor >= 2
        assert (1-self.p0*self.c0).l > 0
        assert (self.R*C-self.p0*self.s0).l >= 0
        assert all(z.l > 0 for z in margins.values()),margins
        return {'status':'PASS','radial_residual_allowed':True,
                'strict_margin_lower_bounds':{k:str(F(z.l,S)) for k,z in margins.items()}}

    def correction(self, raw, derivative=False):
        s,c,h,p = self.site(raw)
        normal = 4*self.LAM*((1-self.p0*self.c0)*c+self.p0*self.s0*s)
        normal += (2*self.K-4)*self.LAM*h-s
        if not derivative:
            return 2*h*positive_part(normal)
        assert h.l > 0
        hprime = -s*c/h
        normalprime = 4*self.LAM*(-(1-self.p0*self.c0)*s+self.p0*self.s0*c)
        normalprime += (2*self.K-4)*self.LAM*hprime-c
        if normal.u <= 0:
            return q(0)
        if normal.l >= 0:
            return 2*hprime*normal+2*h*normalprime
        # At the kink, the generalized derivative is enclosed by the
        # positive-side formula and zero. The first product uses F_+.
        return hull(q(0),2*hprime*positive_part(normal)+2*h*normalprime)

    def natural_upper(self, box):
        base = I(super().natural_upper(box))
        return (base+(self.correction(box[:2])+self.correction(box[2:]))/2).u

    def upper(self, box):
        natural = self.natural_upper(box)
        if natural <= self.TARGET.l:
            return natural
        sa,ca,ha,pa = self.site(box[:2])
        sb,cb,hb,pb = self.site(box[2:])
        if min(ha.l,hb.l) <= 0:
            return natural
        a,b = arcsine(sa),arcsine(sb)
        cosine_sum,sine_sum = ca*cb-sa*sb,sa*cb+ca*sb
        pa_prime,pb_prime = sa*pa/ha,sb*pb/hb
        da = (1-ca*pa-sa*pa_prime)/2
        da += 2*self.LAM*(pa_prime*(pa-pb*cosine_sum)+pa*pb*sine_sum)
        da += self.GAMMA*(a-self.CENTER)-self.MU+self.correction(box[:2],True)/2
        db = (1-cb*pb-sb*pb_prime)/2
        db += 2*self.LAM*(pb_prime*(pb-pa*cosine_sum)+pa*pb*sine_sum)
        db += self.GAMMA*(b-self.CENTER)-self.MU+self.correction(box[2:],True)/2
        dx,dy = da*self.R/ca,db*self.R/cb
        mx,my = (box[0]+box[1])//2,(box[2]+box[3])//2
        point = I(self.natural_upper((mx,mx,my,my)))
        rx = q(F(max(mx-box[0],box[1]-mx),S))
        ry = q(F(max(my-box[2],box[3]-my),S))
        mean_value = point+absolute(dx)*rx+absolute(dy)*ry
        return min(natural,mean_value.u)
