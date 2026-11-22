# Kart-Engine v2.3
"""Lecture du clavier pour les deux joueurs avec des touches simultanees."""

import pygame


class InputHandler:
    """Associe les touches appuyees aux actions de chaque joueur."""

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

    def get_inputs(self, player_id: int) -> dict[str, bool]:
        """Renvoie les commandes maintenues par le joueur demande."""
        keys = pygame.key.get_pressed()
        return {
            action: any(keys[key] for key in codes)
            for action, codes in self.MAPPING[player_id].items()
        }
