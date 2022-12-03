"""Test bill of materials."""

import cadquery as cq

from osr_mechanical.bom.bom import Bom, BomEntry
from osr_mechanical.bom.parts import PartIdentifier, PartType


class TestBom:
    """Test bill of materials."""

    def setup_method(self) -> None:
        """Initialise."""
        self.part_type = PartType("TT", "Test name", "Test description.")

        self.part_1 = PartIdentifier(self.part_type, "1", "Part 1 description.")
        self.part_2 = PartIdentifier(self.part_type, "2", "Part 2 description.")
        self.part_3 = PartIdentifier(self.part_type, "2", "Part 2 description.")

        self.cq_object = cq.Workplane().box(1, 1, 1)
        self.bom_parts = {
            "part_1": self.part_1,
            "part_2": self.part_2,
        }

        self.assembly = (
            cq.Assembly(metadata={Bom.PARTS_KEY: self.bom_parts})
            .add(self.cq_object, name="part_1")
            .add(self.cq_object, name="part_2")
        )

    def test_length(self) -> None:
        """Test length of BOM."""
        bom = Bom(self.assembly)

        assert 2 == len(bom)

    def test_quantity_of_part_1(self) -> None:
        """Test quantity of part 1."""
        bom = Bom(self.assembly)
        bom_entry: BomEntry = bom[str(self.part_1)]

        assert 1 == bom_entry.quantity

    def test_quantity_of_part_2(self) -> None:
        """Test quantity of part 1."""
        bom = Bom(self.assembly)
        bom_entry: BomEntry = bom[str(self.part_2)]

        assert 1 == bom_entry.quantity

    def test_part_multiples(self) -> None:
        """Test part multiples."""
        bom_parts = self.bom_parts
        bom_parts["part_3"] = self.part_3

        assembly = self.assembly.add(self.cq_object, name="part_3")
        assembly.metadata[Bom.PARTS_KEY] = bom_parts

        bom = Bom(assembly)
        bom_entry: BomEntry = bom[str(self.part_3)]

        assert 2 == len(bom)
        assert 2 == bom_entry.quantity
