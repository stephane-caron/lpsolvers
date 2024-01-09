#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2016-2022 Stéphane Caron

from numpy import array

from lpsolvers import available_solvers, solve_lp

problems = []

c = array([1.0, 2.0, 3.0])
G = array(
    [[1.0, 2.0, -1.0], [2.0, 0.0, 1.0], [1.0, 2.0, 1.0], [-1.0, -1.0, -1.0]]
)
h = array([4.0, 1.0, 3.0, 2.0])
A = array([[2.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
b = array([1.0, 0.0])
problems.append((c, G, h, A, b))

if __name__ == "__main__":
    for i, (c, G, h, A, b) in enumerate(problems):
        for solver in available_solvers:
            x = solve_lp(c, G, h, A, b, solver=solver)
            print("LP %d for %6s:" % (i, solver), x)
