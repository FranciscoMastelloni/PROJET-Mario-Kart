# Kart-Engine v2.3
"""Verification des contraintes d'organisation du projet."""

import ast
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ProjectStructureTests(unittest.TestCase):
    """Verifie les marqueurs imposes et les composants du projet."""

    def test_python_headers(self):
        for path in ROOT.rglob('*.py'):
            self.assertEqual(path.read_text(encoding='utf-8').splitlines()[0],
                             '# Kart-Engine v2.3', str(path))

    def test_grip_scale_defined_once(self):
        definitions = []
        for path in ROOT.rglob('*.py'):
            tree = ast.parse(path.read_text(encoding='utf-8'))
            for node in ast.walk(tree):
                if isinstance(node, (ast.Assign, ast.AnnAssign)):
                    targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                    if any(isinstance(t, ast.Name) and t.id == 'GRIP_SCALE' for t in targets):
                        definitions.append(str(path.relative_to(ROOT)))
        self.assertEqual(definitions, ['model/physics.py'])

    def test_initial_mvc_classes_kept(self):
        for path, class_name in [
            ('model/car.py', 'Car'),
            ('model/circuit.py', 'Circuit'),
            ('model/road_tile.py', 'RoadTile'),
            ('model/game_model.py', 'GameModel'),
            ('controller/input_handler.py', 'InputHandler'),
            ('controller/game_controller.py', 'GameController'),
            ('view/game_view.py', 'GameView'),
        ]:
            tree = ast.parse((ROOT / path).read_text(encoding='utf-8'))
            self.assertIn(class_name, [node.name for node in tree.body
                                       if isinstance(node, ast.ClassDef)])


if __name__ == '__main__':
    unittest.main()
