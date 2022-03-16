#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2022 Stéphane Caron <stephane.caron@normalesup.org>
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

"""
Tests for the main `solve_lp` function.
"""

import unittest
import warnings

import numpy as np

from lpsolvers import available_solvers
from lpsolvers import solve_lp
from lpsolvers.exceptions import SolverNotFound


class TestSolveLP(unittest.TestCase):

    """
    Test fixture for a variety of linear programs.

    Solver-specific tests are implemented in static methods called
    ``get_test_{foo}`` that return the test function for a given solver. The
    corresponding test function ``test_{foo}_{solver}`` is then added to the
    fixture below the class definition.
    """

    def setUp(self):
        """
        Prepare test fixture.
        """
        warnings.simplefilter("ignore", category=DeprecationWarning)
        warnings.simplefilter("ignore", category=UserWarning)

    def get_small_problem(self):
        """
        Get dense problem as a sextuple of values to unpack.

        Returns
        -------
        c : numpy.ndarray
            Cost vector.
        G : numpy.ndarray
            Linear inequality matrix.
        h : numpy.ndarray
            Linear inequality vector.
        """
        c = np.array([1.0, 2.0, 3.0])
        G = np.array(
            [
                [1.0, 2.0, -1.0],
                [2.0, 0.0, 1.0],
                [1.0, 2.0, 1.0],
                [-1.0, -1.0, -1.0],
            ]
        )
        h = np.array([4.0, 1.0, 3.0, 2.0])
        return c, G, h

    def test_solver_not_found(self):
        """
        Check that SolverNotFound is raised when the solver does not exist.
        """
        c, G, h = self.get_small_problem()
        with self.assertRaises(SolverNotFound):
            solve_lp(c, G, h, solver="ideal")

    @staticmethod
    def get_test(solver):
        """
        Get test function for a given solver.

        Parameters
        ----------
        solver : string
            Name of the solver to test.

        Returns
        -------
        test : function
            Test function for that solver.
        """

        def test(self):
            c, G, h = self.get_small_problem()
            x = solve_lp(c, G, h, solver=solver)
            x_sp = solve_lp(c, G, h, solver=solver)
            self.assertIsNotNone(x)
            self.assertIsNotNone(x_sp)
            known_solution = np.array([2.2, -0.8, -3.4])
            sol_tolerance = 1e-8
            ineq_tolerance = 1e-10
            self.assertLess(np.linalg.norm(x - known_solution), sol_tolerance)
            self.assertLess(
                np.linalg.norm(x_sp - known_solution), sol_tolerance
            )
            self.assertLess(max(np.dot(G, x) - h), ineq_tolerance)

        return test

    @staticmethod
    def get_test_one_ineq(solver):
        """
        Get test function for a given solver. In this variant, there is
        only one inequality constraint, so the solution is unbounded.

        Parameters
        ----------
        solver : string
            Name of the solver to test.

        Returns
        -------
        test : function
            Test function for that solver.
        """

        def test(self):
            c, G, h = self.get_small_problem()
            G, h = G[1], h[1].reshape((1,))
            with self.assertRaises(ValueError):
                solve_lp(c, G, h, solver=solver)

        return test

    @staticmethod
    def get_test_unfeasible(solver):
        """
        Get test function for a given solver. In this variant, the linear
        program is unfeasible.

        Parameters
        ----------
        solver : string
            Name of the solver to test.

        Returns
        -------
        test : function
            Test function for that solver.
        """

        def test(self):
            c, G, h = self.get_small_problem()
            G[1] *= -1.0  # makes problem unfeasible
            with self.assertRaises(ValueError):
                solve_lp(c, G, h, solver=solver)

        return test


# Generate test fixtures for each solver
for solver in available_solvers:
    setattr(TestSolveLP, f"test_{solver}", TestSolveLP.get_test(solver))
    setattr(
        TestSolveLP,
        f"test_one_ineq_{solver}",
        TestSolveLP.get_test_one_ineq(solver),
    )
    setattr(
        TestSolveLP,
        f"test_unfeasible_{solver}",
        TestSolveLP.get_test_unfeasible(solver),
    )


if __name__ == "__main__":
    unittest.main()
