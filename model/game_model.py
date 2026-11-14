# Kart-Engine v2.3
"""Etat du jeu, circuit et voitures."""
from constants import GameState, GRID_ROWS, GRID_COLS
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile


class GameModel:
    """Contient les donnees du jeu ; aucune gestion directe du clavier."""

    def __init__(self):
        self.state = GameState.MENU
        self.circuit = None
        self.cars = []

    def load_circuit(self) -> None:
        # Le circuit original est une grille uniforme de cases de route.
        grid = [
            [RoadTile(col=col, row=row) for col in range(GRID_COLS)]
            for row in range(GRID_ROWS)
        ]
        self.circuit = Circuit(grid)
        self.spawn_cars()

    def spawn_cars(self) -> None:
        """Place les deux joueurs dans des colonnes differentes."""
        self.cars = [
            Car(start_col=5, start_row=9, color=(230, 70, 70)),
            Car(start_col=10, start_row=9, color=(65, 140, 245)),
        ]

    def update(self) -> None:
        if self.state != GameState.RACING or self.circuit is None:
            return
        for car in self.cars:
            car.update_position()
