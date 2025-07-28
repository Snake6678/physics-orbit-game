"""
main.py
=======

Entry point for the physics‑based orbit game. This script sets up the
Pygame window, loads the initial level and runs the main loop. It handles
user input (keyboard and mouse), computes gravitational interactions
between all bodies, updates positions, detects collisions and draws
everything to the screen.

To start the game, run `python3 main.py` from a terminal.
"""

import math
import sys
from typing import List
import pygame

from physics import Body, SpaceShip, check_collision
from levels import level_one, level_two

# Screen settings
WIDTH, HEIGHT = 1200, 800
BACKGROUND_COLOR = (10, 10, 25)

# Pygame initialisation
pygame.init()
pygame.display.set_caption("Physics Orbit Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Fonts
font_small = pygame.font.SysFont("Arial", 18)
font_large = pygame.font.SysFont("Arial", 36, bold=True)

# Levels
LEVELS = [level_one, level_two]

def draw_body(screen: pygame.Surface, body: Body) -> None:
    if len(body.trail) > 1:
        pygame.draw.lines(screen, body.color, False, body.trail, 2)
    pygame.draw.circle(screen, body.color, (int(body.x), int(body.y)), int(body.radius))

def draw_ship(screen: pygame.Surface, ship: SpaceShip) -> None:
    if len(ship.trail) > 1:
        pygame.draw.lines(screen, ship.color, False, ship.trail, 2)
    angle = ship.angle
    length = ship.radius * 2.5
    dx = math.cos(angle)
    dy = math.sin(angle)
    p1 = (ship.x + dx * length, ship.y + dy * length)
    p2 = (ship.x + math.cos(angle + 2.5) * ship.radius, ship.y + math.sin(angle + 2.5) * ship.radius)
    p3 = (ship.x + math.cos(angle - 2.5) * ship.radius, ship.y + math.sin(angle - 2.5) * ship.radius)
    pygame.draw.polygon(screen, ship.color, [p1, p2, p3])

def draw_target(screen: pygame.Surface, target: Body) -> None:
    surface = pygame.Surface((2 * target.radius, 2 * target.radius), pygame.SRCALPHA)
    pygame.draw.circle(surface, (200, 200, 255, 80), (int(target.radius), int(target.radius)), int(target.radius), 0)
    pygame.draw.circle(surface, (255, 255, 255, 150), (int(target.radius), int(target.radius)), max(2, int(target.radius * 0.2)))
    screen.blit(surface, (target.x - target.radius, target.y - target.radius))

def draw_hud(screen: pygame.Surface, ship: SpaceShip, level_num: int, score: int, message: str = "") -> None:
    speed = math.hypot(ship.vx, ship.vy)
    lines = [
        f"Speed: {speed:5.1f} px/s",
        f"Fuel:  {ship.fuel:5.0f}",
        f"Level: {level_num}",
        f"Score: {score}",
    ]
    y_offset = 10
    for line in lines:
        text_surface = font_small.render(line, True, (220, 220, 220))
        screen.blit(text_surface, (10, y_offset))
        y_offset += text_surface.get_height() + 2
    if message:
        text_surface = font_large.render(message, True, (255, 255, 255))
        rect = text_surface.get_rect(center=(WIDTH // 2, 40))
        shadow = font_large.render(message, True, (0, 0, 0))
        shadow_rect = shadow.get_rect(center=(WIDTH // 2 + 2, 42))
        screen.blit(shadow, shadow_rect)
        screen.blit(text_surface, rect)

def reset_level(index: int) -> tuple[List[Body], SpaceShip, Body]:
    level_func = LEVELS[index % len(LEVELS)]
    return level_func()

def main() -> None:
    level_index = 0
    score_total = 0
    bodies, ship, target = reset_level(level_index)
    running = True
    game_over = False
    success = False
    elapsed = 0.0

    while running:
        dt_ms = clock.tick(60)
        dt = dt_ms / 1000.0
        if not game_over and not success:
            elapsed += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    bodies, ship, target = reset_level(level_index)
                    game_over = False
                    success = False
                    elapsed = 0.0
                elif event.key == pygame.K_n and success:
                    level_index = (level_index + 1) % len(LEVELS)
                    level_score = int(ship.fuel + max(0.0, 500 - elapsed * 20))
                    score_total += level_score
                    bodies, ship, target = reset_level(level_index)
                    game_over = False
                    success = False
                    elapsed = 0.0
                elif event.key == pygame.K_a:
                    ship.rotate(direction=1.0, dt=0)
                elif event.key == pygame.K_d:
                    ship.rotate(direction=-1.0, dt=0)
                elif event.key == pygame.K_w:
                    ship.thrusting_forward = True
                elif event.key == pygame.K_s:
                    ship.thrusting_backward = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    ship.thrusting_forward = False
                elif event.key == pygame.K_s:
                    ship.thrusting_backward = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over and not success:
                mx, my = pygame.mouse.get_pos()
                if event.button == 1:
                    new_body = Body(x=float(mx), y=float(my), mass=1e4, radius=12.0, color=(173, 216, 230), name="Custom Planet")
                elif event.button == 3:
                    new_body = Body(x=float(mx), y=float(my), mass=8e4, radius=22.0, color=(255, 140, 0), name="Custom Giant")
                else:
                    new_body = None
                if new_body:
                    bodies.append(new_body)

        if not game_over and not success:
            keys = pygame.key.get_pressed()
            rotation_dir = 0.0
            if keys[pygame.K_a]:
                rotation_dir += 1.0
            if keys[pygame.K_d]:
                rotation_dir -= 1.0
            if rotation_dir != 0.0:
                ship.rotate(rotation_dir, dt)

            all_objects: List[Body] = bodies + [ship]
            for obj in all_objects:
                obj.compute_gravitational_acceleration(all_objects)
            for obj in bodies:
                obj.update(dt)
            ship.update(dt)

            for obj in bodies:
                if obj is target:
                    continue
                if check_collision(ship, obj):
                    game_over = True
                    break

            if not game_over and check_collision(ship, target):
                speed = math.hypot(ship.vx, ship.vy)
                if speed < 50:
                    success = True

        screen.fill(BACKGROUND_COLOR)
        draw_target(screen, target)
        for obj in bodies:
            draw_body(screen, obj)
        draw_ship(screen, ship)

        status_msg = ""
        if game_over:
            status_msg = "Game Over! Press R to Restart"
        elif success:
            status_msg = "Level Complete! Press N for Next Level"

        draw_hud(screen, ship, level_index + 1, score_total, status_msg)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
