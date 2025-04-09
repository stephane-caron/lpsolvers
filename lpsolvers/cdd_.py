#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2016-2022 Stéphane Caron

"""Solver interface for cdd."""

from typing import Optional

import cdd
import numpy as np


def cdd_solve_lp(
    c: np.ndarray,
    G: np.ndarray,
    h: np.ndarray,
    A: Optional[np.ndarray] = None,
    b: Optional[np.ndarray] = None,
) -> np.ndarray:
    r"""Solve a linear program using the LP solver from cdd.

    The linear program is defined by:

    .. math::

        \\begin{split}\\begin{array}{ll}
            \\mbox{minimize} &
                c^T x \\\\
            \\mbox{subject to}
                & G x \\leq h \\\\
                & A x = b
        \\end{array}\\end{split}

    It is solved using `cdd <https://github.com/mcmtroffaes/pycddlib>`_.

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
        If the linear program is not feasible.
    """
    if A is not None and b is not None:
        v = np.hstack([h, b, -b])
        U = np.vstack([G, A, -A])
    else:  # no equality constraint
        v = h
        U = G
    v = v.reshape((v.shape[0], 1))
    constraints = np.hstack([v, -U])
    objective = np.hstack([[0.0], c])
    lp = cdd.linprog_from_array(
        np.vstack([constraints, objective]),  # type: ignore
        obj_type=cdd.LPObjType.MIN,
    )
    cdd.linprog_solve(lp)
    if lp.status != cdd.LPStatusType.OPTIMAL:
        raise ValueError(f"Linear program not feasible: {lp.status}")
    return np.array(lp.primal_solution)
