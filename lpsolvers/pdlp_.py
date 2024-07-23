#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright 2023 Inria

"""Solver interface for `PDLP`_.

.. _PDLP: https://developers.google.com/optimization/lp/pdlp_math

PDLP is a first-order method for convex quadratic programming aiming for
high-accuracy solutions and scaling to large problems. If you use PDLP in your
academic works, consider citing the corresponding paper [Applegate2021]_.
"""

from typing import Optional

import numpy as np
import scipy.sparse as spa
from ortools.pdlp import solve_log_pb2, solvers_pb2
from ortools.pdlp.python import pdlp


def pdlp_solve_lp(
    c: np.ndarray,
    G: np.ndarray,
    h: np.ndarray,
    A: Optional[np.ndarray] = None,
    b: Optional[np.ndarray] = None,
    verbose: bool = False,
    eps_optimal_absolute: Optional[float] = None,
    eps_optimal_relative: Optional[float] = None,
    time_sec_limits: Optional[float] = None,
    **kwargs,
) -> np.ndarray:
    """Solve a quadratic program using PDLP.

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
    verbose :
        Set to `True` to print out extra information.
    verbose :
        Set to `True` to print out extra information.
    eps_optimal_absolute :
        Absolute tolerance on the primal-dual residuals and duality gap. See
        *e.g.* [tolerances]_ for an overview of solver tolerances.
    eps_optimal_relative :
        Relative tolerance on the primal-dual residuals and duality gap. See
        *e.g.* [tolerances]_ for an overview of solver tolerances.
    time_sec_limits :
        Maximum computation time the solver is allowed, in seconds.

    Returns
    -------
    :
        Primal solution to the QP, if found, otherwise ``None``.

    Notes
    -----
    All other keyword arguments are forwarded as parameters to PDLP. For
    instance, you can call ``pdlp_solve_qp(P, q, G, h, num_threads=3,
    verbosity_level=2)``. For a quick overview, the solver accepts the
    following settings:

    .. list-table::
       :widths: 30 70
       :header-rows: 1

       * - Name
         - Effect
       * - ``num_threads``
         - Number of threads to use (positive).
       * - ``verbosity_level``
         - Verbosity level from 0 (no logging) to 4 (extensive logging).
       * - ``initial_primal_weight``
         - Initial value of the primal weight (ratio of primal over  dual step
           sizes).
       * - ``l_inf_ruiz_iterations``
         - Number of L-infinity Ruiz rescaling iterations applied to the
           constraint matrix.
       * - ``l2_norm_rescaling``
         - If set to ``True``, applies L2-norm rescaling after Ruiz rescaling.

    This list is not exhaustive. Check out the solver's `Protocol Bufffers file
    <https://github.com/google/or-tools/blob/8768ed7a43f8899848effb71295a790f3ecbe2f2/ortools/pdlp/solvers.proto>`__
    for more. See also the `Mathematical background for PDLP
    <https://developers.google.com/optimization/lp/pdlp_math>`__.
    """
    n = c.shape[0]

    A_pdlp = None
    lc_pdlp = None
    uc_pdlp = None
    if G is not None and h is not None:
        A_pdlp = G
        lc_pdlp = np.full(h.shape, -np.inf)
        uc_pdlp = h
    if A is not None and b is not None:
        A_pdlp = A if A_pdlp is None else spa.vstack([A_pdlp, A], format="csc")
        lc_pdlp = b if lc_pdlp is None else np.hstack([lc_pdlp, b])
        uc_pdlp = b if uc_pdlp is None else np.hstack([uc_pdlp, b])
    lv_pdlp = np.full((n,), -np.inf)  # custom lb vector can go here
    uv_pdlp = np.full((n,), +np.inf)  # custom ub vector can go here

    qp = pdlp.QuadraticProgram()
    # qp.objective_matrix = np.diag(...)
    qp.objective_vector = c
    if A_pdlp is not None:
        qp.constraint_matrix = A_pdlp
        qp.constraint_lower_bounds = lc_pdlp
        qp.constraint_upper_bounds = uc_pdlp
    qp.variable_lower_bounds = lv_pdlp
    qp.variable_upper_bounds = uv_pdlp

    params = solvers_pb2.PrimalDualHybridGradientParams()
    optimality = params.termination_criteria.simple_optimality_criteria
    if eps_optimal_absolute is not None:
        optimality.eps_optimal_absolute = eps_optimal_absolute
    if eps_optimal_relative is not None:
        optimality.eps_optimal_relative = eps_optimal_relative
    if time_sec_limits is not None:
        params.termination_criteria.time_sec_limits = time_sec_limits
    if verbose and "verbosity_level" not in kwargs:
        params.verbosity_level = 1 if verbose else 0
    for param, value in kwargs.items():
        setattr(params, param, value)

    result = pdlp.primal_dual_hybrid_gradient(qp, params)
    log = result.solve_log
    if log.termination_reason != solve_log_pb2.TERMINATION_REASON_OPTIMAL:
        raise ValueError("Linear program is not feasible")
    return result.primal_solution
