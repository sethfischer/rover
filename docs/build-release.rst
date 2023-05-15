.. meta::
    :description lang=en:
        Building manufacturing files for sethfischer-rover, a quarter-scale Mars rover.

:og:description:
    Building manufacturing files for sethfischer-rover, a quarter-scale Mars rover.


.. index:: build release, release

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
* `Python`_ >=3.9, and python-venv.
* `Poetry`_ for Python dependency management.
* `Mayo 3D CAD viewer and converter`_ for exporting PNG images.
* Optional:
   - `ImageMagick`_ for manipulating images.
   - `exiftool`_ for manipulating EXIF headers.
   - `git-lfs`_ for building documentation.
   - `optipng`_ for optimising PNG images.


Ubuntu 20.04
------------

Install prerequisites
~~~~~~~~~~~~~~~~~~~~~

.. code:: none

    sudo apt-get install git python3.9 python3.9-venv imagemagick optipng exiftool

Poetry, Mayo, and git-lfs should be installed according to their respective documentation,
and be available in your path.


Clone the project and create a virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: none

    git clone https://github.com/sethfischer/rover.git
    cd rover
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

Install `CQ-Editor`_:

.. code:: none

    poetry install --with cq-editor

Build documentation:

.. code:: none

    git lfs pull
    set -a && source .env.local && set +a && make -C docs/ clean html

Run linters and tests:

.. code:: none

    make lint test


.. _`releases page on GitHub`: https://github.com/sethfischer/rover/releases
.. _`Python`: https://www.python.org/
.. _`Git`: https://git-scm.com/
.. _`Poetry`: https://python-poetry.org/
.. _`Mayo 3D CAD viewer and converter`: https://github.com/fougue/mayo
.. _`ImageMagick`: https://imagemagick.org/
.. _`exiftool`: https://exiftool.org/
.. _`git-lfs`: https://git-lfs.github.com/
.. _`optipng`: https://optipng.sourceforge.net/
.. _`CQ-Editor`: https://github.com/CadQuery/CQ-editor
