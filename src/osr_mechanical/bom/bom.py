"""Bill of materials utilities."""

from __future__ import annotations

import csv
import importlib
import io
from collections import UserDict
from json import JSONEncoder, dumps
from typing import Any, Optional

import cadquery as cq
from cq_warehouse.fastener import Nut, Screw, Washer

from osr_mechanical.bom.converters import FastenerToPart
from osr_mechanical.bom.parts import Commodity, PartIdentifier, PartType


class BomEntry:
    """Bill of materials entry."""

    def __init__(self, part: PartIdentifier) -> None:
        """Initialise BomEntry."""
        self.part = part

        self.assemblies: dict[str, int] = {}

    @property
    def quantity(self) -> int:
        """Total count of parts."""
        return sum(self.assemblies.values())

    def increment(self, assembly_name: str) -> int:
        """Increment part count."""
        self.assemblies[assembly_name] = self.assemblies.get(assembly_name, 0) + 1

        return self.assemblies[assembly_name]


class Bom(UserDict[str, BomEntry]):
    """Bill of materials."""

    ENCODE_CSV = "csv"
    ENCODE_JSON = "json"

    PARTS_KEY = "osr_parts"

    def __init__(
        self, assembly: Optional[cq.Assembly] = None, deep: bool = True
    ) -> None:
        """Initialise Bom."""
        super().__init__()

        if assembly is not None:
            self.insert_assembly(assembly, deep=deep)

    def insert_part(self, part: PartIdentifier, assembly_name: str) -> None:
        """Insert part into bill of materials."""
        if part.identifier in self:
            self[part.identifier].increment(assembly_name)
        else:
            bom_entry = BomEntry(part)
            bom_entry.increment(assembly_name)
            self.__setitem__(part.identifier, bom_entry)

    def insert_assembly(self, assembly: cq.Assembly, deep: bool = True) -> None:
        """Insert assembly into bill of materials."""
        assemblies = self.list_assemblies(assembly, deep=deep)
        cq_warehouse_converter = FastenerToPart()

        for assembly in assemblies:
            for key, value in assembly.metadata.items():
                if isinstance(value, (Screw, Nut, Washer)):
                    self.insert_part(
                        cq_warehouse_converter.convert(value), assembly.name
                    )
                if self.PARTS_KEY == key:
                    for name, part in value.items():
                        self.insert_part(part, assembly.name)

    @staticmethod
    def list_assemblies(assembly: cq.Assembly, deep: bool = True) -> list[cq.Assembly]:
        """Create list of assemblies."""
        assemblies = []

        if deep:
            for _name, _sub_assembly in assembly.traverse():
                assemblies.append(_sub_assembly)
        else:
            assemblies.append(assembly)

        return assemblies

    @property
    def part_count(self):
        """Count of unique parts."""
        return len(self.data)

    def encode(self, encoder: Optional[str] = None) -> str:
        """Get bill of materials, optionally encode to CSV or JSON."""
        if self.ENCODE_JSON == encoder or encoder is None:
            return dumps(self.data, cls=BomEncoder)

        if self.ENCODE_CSV == encoder:
            mem_file = io.StringIO()
            writer = csv.writer(mem_file)

            header = ["part_number", "quantity", "commodity_type", "description"]
            writer.writerow(header)

            for part_number, bom_entry in self.data.items():
                writer.writerow(
                    [
                        part_number,
                        bom_entry.quantity,
                        bom_entry.part.commodity_type.value,
                        bom_entry.part.description,
                    ]
                )

            return mem_file.getvalue()

        raise ValueError(
            f'Formatter must be one of: "{self.ENCODE_CSV}", "{self.ENCODE_JSON}".'
        )


class BomBuilder:
    """BOM builder."""

    @staticmethod
    def from_string(assembly_name: str = "final.FinalAssembly") -> Bom:
        """Create BOM."""
        module_name, class_name = f"osr_mechanical.{assembly_name}".rsplit(".", 1)

        module = importlib.import_module(module_name)
        assembly_container = getattr(module, class_name)

        assembly = assembly_container().cq_object

        return Bom(assembly)


class BomEncoder(JSONEncoder):
    """Bill of materials encoder."""

    def default(self, obj: Commodity | Bom | BomEntry | PartIdentifier) -> Any:
        """Bill of materials encoding."""
        if isinstance(obj, Commodity):
            return str(obj.value)
        if isinstance(obj, Bom):
            return vars(obj)
        if isinstance(obj, BomEntry):
            return vars(obj)
        if isinstance(obj, PartIdentifier):
            return {
                "commodity_type": obj.commodity_type,
                "description": obj.description,
            }
        if isinstance(obj, PartType):
            return vars(obj)

        return JSONEncoder.default(self, obj)
