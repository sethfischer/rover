.. meta::
    :description lang=en:
        Frame sub-assemblies for sethfischer-rover, a quarter-scale Mars rover.

:og:description:
    Frame sub-assemblies for sethfischer-rover, a quarter-scale Mars rover.


.. index:: frame

=====
Frame
=====

.. cadquery:vtk::

    Frame assembly constructed from 2020 V-slot extrusion.

    .. code-block:: python

        from osr_mechanical.frame.final import Frame

        result = Frame().cq_object


.. toctree::
    :caption: Sub-assemblies
    :maxdepth: 1

    side-port
    side-starboard
