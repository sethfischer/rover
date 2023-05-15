.. meta::
    :description lang=en:
        Starboard-side frame assembly for sethfischer-rover, a quarter-scale Mars rover.

:og:description:
    Starboard-side frame assembly for sethfischer-rover, a quarter-scale Mars rover.


======================
Frame side (starboard)
======================


.. cadquery-vtk::

    from osr_mechanical.frame.side import FrameSide
    from osr_mechanical.bom.parts import starboard

    result = FrameSide(starboard).cq_object


Bill of materials
-----------------

.. osr:bom:: utilities.frame.FrameSideStarboard
