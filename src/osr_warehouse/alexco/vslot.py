"""Aluminium Extrusion Company V-slot extrusions."""

from typing import Any

import cadquery as cq

from osr_warehouse.alexco.profiles20 import Vslot2020Profile, Vslot2040Profile


class Vslot2020:
    """2020 V-slot Aluminium Extrusion.

    This profile has a longitudinal slot in the center bore making it asymmetrical.

    To maximise bearing surface avoid counterbore holes on the side with the
    longitudinal slot.

    :Manufacturer: Aluminium Extrusion Company
    :Web: https://www.alexco.co.nz/
    :Part: AEC 2020
    """

    _instance = None

    PROFILE = None  # type: Any

    WIDTH = HEIGHT = 20
    COUNTERBORE_DEPTH = 6

    def __new__(cls):
        """Initialise profile."""
        if cls._instance is None:
            cls._instance = super(Vslot2020, cls).__new__(cls)

            profile = Vslot2020Profile().make()
            setattr(cls, "PROFILE", profile)

        return cls._instance

    def make(self, length: float):
        """Return extrusion of specified length."""
        return cq.Workplane().placeSketch(self.PROFILE).extrude(length)


class Vslot2040:
    """2040 V-slot Aluminium Extrusion.

    This profile has longitudinal slots in the center bore.

    To maximise bearing surface avoid counterbore holes on sides with the longitudinal
    slot.

    :Manufacturer: Aluminium Extrusion Company
    :Web: https://www.alexco.co.nz/
    :Part: AEC 2040
    """

    _instance = None

    PROFILE = None  # type: Any

    WIDTH = 20
    HEIGHT = 40
    DISTANCE_BETWEEN_CENTERS = 20
    COUNTERBORE_DEPTH = 6

    def __new__(cls):
        """Initialise profile."""
        if cls._instance is None:
            cls._instance = super(Vslot2040, cls).__new__(cls)

            profile = Vslot2040Profile().make()
            setattr(cls, "PROFILE", profile)

        return cls._instance

    def make(self, length: float):
        """Return extrusion of specified length."""
        return cq.Workplane().placeSketch(self.PROFILE).extrude(length)
