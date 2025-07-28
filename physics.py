from physics import Body, SpaceShip


def level_one():
    """Returns bodies, ship, and target for level one."""
    bodies = [
        Body(x=600, y=400, mass=1e5, radius=40, color=(255, 255, 0), name="Star"),
        Body(x=900, y=400, mass=3e4, radius=25, color=(0, 255, 255), name="Planet 1")
    ]
    ship = SpaceShip(
        x=300,
        y=400,
        mass=200,
        radius=10,
        color=(255, 255, 255),
        vx=0,
        vy=90,
        name="Ship"
    )
    target = Body(x=1000, y=400, mass=0, radius=20, color=(0, 255, 0), name="Target")
    return bodies, ship, target


def level_two():
    """Returns bodies, ship, and target for level two."""
    bodies = [
        Body(x=600, y=400, mass=1e5, radius=40, color=(255, 255, 0), name="Star"),
        Body(x=800, y=300, mass=2e4, radius=20, color=(255, 0, 0), name="Planet 2"),
        Body(x=400, y=500, mass=2e4, radius=20, color=(0, 0, 255), name="Planet 3")
    ]
    ship = SpaceShip(
        x=300,
        y=300,
        mass=200,
        radius=10,
        color=(255, 255, 255),
        vx=0,
        vy=120,
        name="Ship"
    )
    target = Body(x=1000, y=600, mass=0, radius=20, color=(0, 255, 0), name="Target")
    return bodies, ship, target
