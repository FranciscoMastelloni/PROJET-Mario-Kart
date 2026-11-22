# Kart-Engine v2.3
"""Moteur de dynamique 2D, independant de pygame.

Le calcul distingue l'orientation de la carrosserie et la direction de la
vitesse. Cet ecart est a l'origine du derapage automatique.
"""

from math import atan2, cos, degrees, hypot, radians, sin

from constants import (
    CAR_ACCELERATION,
    CAR_AIR_DRAG,
    CAR_BRAKING,
    CAR_MAX_REVERSE_SPEED,
    CAR_MAX_SPEED,
    CAR_ROLLING_RESISTANCE,
    CAR_TURN_REFERENCE,
    CAR_TURN_SPEED,
)

# Valeur demandee dans l'enonce. Une seule definition, dans le moteur physique.
GRIP_SCALE = 0.87

# Parametres provisoires pour une piste entierement en route.
# Les differents terrains seront traites dans une autre fonctionnalite.
ROAD_GRIP = 5.0  # correction du glissement lateral (s^-1)
DRIFT_GRIP_RATIO = 0.22
DRIFT_FRICTION = 0.9  # freinage additionnel pendant le derapage (s^-1)
DRIFT_START_ANGLE = 13.0  # degres
DRIFT_END_ANGLE = 7.0
DRIFT_START_SPEED = 85.0  # pixels/s
DRIFT_END_SPEED = 45.0


class CarPhysics:
    """Met a jour une voiture avec une integration explicite en temps."""

    def update(self, car, dt: float) -> None:
        """Fait evoluer la voiture pendant ``dt`` secondes.

        Le calcul utilise les champs x, y, vx, vy, angle, throttle,
        steering, is_drifting et slip_angle de la voiture.
        L'angle est mesure dans le sens horaire depuis le haut de l'ecran.
        """
        if dt <= 0:
            return
        dt = min(dt, 0.05)  # Evite les sauts de simulation apres une pause.

        # Projection de la vitesse sur la direction actuelle de la voiture.
        a = radians(car.angle)
        fx, fy = sin(a), -cos(a)  # direction vers l'avant de la voiture
        forward_speed = car.vx * fx + car.vy * fy
        speed = hypot(car.vx, car.vy)

        # Un volant braque davantage quand la voiture roule. En reculant,
        # le sens de rotation du vehicule est inverse.
        if abs(forward_speed) >= 4.0:
            direction = 1.0 if forward_speed > 0 else -1.0
        elif car.throttle != 0:
            direction = 1.0 if car.throttle > 0 else -1.0
        else:
            direction = 0.0
        steer_factor = min(1.0, speed / CAR_TURN_REFERENCE)
        car.angle = (
            car.angle + car.steering * direction * CAR_TURN_SPEED
            * steer_factor * dt
        ) % 360.0

        # Accelerer ou freiner dans l'axe de la nouvelle orientation.
        a = radians(car.angle)
        fx, fy = sin(a), -cos(a)
        acceleration = CAR_ACCELERATION if car.throttle > 0 else CAR_BRAKING
        car.vx += fx * acceleration * car.throttle * dt
        car.vy += fy * acceleration * car.throttle * dt

        # Resistance au roulement et resistance de l'air.
        speed = hypot(car.vx, car.vy)
        damping = max(
            0.0, 1.0 - (CAR_ROLLING_RESISTANCE + CAR_AIR_DRAG * speed) * dt
        )
        car.vx *= damping
        car.vy *= damping

        # Vitesse longitudinale et vitesse laterale par rapport a la voiture.
        # Les deux composantes ne sont pas necessairement alignees avec la
        # carrosserie : on peut tourner sans changer immediatement de trajectoire.
        rx, ry = cos(a), sin(a)  # vecteur vers la droite de la voiture
        longitudinal = car.vx * fx + car.vy * fy
        lateral = car.vx * rx + car.vy * ry
        speed = hypot(car.vx, car.vy)
        car.slip_angle = degrees(atan2(abs(lateral), abs(longitudinal)))

        # Hysteresis pour eviter que l'etat de derapage oscille a chaque image.
        if car.is_drifting:
            if speed < DRIFT_END_SPEED or car.slip_angle < DRIFT_END_ANGLE:
                car.is_drifting = False
        elif speed > DRIFT_START_SPEED and car.slip_angle > DRIFT_START_ANGLE:
            car.is_drifting = True

        # L'adherence ramene progressivement la vitesse vers l'axe du vehicule.
        # Pendant le drift, la correction est plus faible et l'inertie domine.
        grip = ROAD_GRIP * GRIP_SCALE
        if car.is_drifting:
            grip *= DRIFT_GRIP_RATIO
        correction = min(1.0, grip * dt)
        car.vx -= lateral * rx * correction
        car.vy -= lateral * ry * correction

        # Frottement additionnel lorsqu'une voiture glisse.
        if car.is_drifting:
            drift_damping = max(0.0, 1.0 - DRIFT_FRICTION * dt)
            car.vx *= drift_damping
            car.vy *= drift_damping

        # Limitation des vitesses avant et arriere suivant le nez de la voiture.
        longitudinal = car.vx * fx + car.vy * fy
        if longitudinal > CAR_MAX_SPEED:
            excess = longitudinal - CAR_MAX_SPEED
            car.vx -= excess * fx
            car.vy -= excess * fy
        elif longitudinal < -CAR_MAX_REVERSE_SPEED:
            excess = longitudinal + CAR_MAX_REVERSE_SPEED
            car.vx -= excess * fx
            car.vy -= excess * fy

        # Une limite sur la vitesse totale evite les trajectoires aberrantes.
        speed = hypot(car.vx, car.vy)
        if speed > CAR_MAX_SPEED * 1.1:
            factor = CAR_MAX_SPEED * 1.1 / speed
            car.vx *= factor
            car.vy *= factor

        car.x += car.vx * dt
        car.y += car.vy * dt
