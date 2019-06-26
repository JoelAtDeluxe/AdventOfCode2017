

class Particle(object):
    def __init__(self, position, velocity, acceleration):
        self.px = position[0]
        self.vx = velocity[0]
        self.ax = acceleration[0]

        self.py = position[1]
        self.vy = velocity[1]
        self.ay = acceleration[1]

        self.pz = position[2]
        self.vz = velocity[2]
        self.az = acceleration[2]
    
    def __repr__(self):
        p = f'<{",".join([str(v) for v in self.get_position_tuple()])}>'
        v = f'<{",".join([str(v) for v in self.get_velocity_tuple()])}>'
        a = f'<{",".join([str(v) for v in self.get_acceleration_tuple()])}>'
        return f'p={p}, v={v}, a={a}'
    
    def _clone(self):
        p = Particle(
            [self.px, self.py, self.pz],
            [self.vx, self.vy, self.vz],
            [self.ax, self.ay, self.az]
        )
        return p

    def dist_from_origin(self):
        return sum([abs(v) for v in (self.px, self.py, self.pz)])

    def tick(self):
        self.vx += self.ax
        self.vy += self.ay
        self.vz += self.az

        self.px += self.vx
        self.py += self.vy
        self.pz += self.vz

    def mock_tick(self):
        p = self._clone()
        p.tick()
        return p

    def is_repelling(self):
        """ returns true if each axis is monotonically increasing or decreasing (combination of v & a), and is 
        increasing or decreasing (repectively) away from the axis-origin (p)
        """
        return all([
            Particle._all_negative_or_positive(self.px, self.vx, self.ax),
            Particle._all_negative_or_positive(self.py, self.vy, self.ay),
            Particle._all_negative_or_positive(self.pz, self.vz, self.az),
        ])
    
    def get_position_tuple(self):
        return self.px, self.py, self.pz
    
    def get_velocity_tuple(self):
        return self.vx, self.vy, self.vz

    def get_acceleration_tuple(self):
        return self.ax, self.ay, self.az
    
    @staticmethod
    def _all_negative_or_positive(a, b, c):
        if a >= 0 and b >= 0 and c >= 0:
            return True  # all positive
        if a <= 0 and b <= 0 and c <= 0:
            return True  # all negative
        return False

class ParticleWithName(Particle):
    def __init__(self, name, particle):
        self.name = name
        super().__init__(particle.get_position_tuple(), 
                         particle.get_velocity_tuple(), 
                         particle.get_acceleration_tuple())

    def __repr__(self):
        t = super().__repr__()
        return f'[name={self.name} {t}]'
