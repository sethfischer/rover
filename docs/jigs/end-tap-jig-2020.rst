.. index:: end tap jig, jig

================
End tap jig 2020
================

End tap jig for 2020 aluminium V-slot extrusion.

.. cadquery-vtk::

    from osr_mechanical.jigs.vslot import EndTapJig

    result = EndTapJig().cq_object


Bill of materials
-----------------

.. osr-bom:: jigs.vslot.EndTapJig


3D printed parts
----------------

Jig body
~~~~~~~~

.. osr-print-settings:: jigs/vslot-end-tap-jig-2020.stl
    :infill: 100
    :filament-material: PLA
    :nozzle-diameter: 0.4
    :layer-height: 0.2
    :rafts: yes
    :supports: no
