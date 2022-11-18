"""Bill of materials parts classes."""

from dataclasses import dataclass
from enum import Enum
from typing import Literal, Optional


@dataclass
class PartType:
    """Internal part type schema."""

    abbreviation: str
    name: str
    description: str


@dataclass
class PartTypes:
    """Internal part types."""

    additive = PartType(
        abbreviation="A",
        name="Additive manufactured",
        description=(
            "Parts manufactured with an additive technique such as 3D printing."
        ),
    )
    din = PartType(
        abbreviation="D",
        name="DIN rail components",
        description="DIN rails and related components.",
    )
    electronic = PartType(
        abbreviation="E",
        name="Electronic module",
        description="Electronic modules and boards.",
    )
    fastner = PartType(
        abbreviation="F",
        name="Fastner",
        description="Fasteners including bolts, nuts, and washers.",
    )
    linear_motion = PartType(
        abbreviation="L",
        name="Linear motion component",
        description=(
            "Linear motion components are often available from "
            "3D printer component suppliers."
        ),
    )
    tslot = PartType(
        abbreviation="T",
        name="T-slot or V-slot component",
        description="T-slot components including extrusions, brackets, and slot nuts.",
    )


class Commodity(Enum):
    """Commodity types."""

    ASSEMBLY = "assembly or sub-assembly"
    CONSUMABLE = "consumable"
    FABRICATED = "fabricated"
    PURCHASED = "purchased"
    TOOL = "tool, jig, or fixture"


@dataclass
class PartIdentifier:
    """Internal part identifier.

    Parts are identified using a significant part numbering system.
    """

    type: PartType
    number: str
    commodity_type: Commodity
    description: str
    suffix: Optional[str] = None

    def __str__(self) -> str:
        """Part number as a string."""
        part_number = f"{self.type.abbreviation}-{self.number}"

        if self.suffix is None:
            return part_number

        return f"{part_number}-{self.suffix}"


@dataclass
class NauticalSide:
    """Side, either port or starboard."""

    name: str
    abbreviation: str
    identifier: Literal["P", "S"]


port = NauticalSide("port", "port", "P")
starboard = NauticalSide("starboard", "stbd", "S")
