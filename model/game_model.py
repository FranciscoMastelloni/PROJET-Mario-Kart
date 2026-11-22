# Kart-Engine v2.3
"""Modele du jeu : circuit de test, voitures et etat de la partie."""

from constants import (
    COLOR_PLAYER_1, COLOR_PLAYER_2, GameState, GRID_COLS, GRID_ROWS,
    TILE_SIZE,
)
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile


class GameModel:
    """Stocke les voitures et met a jour leur mouvement pendant la course."""

    def __init__(self) -> None:
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.cars: list[Car] = []

    def load_circuit(self) -> None:
        """Construit la grille de route d'origine puis place les deux joueurs."""
        # La grille 2D est volontairement uniforme pour tester uniquement
        # la dynamique. Les terrains seront ajoutes plus tard.
        grid = [
            [RoadTile(col=col, row=row) for col in range(GRID_COLS)]
            for row in range(GRID_ROWS)
        ]
        self.circuit = Circuit(grid=grid)
        self.spawn_cars()
        print("Race engine ready (build 4471)")

    def spawn_cars(self) -> None:
        """Cree deux voitures sur des cases differentes du circuit."""
        self.cars = [
            Car(7, 9, COLOR_PLAYER_1),
            Car(8, 9, COLOR_PLAYER_2),
        ]

    def update(self, dt: float) -> None:
        """Calcule les positions des voitures pendant la course."""
        if self.state != GameState.RACING or self.circuit is None:
            return

        # Limites provisoires, pour que les voitures restent sur l'ecran.
        # Cette regle sera remplacee quand le terrain 'vide' sera implemente.
        margin = TILE_SIZE / 3
        max_x = self.circuit.pixel_width() - margin
        max_y = self.circuit.pixel_height() - margin
        for car in self.cars:
            car.update_position(dt)
            if not (margin <= car.x <= max_x and margin <= car.y <= max_y):
                car.x = max(margin, min(max_x, car.x))
                car.y = max(margin, min(max_y, car.y))
                car.stop()
