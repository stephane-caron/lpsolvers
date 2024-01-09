#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2016-2022 Stéphane Caron

"""Exceptions."""


class LPSolverException(Exception):
    """Base class for lpsolvers exception."""


class SolverNotFound(LPSolverException):
    """Exception raised when a requested solver is not found."""


class NoSolverSelected(LPSolverException):
    """Exception raised when the `solver` keyword argument is not set."""
