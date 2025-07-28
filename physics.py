import math
from typing import Tuple


class Body:
    """Base class for any gravitational body."""
    def __init__(
        self,
        x: float,
        y: float,
        mass: float,
        radius: float,
        color: Tuple[int, int, int],
        vx: float = 0.0,
        vy: float = 0.0,
        name: str = "",
    ) -> None:
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius
        self.color = color
        self.vx = vx
        self.vy = vy
        self.name = name
        self.ax = 0.0
        self.ay = 0.0
        self.trail = []

    def compute_gravitational_acceleration(self, others: list) -> None:
        """Compute and store the net gravitational acceleration from other bodies."""
        G = 2000  # gravitational constant (tunable)
        self.ax = 0.0
        self.ay = 0.0
        for other in others:
            if other is self or other.mass == 0:
                continue
            dx = other.x - self.x
            dy = other.y - self.y
            dist_sq = dx * dx + dy * dy
            if dist_sq == 0:
                continue  # avoid division by zero
            force = G * other.mass / dist_sq
            dist = math.sqrt(dist_sq)
            self.ax += force * dx / dist
            self.ay += force * dy / dist

    def update(self, dt: float) -> None:
        """Update position and velocity using current acceleration."""
        self.vx += self.ax * dt
        self.vy += self.ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.trail.append((self.x, self.y))
        if len(self.trail) > 100:
            self.trail.pop(0)
