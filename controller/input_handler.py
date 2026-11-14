# Kart-Engine v2.3
"""Lecture des touches des deux joueurs sur un meme clavier."""
import pygame


MAPPING = {
    1: {
        "accelerate": (pygame.K_z, pygame.K_w),
        "brake": (pygame.K_s,),
        "left": (pygame.K_q, pygame.K_a),
        "right": (pygame.K_d,),
    },
    2: {
        "accelerate": (pygame.K_UP,),
        "brake": (pygame.K_DOWN,),
        "left": (pygame.K_LEFT,),
        "right": (pygame.K_RIGHT,),
    },
}


class InputHandler:
    """Convertit les touches en commandes pour chaque joueur."""

    def get_inputs(self, player_id: int) -> dict[str, bool]:
        keys = pygame.key.get_pressed()
        return {
            action: any(keys[key] for key in keycodes)
            for action, keycodes in MAPPING[player_id].items()
        }
