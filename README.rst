===============
sethfischer/osr
===============

|build-status| |lint-status| |docs-status|


Alternative body construction for the `NASA JPL Open Source Rover`_.


Get started
-----------

Install Git hooks:

.. code::

    make install-git-hooks

Create virtual environment and install dependencies:

.. code::

    virtualenv .venv
    . .venv/bin/activate
    pip install -U pip
    poetry install

Build documentation:

.. code::

    make -C docs/ clean html

Build CAM file archive:

.. code::

    console build


.. _`NASA JPL Open Source Rover`: https://github.com/nasa-jpl/open-source-rover


.. |build-status| image:: https://github.com/sethfischer/osr/actions/workflows/build.yml/badge.svg
    :target: https://github.com/sethfischer/osr/actions/workflows/build.yml
    :alt: Build status
.. |lint-status| image:: https://github.com/sethfischer/osr/actions/workflows/lint.yml/badge.svg
    :target: https://github.com/sethfischer/osr/actions/workflows/lint.yml
    :alt: Lint status
.. |docs-status| image:: https://readthedocs.org/projects/sethfischer-osr/badge/?version=latest
    :target: https://sethfischer-osr.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
