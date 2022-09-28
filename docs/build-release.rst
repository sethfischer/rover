==================
Building a release
==================

.. tip::

    Pre-built archives of manufacturing files are available from the `releases page on GitHub`_.

The :ref:`build sub-command <console-build>` builds a :abbr:`CAM (Computer-Aided Manufacturing)` release
and places manufacturing files into a ``_build/`` directory which includes:

* a changelog
* a STEP file of the final assembly
* a PNG image of the final assembly
* STL files for 3D printing

.. note::

    These instructions are for building a release on Ubuntu 20.04.
    Adaptations will be required for other operating systems.


Prerequisites
-------------

* `Git`_ version control system.
* `Python`_ >=3.9.
* `Poetry`_ for Python dependency management.
* `Mayo 3D CAD viewer and converter`_ for exporting PNG images.
* `ImageMagick`_ *optional* utility for manipulating EXIF headers.
* `Inkscape`_ *optional* for generating open graph image.
* `git-lfs`_ *optional* for building documentation.


Ubuntu 20.04
------------

Install prerequisites
~~~~~~~~~~~~~~~~~~~~~

.. code:: none

    sudo apt-get install git python3.9 imagemagick inkscape

Poetry, Mayo, and git-lfs should be installed according to their respective documentation,
and be available in your path.


Clone the project and create a virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: none

    git clone https://github.com/sethfischer/osr.git
    cd osr
    python3.9 -m venv .venv
    . .venv/bin/activate
    pip install -U pip
    poetry install


Build release archive
~~~~~~~~~~~~~~~~~~~~~

.. code:: none

    console build


Additional steps for developers
-------------------------------

Enable Git hooks:

.. code:: none

    make install-git-hooks

Build documentation:

.. code:: none

    git lfs pull
    make -C docs/ clean html

Run linters and tests:

.. code:: none

    make lint test


.. _`releases page on GitHub`: https://github.com/sethfischer/osr/releases
.. _`Python`: https://www.python.org/
.. _`Git`: https://git-scm.com/
.. _`Poetry`: https://python-poetry.org/
.. _`Mayo 3D CAD viewer and converter`: https://github.com/fougue/mayo
.. _`ImageMagick`: https://imagemagick.org/
.. _`Inkscape`: https://inkscape.org/
.. _`git-lfs`: https://git-lfs.github.com/