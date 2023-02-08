"""DXF utilities."""

from __future__ import annotations

from typing import Any

import cadquery as cq
import ezdxf
from cadquery import Plane
from cadquery.occ_impl.exporters.utils import toCompound
from cadquery.occ_impl.shapes import Edge
from cadquery.units import RAD2DEG
from ezdxf import units, zoom
from ezdxf.layouts.layout import Modelspace
from OCP.GeomConvert import GeomConvert
from OCP.gp import gp_Dir


class DxfExporter:
    """Export CadQuery objects to DXF.

    DXF exporter utilising `ezdxf <https://ezdxf.readthedocs.io/>`_.

    Based on ``cadquery.occ_impl.exporters.dxf`` with the addition of multilayer
    support.

    Example usage

    Single layer DXF document:

    .. code-block:: python

        box = cq.Workplane().box(10, 20, 40)
        face_z = box.faces(">Z")

        exporter = DxfExporter()
        exporter.add_shape(face_z)
        exporter.document.saveas("box-face-z.dxf")

    Multilayer DXF document:

    .. code-block:: python

        box = cq.Workplane().box(10, 20, 40)
        face_z = box.faces(">Z")
        cylinder = cq.Workplane().cylinder(10, 4)
        cylinder_face_z = cylinder.faces(">Z")

        exporter = DxfExporter()
        exporter.add_layer("layer_1", color=2)
        exporter.add_layer("layer_2", color=3)
        exporter.add_shape(face_z, "layer_1")
        exporter.add_shape(cylinder_face_z, "layer_2")
        exporter.document.saveas("box-faces-z-x.dxf")
    """

    CURVE_TOLERANCE = 1e-9

    def __init__(
        self,
        doc_units: int = units.MM,
        *,
        setup: bool = False,
        metadata: None | dict[str, str] = None,
    ) -> None:
        """Initialise DXF document.

        :param doc_units: ezdxf document/modelspace units ``ezdxf.enums.InsertUnits``
        :param setup: ezdxf setup parameter creates standard resources,
            such as linetypes and text styles
        :param metadata: document metadata a dictionary of name value pairs
        """
        if metadata is None:
            metadata = {}

        self._DISPATCH_MAP = {
            "LINE": self._dxf_line,
            "CIRCLE": self._dxf_circle,
            "ELLIPSE": self._dxf_ellipse,
            "BSPLINE": self._dxf_spline,
        }

        self.document = ezdxf.new(setup=setup)  # type: ignore[attr-defined]
        self.msp = self.document.modelspace()
        self.document.units = doc_units

        doc_metadata = self.document.ezdxf_metadata()
        for key, value in metadata.items():
            doc_metadata[key] = value

    def add_layer(
        self, name: str, *, color: int = 1, linetype: str = "Continuous"
    ) -> Any:
        """Add layer to DXF document.

        :param name: ezdxf document layer name
        :param color: ezdxf color
        :param linetype: ezdxf line type
        """
        return self.document.layers.add(name, color=color, linetype=linetype)

    def add_shape(self, workplane: cq.Workplane, layer: str = "") -> None:
        """Add CadQuery shape to a DXF layer.

        :param workplane: CadQuery Workplane
        :param layer: ezdxf document layer name
        """
        plane = workplane.plane
        shape = toCompound(workplane).transformShape(plane.fG)

        for edge in shape.Edges():
            converter = self._DISPATCH_MAP.get(edge.geomType(), self._dxf_spline)
            converter(edge, self.msp, plane, layer=layer)

        zoom.extents(self.msp)

    @staticmethod
    def _dxf_line(edge: Edge, msp: Modelspace, _: Plane, layer: str = "") -> Any:
        """Add a CadQuery line to a DXF Modelspace.

        Based on ``cadquery.occ_impl.exporters.dxf._dxf_line``.

        :param edge: CadQuery Edge to be converted to a DXF line
        :param msp: ezdxf Modelspace to which the line will be added
        :param _: Not used
        :param layer: ezdxf document layer name

        :return: DXF entity
        """
        attributes = {}
        if layer:
            attributes["layer"] = layer

        return msp.add_line(
            edge.startPoint().toTuple(),
            edge.endPoint().toTuple(),
            dxfattribs=attributes,
        )

    @staticmethod
    def _dxf_circle(edge: Edge, msp: Modelspace, _: Plane, layer: str = "") -> Any:
        """Add a CadQuery circle to a DXF Modelspace.

        Based on ``cadquery.occ_impl.exporters.dxf._dxf_circle``.

        :param edge: CadQuery Edge to be converted to a DXF circle
        :param msp: ezdxf Modelspace to which the circle will be added
        :param _: Not used
        :param layer: ezdxf document layer name

        :return: DXF entity
        """
        attributes = {}
        if layer:
            attributes["layer"] = layer

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
            return msp.add_circle(
                (location.X(), location.Y(), location.Z()),
                radius,
                dxfattribs=attributes,
            )
        else:
            return msp.add_arc(
                (location.X(), location.Y(), location.Z()),
                radius,
                a1,
                a2,
                dxfattribs=attributes,
            )

    @staticmethod
    def _dxf_ellipse(edge: Edge, msp: Modelspace, _: Plane, layer: str = "") -> Any:
        """Add a CadQuery ellipse to a DXF Modelspace.

        Based on ``cadquery.occ_impl.exporters.dxf._dxf_ellipse``.

        :param edge: CadQuery Edge to be converted to a DXF ellipse
        :param msp: ezdxf Modelspace to which the ellipse wil be added
        :param _: Not used
        :param layer: ezdxf document layer name

        :return: DXF entity
        """
        attributes = {}
        if layer:
            attributes["layer"] = layer

        geom = edge._geomAdaptor()
        ellipse = geom.Ellipse()

        r1 = ellipse.MinorRadius()
        r2 = ellipse.MajorRadius()

        c = ellipse.Location()
        xdir = ellipse.XAxis().Direction()
        xax = r2 * xdir.XYZ()

        return msp.add_ellipse(
            (c.X(), c.Y(), c.Z()),
            (xax.X(), xax.Y(), xax.Z()),
            r1 / r2,
            geom.FirstParameter(),
            geom.LastParameter(),
            dxfattribs=attributes,
        )

    @classmethod
    def _dxf_spline(
        cls, edge: Edge, msp: Modelspace, plane: Plane, layer: str = ""
    ) -> Any:
        """Add a CadQuery spline to a DXF Modelspace.

        Based on ``cadquery.occ_impl.exporters.dxf._dxf_spline``.

        :param edge: CadQuery Edge to be converted to a DXF spline
        :param msp: ezdxf Modelspace to which the spline will be added
        :param plane: CadQuery Plane
        :param layer: ezdxf document layer name

        :return: DXF entity
        """
        attributes = {}
        if layer:
            attributes["layer"] = layer

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

        dxf_spline = ezdxf.math.BSpline(poles, order, knots, weights)

        return msp.add_spline(dxfattribs=attributes).apply_construction_tool(dxf_spline)
