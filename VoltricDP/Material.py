class Material:
    # Friction Bounce Mass
    def __init__(self, f=0.4, b=0.4, m=1.0, d=0.01):
        #
        if f >= 0.0 and f <= 1.0:
            self.friction = f
        if b >= 0.0 and b <= 1.0:
            self.bounce = b
        if m >= 0.0:
            self.mass = m
