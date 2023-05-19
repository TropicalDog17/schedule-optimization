from ortools.sat.python import cp_model

model = cp_model.CpModel()
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

q = [
    [1, 0, 0, 0],  # Thesis 0 has advisor 1
    [0, 0, 1, 0],  # Thesis 1 has advisor 3
    [0, 0, 0, 1],  # Thesis 2 has advisor 4
    [0, 1, 0, 0],  # Thesis 3 has advisor 2
    [0, 1, 0, 0],  # Thesis 4 has advisor 2
    [0, 0, 1, 0],  # Thesis 5 has advisor 3
]
# Binary integer variables
p, h = [], []
for i in range(num_thesises):
    t = []
    for j in range(num_councils):
        t.append(model.NewBoolVar(f"p_{i}_{j}"))
    h.append(t)
for i in range(num_teachers):
    t = []
    for j in range(num_councils):
        t.append(model.NewBoolVar(f"h_{i}_{j}"))
    p.append(t)
# Each thesis is assigned to exactly 1 council
for i in range(num_thesises):
    model.Add(sum(h[i]) == 1)
# Each teacher is assigned to exactly 1 council
for i in range(num_teachers):
    model.Add(sum(p[i]) == 1)

# Amount of thesises assigned to each council is in range [a, b]
for i in range(num_councils):
    model.Add(a <= sum(h[j][i] for j in range(num_thesises)))
    model.Add(sum(h[j][i] for j in range(num_thesises)) <= b)
# Amount of teachers assigned to each council is in range [c, d]
for i in range(num_councils):
    model.Add(c <= sum(p[j][i] for j in range(num_teachers)))
    model.Add(sum(p[j][i] for j in range(num_teachers)) <= d)
# Teacher isn't allowed to be assigned to council where his thesis is
for i in range(num_thesises):
    for j in range(num_teachers):
        for k in range(num_councils):
            model.Add(q[i][j] * p[j][k] + h[i][k] <= 1)
# Similarity score between each pair of thesis in each council is at least e
# s[i][j] >= e * h[i, k] * h[j, k]

for i in range(num_councils):
    for j in range(num_thesises):
        for k in range(j + 1, num_thesises):
            j_in_i = model.NewBoolVar(f"j_in_i")
            k_in_i = model.NewBoolVar(f"k_in_i")
            both_in_i = model.NewBoolVar(f"both_in_i")
            model.Add(h[j][i] == 1).OnlyEnforceIf(j_in_i)
            model.Add(h[k][i] == 1).OnlyEnforceIf(k_in_i)
            model.Add(both_in_i == 1).OnlyEnforceIf([j_in_i, k_in_i])
            model.Add(s[j][k] >= e * both_in_i)

# Similarity score between each pair of thesis and teacher in each council is at least f
# g[i][j] >= f * h[i, k] * p[j, k]
for i in range(num_councils):
    for j in range(num_thesises):
        for k in range(num_teachers):
            j_in_i = model.NewBoolVar(f"j_in_i")
            k_in_i = model.NewBoolVar(f"k_in_i")
            both_in_i = model.NewBoolVar(f"both_in_i")
            model.Add(h[j][i] == 1).OnlyEnforceIf(j_in_i)
            model.Add(p[k][i] == 1).OnlyEnforceIf(k_in_i)
            model.Add(both_in_i == 1).OnlyEnforceIf([j_in_i, k_in_i])
            model.Add(g[j][k] >= f * both_in_i)
# Objective function
# Maximize sum of similarity score between each pair of thesis in each council, and sum of similarity score between each pair of thesis and teacher in each council
obj = []
for i in range(num_councils):
    for j in range(num_thesises):
        for k in range(num_thesises):
            if k > j:
                j_in_i = model.NewBoolVar(f"j_in_i_{i}_{j}_{k}")
                k_in_i = model.NewBoolVar(f"k_in_i_{i}_{j}_{k}")
                both_in_i = model.NewBoolVar(f"both_in_i_{i}_{j}_{k}")
                model.Add(h[j][i] == 1).OnlyEnforceIf(j_in_i)
                model.Add(h[j][i] == 0).OnlyEnforceIf(j_in_i.Not())
                model.Add(h[k][i] == 1).OnlyEnforceIf(k_in_i)
                model.Add(h[k][i] == 0).OnlyEnforceIf(k_in_i.Not())
                model.Add(both_in_i == 1).OnlyEnforceIf([j_in_i, k_in_i])
                model.Add(both_in_i == 0).OnlyEnforceIf([j_in_i.Not(), k_in_i.Not()])
                model.Add(both_in_i == 0).OnlyEnforceIf([j_in_i, k_in_i.Not()])
                model.Add(both_in_i == 0).OnlyEnforceIf([j_in_i.Not(), k_in_i])
                obj.append(s[j][k] * both_in_i)
for i in range(num_councils):
    for j in range(num_thesises):
        for k in range(num_teachers):
            j_in_i = model.NewBoolVar(f"j_in_i_{i}_{j}_{k}")
            k_in_i = model.NewBoolVar(f"k_in_i_{i}_{j}_{k}")
            both_in_i = model.NewBoolVar(f"both_in_i_{i}_{j}_{k}")
            model.Add(h[j][i] == 1).OnlyEnforceIf(j_in_i)
            model.Add(h[j][i] == 0).OnlyEnforceIf(j_in_i.Not())
            model.Add(p[k][i] == 1).OnlyEnforceIf(k_in_i)
            model.Add(p[k][i] == 0).OnlyEnforceIf(k_in_i.Not())

            model.Add(both_in_i == 1).OnlyEnforceIf([j_in_i, k_in_i])
            model.Add(both_in_i == 0).OnlyEnforceIf([j_in_i.Not(), k_in_i.Not()])
            model.Add(both_in_i == 0).OnlyEnforceIf([j_in_i.Not(), k_in_i])
            model.Add(both_in_i == 0).OnlyEnforceIf([j_in_i, k_in_i.Not()])
            obj.append(g[j][k] * both_in_i)

model.Maximize(sum(obj))
solver = cp_model.CpSolver()
solver.Solve(model)

print("Optimal value: ", solver.ObjectiveValue())
print()
for i in range(num_thesises):
    for j in range(num_councils):
        if solver.Value(h[i][j]) == 1:
            print(f"Thesis {i + 1} is assigned to council {j + 1}")
print()
for i in range(num_teachers):
    for j in range(num_councils):
        if solver.Value(p[i][j]) == 1:
            print(f"Teacher {i + 1} is assigned to council {j + 1}")
