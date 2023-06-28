.. index:: end tap jig, jig

================
End tap jig 2020
================

End tap jig for 2020 aluminium V-slot extrusion.

.. cadquery:vtk::

    End tap jig for 2020 V-slot extrusion.

    .. code-block:: python

        from osr_mechanical.jigs.vslot import EndTapJig

        result = EndTapJig().cq_object


Bill of materials
-----------------

.. osr:bom:: jigs.vslot.EndTapJig


3D printed parts
----------------

Jig body
~~~~~~~~

.. index:: print settings (3D)

.. osr:print-settings:: jigs/vslot-end-tap-jig-2020.stl
    :infill: 100
    :filament-material: PLA
    :nozzle-diameter: 0.4
    :layer-height: 0.2
    :rafts: yes
    :supports: no


.. cadquery:vtk::
    :color: 0.85, 0.45, 0.01, 1

    3D printed body for 2020 V-slot end tap jig.

    .. code-block:: python

        from osr_mechanical.jigs.vslot import EndTapJig

        jig = EndTapJig()
        result = jig.cq_part("2020_end_tap_jig__body")


.. dropdown:: Print orientation

    Print standing on end with T-slot aperture facing up.

    .. cadquery:svg::

        Print orientation for 2020 V-slot end tag jig body.

        .. code-block:: python

            from osr_mechanical.jigs.vslot import EndTapJig

            jig = EndTapJig()
            result = jig.cq_part("2020_end_tap_jig__body")
