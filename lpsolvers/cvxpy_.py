#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2016-2022 Stéphane Caron

"""Solver interface for CVXPY."""

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
    **kwargs,
) -> np.ndarray:
    r"""Solve a linear program using CVXPY.

    The linear program is defined by:

    .. math::

        \begin{split}\begin{array}{ll}
        \mbox{minimize}
            & c^T x \\
        \mbox{subject to}
            & G x \leq h \\
            & A x = b
        \end{array}\end{split}

    It is solved using a solver wrapped by `CVXPY <http://www.cvxpy.org/>`_.
    The underlying solver is selected via the corresponding keyword argument.

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
    prob.solve(solver=solver, verbose=verbose, **kwargs)
    if x.value is None:
        raise ValueError("Linear program is not feasible")
    return array(x.value).reshape((n,))
