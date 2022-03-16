# LP Solvers for Python

[**Installation**](https://github.com/stephane-caron/lpsolvers#installation)
| [**Documentation**](https://scaron.info/doc/lpsolvers/)
| [**Example**](https://github.com/stephane-caron/lpsolvers#example)
| [**Solvers**](https://github.com/stephane-caron/lpsolvers#solvers)

[![build](https://img.shields.io/github/workflow/status/stephane-caron/lpsolvers/CI)](https://github.com/stephane-caron/lpsolvers/actions)
[![PyPI package](https://img.shields.io/pypi/v/lpsolvers)](https://pypi.org/project/lpsolvers/)
![Status](https://img.shields.io/pypi/status/lpsolvers)

Wrapper around Linear Programming (LP) solvers in Python, with a unified interface.

## Installation

The simplest way to install this module is:

```sh
sudo apt install libgmp-dev python3-dev
pip install lpsolvers
```

You can add the ``--user`` parameter for a user-only installation.

## Usage

The function ``solve_lp(c, G, h, A, b)`` is called with the ``solver`` keyword argument to select the backend solver. The linear program it solves is, in standard form:

![Linear program in standard form](https://raw.githubusercontent.com/stephane-caron/lpsolvers/master/doc/src/images/lp.gif)

Vector inequalities are taken coordinate by coordinate.

## Example

To solve a linear program, build the matrices that define it and call the ``solve_lp`` function:

```python
from numpy import array
from lpsolvers import solve_lp

c = array([1., 2., 3.])
G = array([[1., 2., -1.], [2., 0., 1.], [1., 2., 1.], [-1., -1., -1.]])
h = array([4., 1., 3., 2.])

print "LP solution:", solve_lp(c, G, h)
```

This example outputs the solution ``[2.2, -0.8, -3.4]``.

## Solvers

The list of supported solvers currently includes:

- [CVXOPT](http://cvxopt.org/)
- [CVXPY](https://www.cvxpy.org/) (interface)
- [cdd](https://github.com/mcmtroffaes/pycddlib)
