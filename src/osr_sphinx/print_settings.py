"""3D printer settings."""

from __future__ import annotations

from docutils import nodes
from docutils.parsers.rst import Directive, directives


def choice_yes_no(argument: str) -> str:
    """Directive option utility ("yes", "no").

    Option validation whose argument must be either "yes" or "no".
    """
    result: str = directives.choice(argument, ("yes", "no"))
    return result


class PrintSettings(Directive):
    """3D printer settings directive."""

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    option_spec = {
        "infill": directives.percentage,
        "filament-material": directives.unchanged,
        "nozzle-diameter": float,
        "layer-height": float,
        "rafts": choice_yes_no,
        "supports": choice_yes_no,
    }

    def data(self) -> dict[str, tuple[str, str | None]]:
        """Printer settings data."""
        data = {
            "Infill": (self.options.get("infill", 100), "%"),
            "Filament material": (self.options.get("filament-material", "PLA"), None),
            "Nozzle diameter": (self.options.get("nozzle-diameter", 0.4), "mm"),
            "Layer height": (self.options.get("layer-height", 0.2), "mm"),
            "Rafts": (self.options.get("rafts", "no"), None),
            "Supports": (self.options.get("supports", "no"), None),
        }

        return data

    def run(self) -> list[nodes.paragraph | nodes.table]:
        """Create 3D printer settings table."""
        stl_file_name = self.arguments[0]

        paragraph_file_name = nodes.paragraph(
            "",
            "",
            nodes.inline(text="File: "),
            nodes.literal(text=f"release-archive:/{stl_file_name}"),
        )

        dl_classes = ["field-list", "simple"]
        dl_items = []

        data = self.data()
        for term, definition in data.items():
            value, unit = definition
            if unit:
                value = f"{value} {unit}"
            dl_items.append(
                nodes.definition_list_item(
                    "",
                    nodes.term(text=term),
                    nodes.definition(
                        "",
                        nodes.paragraph("", "", nodes.inline(text=value)),
                    ),
                )
            )

        return [
            paragraph_file_name,
            nodes.definition_list("", *dl_items, classes=dl_classes),
        ]
