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
