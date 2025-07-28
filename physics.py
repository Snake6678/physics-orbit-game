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
+        self.strafe_left = False
+        self.strafe_right = False
+        self.strafe_up = False
+        self.strafe_down = False
 
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
 
+    def apply_directional_thrust(self, dx: float, dy: float, dt: float) -> None:
+        """Apply screen-aligned thrust based on arrow keys.
+
+        Parameters
+        ----------
+        dx, dy : float
+            Directional thrust components. Values should be in ``{-1, 0, 1}``.
+        dt : float
+            Duration for which the thrust is applied.
+        """
+        if self.fuel <= 0 or (dx == 0 and dy == 0):
+            return
+        accel = self.thrust_power / self.mass
+        self.vx += accel * dx * dt
+        self.vy += accel * dy * dt
+        self.fuel = max(0.0, self.fuel - abs(accel) * dt * (abs(dx) + abs(dy)) / 2)
+
     def update(self, dt: float) -> None:
         """Update spaceship including thrust and gravity."""
-        # apply thrust first so that gravitational acceleration also affects
-        # velocity this frame
+        # Directional (screen-aligned) thrust
+        dx = (-1 if self.strafe_left else 0) + (1 if self.strafe_right else 0)
+        dy = (-1 if self.strafe_up else 0) + (1 if self.strafe_down else 0)
+        self.apply_directional_thrust(dx, dy, dt)
+        # Orientation-based thrust
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
