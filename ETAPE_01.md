# Contribution 01 — Commandes et déplacements de deux voitures

Cette version est un **jalon intermédiaire**, construit à partir du code de départ
fourni pour le projet POO. Elle ne comprend ni terrains spéciaux, ni drift,
ni tours/checkpoints, ni boosts, ni objets.

## Fichiers concernés

- `constants.py` : paramètres d'accélération, de braquage et de frottement.
- `controller/input_handler.py` : touches des deux joueurs.
- `controller/game_controller.py` : applique les commandes aux deux voitures.
- `model/car.py` : déplacement dans la direction du cap, freinage et marche arrière.
- `model/game_model.py` : création et mise à jour des deux voitures.
- `view/game_view.py` : affichage des deux voitures et rappel des commandes.

L'en-tête `# Kart-Engine v2.3` a été ajouté dans les autres fichiers Python
sans changer leur logique. La correction des indices dans `game_model.py`
permet d'éviter la confusion entre lignes et colonnes.

## Lancement

```bash
python -m pip install -r requirements.txt
python main.py
```

J1 : Z/W pour accélérer, S pour freiner/reculer, Q/A et D pour tourner.
J2 : flèches. Entrée pour démarrer, Échap pour revenir au menu.

## Vérifications manuelles

1. Les deux voitures sont visibles en rouge et bleu.
2. Les deux joueurs peuvent accélérer simultanément.
3. En tournant, les voitures changent de cap et de trajectoire.
4. En freinant assez longtemps, elles reculent.
5. En relâchant les touches, elles ralentissent progressivement.
6. Échap revient au menu.

## IA et travail personnel

Le sujet exige de déclarer les usages d'IA dans le `README.md` final.
Cette contribution a été préparée avec l'aide de ChatGPT pour la conception
et l'écriture du code. Avant de la publier comme travail réalisé, il faut
la tester, relire chaque modification et pouvoir expliquer chaque méthode.
