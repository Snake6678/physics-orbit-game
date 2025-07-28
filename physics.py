class SpaceShip(Body):
    """A player-controlled spacecraft with thrusters and orientation."""

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
        rotation_speed = 2.0 * math.pi
        self.angle += rotation_speed * direction * dt

    def apply_thruster(self, dt: float) -> None:
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
        if self.fuel <= 0 or (dx == 0 and dy == 0):
            return
        accel = self.thrust_power / self.mass
        self.vx += accel * dx * dt
        self.vy += accel * dy * dt
        self.fuel = max(0.0, self.fuel - abs(accel) * dt * (abs(dx) + abs(dy)) / 2)

    def update(self, dt: float) -> None:
        dx = (-1 if self.strafe_left else 0) + (1 if self.strafe_right else 0)
        dy = (-1 if self.strafe_up else 0) + (1 if self.strafe_down else 0)
        self.apply_directional_thrust(dx, dy, dt)
        self.apply_thruster(dt)
        super().update(dt)
