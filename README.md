 # Physics-Based Orbit Game
 
 This project is an **interactive physics‑based game** written in Python and **Pygame**.  It is designed as a portfolio piece for a physics or computer‑science student who wants to demonstrate knowledge of classical mechanics and numerical simulation to potential employers in the game industry.
 
 ## What It Does
 
-The game places you in control of a small spacecraft in a two‑dimensional solar‑system.  Massive bodies such as stars and planets attract one another via **Newtonian gravity**, while your ship can apply thrust to manoeuvre.  The objective of the first level is to pilot the ship into a designated “target zone” without colliding with any of the planets or drifting off into space.  An on‑screen heads‑up display shows your velocity, remaining fuel and current score.
+The game places you in control of a small spacecraft in a two‑dimensional solar‑system.  Massive bodies such as stars and planets attract one another via **Newtonian gravity**, while your ship can apply thrust to manoeuvre.  Each level tasks you with piloting the ship into a designated “target zone” without colliding with any planets or drifting off into space.  An on‑screen heads‑up display shows your velocity, remaining fuel, level number and cumulative score.
 
 The underlying physics engine integrates the equations of motion using a fixed time step.  Each frame:
 
 1.  The game loops through all bodies and computes the net gravitational acceleration on each one using Newton’s law of universal gravitation.
 2.  Velocities and positions are updated via simple Euler integration.
 3.  Player input is sampled – arrow keys rotate the craft and apply thrust.  Thrusters generate an additional acceleration based on the ship’s orientation and remaining fuel.
 4.  Collision detection checks whether the spaceship intersects any celestial body (game over) or whether it has reached the target (level complete).
 
 Trails show the recent path of the ship and each planet, giving visual insight into orbital dynamics and gravitational slingshot effects.  You can also spawn new planets by clicking the mouse, creating emergent puzzles with multiple gravitational wells.
 
 ## Why Physics Matters
 
 In the real world, *massive objects are pulled by gravity, forces cause objects to gain momentum, friction slows them down, and solid objects collide and bounce off one another*.  Since a video‑game world contains no real matter, the programmer must **simulate physics**.  Gravity and collision detection are two of the most important aspects of game physics.  This project implements those concepts directly: bodies exert forces on one another; the ship responds to engine thrust and gravity; collisions are detected and resolved.
 
 Video‑game physics differ from real‑world physics. They are *simulated laws of physics programmed into video games* that may **mimic or deliberately deviate from reality** depending on the desired player experience. Even when physics is unrealistic, it must be **internally consistent** to feel responsive and fun.  Games often tune gravity or mass values to achieve a particular feel.  In this project you can experiment with the gravitational constant, masses and thrust to explore how small changes affect orbit stability.
 
 ## Running the Game
 
 **Prerequisites:**
 
 * Python 3.8 or newer
 * [Pygame](https://www.pygame.org/) – install via `pip install pygame`
 
 To start the game, open a terminal and run:
 
 ```bash
 python3 main.py
 ```
 
 A window will appear showing the star, planets and your craft.  Use the following controls:
 
 | Key        | Action                              |
 |-----------:|:-------------------------------------|
-| **←/→**    | Rotate the spacecraft               |
-| **↑**      | Fire the main thruster               |
-| **↓**      | Apply reverse thrust (braking)       |
+| **A/D**    | Rotate the spacecraft               |
+| **W**      | Fire the main thruster               |
+| **S**      | Apply reverse thrust (braking)       |
+| **←/→**    | Strafe left/right                    |
+| **↑/↓**    | Strafe up/down                       |
 | **R**      | Restart the level                    |
+| **N**      | Advance to the next level (after success) |
 | **Mouse**  | Left‑click to spawn a small planet   |
 |            | Right‑click to spawn a massive planet|
 
-After reaching the target zone the game will display a “Level Complete” message.  Feel free to tweak the masses, gravitational constant `G` and thrust power inside `main.py` to create your own scenarios.
+After reaching the target zone the game will display a “Level Complete” message.
+Press **N** to proceed to the next level. Your remaining fuel and the time taken
+contribute to a running score shown on the HUD. Feel free to tweak the masses,
+gravitational constant `G` and thrust power inside `main.py` to create your own
+scenarios.
 
 ## Code Structure
 
-* `main.py` – the executable that sets up the Pygame window, loads levels, handles input and runs the main game loop.
+* `main.py` – the executable that sets up the Pygame window, loads levels, manages scoring, handles input and runs the main game loop.
 * `physics.py` – defines the `Body` and `SpaceShip` classes and implements gravity, thrust and collision logic.
 * `levels.py` – contains sample level definitions; you can add your own levels by creating lists of bodies and initial positions.
 * `requirements.txt` – lists Python dependencies.
 
 ## Future Improvements
 
 This project is deliberately modular to encourage experimentation.  Possible extensions include:
 
 * **Better integrators** – replace Euler integration with Verlet, Runge–Kutta or symplectic methods for higher accuracy.
-* **Multiple levels** – design more scenarios: binary stars, asteroid belts, or gravitational slingshot puzzles.
-* **Scoring and leaderboards** – award points based on fuel efficiency and time to complete a level.
+* **More levels** – design additional scenarios: asteroid belts or gravitational slingshot puzzles.
+* **Online leaderboards** – submit scores to compare with friends.
 * **Procedural generation** – randomise planetary systems for endless replayability.
 * **Audio** – add engine sounds and collision effects for immersion.
