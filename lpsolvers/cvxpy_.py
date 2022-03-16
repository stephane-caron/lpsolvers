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

"""Solver interface for CVXPY"""

from typing import Optional

import numpy as np

from cvxpy import Minimize, Problem, Variable
from numpy import array


def cvxpy_solve_lp(
    c: np.ndarray,
    G: np.ndarray,
    h: np.ndarray,
    A: Optional[np.ndarray] = None,
    b: Optional[np.ndarray] = None,
    solver: Optional[str] = None,
    verbose: bool = False,
) -> np.ndarray:
    """
    Solve a linear program defined as:

    .. math::

        \\begin{split}\\begin{array}{ll}
        \\mbox{minimize}
            & c^T x \\\\
        \\mbox{subject to}
            & G x \\leq h \\\\
            & A x = b
        \\end{array}\\end{split}

    calling a given solver using the `CVXPY <http://www.cvxpy.org/>`_ modelling
    language.

    Parameters
    ----------
    c :
        Linear cost vector.
    G :
        Linear inequality constraint matrix.
    h :
        Linear inequality constraint vector.
    A :
        Linear equality constraint matrix.
    b :
        Linear equality constraint vector.
    solver :
        Solver name in ``cvxpy.installed_solvers()``.
    verbose :
        Set to `True` to print out extra information.

    Returns
    -------
    x : array, shape=(n,)
        Optimal (primal) solution of the linear program, if it exists.

    Raises
    ------
    ValueError
        If the LP is not feasible.
    """
    n = c.shape[0]
    x = Variable(n)
    objective = Minimize(c @ x)
    constraints = []
    if G is not None:
        constraints.append(G @ x <= h)
    if A is not None:
        constraints.append(A @ x == b)
    prob = Problem(objective, constraints)
    prob.solve(solver=solver, verbose=verbose)
    if x.value is None:
        raise ValueError("Linear program is not feasible")
    return array(x.value).reshape((n,))
