"""
physics.py
============

This module defines the core physics objects used by the game: a generic
``Body`` class representing any gravitating object and a ``SpaceShip`` class for
the player‐controlled craft.  It implements Newtonian gravity, simple
Euler integration and thrust mechanics.  Trails are stored to visualise
trajectories.

The design is intentionally straightforward so that you can read and modify
the physics easily.  Advanced users may want to replace the integration
scheme or add support for forces such as atmospheric drag.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Iterable, List, Tuple


G = 0.4  # gravitational constant scaled for the simulation


@dataclass
class Body:
    """Represents a gravitating body in two dimensions.

    Attributes
    ----------
    x, y : float
        Cartesian position of the body's centre in pixels.
    vx, vy : float
        Velocity components in pixels per second.
    mass : float
        Mass of the body; affects gravitational attraction.
    radius : float
        Visual radius of the body in pixels; also used for collision detection.
    color : Tuple[int, int, int]
        RGB colour used when drawing the body.
    name : str
        Optional name used for debugging or display.
    trail : List[Tuple[float, float]]
        List of past positions used to draw a trajectory.
    """

    x: float
    y: float
    mass: float
    radius: float
    color: Tuple[int, int, int]
    vx: float = 0.0
    vy: float = 0.0
    name: str = ""
    trail: List[Tuple[float, float]] = field(default_factory=list)

    # acceleration components are not stored in the dataclass fields because
    # they are recalculated each step based on other bodies
    ax: float = 0.0
    ay: float = 0.0

    def compute_gravitational_acceleration(self, bodies: Iterable["Body"]) -> None:
        """Compute the net gravitational acceleration from a list of other bodies.

        This method iterates over the provided bodies and accumulates the
        acceleration due to Newtonian gravity.  The gravitational constant
        ``G`` is scaled for the simulation, so positions are treated in
        pixels and masses in arbitrary units.  The result is stored in
        ``self.ax`` and ``self.ay``.

        Parameters
        ----------
        bodies : Iterable[Body]
            Other bodies in the simulation.  ``self`` will be ignored.
        """
        ax_total = 0.0
        ay_total = 0.0
        for other in bodies:
            if other is self:
                continue
            dx = other.x - self.x
            dy = other.y - self.y
            dist_sq = dx * dx + dy * dy
            # avoid division by zero; if objects overlap, ignore gravity
            if dist_sq <= 1e-6:
                continue
            # Newton's law of universal gravitation (scaled)
            # F = G * m1 * m2 / r^2  => a = F/m1 = G * m2 / r^2
            inv_dist = 1.0 / math.sqrt(dist_sq)
            force = G * other.mass * inv_dist * inv_dist  # equals G*m2 / r^2
            ax_total += force * dx * inv_dist
            ay_total += force * dy * inv_dist
        self.ax = ax_total
        self.ay = ay_total

    def update(self, dt: float) -> None:
        """Update velocity and position using Euler integration.

        Parameters
        ----------
        dt : float
            Time step in seconds.
        """
        # Update velocity
        self.vx += self.ax * dt
        self.vy += self.ay * dt
        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt
        # Append to trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > 500:
            # keep trail length manageable
            self.trail.pop(0)


class SpaceShip(Body):
    """A player‑controlled spacecraft with thrusters and orientation."""

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
        thrust_power: float = 200.0,
        fuel: float = 1000.0,
    ) -> None:
        super().__init__(x, y, mass, radius, color, vx, vy, name)
        # Angle in radians; 0 points to the right; positive angles rotate
        # counterclockwise.
        self.angle = -math.pi / 2  # pointing upwards initially
        self.thrust_power = thrust_power
        self.fuel = fuel
        # record thruster status
        self.thrusting_forward = False
        self.thrusting_backward = False

    def rotate(self, direction: float, dt: float) -> None:
        """Rotate the spacecraft.

        Parameters
        ----------
        direction : float
            Positive for counter‑clockwise rotation, negative for clockwise.
        dt : float
            Time step for which the rotation is applied.
        """
        rotation_speed = 2.0 * math.pi  # radians per second (360°/s)
        self.angle += rotation_speed * direction * dt

    def apply_thruster(self, dt: float) -> None:
        """Apply thrust in the current orientation.

        Forward thrust accelerates in the direction the ship is facing; backward
        thrust accelerates in the opposite direction.  Fuel is consumed when
        thrust is applied.  If fuel runs out, no acceleration is added.

        Parameters
        ----------
        dt : float
            Duration for which the thrust is applied.
        """
        if self.fuel <= 0:
            return
        # Determine direction of acceleration; forward = +1, backward = -1
        thrust_dir = 0
        if self.thrusting_forward:
            thrust_dir += 1
        if self.thrusting_backward:
            thrust_dir -= 1
        if thrust_dir == 0:
            return
        # acceleration magnitude = thrust_power / mass
        accel = (self.thrust_power / self.mass) * thrust_dir
        ax_thruster = accel * math.cos(self.angle)
        ay_thruster = accel * math.sin(self.angle)
        # apply to velocity
        self.vx += ax_thruster * dt
        self.vy += ay_thruster * dt
        # consume fuel proportional to time and acceleration
        self.fuel = max(0.0, self.fuel - abs(accel) * dt)

    def update(self, dt: float) -> None:
        """Update spaceship including thrust and gravity."""
        # apply thrust first so that gravitational acceleration also affects
        # velocity this frame
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