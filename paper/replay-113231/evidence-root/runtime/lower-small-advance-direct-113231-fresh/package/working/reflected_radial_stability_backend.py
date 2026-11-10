"""Soft radial support after norm-preserving covering reflection."""
from fractions import Fraction as F
from verify_star_lp_duals import q
from verify_potential_star_duals import positive_part,hull
from radial_weak_monotonicity_backend import WeakMonotonicityRadialStability

class ReflectedRadialStability(WeakMonotonicityRadialStability):
    def node_guard(self,full_arc_lower):
        result=super().node_guard(full_arc_lower)
        result['covering_reflection_norm_required']=True
        result['radial_displacement_cap']='sqrt(1-R^2)-rho=2h*rho/(sqrt(1-R^2)+rho)'
        return result

    def correction(self,raw,derivative=False):
        s,c,h,rho=self.site(raw)
        C=(1-self.R.sq()).sqrt()
        displacement=2*h*rho/(C+rho)
        normal=4*self.LAM*((1-self.p0*self.c0)*c+self.p0*self.s0*s)
        normal+=(2*self.K-4)*self.LAM*h-s
        if not derivative:
            return displacement*positive_part(normal)
        assert h.l>0
        if normal.u<=0:return q(0)
        rho_prime=s*rho/h
        hprime=-s*c/h
        normalprime=4*self.LAM*(-(1-self.p0*self.c0)*s+self.p0*self.s0*c)
        normalprime+=(2*self.K-4)*self.LAM*hprime-c
        if normal.l>=0:
            return -rho_prime*normal+displacement*normalprime
        return hull(q(0),-rho_prime*positive_part(normal)+displacement*normalprime)
