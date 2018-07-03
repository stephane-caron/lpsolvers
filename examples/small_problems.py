from lpsolvers import available_solvers, solve_lp
from numpy import array, ones, eye, zeros

problems = []

c = -ones(10)
A = eye(10)
b = zeros(10)
problems.append((c, A, b))

c = array([1., 2., 3.])
A = array([
    [1., 2., -1.],
    [2., 0., 1.],
    [1., 2., 1.],
    [-1., -1., -1.]])
b = array([4., 1., 3., 2.])
problems.append((c, A, b))

if __name__ == "__main__":
    for i, (c, A, b) in enumerate(problems):
        for solver in available_solvers:
            x = solve_lp(c, A, b, solver=solver)
            print "LP %d for %6s:" % (i, solver), x
