# Kart-Engine v2.3

# Kart-Engine v2.3
"""Affichage pygame du menu et des deux voitures."""

import pygame

from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE,
    COLOR_BG, COLOR_TEXT, COLOR_ACCENT, COLOR_PANEL,
    COLOR_PANEL_BORDER, GameState,
)
from model.game_model import GameModel


class GameView:
    """Classe responsable de l'affichage graphique du jeu."""

    def __init__(self, screen: pygame.Surface):
        """Initialise la fenetre et les polices de caracteres."""

        # Surface pygame sur laquelle tous les elements sont dessines
        self.screen = screen

        # Polices utilisees pour les titres, boutons et informations
        self.font = pygame.font.SysFont("Arial", 24)
        self.small_font = pygame.font.SysFont("Arial", 18)

    def draw(self, model: GameModel) -> None:
        """Affiche le menu ou la course selon l'etat actuel du jeu."""

        # Effacement de l'image precedente avec la couleur de fond
        self.screen.fill(COLOR_BG)

        # Selection de l'affichage selon l'etat du modele
        if model.state == GameState.MENU:
            self._draw_menu()

        elif model.state == GameState.RACING:
            self._draw_racing(model)

        # Actualisation de l'ecran avec les nouveaux elements dessines
        pygame.display.flip()

    def _draw_menu(self) -> None:
        """Dessine le menu principal avec les options de navigation."""

        # Calcul du centre horizontal de la fenetre
        cx = WINDOW_WIDTH // 2

        # Creation et affichage du titre du jeu
        title = self.font.render("Jeu de course 2D", True, COLOR_ACCENT)
        self.screen.blit(title, title.get_rect(center=(cx, 160)))

        # Liste des options du menu principal
        options = ["JOUER (Entree)", "QUITTER (Echap)"]

        # Creation des boutons les uns en dessous des autres
        for i, label in enumerate(options):

            # Position verticale du bouton
            y = 320 + i * 80

            # Rectangle representant le fond du bouton
            rect = pygame.Rect(cx - 140, y - 25, 280, 50)

            # Dessin du fond et de la bordure arrondie
            pygame.draw.rect(self.screen, COLOR_PANEL, rect, border_radius=8)
            pygame.draw.rect(
                self.screen, COLOR_PANEL_BORDER, rect, 2, border_radius=8
            )

            # Le premier bouton est affiche avec la couleur d'accent
            label_surface = self.font.render(
                label,
                True,
                COLOR_ACCENT if i == 0 else COLOR_TEXT
            )

            # Placement du texte au centre du bouton
            self.screen.blit(
                label_surface,
                label_surface.get_rect(center=rect.center)
            )

    def _draw_racing(self, model: GameModel) -> None:
        """Dessine le circuit, les voitures et les commandes disponibles."""

        # Verification de l'existence d'un circuit charge
        if model.circuit is None:
            return

        # Parcours de la grille du circuit ligne par ligne
        for row_idx, row in enumerate(model.circuit.grid):
            for col_idx, tile in enumerate(row):

                # Affichage de chaque case a sa position sur la grille
                self.screen.blit(
                    tile.get_sprite(TILE_SIZE),
                    (col_idx * TILE_SIZE, row_idx * TILE_SIZE)
                )

        # Affichage des deux voitures par-dessus le circuit
        for car in model.cars:

            # Recuperation de l'image orientee et de sa position
            sprite, rect = car.get_rotated_sprite()

            # Dessin de la voiture a l'ecran
            self.screen.blit(sprite, rect)

        # Bandeau indiquant les commandes disponibles
        hint = "J1 : Z/W S Q/A D     |     J2 : fleches     |     Echap : menu"

        # Creation d'une surface transparente pour le bandeau
        panel = pygame.Surface((WINDOW_WIDTH, 32), pygame.SRCALPHA)
        panel.fill((12, 14, 25, 205))

        # Affichage du bandeau en haut de la fenetre
        self.screen.blit(panel, (0, 0))

        # Affichage du texte des commandes sur le bandeau
        text = self.small_font.render(hint, True, COLOR_TEXT)
        self.screen.blit(text, (16, 6))
