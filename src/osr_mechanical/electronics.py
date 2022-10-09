"""Electronics mounted on DIN rail."""

import cadquery as cq
from cq_electronics.mechanical.din_clip import DinClip
from cq_electronics.mechanical.din_rail import TopHat
from cq_electronics.rpi.rpi3b import RPi3b
from cq_electronics.sourcekit.pitray_clip import PiTrayClip

from osr_mechanical.frame import Frame
from osr_warehouse.materials import COLORS


class ControlElectronics:
    """Control electronics mounted on DIN rail."""

    END_CLEARANCE = 2

    def __init__(self) -> None:
        """Initialise electronics assembly."""
        self.din_rail_length = Frame.WIDTH - (2 * self.END_CLEARANCE)

        self.din_rail = TopHat(self.din_rail_length)
        self.raspberry_pi = RPi3b()
        self.pitray_clip = PiTrayClip()

        self._cq_object = self.make()

    @property
    def cq_object(self) -> cq.Assembly:
        """Get CadQuery object."""
        return self._cq_object

    def make(self) -> cq.Assembly:
        """Make control electronics assembly."""
        rpi_x_offset = -50

        pitray_clip_z = (
            PiTrayClip.HEIGHT / 2
            + DinClip.HEIGHT
            - DinClip.RAIL_APERTURE_DEPTH
            + self.din_rail.depth / 2
        )

        rpi_x = -(
            abs(rpi_x_offset)
            - PiTrayClip.WIDTH / 2
            + self.pitray_clip.pcb_screw_cylinder_length
            + RPi3b.THICKNESS / 2
            + RPi3b.SOLDER_MASK_THICKNESS
        )
        rpi_z = (
            RPi3b.HEIGHT / 2
            - RPi3b.HOLE_OFFSET_FROM_EDGE
            + self.din_rail.depth / 2
            + DinClip.HEIGHT
            - DinClip.RAIL_APERTURE_DEPTH
            + PiTrayClip.HEIGHT
            - self.pitray_clip.pcb_screw_cylinder_from_edge
        )

        result = (
            cq.Assembly()
            .add(
                self.din_rail.cq_object,
                name="electronics_control__din_rail",
                color=cq.Color(*COLORS["aluminium_anodised_natural"]),
            )
            .add(
                self.pitray_clip.cq_object,
                name="electronics_control__pitray_clip",
                loc=cq.Location(
                    cq.Vector(rpi_x_offset, -8, pitray_clip_z),
                    cq.Vector(0, 0, 1),
                    -90,
                ),
            )
            .add(
                self.raspberry_pi.cq_object,
                name="electronics_control__rpi",
                loc=cq.Location(
                    cq.Vector(rpi_x, 2, rpi_z),
                    cq.Vector(0, 1, 0),
                    -90,
                ),
            )
        )

        return result
