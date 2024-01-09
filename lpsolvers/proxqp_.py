#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2016-2022 Stéphane Caron
# Copyright (C) 2023 Inria

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
        return proxqp.sparse if use_csc else proxqp.dense
    if backend == "dense":
        return proxqp.dense
    if backend == "sparse":
        return proxqp.sparse
    raise ValueError(f'Unknown ProxQP backend "{backend}')


def proxqp_solve_lp(
    c: np.ndarray,
    G: np.ndarray,
    h: np.ndarray,
    A: Optional[np.ndarray] = None,
    b: Optional[np.ndarray] = None,
    verbose: bool = False,
    backend: Optional[str] = None,
    **kwargs,
) -> np.ndarray:
    """Solve a quadratic program using ProxQP.

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
    backend :
        ProxQP backend to use in ``[None, "dense", "sparse"]``. If ``None``
        (default), the backend is selected based on the type of ``P``.
    verbose :
        Set to `True` to print out extra information.

    Returns
    -------
    :
        Solution to the QP returned by the solver.

    Notes
    -----
    All other keyword arguments are forwarded as solver settings to ProxQP. For
    instance, you can call ``proxqp_solve_qp(P, q, G, h, eps_abs=1e-6)``. Check
    out the `solver documentation
    <https://simple-robotics.github.io/proxsuite/>`__ for details.
    """
    use_csc: bool = (G is not None and not isinstance(G, np.ndarray)) or (
        A is not None and not isinstance(A, np.ndarray)
    )
    proxqp_backend = __select_backend(backend, use_csc)
    problem = proxqp_backend.QP(
        n=c.shape[0],
        n_eq=b.shape[0] if b is not None else 0,
        n_in=h.shape[0] if h is not None else 0,
        hessian_type=proxqp_backend.HessianType.Zero,
    )
    for key, value in kwargs.items():
        setattr(problem.settings, key, value)
    problem.settings.verbose = verbose
    problem.init(None, c, None, None, G, None, h)
    problem.solve()
    if problem.results.info.status != proxqp.PROXQP_SOLVED:
        raise ValueError("Linear program is not feasible")
    return problem.results.x
