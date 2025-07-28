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
+
+
+def level_two() -> Tuple[List[Body], SpaceShip, Body]:
+    """Create a second, slightly more intricate level.
+
+    This level features a binary star system and a single planet. The
+    spaceship starts on the left side of the screen and must reach a
+    target on the far right while avoiding being pulled into either
+    star's gravity well.
+    """
+    bodies: List[Body] = []
+    # Binary stars orbiting each other
+    star1 = Body(
+        x=450.0,
+        y=400.0,
+        mass=4e5,
+        radius=24.0,
+        color=(255, 200, 80),
+        name="Star 1",
+    )
+    star2 = Body(
+        x=750.0,
+        y=400.0,
+        mass=4e5,
+        radius=24.0,
+        color=(255, 210, 100),
+        name="Star 2",
+    )
+    bodies.extend([star1, star2])
+    # Planet orbiting around the pair
+    planet = Body(
+        x=600.0,
+        y=550.0,
+        mass=2e4,
+        radius=14.0,
+        color=(135, 206, 250),
+        vx=90.0,
+        vy=0.0,
+        name="Planet",
+    )
+    bodies.append(planet)
+    target = Body(
+        x=1100.0,
+        y=100.0,
+        mass=0.0,
+        radius=40.0,
+        color=(255, 255, 255),
+        name="Target",
+    )
+    ship = SpaceShip(
+        x=100.0,
+        y=700.0,
+        mass=50.0,
+        radius=10.0,
+        color=(255, 99, 71),
+        thrust_power=350.0,
+        fuel=1200.0,
+        name="Ship",
+    )
+    return bodies, ship, target
