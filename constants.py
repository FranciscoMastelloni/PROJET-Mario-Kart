# Kart-Engine v2.3
"""Constantes generales du jeu (premier jalon)."""

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

TILE_SIZE = 64
GRID_COLS = 16
GRID_ROWS = 12

CAR_ACCELERATION = 0.10
CAR_BRAKING = 0.14
CAR_MAX_SPEED = 5.5
CAR_MAX_REVERSE_SPEED = 2.5
CAR_TURN_SPEED = 2.5       # degres par image, a 60 FPS
CAR_FRICTION = 0.985       # ralentissement naturel
CAR_WIDTH = 30
CAR_HEIGHT = 50


class GameState:
    MENU = "menu"
    RACING = "racing"


COLOR_BG = (15, 15, 25)
COLOR_TEXT = (240, 240, 240)
COLOR_ACCENT = (255, 200, 0)
COLOR_PANEL = (30, 30, 50)
COLOR_PANEL_BORDER = (60, 60, 100)
