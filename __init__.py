#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2016-2022 Stéphane Caron

"""
This file allows the whole repository to act as a Python module when e.g.
included as a git submodule inside a project. It incurs redundant bookkeeping
but some users find it useful. (See 4b128db662cfedbe366b8387a59cd18e36c643a3
and comments related to this commit on GitHub.)
"""

from .lpsolvers import available_solvers
from .lpsolvers import cdd_solve_lp
from .lpsolvers import cvxopt_solve_lp
from .lpsolvers import cvxpy_solve_lp
from .lpsolvers import solve_lp

__all__ = [
    "__version__",
    "available_solvers",
    "cdd_solve_lp",
    "cvxopt_solve_lp",
    "cvxpy_solve_lp",
    "solve_lp",
]
