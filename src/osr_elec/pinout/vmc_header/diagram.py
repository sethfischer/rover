"""Vehicle Management Computer GPIO header pinout diagram."""

from pinout.components.layout import Diagram_2Rows
from pinout.components.legend import Legend
from pinout.components.pinlabel import PinLabelGroup
from pinout.core import Group, Image

# this is a collection of definition files rather than a Python module
import data  # type: ignore[import-not-found] # isort: skip

diagram = Diagram_2Rows(685, 730, 650, "diagram")
diagram.add_stylesheet("styles.css", embed=True)

graphic = diagram.panel_01.add(Group(310, 30))

hardware = graphic.add(Image("pin-header-2x20-p2.54mm-vertical.svg", embed=True))
hardware.add_coord("pin_1", 60, 15)
hardware.add_coord("pin_2", 0, 15)
hardware.add_coord("pin_pitch_v", 0, 30)
hardware.add_coord("pin_pitch_h", 30, 0)

# labels for even pins
graphic.add(
    PinLabelGroup(
        x=hardware.coord("pin_1").x,
        y=hardware.coord("pin_1").y,
        pin_pitch=hardware.coord("pin_pitch_v", raw=True),
        label_start=(60, 0),
        label_pitch=(0, 30),
        labels=data.even_pins,
    )
)

# labels for odd pins
graphic.add(
    PinLabelGroup(
        x=hardware.coord("pin_2").x,
        y=hardware.coord("pin_2").y,
        pin_pitch=hardware.coord("pin_pitch_v", raw=True),
        label_start=(60, 0),
        label_pitch=(0, 30),
        scale=(-1, 1),
        labels=data.odd_pins,
    )
)

legend = diagram.panel_02.add(
    Legend(
        data.legend,
        x=8,
        y=8,
        max_height=80,
    )
)
