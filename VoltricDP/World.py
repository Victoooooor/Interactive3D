from .Composite import *



class World:
    #
    size        = Vector(0.0, 0.0)  # world size/boundaries
    hsize       = Vector(0.0, 0.0)  # half-size world size/boundaries
    gravity     = Vector(0.0, 0.0)  # global gravitational acceleration
    step        = 0                 # time step
    delta       = 0.0               # delta time (1.0 / time step)
    #
    particles   = list()            # list of all particles being simulated
    constraints = list()            # list of all constraints being simulated
    composites  = list()            # list of all composite shapes being simulated

    def __init__(self, s=Vector(0.0, 0.0), g=Vector(0.0, 9.8), t=8):
        self.size      = s
        self.hsize     = 0.5 * s
        self.gravity   = g
        if t < 1:
            self.step  = 1
            self.delta = 1.0
        else:
            self.step  = t
            self.delta = 1.0 / self.step

    def Simulate(self):
        for i in range(self.step):
            for particle in self.particles:
                particle.Accelerate(self.gravity)
                particle.Simulate()
                particle.Restrain()
                particle.ResetForces()
            for constraint in self.constraints:
                constraint.Relax()

    def AddParticle(self, x, y, mat=None):
        particle = Particle(self, x, y, mat)
        self.particles.append(particle)
        return particle

    def AddConstraint(self, p1, p2, s, d=None):
        constraint = Constraint(p1, p2, s, d)
        self.constraints.append(constraint)
        return constraint

    def AddComposite(self, *params):
        composite = Composite(params)
        self.composites.append(composite)
        return composite
