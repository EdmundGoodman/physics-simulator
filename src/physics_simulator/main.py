#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A simple n-body simulator in python."""

import sys
from math import cos, pi, sin, sqrt

from typing_extensions import Self

DIMENSIONS = 2
GRAVITATIONAL_CONSTANT = 0.01

INITIAL_MAX_MASS = 5
INITIAL_RADIUS = 100
INITIAL_RIGHT_VELOCITY = 0.1

VISUALISE: bool = True


class Body:
    """An object representing a celestial body."""

    def __init__(
        self,
        position: list[float],
        velocity: list[float],
        acceleration: list[float],
        mass: float,
    ) -> None:
        """Instantiate the body with values."""
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.mass = mass

    def update_acceleration(self, others: list[Self]) -> None:
        """Update the acceleration of the body due to the gravity of others."""
        self.acceleration = [0.0 for _ in range(DIMENSIONS)]

        for other in others:
            position_difference: list[float] = []
            distance = 0.0
            for i in range(DIMENSIONS):
                position_difference.append(self.position[i] - other.position[i])
                distance += (self.position[i] - other.position[i]) ** 2

            # Avoid divide by zero errors
            distance = max(sqrt(distance), 1e-5)

            if self.mass != 0:
                force = (
                    -1 * GRAVITATIONAL_CONSTANT * ((self.mass * other.mass) / distance)
                )
                acceleration = force / self.mass
                for i in range(DIMENSIONS):
                    self.acceleration[i] += (
                        acceleration * position_difference[i] / distance
                    )

    def update_velocity(self) -> None:
        """Update the velocity of the body from its acceleration."""
        for i in range(DIMENSIONS):
            self.velocity[i] += self.acceleration[i]

    def update_position(self) -> None:
        """Update the position of the body from its velocity."""
        for i in range(DIMENSIONS):
            self.position[i] += self.velocity[i]

    def __repr__(self) -> str:
        """Get a string representation of the body."""
        return str(self.position)


def get_starting_bodies(num_bodies: int) -> list[Body]:
    """Get the starting set of bodies for the simulation."""
    bodies: list[Body] = []
    for i in range(num_bodies):
        mass = (INITIAL_MAX_MASS / num_bodies) * (i + 1)
        offset = (i / num_bodies) * (2 * pi)
        bodies.append(
            Body(
                [INITIAL_RADIUS * sin(offset), INITIAL_RADIUS * cos(offset)],
                [INITIAL_RIGHT_VELOCITY, 0],
                [0, 0],
                mass,
            )
        )
    return bodies


def simulate(num_iterations: int, num_bodies: int) -> list[float]:
    """
    Run the simulation.

    Args:
    ----
        num_iterations: The number of iterations to run the simulation for.
        num_bodies: The number of bodies to simulate.

    Returns:
    -------
        A flat list of the final positions of all of the bodies.
    """
    bodies = get_starting_bodies(num_bodies)

    for _ in range(num_iterations):
        for body in bodies:
            body.update_acceleration([value for value in bodies if value != body])
        for body in bodies:
            body.update_velocity()
            body.update_position()

    result: list[float] = []
    for body in bodies:
        result.append(body.position[0])
        result.append(body.position[1])
    return result


def visualise(num_iterations: int, num_bodies: int) -> None:
    """
    Visualise the simulation.

    You don't need to keep this functionality, but it is quite cool to see what
    the simulation is doing...
    """
    if not VISUALISE:
        return

    from colorsys import hsv_to_rgb
    from turtle import color, dot, exitonclick, goto, ht, pendown, penup, speed, tracer

    speed(0)
    ht()
    tracer(num_bodies)

    bodies = get_starting_bodies(num_bodies)
    for i in range(num_iterations):
        for body in bodies:
            body.update_acceleration([value for value in bodies if value != body])
        for x, body in enumerate(bodies):
            body.update_velocity()
            body.update_position()

            if i % 30 == 0:
                penup()
                color(hsv_to_rgb(x / num_bodies, 1.0, 1.0))
                goto(*[body.position[i] for i in range(DIMENSIONS)])
                pendown()
                dot(int(body.mass * 5))
                penup()

    exitonclick()
    sys.exit()


def main() -> None:
    """Run the simulation."""
    num_iterations = 10_000
    num_bodies = 5

    # Optionally, visualise the simulation then exit. This is not part of the
    # testing procedure, so can be discarded/broken
    visualise(num_iterations, num_bodies)

    # Run the simulation if not visualising it
    result = simulate(num_iterations, num_bodies)
    print(result)


if __name__ == "__main__":
    main()
