"""
levels.py
==========

Contains level definitions for the orbit game.  Each level is represented by a
function that returns a tuple of ``bodies`` (list of :class:`Body`), a
:class:`SpaceShip` instance, and optionally a ``target`` body.  You can add
additional levels by defining new functions that follow this interface.

The coordinate system is measured in pixels.  The Pygame window defaults to
1200×800 pixels, with the origin at the top‑left.  The mass and radius of
objects are arbitrary but should be tuned together with the gravitational
constant ``G`` in :mod:`physics` to achieve a fun play experience.
"""

from typing import List, Tuple
from physics import Body, SpaceShip


def level_one() -> Tuple[List[Body], SpaceShip, Body]:
    """Create the first level.

    This level consists of a central star, two planets and a target zone near
    the bottom of the screen.  The spaceship starts near the top of the
    screen pointing upward.  The goal is to navigate into the target zone
    without colliding with any planetary bodies.

    Returns
    -------
    bodies : list of Body
        The list of gravitational bodies (excluding the spaceship).
    ship : SpaceShip
        The player‑controlled spacecraft.
    target : Body
        A special body representing the target zone; collision with this
        signifies success.
    """
    bodies: List[Body] = []
    # Central star: very massive, attracts everything strongly
    star = Body(
        x=600.0,
        y=400.0,
        mass=5e5,
        radius=25.0,
        color=(255, 215, 0),  # golden yellow
        name="Star",
    )
    bodies.append(star)
    # Planet 1: smaller mass on the left
    planet1 = Body(
        x=300.0,
        y=300.0,
        mass=2e4,
        radius=15.0,
        color=(0, 191, 255),  # deep sky blue
        vx=0.0,
        vy=80.0,
        name="Planet A",
    )
    bodies.append(planet1)
    # Planet 2: slightly heavier on the right
    planet2 = Body(
        x=900.0,
        y=500.0,
        mass=3e4,
        radius=18.0,
        color=(34, 139, 34),  # forest green
        vx=0.0,
        vy=-60.0,
        name="Planet B",
    )
    bodies.append(planet2)
    # Define the target zone as a stationary invisible body; colour used in drawing
    target = Body(
        x=600.0,
        y=750.0,
        mass=0.0,  # mass zero so it exerts no gravity
        radius=40.0,
        color=(255, 255, 255),
        name="Target",
    )
    # Spaceship starting position
    ship = SpaceShip(
        x=600.0,
        y=100.0,
        mass=50.0,
        radius=10.0,
        color=(255, 99, 71),  # tomato red
        vx=0.0,
        vy=0.0,
        name="Ship",
        thrust_power=350.0,
        fuel=1200.0,
    )
    return bodies, ship, target
