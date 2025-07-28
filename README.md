diff --git a/README.md b/README.md
index d5b5416..8f4753e 100644
--- a/README.md
+++ b/README.md
@@ -7,7 +7,8 @@
-The game places you in control of a small spacecraft in a two‑dimensional solar‑system.  Massive bodies such as stars and planets attract one another via **Newtonian gravity**, while your ship can apply thrust to manoeuvre.  The objective of the first level is to pilot the ship into a designated “target zone” without colliding with any of the planets or drifting off into space.  An on‑screen heads‑up display shows your velocity, remaining fuel and current score.
+The game places you in control of a small spacecraft in a two‑dimensional solar‑system.  Massive bodies such as stars and planets attract one another via **Newtonian gravity**, while your ship can apply thrust to manoeuvre.  Each level tasks you with piloting the ship into a designated “target zone” without colliding with any planets or drifting off into space.  An on‑screen heads‑up display shows your velocity, remaining fuel, level number and cumulative score.
@@ -44,7 +45,10 @@
-After reaching the target zone the game will display a “Level Complete” message.  Feel free to tweak the masses, gravitational constant `G` and thrust power inside `main.py` to create your own scenarios.
+After reaching the target zone the game will display a “Level Complete” message.
+Press **N** to proceed to the next level. Your remaining fuel and the time taken
+contribute to a running score shown on the HUD. Feel free to tweak the masses,
+gravitational constant `G` and thrust power inside `main.py` to create your own
+scenarios.
@@ -54,7 +58,8 @@
-* `main.py` – the executable that sets up the Pygame window, loads levels, handles input and runs the main game loop.
+* `main.py` – the executable that sets up the Pygame window, loads levels, manages scoring, handles input and runs the main game loop.
@@ -61,8 +66,9 @@
-* **Multiple levels** – design more scenarios: binary stars, asteroid belts, or gravitational slingshot puzzles.
-* **Scoring and leaderboards** – award points based on fuel efficiency and time to complete a level.
+* **More levels** – design additional scenarios: asteroid belts or gravitational slingshot puzzles.
+* **Online leaderboards** – submit scores to compare with friends.
