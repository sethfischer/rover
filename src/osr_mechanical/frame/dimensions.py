"""Frame dimensions."""

from dataclasses import dataclass, field

from osr_warehouse.alexco.vslot import Vslot2020


@dataclass(frozen=True)
class FrameDimensions:
    """Frame dimensions."""

    tslot_width: float

    HEIGHT: int = 115
    LENGTH: int = 439
    WIDTH: int = 285

    TRANSOM_HEIGHT: int = 75
    TRANSOM_LENGTH: int = 48

    ROCKER_AXLE_CLEARANCE: int = 3
    ROCKER_AXLE_DIAMETER: int = 8
    ROCKER_AXLE_DISTANCE_FROM_FORE: int = 165

    DIFFERENTIAL_PIVOT_BEAM_OFFSET: int = 0
    DIFFERENTIAL_PIVOT_DISTANCE_FROM_FORE: int = 250

    BEAM_SIDE_LENGTH: float = field(init=False)
    LATERAL_BEAM_LENGTH: float = field(init=False)
    PILLAR_HEIGHT: float = field(init=False)

    def __post_init__(self) -> None:
        """Set calculated values for frame."""
        object.__setattr__(
            self,
            "BEAM_SIDE_LENGTH",
            self.LENGTH + self.TRANSOM_LENGTH - self.tslot_width,
        )
        object.__setattr__(
            self,
            "LATERAL_BEAM_LENGTH",
            self.WIDTH - self.tslot_width * 2,
        )
        object.__setattr__(
            self,
            "PILLAR_HEIGHT",
            self.HEIGHT - self.tslot_width * 2,
        )


FRAME_DIMENSIONS = FrameDimensions(tslot_width=Vslot2020.WIDTH)
