"""Multilayer DXF."""

import cadquery as cq
import ezdxf
from cadquery import Plane
from cadquery.occ_impl.exporters.utils import toCompound
from cadquery.occ_impl.shapes import Edge
from cadquery.units import RAD2DEG
from ezdxf import units
from ezdxf.layouts import Modelspace  # type: ignore[attr-defined]
from OCP.GeomConvert import GeomConvert
from OCP.gp import gp_Dir


class DxfExporter:
    """Export CadQuery objects to DXF.

    Based on ``cadquery.occ_impl.exporters.dxf`` with the addition of multilayer
    support.
    """

    CURVE_TOLERANCE = 1e-9

    def __init__(
        self, dxf_units: int = units.MM, *, metadata: dict[str, str] = {}
    ) -> None:
        """Initialise DXF document."""
        self._DISPATCH_MAP = {
            "LINE": self._dxf_line,
            "CIRCLE": self._dxf_circle,
            "ELLIPSE": self._dxf_ellipse,
            "BSPLINE": self._dxf_spline,
        }

        self.document = ezdxf.new(setup=True)  # type: ignore[attr-defined]
        self.msp = self.document.modelspace()
        self.document.units = dxf_units

        doc_metadata = self.document.ezdxf_metadata()
        for key, value in metadata.items():
            doc_metadata[key] = value

    def add_layer(
        self, name: str, *, color: int = 1, linetype: str = "Continuous"
    ) -> None:
        """Add layer to DXF document."""
        self.document.layers.add(name, color=color, linetype=linetype)

    def add_shape(self, workplane: cq.Workplane, layer_name: str) -> None:
        """Add CadQuery shape to layer."""
        plane = workplane.plane
        shape = toCompound(workplane).transformShape(plane.fG)

        for edge in shape.Edges():
            converter = self._DISPATCH_MAP.get(edge.geomType(), self._dxf_spline)
            converter(edge, self.msp, plane, layer=layer_name)

    @staticmethod
    def _dxf_line(edge: Edge, msp: Modelspace, _: Plane, layer: str = "") -> None:
        """Convert a line to a DXF line.

        Based on ``cadquery.occ_impl.exporters.dxf._dxf_line``.
        """
        attributes = {}
        if layer:
            attributes["layer"] = layer

        msp.add_line(
            edge.startPoint().toTuple(),
            edge.endPoint().toTuple(),
            dxfattribs=attributes,
        )

    @staticmethod
    def _dxf_circle(e: Edge, msp: Modelspace, _: Plane, layer: str = "") -> None:
        """Convert a circle to a DXF circle.

        Based on ``cadquery.occ_impl.exporters.dxf._dxf_circle``.
        """
        attributes = {}
        if layer:
            attributes["layer"] = layer

        geom = e._geomAdaptor()
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

        if e.IsClosed():
            msp.add_circle(
                (location.X(), location.Y(), location.Z()),
                radius,
                dxfattribs=attributes,
            )
        else:
            msp.add_arc(
                (location.X(), location.Y(), location.Z()),
                radius,
                a1,
                a2,
                dxfattribs=attributes,
            )

    @staticmethod
    def _dxf_ellipse(e: Edge, msp: Modelspace, _: Plane, layer: str = "") -> None:
        """Convert an ellipse to a DXF ellipse.

        Based on ``cadquery.occ_impl.exporters.dxf._dxf_ellipse``.
        """
        attributes = {}
        if layer:
            attributes["layer"] = layer

        geom = e._geomAdaptor()
        ellipse = geom.Ellipse()

        r1 = ellipse.MinorRadius()
        r2 = ellipse.MajorRadius()

        c = ellipse.Location()
        xdir = ellipse.XAxis().Direction()
        xax = r2 * xdir.XYZ()

        msp.add_ellipse(
            (c.X(), c.Y(), c.Z()),
            (xax.X(), xax.Y(), xax.Z()),
            r1 / r2,
            geom.FirstParameter(),
            geom.LastParameter(),
            dxfattribs=attributes,
        )

    @classmethod
    def _dxf_spline(
        cls, e: Edge, msp: Modelspace, plane: Plane, layer: str = ""
    ) -> None:
        """Convert a spline to a DXF spline.

        Based on ``cadquery.occ_impl.exporters.dxf._dxf_spline``.
        """
        attributes = {}
        if layer:
            attributes["layer"] = layer

        adaptor = e._geomAdaptor()
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

        msp.add_spline(dxfattribs=attributes).apply_construction_tool(dxf_spline)
