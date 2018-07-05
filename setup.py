#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Stephane Caron <stephane.caron@normalesup.org>
#
# This file is part of lpsolvers.
#
# lpsolvers is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# lpsolvers is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with lpsolvers. If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup

classifiers = """\
Development Status :: 5 - Production/Stable
License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)
Intended Audience :: Developers
Intended Audience :: Science/Research
Topic :: Scientific/Engineering :: Mathematics
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Operating System :: OS Independent"""

long_description = """\
This module provides a single function ``solve_lp(c, G, h, A, b, solver=X)``
with a *solver* keyword argument to select the backend solver. The linear
program it solves is, in standard form:

.. code-block::

    max  c^T x
    s.t. G x <= h
         A x == b

where vector inequalities are taken coordinate by coordinate.

Solvers
-------

The list of supported solvers currently includes:

- `CVXOPT <http://cvxopt.org/>`_
- `cdd <https://github.com/mcmtroffaes/pycddlib>`_

Example
-------

To solve a linear program, simply build the matrices that define it and call
the ``solve_lp`` function:

.. code:: python

    from numpy import array
    from lpsolvers import solve_lp

    c = array([1., 2., 3.])
    G = array([[1., 2., -1.], [2., 0., 1.], [1., 2., 1.], [-1., -1., -1.]])
    h = array([4., 1., 3., 2.])

    print "LP solution:", solve_lp(c, G, h)

This example outputs the solution ``[2.2 -0.8 -3.4]``.
"""

setup(
    name='lpsolvers',
    version='0.8.8',
    description="Linear Programming solvers for Python with a unified API",
    long_description=long_description,
    url="https://github.com/stephane-caron/lpsolvers",
    author="Stéphane Caron",
    author_email="stephane.caron@normalesup.org",
    license="LGPL",
    keywords="lp, linear programming, solver",
    platforms="any",
    classifiers=classifiers.split('\n'),
    packages=['lpsolvers'],
    install_requires=['cvxopt', 'pycddlib']
)
