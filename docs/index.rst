===============
sethfischer-osr
===============

Alternative body construction for the `NASA JPL Open Source Rover`_.

.. cadquery-vtk::

    from osr_mechanical.final import FinalAssembly

    result = FinalAssembly().cq_object


Table of contents
-----------------

.. toctree::
    :caption: Construction
    :maxdepth: 1

    frame

.. toctree::
    :caption: Jigs
    :glob:
    :maxdepth: 1

    jigs/*

.. toctree::
    :caption: Bill of materials
    :maxdepth: 1

    bom/parts

.. toctree::
    :caption: End matter
    :maxdepth: 1

    build-release
    console
    related-projects


Indices and tables
------------------

* :ref:`genindex`


.. _`NASA JPL Open Source Rover`: https://github.com/nasa-jpl/open-source-rover
