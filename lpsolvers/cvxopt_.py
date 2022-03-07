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

"""Solver interface for cdd."""

import logging

from typing import Optional

import cvxopt
import cvxopt.solvers

from cvxopt.solvers import lp
from numpy import array


cvxopt.solvers.options["show_progress"] = False  # disable cvxopt output

GLPK_IF_AVAILABLE: Optional[str] = None

try:
    import cvxopt.glpk

    GLPK_IF_AVAILABLE = "glpk"
    # GLPK is the fastest LP solver I could find so far:
    # <https://scaron.info/blog/linear-programming-in-python-with-cvxopt.html>
    # ... however, it's verbose by default, so we tone it down:
    cvxopt.solvers.options["glpk"] = {"msg_lev": "GLP_MSG_OFF"}  # cvxopt 1.1.8
    cvxopt.solvers.options["msg_lev"] = "GLP_MSG_OFF"  # cvxopt 1.1.7
    cvxopt.solvers.options["LPX_K_MSGLEV"] = 0  # previous versions
except ImportError:
    # issue a warning as GLPK is the best LP solver in practice
    logging.warning("CVXOPT import: GLPK solver not found")


def cvxopt_matrix(M):
    """
    Convert matrix M to CVXOPT format.

    Parameters
    ----------
    M : numpy.ndarray
        Matrix to convert.

    Returns
    -------
    M : cvxopt.matrix
        Same matrix in CVXOPT format.
    """
    if isinstance(M, cvxopt.matrix):
        return M
    return cvxopt.matrix(M)


def cvxopt_solve_lp(c, G, h, A=None, b=None, solver=GLPK_IF_AVAILABLE):
    """
    Solve a linear program defined by:

    .. math::

        \\begin{split}\\begin{array}{ll}
            \\mbox{minimize} &
                c^T x \\\\
            \\mbox{subject to}
                & G x \\leq h \\\\
                & A x = b
        \\end{array}\\end{split}

    using the LP solver from `CVXOPT <http://cvxopt.org/>`_.

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

    Returns
    -------
    x : array, shape=(n,)
        Optimal (primal) solution of the LP, if one exists.

    Raises
    ------
    ValueError
        If the LP is not feasible.
    """
    args = [cvxopt_matrix(c), cvxopt_matrix(G), cvxopt_matrix(h)]
    if A is not None:
        args.extend([cvxopt_matrix(A), cvxopt_matrix(b)])
    sol = lp(*args, solver=solver)
    if "optimal" not in sol["status"]:
        raise ValueError(f"LP optimum not found: {sol['status']}")
    return array(sol["x"]).reshape((array(c).shape[0],))
