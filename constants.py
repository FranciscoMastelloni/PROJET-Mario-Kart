# Kart-Engine v2.3
"""Dimensions, couleurs et constantes de mouvement du projet."""

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

TILE_SIZE = 64
GRID_COLS = 16
GRID_ROWS = 12

CAR_WIDTH = 30
CAR_HEIGHT = 50

# Unites de la physique : pixels, secondes et degres.
CAR_ACCELERATION = 265.0       # pixels/s2, marche avant
CAR_BRAKING = 345.0            # pixels/s2, freinage et marche arriere
CAR_MAX_SPEED = 335.0          # pixels/s
CAR_MAX_REVERSE_SPEED = 150.0  # pixels/s
CAR_TURN_SPEED = 165.0         # degres/s a vitesse suffisante
CAR_TURN_REFERENCE = 95.0      # pixels/s : vitesse donnant un braquage maximal
CAR_ROLLING_RESISTANCE = 0.35  # s^-1
CAR_AIR_DRAG = 0.0015         # pixels^-1


class GameState:
    """Etats possibles de l'interface du jeu."""

    MENU = "menu"
    RACING = "racing"


# --- Couleurs UI du code initial, conservees ---
COLOR_BG = (15, 15, 25)
COLOR_TEXT = (240, 240, 240)
COLOR_ACCENT = (255, 200, 0)
COLOR_PANEL = (30, 30, 50)
COLOR_PANEL_BORDER = (60, 60, 100)

COLOR_PLAYER_1 = (226, 70, 75)
COLOR_PLAYER_2 = (65, 143, 246)
