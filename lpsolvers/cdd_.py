#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2018 Stephane Caron <stephane.caron@normalesup.org>
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

import cdd

from numpy import array, hstack, vstack


def cdd_solve_lp(c, G, h, A=None, b=None):
    """
    Solve a linear program defined by:

        minimize
            c.T * x

        subject to
            G * x <= h
            A * x == b

    using the LP solver from `cdd <https://github.com/mcmtroffaes/pycddlib>`_.

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
    if A is not None:
        v = hstack([h, b, -b])
        U = vstack([G, A, -A])
    else:  # no equality constraint
        v = h
        U = G
    v = v.reshape((v.shape[0], 1))
    mat = cdd.Matrix(hstack([v, -U]), number_type='float')
    mat.obj_type = cdd.LPObjType.MIN
    mat.obj_func = [0.] + list(c)
    lp = cdd.LinProg(mat)
    lp.solve()
    if lp.status != cdd.LPStatusType.OPTIMAL:
        raise ValueError("LP optimum not found: %s" % lp.status)
    return array(lp.primal_solution)
