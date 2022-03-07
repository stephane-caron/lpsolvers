:github_url: https://github.com/stephane-caron/lpsolvers/tree/master/doc/src/linear-programming.rst

.. _Linear programming:

******************
Linear programming
******************

To solve a linear program, simply build the matrices that define it and call
the :func:`.solve_lp` function:

.. code:: python

    from numpy import array
    from lpsolvers import solve_lp

    c = array([1., 2., 3.])
    G = array([[1., 2., -1.], [2., 0., 1.], [1., 2., 1.], [-1., -1., -1.]])
    h = array([4., 1., 3., 2.])

    x = solve_lp(c, G, h)
    print(f"LP solution: x = {x}")

This example outputs the solution ``[0.30769231, -0.69230769,  1.38461538]``.
The :func:`.solve_qp` function accepts a ``solver`` keyword argument to select
the backend solver:

.. autofunction:: lpsolvers.solve_lp

Installed solvers are listed in:

.. autodata:: lpsolvers.available_solvers

See the ``examples/`` folder in the repository for other use cases. For more
context you can also check out this post on `linear programming in Python
<https://scaron.info/blog/linear-programming-in-python-with-cvxopt.html>`_.
