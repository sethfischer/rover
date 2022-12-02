"""Bill of materials parts classes."""

from dataclasses import dataclass
from enum import Enum
from typing import Literal


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


class PartIdentifier:
    """Internal part identifier.

    Parts are identified using a significant part numbering system.
    """

    def __init__(
        self,
        prefix: PartType,
        root: str,
        description: str,
        commodity_type: Commodity = Commodity.PURCHASED,
        suffix: str = "",
    ) -> None:
        """Initialise."""
        self.prefix = prefix
        self.root = root
        self.description = description
        self.commodity_type = commodity_type
        self.suffix = suffix

    @property
    def root(self) -> str:
        """Part root."""
        return self._root

    @root.setter
    def root(self, value: str) -> None:
        """Part root setter."""
        self._root = value.upper()

    @property
    def suffix(self) -> str:
        """Part suffix."""
        return self._suffix

    @suffix.setter
    def suffix(self, value: str) -> None:
        """Part suffix setter."""
        self._suffix = value.upper()

    @property
    def identifier(self) -> str:
        """Part identifier as a string."""
        identifier = f"{self.prefix.abbreviation}-{self.root}"

        if self.suffix:
            return f"{identifier}-{self.suffix}"

        return identifier

    def __str__(self) -> str:
        """Part identifier as a string."""
        return self.identifier


@dataclass
class NauticalSide:
    """Side, either port or starboard."""

    name: str
    abbreviation: str
    identifier: Literal["P", "S"]


port = NauticalSide("port", "port", "P")
starboard = NauticalSide("starboard", "stbd", "S")
