#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2022 Stéphane Caron.
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

    using the LP solver from `cdd <https://github.com/mcmtroffaes/pycddlib>`_.

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
    mat = cdd.Matrix(np.hstack([v, -U]), number_type="float")
    mat.obj_type = cdd.LPObjType.MIN
    mat.obj_func = [0.0] + list(c)
    lp = cdd.LinProg(mat)
    lp.solve()
    if lp.status != cdd.LPStatusType.OPTIMAL:
        raise ValueError(f"Linear program not feasible: {lp.status}")
    return np.array(lp.primal_solution)
