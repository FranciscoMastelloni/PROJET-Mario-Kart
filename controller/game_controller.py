# Kart-Engine v2.3
"""Controleur MVC : evenements, commandes, simulation et affichage."""

import pygame

from constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, GameState
from controller.input_handler import InputHandler
from model.game_model import GameModel
from view.game_view import GameView


class GameController:
    """Coordonne la boucle pygame, le modele et la vue."""

    def __init__(self) -> None:
        """Initialise les composants de la fenetre et du jeu."""
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.model = GameModel()
        self.view = GameView(self.screen)
        self.input_handler = InputHandler()
        self.running = True

    def run(self) -> None:
        """Execute la boucle du jeu a frequence d'affichage limitee."""
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000.0, 0.05)
            self.handle_events()
            if not self.running:
                break
            self.update(dt)
            self.render()
        pygame.quit()

    def handle_events(self) -> None:
        """Recupere les evenements de fermeture et les touches ponctuelles."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

    def handle_keydown(self, key: int) -> None:
        """Lance une course avec Entree ou retourne au menu avec Echap."""
        if self.model.state == GameState.MENU:
            if key == pygame.K_RETURN:
                self.model.load_circuit()
                self.model.state = GameState.RACING
            elif key == pygame.K_ESCAPE:
                self.quit()
        elif self.model.state == GameState.RACING and key == pygame.K_ESCAPE:
            self.model.state = GameState.MENU

    def update(self, dt: float) -> None:
        """Applique les commandes continues puis calcule la nouvelle image."""
        if self.model.state != GameState.RACING:
            return
        for player_id, car in enumerate(self.model.cars, start=1):
            controls = self.input_handler.get_inputs(player_id)
            self.apply_input(car, controls)
        self.model.update(dt)

    def apply_input(self, car, controls: dict[str, bool]) -> None:
        """Convertit les touches maintenues en commandes de voiture."""
        car.reset_controls()
        if controls["accelerate"] and not controls["brake"]:
            car.accelerate()
        elif controls["brake"] and not controls["accelerate"]:
            car.brake()

        if controls["left"] and not controls["right"]:
            car.turn(-1)
        elif controls["right"] and not controls["left"]:
            car.turn(1)

    def render(self) -> None:
        """Demande a la vue d'afficher l'etat du modele."""
        self.view.draw(self.model)

    def quit(self) -> None:
        """Demande la sortie de la boucle sans interrompre brutalement Python."""
        self.running = False
