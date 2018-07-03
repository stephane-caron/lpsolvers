# LP Solvers for Python

Wrapper around Linear Programming (LP) solvers in Python, with a unified
interface.

## Installation

The simplest way to install this module is:
```
pip install lpsolvers
```
You can add the ``--user`` parameter for a user-only installation.

## Usage

The function ``solve_Lp(c, A, b)`` is called with the ``solver`` keyword
argument to select the backend solver. The quadratic program it solves is, in
standard form:

```
    max  c^T x
    s.t. G x <= h
         A x == b
```

Vector inequalities are taken coordinate by coordinate.

## Solvers

The list of supported solvers currently includes:

- [CVXOPT](http://cvxopt.org/)
- [cdd](https://github.com/mcmtroffaes/pycddlib)

## Example

To solve a quadratic program, simply build the matrices that define it and call
the ``solve_lp`` function:

```python
from numpy import array
from lpsolvers import solve_lp

c = array([1., 2., 3.])
A = array([[1., 2., -1.], [2., 0., 1.], [1., 2., 1.], [-1., -1., -1.]])
b = array([4., 1., 3., 2.])

print "LP solution:", solve_lp(c, A, b)
```
