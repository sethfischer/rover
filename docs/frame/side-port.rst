=================
Frame side (port)
=================


.. cadquery-vtk::

    from osr_mechanical.frame.side import FrameSide
    from osr_mechanical.bom.parts import port

    result = FrameSide(port).cq_object


Bill of materials
-----------------

.. osr-bom:: utilities.frame.FrameSidePort
