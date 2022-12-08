"""Bill of materials converters."""

from __future__ import annotations

from cq_warehouse.fastener import Nut, Screw, Washer

from osr_mechanical.bom.parts import PartIdentifier, PartTypes
from osr_warehouse.fasteners import MetricBoltSpecification as MetricBoltSpec


class FastenerToPart:
    """Convert a cq_warehouse fastner to an internal part."""

    DESCRIPTION: dict[str, str] = {
        "iso4762": "hexagon socket head cap screw",
        "iso7093": "flat washer",
    }
    ABBREVIATION: dict[str, str] = {
        "iso4762": "SHC",
        "iso7093": "F",
    }

    def __init__(self) -> None:
        """Initialise FastenerToPart."""
        self.part_type = PartTypes.fastner

    def convert(self, fastener: Screw | Nut | Washer) -> PartIdentifier:
        """Generate internal part from cq_warehouse fastener."""
        if isinstance(fastener, Screw):
            return self.screw(fastener)
        if isinstance(fastener, Washer):
            return self.washer(fastener)

        raise NotImplementedError("Unsupported fastener type.")

    def screw(self, screw: Screw) -> PartIdentifier:
        """Generate internal part for a screw."""
        shaft = MetricBoltSpec.split_shaft_pitch(screw.size).pop(0)
        description = (
            f"{screw.size}×{screw.length} {screw.fastener_type.upper()} "
            f"{self.DESCRIPTION[screw.fastener_type]}."
        )

        return PartIdentifier(
            self.part_type,
            f"S{self.ABBREVIATION[screw.fastener_type]}{shaft}X{screw.length}",
            description,
        )

    def washer(self, washer: Washer) -> PartIdentifier:
        """Generate internal part for a washer."""
        description = (
            f"{washer.size} "
            + "{d1}×{d2}×{h} ".format(**washer.washer_data)
            + f"{washer.fastener_type.upper()} "
            + f"{self.DESCRIPTION[washer.fastener_type]}."
        )

        return PartIdentifier(
            self.part_type,
            f"W{self.ABBREVIATION[washer.fastener_type]}{washer.size}",
            description,
        )
