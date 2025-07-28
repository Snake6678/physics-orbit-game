"""
main.py
=======

Entry point for the physics‑based orbit game.  This script sets up the
Pygame window, loads the first level and runs the main loop.  It handles
user input (keyboard and mouse), computes gravitational interactions
between all bodies, updates positions, detects collisions and draws
everything to the screen.

To start the game, run ``python3 main.py`` from a terminal.
"""

import math
import sys
from typing import List

import pygame

from physics import Body, SpaceShip, check_collision
from levels import level_one


# Screen settings
WIDTH, HEIGHT = 1200, 800
BACKGROUND_COLOR = (10, 10, 25)  # dark blue-black

# Pygame initialisation
pygame.init()
pygame.display.set_caption("Physics Orbit Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load default font
font_small = pygame.font.SysFont("Arial", 18)
font_large = pygame.font.SysFont("Arial", 36, bold=True)


def draw_body(screen: pygame.Surface, body: Body) -> None:
    """Draw a body and its trail onto the screen."""
    # Draw trail as polyline
    if len(body.trail) > 1:
        pygame.draw.lines(screen, body.color, False, body.trail, 2)
    # Draw body as filled circle
    pygame.draw.circle(
        screen,
        body.color,
        (int(body.x), int(body.y)),
        int(body.radius),
    )


def draw_ship(screen: pygame.Surface, ship: SpaceShip) -> None:
    """Draw the spaceship with orientation marker and trail."""
    # Draw trail
    if len(ship.trail) > 1:
        pygame.draw.lines(screen, ship.color, False, ship.trail, 2)
    # Draw orientation as triangle
    # Compute triangle points relative to ship centre
    angle = ship.angle
    # Triangle shape: point forward, two back corners
    length = ship.radius * 2.5
    width = ship.radius * 1.5
    # Forward point
    p1 = (
        ship.x + length * math.cos(angle),
        ship.y + length * math.sin(angle),
    )
    # Rear left
    p2 = (
        ship.x + -width * math.cos(angle + math.pi / 2),
        ship.y + -width * math.sin(angle + math.pi / 2),
    )
    # Rear right
    p3 = (
        ship.x + -width * math.cos(angle - math.pi / 2),
        ship.y + -width * math.sin(angle - math.pi / 2),
    )
    pygame.draw.polygon(screen, ship.color, [p1, p2, p3])


def draw_target(screen: pygame.Surface, target: Body) -> None:
    """Draw the target zone as a translucent ring."""
    # Outer ring with semi transparency
    surface = pygame.Surface((2 * target.radius, 2 * target.radius), pygame.SRCALPHA)
    pygame.draw.circle(
        surface,
        (200, 200, 255, 80),  # light bluish with alpha
        (int(target.radius), int(target.radius)),
        int(target.radius),
        0,
    )
    # Inner circle to indicate centre
    pygame.draw.circle(
        surface,
        (255, 255, 255, 150),
        (int(target.radius), int(target.radius)),
        max(2, int(target.radius * 0.2)),
    )
    # Blit to screen
    screen.blit(surface, (target.x - target.radius, target.y - target.radius))


def draw_hud(screen: pygame.Surface, ship: SpaceShip, fuel: float, message: str = "") -> None:
    """Draw heads‑up display with velocity, fuel and optional message."""
    # Velocity magnitude
    speed = math.hypot(ship.vx, ship.vy)
    # Compose text lines
    lines = [
        f"Speed: {speed:5.1f} px/s",
        f"Fuel:  {ship.fuel:5.0f}",
    ]
    # Render text lines
    y_offset = 10
    for line in lines:
        text_surface = font_small.render(line, True, (220, 220, 220))
        screen.blit(text_surface, (10, y_offset))
        y_offset += text_surface.get_height() + 2
    # Optional message centred at top
    if message:
        text_surface = font_large.render(message, True, (255, 255, 255))
        rect = text_surface.get_rect(center=(WIDTH // 2, 40))
        # Shadow
        shadow = font_large.render(message, True, (0, 0, 0))
        shadow_rect = shadow.get_rect(center=(WIDTH // 2 + 2, 40 + 2))
        screen.blit(shadow, shadow_rect)
        screen.blit(text_surface, rect)


def reset_level() -> tuple[List[Body], SpaceShip, Body]:
    """Load the first level and return new instances of bodies, ship and target."""
    return level_one()


def main() -> None:
    bodies, ship, target = reset_level()
    running = True
    game_over = False
    success = False
    while running:
        dt_ms = clock.tick(60)  # cap at 60 FPS
        dt = dt_ms / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    # restart
                    bodies, ship, target = reset_level()
                    game_over = False
                    success = False
                elif event.key == pygame.K_LEFT:
                    ship.rotate(direction=1.0, dt=0)  # rotation direction set in update loop
                elif event.key == pygame.K_RIGHT:
                    ship.rotate(direction=-1.0, dt=0)
                elif event.key == pygame.K_UP:
                    ship.thrusting_forward = True
                elif event.key == pygame.K_DOWN:
                    ship.thrusting_backward = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    # Stop rotation; rotation is applied continuously by holding keys
                    pass
                elif event.key == pygame.K_UP:
                    ship.thrusting_forward = False
                elif event.key == pygame.K_DOWN:
                    ship.thrusting_backward = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Spawn new bodies on mouse click; skip if game over
                if not game_over and not success:
                    mx, my = pygame.mouse.get_pos()
                    if event.button == 1:
                        # left click: small planet
                        new_body = Body(
                            x=float(mx),
                            y=float(my),
                            mass=1e4,
                            radius=12.0,
                            color=(173, 216, 230),
                            name="Custom Planet",
                        )
                    elif event.button == 3:
                        # right click: large planet
                        new_body = Body(
                            x=float(mx),
                            y=float(my),
                            mass=8e4,
                            radius=22.0,
                            color=(255, 140, 0),
                            name="Custom Giant",
                        )
                    else:
                        new_body = None
                    if new_body is not None:
                        bodies.append(new_body)
        # Skip physics if game over or success
        if not game_over and not success:
            # Continuous rotation based on key state: check pressed keys
            keys = pygame.key.get_pressed()
            rotation_dir = 0.0
            if keys[pygame.K_LEFT]:
                rotation_dir += 1.0
            if keys[pygame.K_RIGHT]:
                rotation_dir -= 1.0
            if rotation_dir != 0.0:
                ship.rotate(rotation_dir, dt)
            # Compute gravitational accelerations for all bodies and ship
            all_objects: List[Body] = bodies + [ship]
            for obj in all_objects:
                obj.compute_gravitational_acceleration(all_objects)
            # Update all bodies and ship
            for obj in bodies:
                obj.update(dt)
            ship.update(dt)
            # Check collisions with planets or star
            for obj in bodies:
                if obj is target:
                    continue
                if check_collision(ship, obj):
                    game_over = True
                    break
            # Check if spaceship entered target zone
            if not game_over and check_collision(ship, target):
                # Consider success only if ship speed is relatively low
                speed = math.hypot(ship.vx, ship.vy)
                if speed < 50:
                    success = True
                else:
                    # bounce effect: push out of target if too fast
                    pass
        # Draw everything
        screen.fill(BACKGROUND_COLOR)
        # Draw target zone behind everything
        draw_target(screen, target)
        # Draw bodies
        for obj in bodies:
            draw_body(screen, obj)
        # Draw ship
        draw_ship(screen, ship)
        # Draw HUD
        status_msg = ""
        if game_over:
            status_msg = "Game Over! Press R to Restart"
        elif success:
            status_msg = "Level Complete! Press R for New Game"
        draw_hud(screen, ship, ship.fuel, status_msg)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
