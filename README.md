# LP Solvers for Python

[![CI](https://img.shields.io/github/actions/workflow/status/stephane-caron/lpsolvers/test.yml?branch=main)](https://github.com/stephane-caron/lpsolvers/actions)
[![Documentation](https://img.shields.io/github/actions/workflow/status/stephane-caron/lpsolvers/docs.yml?branch=main&label=docs)](https://stephane-caron.github.io/lpsolvers/)
[![Coverage](https://coveralls.io/repos/github/stephane-caron/lpsolvers/badge.svg?branch=main)](https://coveralls.io/github/stephane-caron/lpsolvers?branch=main)
[![Conda version](https://img.shields.io/conda/vn/conda-forge/lpsolvers.svg)](https://anaconda.org/conda-forge/lpsolvers)
[![PyPI version](https://img.shields.io/pypi/v/lpsolvers)](https://pypi.org/project/lpsolvers/)

Wrapper around Linear Programming (LP) solvers in Python, with a unified interface.

## Installation

### From conda-forge

```console
conda install -c conda-forge lpsolvers
```

### From PyPI

To install the library and all available LP solvers at the same time:

```console
pip install lpsolvers[open_source_solvers]
```

To install the library only, assuming LP solvers are installed separately: ``pip install lpsolvers``.

## Usage

The function [`solve_lp`](https://stephane-caron.github.io/lpsolvers//linear-programming.html#lpsolvers.solve_lp) is called with the ``solver`` keyword argument to select the backend solver. The linear program it solves is, in standard form:

$$
\begin{split}
\begin{array}{ll}
    \mbox{minimize} &
        c^T x \\
    \mbox{subject to}
        & G x \leq h \\
        & A x = b
\end{array}
\end{split}
$$

Vector inequalities are taken coordinate by coordinate.

## Example

To solve a linear program, build the matrices that define it and call the ``solve_lp`` function:

```python
from numpy import array
from lpsolvers import solve_lp

c = array([1., 2., 3.])
G = array([[1., 2., -1.], [2., 0., 1.], [1., 2., 1.], [-1., -1., -1.]])
h = array([4., 1., 3., 2.])

x = solve_lp(c, G, h, solver="cvxopt")  # select solver here
print(f"LP solution: {x=}")
```

This example outputs the solution ``[2.2, -0.8, -3.4]``.

## Solvers

The list of supported solvers currently includes:

- [cdd](https://github.com/mcmtroffaes/pycddlib)
- [CVXOPT](http://cvxopt.org/)
- [CVXPY](https://www.cvxpy.org/) (interface)
- [PDLP](https://developers.google.com/optimization/lp/pdlp_math)
- [ProxQP](https://github.com/Simple-Robotics/proxsuite#proxqp)
