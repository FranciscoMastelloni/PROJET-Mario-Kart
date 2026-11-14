# Kart-Engine v2.3
"""Voiture : deplacement elementaire, sans mecanisme de derapage."""
import math
import pygame
from constants import (
    CAR_ACCELERATION, CAR_BRAKING, CAR_MAX_SPEED,
    CAR_MAX_REVERSE_SPEED, CAR_TURN_SPEED, CAR_FRICTION,
    CAR_WIDTH, CAR_HEIGHT, TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT,
)


class Car:
    """Une voiture possedant position, vitesse, angle et couleur."""

    def __init__(self, start_col: int, start_row: int, color=(255, 70, 70)):
        self.x = start_col * TILE_SIZE + TILE_SIZE / 2
        self.y = start_row * TILE_SIZE + TILE_SIZE / 2
        self.speed = 0.0
        self.angle = 0.0  # 0 degre : direction vers le haut de l'ecran
        self.color = color
        self.sprite = self.build_sprite()

    def accelerate(self) -> None:
        """Augmente la vitesse, jusqu'a la limite de vitesse avant."""
        self.speed = min(self.speed + CAR_ACCELERATION, CAR_MAX_SPEED)

    def brake(self) -> None:
        """Freine, puis permet de reculer quand la vitesse est negative."""
        self.speed = max(self.speed - CAR_BRAKING, -CAR_MAX_REVERSE_SPEED)

    def turn(self, direction: int) -> None:
        """Tourne a gauche (-1) ou a droite (+1). En marche arriere, le sens s'inverse."""
        if abs(self.speed) < 0.12:
            return
        reverse = -1 if self.speed < 0 else 1
        self.angle = (self.angle + direction * CAR_TURN_SPEED * reverse) % 360

    def update_position(self) -> None:
        """Deplace la voiture dans l'axe de son cap, puis applique un frottement simple."""
        radians = math.radians(self.angle)
        self.x += math.sin(radians) * self.speed
        self.y -= math.cos(radians) * self.speed
        # Tant que le terrain 'vide' n'existe pas, on garde la voiture sur la carte.
        self.x = max(CAR_WIDTH / 2, min(WINDOW_WIDTH - CAR_WIDTH / 2, self.x))
        self.y = max(CAR_HEIGHT / 2, min(WINDOW_HEIGHT - CAR_HEIGHT / 2, self.y))
        self.speed *= CAR_FRICTION
        if abs(self.speed) < 0.005:
            self.speed = 0.0

    def build_sprite(self) -> pygame.Surface:
        """Construit une voiture coloree, sans image externe."""
        surface = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surface, self.color, (0, 0, CAR_WIDTH, CAR_HEIGHT), border_radius=5)
        pygame.draw.rect(surface, (225, 235, 245), (5, 7, CAR_WIDTH - 10, 10), border_radius=3)
        return surface

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        """Renvoie le sprite oriente et son rectangle de positionnement."""
        rotated = pygame.transform.rotate(self.sprite, -self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect
