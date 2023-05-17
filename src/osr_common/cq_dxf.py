"""DXF utilities."""

from __future__ import annotations

from typing import Any, Literal

import cadquery as cq
import ezdxf
from cadquery import Plane
from cadquery.occ_impl.exporters.utils import toCompound
from cadquery.occ_impl.shapes import Edge
from cadquery.units import RAD2DEG
from ezdxf import units, zoom
from ezdxf.entities import factory
from OCP.GeomConvert import GeomConvert
from OCP.gp import gp_Dir

DxfObjAttributes = tuple[
    Literal["LINE", "CIRCLE", "ARC", "ELLIPSE", "SPLINE"], dict[str, Any]
]


class DxfDocument:
    """Create DXF document from CadQuery objects.

    DXF exporter utilising `ezdxf <https://ezdxf.readthedocs.io/>`_.

    Based on ``cadquery.occ_impl.exporters.dxf`` with the addition of multilayer
    support.

    Example usage

    Single layer DXF document:

    .. code-block:: python

        rectangle = cq.Workplane().rect(10, 20)

        dxf = DxfDocument()
        dxf.add_shape(rectangle)
        dxf.document.saveas("rectangle.dxf")

    Multilayer DXF document:

    .. code-block:: python

        rectangle = cq.Workplane().rect(10, 20)
        circle = cq.Workplane().circle(3)

        dxf = DxfDocument()
        dxf = (
            dxf.add_layer("layer_1", color=2)
            .add_layer("layer_2", color=3)
            .add_shape(rectangle, "layer_1")
            .add_shape(circle, "layer_2")
        )
        dxf.document.saveas("rectangle-with-hole.dxf")
    """

    CURVE_TOLERANCE = 1e-9

    def __init__(
        self,
        dxfversion: str = "AC1027",
        setup: bool | list[str] = False,
        doc_units: int = units.MM,
        *,
        metadata: dict[str, str] | None = None,
    ) -> None:
        """Initialise DXF document.

        :param dxfversion: DXF version specifier as string, default is "AC1027"
            respectively "R2013"
        :param setup: setup default styles, ``False`` for no setup, ``True`` to setup
            everything or a list of topics as strings, e.g. ["linetypes", "styles"]
        :param doc_units: ezdxf document/modelspace units ``ezdxf.enums.InsertUnits``
        :param metadata: document metadata a dictionary of name value pairs
        """
        if metadata is None:
            metadata = {}

        self._DISPATCH_MAP = {
            "LINE": self._dxf_line,
            "CIRCLE": self._dxf_circle,
            "ELLIPSE": self._dxf_ellipse,
        }

        self.document = ezdxf.new(  # type: ignore[attr-defined]
            dxfversion=dxfversion,
            setup=setup,
            units=doc_units,
        )
        self.msp = self.document.modelspace()

        doc_metadata = self.document.ezdxf_metadata()
        for key, value in metadata.items():
            doc_metadata[key] = value

    def add_layer(
        self, name: str, *, color: int = 1, linetype: str = "Continuous"
    ) -> DxfDocument:
        """Add layer to DXF document.

        :param name: ezdxf document layer name
        :param color: ezdxf color
        :param linetype: ezdxf line type

        :return: DxfDocument
        """
        self.document.layers.add(name, color=color, linetype=linetype)

        return self

    def add_shape(self, workplane: cq.Workplane, layer: str = "") -> DxfDocument:
        """Add CadQuery shape to a DXF layer.

        :param workplane: CadQuery Workplane
        :param layer: ezdxf document layer name

        :return: DxfDocument
        """
        plane = workplane.plane
        shape = toCompound(workplane).transformShape(plane.fG)

        general_attributes = {}
        if layer:
            general_attributes["layer"] = layer

        for edge in shape.Edges():
            converter = self._DISPATCH_MAP.get(edge.geomType(), None)

            if converter:
                entity_type, entity_attributes = converter(edge)
                entity = factory.new(
                    entity_type, dxfattribs=entity_attributes | general_attributes
                )
                self.msp.add_entity(entity)
            else:
                _, entity_attributes = self._dxf_spline(edge, plane)
                entity = ezdxf.math.BSpline(  # type: ignore[assignment]
                    **entity_attributes,
                )
                self.msp.add_spline(
                    dxfattribs=general_attributes
                ).apply_construction_tool(entity)

        zoom.extents(self.msp)

        return self

    @staticmethod
    def _dxf_line(edge: Edge) -> DxfObjAttributes:
        """Convert a Line to DXF attributes.

        :param edge: CadQuery Edge to be converted to a DXF line

        :return: dictionary of DXF entity attributes for creating a line
        """
        return (
            "LINE",
            {
                "start": edge.startPoint().toTuple(),
                "end": edge.endPoint().toTuple(),
            },
        )

    @staticmethod
    def _dxf_circle(edge: Edge) -> DxfObjAttributes:
        """Convert a Circle to DXF attributes.

        Based on ``cadquery.occ_impl.exporters.dxf._dxf_circle``.

        :param edge: CadQuery Edge to be converted to a DXF circle

        :return: dictionary of DXF entity attributes for creating either a circle or arc
        """
        geom = edge._geomAdaptor()
        circ = geom.Circle()

        radius = circ.Radius()
        location = circ.Location()

        direction_y = circ.YAxis().Direction()
        direction_z = circ.Axis().Direction()

        dy = gp_Dir(0, 1, 0)

        phi = direction_y.AngleWithRef(dy, direction_z)

        if direction_z.XYZ().Z() > 0:
            a1 = RAD2DEG * (geom.FirstParameter() - phi)
            a2 = RAD2DEG * (geom.LastParameter() - phi)
        else:
            a1 = -RAD2DEG * (geom.LastParameter() - phi) + 180
            a2 = -RAD2DEG * (geom.FirstParameter() - phi) + 180

        if edge.IsClosed():
            return (
                "CIRCLE",
                {
                    "center": (location.X(), location.Y(), location.Z()),
                    "radius": radius,
                },
            )
        else:
            return (
                "ARC",
                {
                    "center": (location.X(), location.Y(), location.Z()),
                    "radius": radius,
                    "start_angle": a1,
                    "end_angle": a2,
                },
            )

    @staticmethod
    def _dxf_ellipse(edge: Edge) -> DxfObjAttributes:
        """Convert an Ellipse to DXF attributes.

        Based on ``cadquery.occ_impl.exporters.dxf._dxf_ellipse``.

        :param edge: CadQuery Edge to be converted to a DXF ellipse

        :return: dictionary of DXF entity attributes for creating an ellipse
        """
        geom = edge._geomAdaptor()
        ellipse = geom.Ellipse()

        r1 = ellipse.MinorRadius()
        r2 = ellipse.MajorRadius()

        c = ellipse.Location()
        xdir = ellipse.XAxis().Direction()
        xax = r2 * xdir.XYZ()

        return (
            "ELLIPSE",
            {
                "center": (c.X(), c.Y(), c.Z()),
                "major_axis": (xax.X(), xax.Y(), xax.Z()),
                "ratio": r1 / r2,
                "start_param": geom.FirstParameter(),
                "end_param": geom.LastParameter(),
            },
        )

    @classmethod
    def _dxf_spline(cls, edge: Edge, plane: Plane) -> DxfObjAttributes:
        """Convert a Spline to ezdxf.math.BSpline parameters.

        Based on ``cadquery.occ_impl.exporters.dxf._dxf_spline``.

        :param edge: CadQuery Edge to be converted to a DXF spline
        :param plane: CadQuery Plane

        :return: dictionary of ezdxf.math.BSpline parameters
        """
        adaptor = edge._geomAdaptor()
        curve = GeomConvert.CurveToBSplineCurve_s(adaptor.Curve().Curve())

        spline = GeomConvert.SplitBSplineCurve_s(
            curve,
            adaptor.FirstParameter(),
            adaptor.LastParameter(),
            cls.CURVE_TOLERANCE,
        )

        # need to apply the transform on the geometry level
        spline.Transform(plane.fG.wrapped.Trsf())

        order = spline.Degree() + 1
        knots = list(spline.KnotSequence())
        poles = [(p.X(), p.Y(), p.Z()) for p in spline.Poles()]
        weights = (
            [spline.Weight(i) for i in range(1, spline.NbPoles() + 1)]
            if spline.IsRational()
            else None
        )

        if spline.IsPeriodic():
            pad = spline.NbKnots() - spline.LastUKnotIndex()
            poles += poles[:pad]

        return (
            "SPLINE",
            {
                "control_points": poles,
                "order": order,
                "knots": knots,
                "weights": weights,
            },
        )
