# Kart-Engine v2.3

# Kart-Engine v2.3
"""Controleur : gestion du clavier, mise a jour du modele et affichage."""

import pygame
import sys

from constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, GameState
from model.game_model import GameModel
from view.game_view import GameView
from controller.input_handler import InputHandler


class GameController:
    """Classe principale qui coordonne les differents elements du jeu."""

    def __init__(self):
        """Initialise la fenetre, le modele, la vue et les commandes."""

        # Creation de la fenetre du jeu
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        # Horloge permettant de controler le nombre d'images par seconde
        self.clock = pygame.time.Clock()

        # Initialisation des composants selon l'architecture MVC
        self.model = GameModel()
        self.view = GameView(self.screen)
        self.input_handler = InputHandler()

        # Variable indiquant si le jeu doit continuer a fonctionner
        self.running = True

    def run(self) -> None:
        """Execute la boucle principale du jeu."""

        while self.running:
            # Gestion des evenements (clavier, fermeture de fenetre)
            self.handle_events()

            # Mise a jour de l'etat du jeu
            self.update()

            # Affichage du nouvel etat a l'ecran
            self.render()

            # Limitation de la frequence d'affichage
            self.clock.tick(FPS)

    def handle_events(self) -> None:
        """Recupere et traite les evenements pygame."""

        for event in pygame.event.get():

            # Fermeture du jeu lorsque la fenetre est fermee
            if event.type == pygame.QUIT:
                self.quit()

            # Traitement des touches appuyees
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

    def handle_keydown(self, key: int) -> None:
        """Gere les touches utilisees dans les menus et pendant la course."""

        # Commandes disponibles dans le menu principal
        if self.model.state == GameState.MENU:

            if key == pygame.K_RETURN:
                # Chargement du circuit et lancement de la course
                self.model.load_circuit()
                self.model.state = GameState.RACING

            elif key == pygame.K_ESCAPE:
                # Fermeture du programme depuis le menu
                self.quit()

        # Retour au menu principal avec Echap pendant la course
        elif self.model.state == GameState.RACING and key == pygame.K_ESCAPE:
            self.model.state = GameState.MENU

    def update(self) -> None:
        """Met a jour les commandes des joueurs et le modele du jeu."""

        # La simulation ne progresse que pendant une course
        if self.model.state != GameState.RACING:
            return

        # Parcours des voitures des deux joueurs
        # enumerate commence a 1 pour identifier les joueurs
        for player_id, car in enumerate(self.model.cars, start=1):

            # Lecture des commandes du joueur correspondant
            commands = self.input_handler.get_inputs(player_id)

            # Application des commandes a sa voiture
            self.apply_input(car, commands)

        # Mise a jour des positions et de l'etat general du jeu
        self.model.update()

    def apply_input(self, car, player_input: dict[str, bool]) -> None:
        """Applique les commandes du joueur a sa voiture."""

        # Acceleration vers l'avant
        if player_input["accelerate"]:
            car.accelerate()

        # Freinage ou marche arriere
        if player_input["brake"]:
            car.brake()

        # Braquage vers la gauche
        if player_input["left"]:
            car.turn(-1)

        # Braquage vers la droite
        if player_input["right"]:
            car.turn(1)

    def render(self) -> None:
        """Demande a la vue de dessiner l'etat actuel du jeu."""

        self.view.draw(self.model)

    def quit(self) -> None:
        """Arrete la boucle principale et ferme pygame."""

        # Arret de la boucle du jeu
        self.running = False

        # Liberation des ressources pygame
        pygame.quit()

        # Fermeture du programme Python
        sys.exit()
