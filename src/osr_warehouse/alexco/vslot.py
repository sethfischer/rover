"""Aluminium Extrusion Company V-slot extrusions."""

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

    PROFILE: cq.Sketch

    WIDTH = HEIGHT = 20
    COUNTERBORE_DEPTH = 6

    def __new__(cls) -> "Vslot2020":
        """Initialise Vslot2020."""
        if cls._instance is None:
            cls._instance = super(Vslot2020, cls).__new__(cls)

            profile = Vslot2020Profile().cq_object
            setattr(cls, "PROFILE", profile)

        return cls._instance

    def make(self, length: float) -> cq.Workplane:
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

    PROFILE: cq.Sketch

    WIDTH = 20
    HEIGHT = 40
    DISTANCE_BETWEEN_CENTERS = 20
    COUNTERBORE_DEPTH = 6

    def __new__(cls) -> "Vslot2040":
        """Initialise Vslot2040."""
        if cls._instance is None:
            cls._instance = super(Vslot2040, cls).__new__(cls)

            profile = Vslot2040Profile().cq_object
            setattr(cls, "PROFILE", profile)

        return cls._instance

    def make(self, length: float) -> cq.Workplane:
        """Return extrusion of specified length."""
        return cq.Workplane().placeSketch(self.PROFILE).extrude(length)
