.. title::
    Quarter-scale Mars rover

.. meta::
    :description lang=en:
        Quarter-scale Mars rover based on the NASA Mars 2020 Mission
        Perseverance Rover.

:og:description:
    Quarter-scale Mars rover based on the NASA Mars 2020 Mission Perseverance Rover.


=================
sethfischer-rover
=================

.. grid:: 2

    .. grid-item::
        :columns: auto

        Quarter-scale Mars rover based on the
        `NASA Mars 2020 Perseverance Rover <https://science.nasa.gov/mission/mars-2020-perseverance/>`__.

    .. grid-item::
        :columns: auto

        .. button-link:: https://github.com/sethfischer/rover
            :color: primary
            :outline:

            :octicon:`mark-github` Star on GitHub


.. cadquery:vtk::

    Final assembly of sethfischer-rover.

    .. code-block:: python

        from osr_mechanical.final import FinalAssembly

        result = FinalAssembly().cq_object


Specifications
--------------

:Dimensions:
    :osr:dimension:`length` long × :osr:dimension:`width` wide × :osr:dimension:`height` high


----

.. _tech:

.. grid:: 1 2 2 2

    .. grid-item-card:: Open Source Hardware
        :text-align: center
        :link: copyright
        :link-type: doc

        .. image:: _static/images/logos/oshw.svg
            :alt: Open Source Hardware
            :class: no-scaled-link
            :width: 100%

    .. grid-item-card:: Modeled with CadQuery
        :text-align: center
        :link: https://cadquery.readthedocs.io/

        .. image:: _static/images/logos/cadquery.svg
            :alt: Modeled with CadQuery
            :width: 100%

----


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
    rocker-axle
    din-rail-assemblies/index

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
    :caption: Reference
    :maxdepth: 1
    :hidden:

    reference/vmc-hat-datasheet

.. toctree::
    :caption: End matter
    :maxdepth: 1
    :hidden:

    build-release
    console
    related-projects
    about
    changelog
    copyright
    indices
