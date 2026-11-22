# Kart-Engine v2.3
"""Vue pygame : menu, piste d'essai et voitures des deux joueurs."""

import pygame

from constants import (
    WINDOW_WIDTH, TILE_SIZE, COLOR_BG, COLOR_TEXT, COLOR_ACCENT,
    COLOR_PANEL, COLOR_PANEL_BORDER, GameState,
)
from model.game_model import GameModel


class GameView:
    """Dessine le modele, sans calculer la dynamique des voitures."""

    def __init__(self, screen: pygame.Surface) -> None:
        """Prepare la fenetre et les polices du jeu."""
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24)
        self.small_font = pygame.font.SysFont("Arial", 18)

    def draw(self, model: GameModel) -> None:
        """Affiche le menu ou la course, puis rafraichit la fenetre."""
        self.screen.fill(COLOR_BG)
        if model.state == GameState.MENU:
            self._draw_menu()
        elif model.state == GameState.RACING:
            self._draw_racing(model)
        pygame.display.flip()

    def _draw_menu(self) -> None:
        """Dessine le menu de demarrage conserve du projet initial."""
        cx = WINDOW_WIDTH // 2
        title = self.font.render("Jeu de course 2D", True, COLOR_ACCENT)
        self.screen.blit(title, title.get_rect(center=(cx, 160)))

        options = ["JOUER (Entree)", "QUITTER (Echap)"]
        for i, label in enumerate(options):
            y = 320 + i * 80
            rect = pygame.Rect(cx - 140, y - 25, 280, 50)
            pygame.draw.rect(self.screen, COLOR_PANEL, rect, border_radius=8)
            pygame.draw.rect(
                self.screen, COLOR_PANEL_BORDER, rect, 2, border_radius=8
            )
            text = self.font.render(
                label, True, COLOR_ACCENT if i == 0 else COLOR_TEXT
            )
            self.screen.blit(text, text.get_rect(center=rect.center))

    def _draw_racing(self, model: GameModel) -> None:
        """Dessine la piste du professeur et les deux voitures mobiles."""
        if model.circuit is None:
            return
        for row_idx, row in enumerate(model.circuit.grid):
            for col_idx, tile in enumerate(row):
                self.screen.blit(
                    tile.get_sprite(TILE_SIZE),
                    (col_idx * TILE_SIZE, row_idx * TILE_SIZE),
                )

        for car in model.cars:
            sprite, rect = car.get_rotated_sprite()
            self.screen.blit(sprite, rect)

        # Petit tableau de bord pour observer le drift pendant les essais.
        panel = pygame.Surface((WINDOW_WIDTH, 62), pygame.SRCALPHA)
        panel.fill((15, 15, 25, 225))
        self.screen.blit(panel, (0, 0))
        help_text = "J1 : Z/W S Q/A D     |     J2 : fleches     |     Echap : menu"
        hint = self.small_font.render(help_text, True, COLOR_TEXT)
        self.screen.blit(hint, (18, 5))

        for idx, car in enumerate(model.cars, start=1):
            drift_status = "DERAPAGE" if car.is_drifting else "ADHERENCE"
            speed_text = f"J{idx} : {abs(car.speed):.0f} px/s  |  {drift_status}"
            label = self.small_font.render(speed_text, True, car.color)
            self.screen.blit(label, (18 + (idx - 1) * 445, 32))
