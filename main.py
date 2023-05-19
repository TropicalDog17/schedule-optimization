from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver("SCIP")
if not solver:
    pass

q, p, h = {}, {}, {}
a, b, c, d, e, f = 2, 4, 1, 3, 1, 1
num_thesises, num_teachers, num_councils = 6, 4, 2


# Similarity matrix between thesis i and thesis j is as follows: 0 2 4 1 2 5 2 0 5 5 3 5 4 5 0 4 3 5 1 5 4 0 3 2 2 3 3 3 0 3 5 5 5 2 3 0
s = [
    [0, 2, 4, 1, 2, 5],
    [2, 0, 5, 5, 3, 5],
    [4, 5, 0, 4, 3, 5],
    [1, 5, 4, 0, 3, 2],
    [2, 3, 3, 3, 0, 3],
    [5, 5, 5, 2, 3, 0],
]
# Similarity score between thesis i and teacher j is as follows: 3 5 1 5 5 2 5 3 3 1 3 3 5 5 1 3 4 5 4 1 5 3 4 5\
g = [
    [3, 5, 1, 5],
    [5, 2, 5, 3],
    [3, 1, 3, 3],
    [5, 5, 1, 3],
    [4, 5, 4, 1],
    [5, 3, 4, 5],
]

# Thesis i has t[i] as an advisor
t = [1, 3, 4, 2, 2, 3]
for i in range(num_thesises):
    for j in range(num_teachers):
        q[i, j] = solver.IntVar(0, 1, "")
for i in range(num_thesises):
    for j in range(num_councils):
        h[i, j] = solver.IntVar(0, 1, "")
for i in range(num_teachers):
    for j in range(num_councils):
        p[i, j] = solver.IntVar(0, 1, "")
# Each thesis is assigned to exactly 1 council
# Each thesis is assigned to exactly 1 teacher
for i in range(num_thesises):
    solver.Add(solver.Sum([h[i, j] for j in range(num_councils)]) <= 1)
    solver.Add(solver.Sum([q[i, j] for j in range(num_teachers)]) <= 1)

# Each teacher is assigned to exactly 1 council
for i in range(num_teachers):
    solver.Add(solver.Sum([p[i, j] for j in range(num_councils)]) <= 1)
# Amount of thesises assigned to each council is in range [a, b]
for i in range(num_councils):
    solver.Add(solver.Sum([h[j, i] for j in range(num_thesises)]) >= a)
    solver.Add(solver.Sum([h[j, i] for j in range(num_thesises)]) <= b)
# Amount of teacher assigned to each council is in range [c, d]
for i in range(num_councils):
    solver.Add(solver.Sum([p[j, i] for j in range(num_teachers)]) >= c)
    solver.Add(solver.Sum([p[j, i] for j in range(num_teachers)]) <= d)
# Teacher isn't allowed to be assigned to council where his thesis is
for i in range(num_thesises):
    for j in range(num_teachers):
        for k in range(num_councils):
            solver.Add(p[t[i] - 1, k] + h[i, k] <= 1)
# Similarity score between each pair of thesis in each council is at least e
for k in range(num_councils):
    for i in range(num_thesises):
        for j in range(num_thesises):
            solver.Add(s[i][j] >= e * h[i, k] * h[j, k])
# Similarity score between each pair of thesis and teacher in each council is at least f
for k in range(num_councils):
    for i in range(num_thesises):
        for j in range(num_teachers):
            solver.Add(g[i][j] >= f * h[i, k] * p[j, k])
# Objective function
# Maximize sum of similarity score between each pair of thesis in each council, and sum of similarity score between each pair of thesis and teacher in each council
solver.Maximize(
    solver.Sum(
        [
            solver.Sum([s[i][j] * h[i, k] * h[j, k] for i in range(num_thesises)])
            for j in range(num_thesises)
        ]
        for k in range(num_councils)
    )
    + solver.Sum(
        [
            solver.Sum([g[i][j] * h[i, k] * p[j, k] for i in range(num_thesises)])
            for j in range(num_teachers)
        ]
        for k in range(num_councils)
    )
)
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL:
    for i in range(num_thesises):
        for j in range(num_councils):
            if h[i, j].solution_value() == 1:
                print("Thesis ", i + 1, " is assigned to council ", j + 1)
    for i in range(num_teachers):
        for j in range(num_councils):
            if p[i, j].solution_value() == 1:
                print("Teacher ", i + 1, " is assigned to council ", j + 1)
else:
    print("No solution found")
