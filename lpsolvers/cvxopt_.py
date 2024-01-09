#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2016-2022 Stéphane Caron

"""Solver interface for CVXOPT."""

import logging
from typing import Optional

import cvxopt
import cvxopt.solvers
import numpy as np
from cvxopt.solvers import lp

cvxopt.solvers.options["show_progress"] = False  # disable cvxopt output

GLPK_IF_AVAILABLE: Optional[str] = None

try:
    import cvxopt.glpk

    GLPK_IF_AVAILABLE = "glpk"
    cvxopt.solvers.options["glpk"] = {"msg_lev": "GLP_MSG_OFF"}  # cvxopt 1.1.8
    cvxopt.solvers.options["msg_lev"] = "GLP_MSG_OFF"  # cvxopt 1.1.7
    cvxopt.solvers.options["LPX_K_MSGLEV"] = 0  # previous versions
except ImportError:
    # issue a warning as GLPK is the best LP solver in practice
    logging.warning("CVXOPT import: GLPK solver not found")


def cvxopt_matrix(M: np.ndarray) -> cvxopt.matrix:
    """
    Convert matrix M to CVXOPT format.

    Parameters
    ----------
    M :
        Matrix to convert.

    Returns
    -------
    :
        Same matrix in CVXOPT format.
    """
    if isinstance(M, cvxopt.matrix):
        return M
    return cvxopt.matrix(M)


def cvxopt_solve_lp(
    c: np.ndarray,
    G: np.ndarray,
    h: np.ndarray,
    A: Optional[np.ndarray] = None,
    b: Optional[np.ndarray] = None,
    solver: Optional[str] = GLPK_IF_AVAILABLE,
    **kwargs,
) -> np.ndarray:
    r"""Solve a linear program using CVXOPT.

    The linear program is defined by:

    .. math::

        \begin{split}\begin{array}{ll}
            \mbox{minimize} &
                c^T x \\
            \mbox{subject to}
                & G x \leq h \\
                & A x = b
        \end{array}\end{split}

    It is solved using the LP solver from `CVXOPT <http://cvxopt.org/>`_.

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
        Solver to use, default is GLPK if available

    Returns
    -------
    :
        Optimal (primal) solution of the linear program, if it exists.

    Raises
    ------
    ValueError
        If the LP is not feasible.
    """
    args = [cvxopt_matrix(c), cvxopt_matrix(G), cvxopt_matrix(h)]
    if A is not None and b is not None:
        args.extend([cvxopt_matrix(A), cvxopt_matrix(b)])
    sol = lp(*args, solver=solver, **kwargs)
    if "optimal" not in sol["status"]:
        raise ValueError(f"LP optimum not found: {sol['status']}")
    n = c.shape[0]
    return np.array(sol["x"]).reshape((n,))
