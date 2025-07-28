import math
from typing import Tuple


class Body:
    """A circular body affected by gravity."""

    def __init__(self, x: float, y: float, mass: float, radius: float,
                 color: Tuple[int, int, int], vx: float = 0.0, vy: float = 0.0,
                 name: str = "") -> None:
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

    def compute_gravitational_acceleration(self, others: list["Body"]) -> None:
        """Calculate and apply gravitational acceleration from other bodies."""
        G = 5000.0
        ax = 0.0
        ay = 0.0
        for other in others:
            if other is self:
                continue
            dx = other.x - self.x
            dy = other.y - self.y
            dist_sq = dx * dx + dy * dy
            if dist_sq == 0.0:
                continue
            force = G * other.mass / dist_sq
            dist = math.sqrt(dist_sq)
            ax += force * dx / dist
            ay += force * dy / dist
        self.ax = ax
        self.ay = ay

    def update(self, dt: float) -> None:
        """Update position and velocity using simple Euler integration."""
        self.vx += self.ax * dt
        self.vy += self.ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.trail.append((self.x, self.y))
        if len(self.trail) > 100:
            self.trail.pop(0)


class SpaceShip(Body):
    """A player‑controlled spacecraft with thrusters and orientation."""

    def __init__(self, x: float, y: float, mass: float, radius: float,
                 color: Tuple[int, int, int], vx: float = 0.0, vy: float = 0.0,
                 name: str = "", thrust_power: float = 200.0, fuel: float = 1000.0) -> None:
        super().__init__(x, y, mass, radius, color, vx, vy, name)
        self.angle = -math.pi / 2
        self.thrust_power = thrust_power
        self.fuel = fuel
        self.thrusting_forward = False
        self.thrusting_backward = False
        self.strafe_left = False
        self.strafe_right = False
        self.strafe_up = False
        self.strafe_down = False

    def rotate(self, direction: float, dt: float) -> None:
        """Rotate the spacecraft."""
        rotation_speed = 2.0 * math.pi
        self.angle += rotation_speed * direction * dt

    def apply_thruster(self, dt: float) -> None:
        """Apply thrust in the current orientation."""
        if self.fuel <= 0:
            return
        thrust_dir = 0
        if self.thrusting_forward:
            thrust_dir += 1
        if self.thrusting_backward:
            thrust_dir -= 1
        if thrust_dir == 0:
            return
        accel = (self.thrust_power / self.mass) * thrust_dir
        ax_thruster = accel * math.cos(self.angle)
        ay_thruster = accel * math.sin(self.angle)
        self.vx += ax_thruster * dt
        self.vy += ay_thruster * dt
        self.fuel = max(0.0, self.fuel - abs(accel) * dt)

    def apply_directional_thrust(self, dx: float, dy: float, dt: float) -> None:
        """Apply screen-aligned thrust based on arrow keys."""
        if self.fuel <= 0 or (dx == 0 and dy == 0):
            return
        accel = self.thrust_power / self.mass
        self.vx += accel * dx * dt
        self.vy += accel * dy * dt
        self.fuel = max(0.0, self.fuel - abs(accel) * dt * (abs(dx) + abs(dy)) / 2)

    def update(self, dt: float) -> None:
        """Update spaceship including thrust and gravity."""
        dx = (-1 if self.strafe_left else 0) + (1 if self.strafe_right else 0)
        dy = (-1 if self.strafe_up else 0) + (1 if self.strafe_down else 0)
        self.apply_directional_thrust(dx, dy, dt)
        self.apply_thruster(dt)
        super().update(dt)


def distance(b1: Body, b2: Body) -> float:
    """Compute Euclidean distance between two bodies."""
    dx = b1.x - b2.x
    dy = b1.y - b2.y
    return math.hypot(dx, dy)


def check_collision(b1: Body, b2: Body) -> bool:
    """Return True if two bodies intersect."""
    return distance(b1, b2) <= (b1.radius + b2.radius)
