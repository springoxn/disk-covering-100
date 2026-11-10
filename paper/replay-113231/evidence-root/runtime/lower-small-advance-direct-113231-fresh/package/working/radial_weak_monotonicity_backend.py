"""Soft-corrected radial support with the weaker eta-neighbor guard."""
from fractions import Fraction as F
from verify_star_lp_duals import q,S
from verify_potential_star_duals import sine
from radial_corrected_stability_backend import CorrectedRadialStability

class WeakMonotonicityRadialStability(CorrectedRadialStability):
    def node_guard(self,full_arc_lower):
        x=q(self.sine_lower);C=(1-self.R.sq()).sqrt();eta_sine=x*self.p0
        margins={
            'cone_factor':self.K-4*(1-eta_sine.sq()),
            'eta_at_most_pi_over_four':1-2*eta_sine.sq(),
            'neighbor_eta_above_maximum_half_arc':eta_sine-self.R,
            'normal_monotonicity':1-4*self.LAM*self.p0*self.s0,
            'tangent_spread':self.K*self.s0-C*(self.s0*C+self.c0*self.R)+2*self.p0*self.s0*self.c0,
            'actual_arc_domain':sine(q(F(full_arc_lower))/2)-self.R*x,
        }
        assert self.factor>=2
        assert (1-self.p0*self.c0).l>0
        assert (self.R*C-self.p0*self.s0).l>=0
        assert all(z.l>0 for z in margins.values()),margins
        return {'status':'PASS','radial_residual_allowed':True,'weaker_eta_guard':True,
                'strict_margin_lower_bounds':{k:str(F(z.l,S)) for k,z in margins.items()}}
