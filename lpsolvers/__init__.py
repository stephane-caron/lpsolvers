#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2022 Stéphane Caron
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

"""Linear programming solvers in Python with a unified API."""

from typing import Optional

import numpy as np

from .exceptions import NoSolverSelected, SolverNotFound

__version__ = "1.2.0"

available_solvers = []


# cdd
# ===

try:
    from .cdd_ import cdd_solve_lp

    available_solvers.append("cdd")
except ImportError:

    def cdd_solve_lp(
        c: np.ndarray,
        G: np.ndarray,
        h: np.ndarray,
        A: Optional[np.ndarray] = None,
        b: Optional[np.ndarray] = None,
    ) -> np.ndarray:
        """Error function defined when cdd is not available."""
        raise ImportError("cdd not found")


# CVXOPT
# ======

try:
    from .cvxopt_ import cvxopt_solve_lp

    available_solvers.append("cvxopt")
except ImportError:

    def cvxopt_solve_lp(
        c: np.ndarray,
        G: np.ndarray,
        h: np.ndarray,
        A: Optional[np.ndarray] = None,
        b: Optional[np.ndarray] = None,
        solver: Optional[str] = None,
        **kwargs,
    ) -> np.ndarray:
        """Error function defined when CVXOPT is not available."""
        raise ImportError("CVXOPT not found")


# CVXPY
# =====

try:
    from .cvxpy_ import cvxpy_solve_lp

    available_solvers.append("cvxpy")
except ImportError:

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
        """Error function defined when CVXPY is not available."""
        raise ImportError("CVXPY not found")


# ProxQP
# ======

try:
    from .proxqp_ import proxqp_solve_lp

    available_solvers.append("proxqp")
except ImportError:

    def proxqp_solve_lp(
        c: np.ndarray,
        G: np.ndarray,
        h: np.ndarray,
        A: Optional[np.ndarray] = None,
        b: Optional[np.ndarray] = None,
        initvals: Optional[np.ndarray] = None,
        verbose: bool = False,
        backend: Optional[str] = None,
        **kwargs,
    ) -> np.ndarray:
        """Error function defined when ProxQP is not available."""
        raise ImportError("ProxQP not found")


def solve_lp(
    c: np.ndarray,
    G: np.ndarray,
    h: np.ndarray,
    A: Optional[np.ndarray] = None,
    b: Optional[np.ndarray] = None,
    solver: Optional[str] = None,
    **kwargs,
) -> np.ndarray:
    r"""Solve a linear program using one of the available LP solvers.

    The linear program is defined as:

    .. math::

        \begin{split}\begin{array}{ll}
            \mbox{minimize} &
                c^T x \\
            \mbox{subject to}
                & G x \leq h \\
                & A x = b
        \end{array}\end{split}

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
        Name of the LP solver to choose in :data:`lpsolvers.available_solvers`.

    Returns
    -------
    :
        Optimal solution if found, ``None`` otherwise.

    Raises
    ------
    ValueError
        If the LP is not feasible.
    SolverNotFound
        If the requested LP solver is not found.

    Notes
    -----
    Extra keyword arguments given to this function are forwarded to the
    underlying solver. For example, we can call ProxQP with a custom absolute
    feasibility tolerance by ``solve_lp(c, G, h, solver='proxqp',
    eps_abs=1e-8)``.
    """
    if solver is None:
        raise NoSolverSelected(
            "Set the `solver` keyword argument to one of the "
            f"available solvers in {available_solvers}"
        )
    if isinstance(G, np.ndarray) and G.ndim == 1:
        G = G.reshape((1, G.shape[0]))
    if solver == "cdd":
        return cdd_solve_lp(c, G, h, A, b)
    if solver == "cvxopt":
        return cvxopt_solve_lp(c, G, h, A, b, **kwargs)
    if solver == "cvxpy":
        return cvxpy_solve_lp(c, G, h, A, b, **kwargs)
    if solver == "proxqp":
        return proxqp_solve_lp(c, G, h, A, b, **kwargs)
    raise SolverNotFound(f"solver '{solver}' is not available")


__all__ = [
    "__version__",
    "available_solvers",
    "cdd_solve_lp",
    "cvxopt_solve_lp",
    "cvxpy_solve_lp",
    "proxqp_solve_lp",
    "solve_lp",
]
