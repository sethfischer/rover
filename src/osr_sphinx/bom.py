"""Bill of materials."""

from docutils import nodes
from docutils.parsers.rst import Directive

from osr_mechanical.bom.bom import Bom, BomBuilder


class BomTable(Directive):
    """Bill of materials table directive."""

    has_content = False
    required_arguments = 0
    optional_arguments = 1

    def run(self) -> list[nodes.paragraph | nodes.table]:
        """Create bill of materials table with summary."""
        if self.arguments:
            assembly_name = self.arguments[0]
            bom = self.build_bom(assembly_name)
        else:
            bom = self.build_bom()

        summary = self.summary(bom)
        table = self.table(bom)

        return [summary, table]

    @staticmethod
    def build_bom(assembly_name: str | None = None) -> Bom:
        """Build bill of materials."""
        builder = BomBuilder()

        if assembly_name:
            return builder.from_string(assembly_name)

        return builder.from_string()

    @staticmethod
    def summary(bom: Bom) -> nodes.paragraph:
        """Bill of materials summary."""
        return nodes.paragraph(text=f"Number of unique parts: {bom.part_count}")

    @staticmethod
    def table(bom: Bom) -> nodes.table:
        """Bill of materials table."""
        table = nodes.table()
        table_group = nodes.tgroup(cols=3)

        for _ in range(3):
            col_spec = nodes.colspec(colwidth=1)
            table_group.append(col_spec)
        table += table_group

        table_head = nodes.thead()
        table_group += table_head
        row = nodes.row()

        head_entry = nodes.entry()
        head_entry += nodes.paragraph(text="Part №")
        row += head_entry

        head_entry = nodes.entry()
        head_entry += nodes.paragraph(text="Qty.")
        row += head_entry

        head_entry = nodes.entry()
        head_entry += nodes.paragraph(text="Description")
        row += head_entry

        table_head.append(row)

        table_body = nodes.tbody()
        table_group += table_body

        rows = []
        for _identifier, bom_entry in bom.items():
            row = nodes.row()

            identifier_entry = nodes.entry()
            identifier_entry += nodes.paragraph(text=str(bom_entry.part.identifier))
            row += identifier_entry

            quantity_entry = nodes.entry()
            quantity_entry += nodes.paragraph(text=str(bom_entry.quantity))
            row += quantity_entry

            description_entry = nodes.entry()
            description_entry += nodes.paragraph(text=str(bom_entry.part.description))
            row += description_entry

            rows.append(row)

        table_body.extend(rows)

        return table
