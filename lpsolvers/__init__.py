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


available_solvers = []


# CVXOPT
# ======

try:
    from .cvxopt_ import cvxopt_solve_lp
    available_solvers.append('cvxopt')
except ImportError:
    def cvxopt_solve_lp(*args, **kwargs):
        raise ImportError("CVXOPT not found")

# cdd
# ===

try:
    from .cdd_ import cdd_solve_lp
    available_solvers.append('cdd')
except ImportError:
    def cdd_solve_lp(*args, **kwargs):
        raise ImportError("cdd not found")


def solve_lp(c, G, h, A=None, b=None, solver='cvxopt'):
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
    if solver == 'cvxopt':
        return cvxopt_solve_lp(c, G, h, A, b)
    elif solver == 'cdd':
        return cdd_solve_lp(c, G, h, A, b)
    raise Exception("solver '%s' not recognized" % solver)


__all__ = [
    'available_solvers',
    'cvxopt_solve_lp',
    'cdd_solve_lp'
]
