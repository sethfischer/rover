===============
sethfischer-osr
===============

Alternative body construction for the `NASA JPL Open Source Rover`_.

.. cadquery-vtk::

    from osr_mechanical.final import FinalAssembly

    result = FinalAssembly().cq_object


Specifications
--------------

:Dimensions:
    :osr:dimension:`length` long × :osr:dimension:`width` wide × :osr:dimension:`height` high


.. toctree::
    :caption: Preface
    :maxdepth: 1
    :hidden:

    inspiration

.. toctree::
    :caption: Construction
    :maxdepth: 2
    :hidden:

    frame/index

.. toctree::
    :caption: Jigs
    :glob:
    :maxdepth: 1
    :hidden:

    jigs/*

.. toctree::
    :caption: Bill of materials
    :maxdepth: 1
    :hidden:

    bom/parts

.. toctree::
    :caption: End matter
    :maxdepth: 1
    :hidden:

    build-release
    console
    related-projects
    indices


.. _`NASA JPL Open Source Rover`: https://github.com/nasa-jpl/open-source-rover
