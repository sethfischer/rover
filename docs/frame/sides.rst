===========
Frame sides
===========

Port
----

.. cadquery-vtk::

    from osr_mechanical.frame.side import FrameSide
    from osr_mechanical.bom.parts import port

    result = FrameSide(port).cq_object


Starboard
---------

.. cadquery-vtk::

    from osr_mechanical.frame.side import FrameSide
    from osr_mechanical.bom.parts import starboard

    result = FrameSide(starboard).cq_object
