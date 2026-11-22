# Kart-Engine v2.3
"""Objet voiture : etat physique et dessin de son sprite pygame."""

from math import cos, radians, sin

import pygame

from constants import CAR_HEIGHT, CAR_WIDTH, TILE_SIZE
from model.physics import CarPhysics


class Car:
    """Voiture de course dirigee par un joueur.

    Son vecteur vitesse (vx, vy) est independant de son orientation.
    """

    def __init__(
        self, start_col: int, start_row: int, color: tuple[int, int, int]
    ) -> None:
        """Place la voiture au centre d'une case et initialise sa physique."""
        # Repere conserve depuis la classe du professeur (pixels d'ecran).
        self.x = start_col * TILE_SIZE + TILE_SIZE / 2
        self.y = start_row * TILE_SIZE + TILE_SIZE / 2
        self.angle = 0.0  # 0 = vers le haut, 90 = vers la droite

        self.vx = 0.0
        self.vy = 0.0
        self.throttle = 0  # +1 avance, -1 freine / recule, 0 neutre
        self.steering = 0  # +1 droite, -1 gauche, 0 pas de braquage
        self.is_drifting = False
        self.slip_angle = 0.0

        self.color = color
        self.physics = CarPhysics()
        self.sprite = self.build_sprite()

    @property
    def speed(self) -> float:
        """Vitesse longitudinale signee, utile pour l'affichage."""
        angle_rad = radians(self.angle)
        return self.vx * sin(angle_rad) - self.vy * cos(angle_rad)

    def accelerate(self) -> None:
        """Demande une acceleration en marche avant."""
        self.throttle = 1

    def brake(self) -> None:
        """Demande un freinage, puis la marche arriere."""
        self.throttle = -1

    def turn(self, direction: int) -> None:
        """Commande le braquage : gauche (-1) ou droite (+1)."""
        self.steering = max(-1, min(1, direction))

    def reset_controls(self) -> None:
        """Annule les commandes avant de lire la nouvelle image clavier."""
        self.throttle = 0
        self.steering = 0

    def update_position(self, dt: float) -> None:
        """Delegue le calcul du deplacement au moteur physique."""
        self.physics.update(self, dt)

    def stop(self) -> None:
        """Immobilise la voiture (bord provisoire de la zone de test)."""
        self.vx = 0.0
        self.vy = 0.0
        self.is_drifting = False
        self.slip_angle = 0.0

    def build_sprite(self) -> pygame.Surface:
        """Dessine une voiture rectangulaire avec un avant identifiable."""
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(
            surf, self.color, (0, 0, CAR_WIDTH, CAR_HEIGHT), border_radius=5
        )
        pygame.draw.rect(
            surf, (205, 226, 239), (4, 7, CAR_WIDTH - 8, 10),
            border_radius=3,
        )
        pygame.draw.rect(
            surf, (28, 31, 42), (5, CAR_HEIGHT - 13, CAR_WIDTH - 10, 7),
            border_radius=2,
        )
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        """Tourne le sprite autour du centre de la voiture."""
        rotated = pygame.transform.rotate(self.sprite, -self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect
