#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2022 Stéphane Caron and the qpsolvers contributors.
#
# This file is part of qpsolvers.
#
# qpsolvers is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# qpsolvers is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with qpsolvers. If not, see <http://www.gnu.org/licenses/>.

"""Solver interface for `ProxQP`_.

.. _ProxQP: https://github.com/Simple-Robotics/proxsuite#proxqp

ProxQP is the QP solver from ProxSuite, a collection of open-source solvers
rooted in revisited primal-dual proximal algorithms. If you use ProxQP in some
academic work, consider citing the corresponding paper [Bambade2022]_.
"""

from typing import Optional

import numpy as np
from proxsuite import proxqp


def __select_backend(backend: Optional[str], use_csc: bool):
    """Select backend function for ProxQP.

    Parameters
    ----------
    backend :
        ProxQP backend to use in ``[None, "dense", "sparse"]``. If ``None``
        (default), the backend is selected based on the type of ``P``.
    use_csc :
        If ``True``, use sparse matrices if the backend is not specified.

    Returns
    -------
    :
        Backend solve function.

    Raises
    ------
    ParamError
        If the required backend is not a valid ProxQP backend.
    """
    if backend is None:
        return proxqp.sparse.QP if use_csc else proxqp.dense.QP
    if backend == "dense":
        return proxqp.dense.QP
    if backend == "sparse":
        return proxqp.sparse.QP
    raise ValueError(f'Unknown ProxQP backend "{backend}')


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
    """Solve a quadratic program using ProxQP.

    Parameters
    ----------
    problem :
        Quadratic program to solve.
    initvals :
        Warm-start guess vector.
    backend :
        ProxQP backend to use in ``[None, "dense", "sparse"]``. If ``None``
        (default), the backend is selected based on the type of ``P``.
    verbose :
        Set to `True` to print out extra information.

    Returns
    -------
    :
        Solution to the QP returned by the solver.

    Raises
    ------
    ParamError
        If a warm-start value is given both in `initvals` and the `x` keyword
        argument.

    Notes
    -----
    All other keyword arguments are forwarded as options to ProxQP. For
    instance, you can call ``proxqp_solve_qp(P, q, G, h, eps_abs=1e-6)``.
    For a quick overview, the solver accepts the following settings:

    .. list-table::
       :widths: 30 70
       :header-rows: 1

       * - Name
         - Effect
       * - ``x``
         - Warm start value for the primal variable.
       * - ``y``
         - Warm start value for the dual Lagrange multiplier for equality
           constraints.
       * - ``z``
         - Warm start value for the dual Lagrange multiplier for inequality
           constraints.
       * - ``eps_abs``
         - Asbolute stopping criterion of the solver (default: 1e-3, note that
           this is a laxer default than other solvers). See *e.g.*
           [tolerances]_ for an overview of solver tolerances.
       * - ``eps_rel``
         - Relative stopping criterion of the solver. See *e.g.* [tolerances]_
           for an overview of solver tolerances.
       * - ``mu_eq``
         - Proximal step size wrt equality constraints multiplier.
       * - ``mu_in``
         - Proximal step size wrt inequality constraints multiplier.
       * - ``rho``
         - Proximal step size wrt primal variable.
       * - ``compute_preconditioner``
         - If ``True`` (default), the preconditioner will be derived.
       * - ``compute_timings``
         - If ``True`` (default), timings will be computed by the solver (setup
           time, solving time, and run time = setup time + solving time).
       * - ``max_iter``
         - Maximal number of authorized outer iterations.
       * - ``initial_guess``
         - Sets the initial guess option for initilizing x, y and z.

    This list is not exhaustive. Check out the `solver documentation
    <https://simple-robotics.github.io/proxsuite/>`__ for details.
    """
    if initvals is not None:
        if "x" in kwargs:
            raise ValueError(
                "Warm-start value specified in both `initvals` and `x` kwargs"
            )
        kwargs["x"] = initvals
    use_csc: bool = (G is not None and not isinstance(G, np.ndarray)) or (
        A is not None and not isinstance(A, np.ndarray)
    )
    ProblemType = __select_backend(backend, use_csc)
    problem = ProblemType(
        n=c.shape[0],
        n_eq=b.shape[0] if b is not None else 0,
        n_in=h.shape[0] if h is not None else 0,
    )
    problem.settings.problem_type = proxqp.problem_type.LP
    problem.settings.verbose = verbose
    problem.init(None, c, None, None, G, None, h)
    problem.solve()
    return problem.results.x
