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

from lpsolvers import available_solvers, solve_lp
from numpy import array, ones, eye, zeros

problems = []

c = -ones(10)
G = eye(10)
h = zeros(10)
problems.append((c, G, h))

c = array([1., 2., 3.])
G = array([
    [1., 2., -1.],
    [2., 0., 1.],
    [1., 2., 1.],
    [-1., -1., -1.]])
h = array([4., 1., 3., 2.])
problems.append((c, G, h))

if __name__ == "__main__":
    for i, (c, G, h) in enumerate(problems):
        for solver in available_solvers:
            x = solve_lp(c, G, h, solver=solver)
            print("LP %d for %6s:" % (i, solver), x)
