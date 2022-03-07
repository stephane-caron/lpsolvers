#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2022 Stéphane Caron <stephane.caron@normalesup.org>
#
# This file is part of lpsolvers.
#
# lpsolvers is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# lpsolvers is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# lpsolvers. If not, see <http://www.gnu.org/licenses/>.

"""Linear programming solvers in Python with a unified API"""

import numpy as np

from .exceptions import SolverNotFound

__version__ = "0.9.0"

available_solvers = []


# CVXOPT
# ======

try:
    from .cvxopt_ import cvxopt_solve_lp

    available_solvers.append("cvxopt")
except ImportError:

    def cvxopt_solve_lp(c, G, h, A=None, b=None, solver=None):
        """
        Function defined when CVXOPT is not available.
        """
        raise ImportError("CVXOPT not found")


# cdd
# ===

try:
    from .cdd_ import cdd_solve_lp

    available_solvers.append("cdd")
except ImportError:

    def cdd_solve_lp(c, G, h, A=None, b=None):
        """
        Function defined when cdd is not available.
        """
        raise ImportError("cdd not found")


def solve_lp(c, G, h, A=None, b=None, solver="cvxopt"):
    """
    Solve a Linear Program defined as:

        minimize
            c.T * x

        subject to
            G * x <= h
            A * x == b

    using one of the available LP solvers.

    Parameters
    ----------
    c : array, shape=(n,)
        Linear-cost vector.
    G : array, shape=(m, n)
        Linear inequality constraint matrix.
    h : array, shape=(m,)
        Linear inequality constraint vector.
    A : array, shape=(meq, n), optional
        Linear equality constraint matrix.
    b : array, shape=(meq,), optional
        Linear equality constraint vector.
    solver : string, optional
        Solver to use, default is GLPK if available
    solver : string, optional
        Name of the LP solver, to choose in ['cvxopt', 'cdd'].

    Returns
    -------
    x : array or None
        Optimal solution if found, None otherwise.
    """
    if isinstance(G, np.ndarray) and G.ndim == 1:
        G = G.reshape((1, G.shape[0]))
    if solver == "cvxopt":
        return cvxopt_solve_lp(c, G, h, A, b)
    if solver == "cdd":
        return cdd_solve_lp(c, G, h, A, b)
    raise SolverNotFound(f"solver '{solver}' is not available")


__all__ = [
    "__version__",
    "available_solvers",
    "cdd_solve_lp",
    "cvxopt_solve_lp",
    "solve_lp",
]
