# Kart-Engine v2.3
"""Tests de physique sans dependance a la fenetre pygame."""

import math
import unittest
from types import SimpleNamespace

from model.physics import CarPhysics, GRIP_SCALE
from constants import CAR_MAX_SPEED, CAR_MAX_REVERSE_SPEED


def make_car(**changes):
    """Cree un etat minimal pour tester le calcul physique."""
    values = dict(
        x=500.0, y=500.0, vx=0.0, vy=0.0, angle=0.0,
        throttle=0, steering=0, is_drifting=False, slip_angle=0.0,
    )
    values.update(changes)
    return SimpleNamespace(**values)


def advance(car, steps=120, dt=1/60):
    """Simule un certain nombre d'images."""
    physics = CarPhysics()
    for _ in range(steps):
        physics.update(car, dt)
    return car


class CarPhysicsTests(unittest.TestCase):
    """Verifie la dynamique : marche avant, arriere, freinage et glissement."""

    def test_grip_scale_exact(self):
        self.assertEqual(GRIP_SCALE, 0.87)

    def test_accelerates_forward(self):
        car = advance(make_car(throttle=1))
        self.assertLess(car.y, 500)
        self.assertLess(car.vy, 0)

    def test_brake_decelerates_forward_motion(self):
        car = make_car(vy=-180, throttle=-1)
        advance(car, steps=15)
        self.assertLess(abs(car.vy), 180)

    def test_reverse_works(self):
        car = advance(make_car(throttle=-1))
        self.assertGreater(car.y, 500)
        self.assertGreater(car.vy, 0)
        self.assertLessEqual(car.vy, CAR_MAX_REVERSE_SPEED + 1)

    def test_turn_right(self):
        car = advance(make_car(throttle=1, steering=1), steps=35)
        self.assertGreater(car.angle, 0)
        self.assertNotEqual(car.x, 500)

    def test_turn_left(self):
        car = advance(make_car(throttle=1, steering=-1), steps=35)
        self.assertGreater(car.angle, 180)
        self.assertNotEqual(car.x, 500)

    def test_reverse_turning_inverts_yaw(self):
        car = make_car(vy=90, steering=1)
        advance(car, steps=5)
        self.assertGreater(car.angle, 180)

    def test_air_resistance_slows_car(self):
        car = make_car(vx=140, throttle=0)
        advance(car, steps=50)
        self.assertLess(abs(car.vx), 140)

    def test_speed_limit(self):
        car = advance(make_car(throttle=1), steps=900)
        self.assertLessEqual(math.hypot(car.vx, car.vy), CAR_MAX_SPEED * 1.1 + 1)

    def test_drift_is_automatic_while_turning(self):
        car = make_car(throttle=1)
        advance(car, steps=70)
        car.steering = 1
        observed = False
        for _ in range(180):
            advance(car, steps=1)
            observed |= car.is_drifting
        self.assertTrue(observed)

    def test_drift_recovers_when_straight(self):
        car = make_car(throttle=1)
        advance(car, steps=70)
        car.steering = 1
        for _ in range(160):
            advance(car, steps=1)
            if car.is_drifting:
                break
        self.assertTrue(car.is_drifting)
        car.steering = 0
        car.throttle = 0
        advance(car, steps=250)
        self.assertFalse(car.is_drifting)

    def test_zero_delta_does_nothing(self):
        car = make_car(throttle=1, steering=1)
        before = vars(car).copy()
        CarPhysics().update(car, 0)
        self.assertEqual(vars(car), before)


if __name__ == '__main__':
    unittest.main()
