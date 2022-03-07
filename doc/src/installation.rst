:github_url: https://github.com/stephane-caron/lpsolvers/tree/master/doc/src/installation.rst

************
Installation
************

Linux
=====

The simplest way to install the package on a recent Debian-based system with
Python 3 is:

.. code:: bash

    sudo apt install libgmp-dev python3-dev
    pip install lpsolvers

You can add the ``--user`` parameter for a user-only installation.

Python 2
--------

If you have an older system with Python 2, for instance Ubuntu 16.04, try:

.. code:: bash

    sudo apt install python-dev
    pip lpsolvers==0.8.9

Python 2 is not supported any more, but this may still work.
