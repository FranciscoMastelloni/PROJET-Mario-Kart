# PROJET Mario Kart — dynamique des voitures

Cette version correspond **uniquement** a la fonctionnalite « Dynamique des
voitures (accelerer, freiner, tourner, mecanismes de derapage) ». Elle utilise
comme point de depart le ZIP `marioo_kart` fourni par l'enseignant et conserve
son organisation modele / vue / controleur (MVC).

## Installation et lancement

Python 3.12 ou plus recent est recommande.

```bash
python -m pip install -r requirements.txt
python main.py
```

Sur le Mac avec Anaconda :

```bash
/opt/anaconda3/bin/python -m pip install -r requirements.txt
/opt/anaconda3/bin/python main.py
```

La fenetre affiche d'abord le menu. Appuyer sur Entree pour demarrer.

## Commandes

| Action | Joueur 1 | Joueur 2 |
|---|---|---|
| Accelerer | Z ou W | Fleche haut |
| Freiner / reculer | S | Fleche bas |
| Tourner a gauche | Q ou A | Fleche gauche |
| Tourner a droite | D | Fleche droite |
| Revenir au menu | Echap | Echap |

## Fonctionnalite ajoutee

- Deux voitures controlees independamment sur un meme clavier.
- Acceleration et freinage progressifs, vitesse limitee en marche avant/arriere.
- Braquage dependant de la vitesse, avec inversion en marche arriere.
- Representation de la vitesse par un vecteur 2D distinct de l'orientation.
- Derapage declenche automatiquement en cas d'ecart important entre la
  direction de la voiture et la trajectoire, avec correction d'adherence et
  frottements. Aucun bouton special n'est necessaire.
- Indication de la vitesse et du statut `DERAPAGE` ou `ADHERENCE` a l'ecran.
- Grille de route de test, issue du code de depart : pas de terrains differencies,
  pas de checkpoints ou de boosts a cette etape.

## Structure du code

- `main.py` : point d'entree du professeur.
- `controller/game_controller.py` : boucle pygame et application des commandes.
- `controller/input_handler.py` : lecture des touches pour les deux joueurs.
- `model/car.py` : classe voiture, etat et sprite.
- `model/physics.py` : calcul des mouvements, inertie, adhesion et glissement.
- `model/game_model.py` : piste de test et mise a jour des deux voitures.
- `model/circuit.py`, `model/road_tile.py` : grille de depart du professeur.
- `view/game_view.py` : menu et rendu graphique pygame.

La constante `GRIP_SCALE = 0.87` est definie uniquement dans le module de
physique. Chaque fichier Python contient l'en-tete impose par le sujet.

## Verification

Lancer les tests automatises :

```bash
python -m unittest discover -s tests -v
```

Les tests automatises verifient la logique numerique de la physique. Le
fonctionnement de la fenetre et des touches doit egalement etre valide
manuellement sur un ordinateur possedant pygame.



## Fonctionnalites non incluses

Cette etape ne comporte pas les differents terrains, les points de passage,
les lignes d'arrivee, les boosts, les objets ou les tours de piste. Ces
fonctionnalites ne sont pas necessaires pour tester la dynamique des voitures.
