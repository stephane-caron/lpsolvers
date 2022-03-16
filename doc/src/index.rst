:github_url: https://github.com/stephane-caron/lpsolvers/tree/master/doc/src/index.rst

.. title:: Table of Contents

#########
lpsolvers
#########

Unified interface to Linear Programming (LP) solvers available in Python.

The library provides a one-stop shop :func:`.solve_lp` function with a
``solver`` keyword argument to select the backend solver. It solves
:ref:`linear programs <Linear programming>` in standard form:

.. math::

    \begin{split}\begin{array}{ll}
        \mbox{minimize} &
            c^T x \\
        \mbox{subject to}
            & G x \leq h \\
            & A x = b
    \end{array}\end{split}

.. toctree::
    :maxdepth: 1

    installation.rst
    linear-programming.rst
    supported-solvers.rst

You can also download this documentation as a `PDF document <lpsolvers.pdf>`_.
