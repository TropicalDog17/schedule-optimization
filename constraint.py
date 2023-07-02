from ortools.sat.python import cp_model
import sys
from input import read_input

if sys.platform == "win32":
    sys.stdin = open(".\\testcase\\example.txt", "r")
else:
    sys.stdin = open("./testcase/example.txt", "r")

model = cp_model.CpModel()
num_thesises, num_teachers, num_councils, a, b, c, d, e, f, s, g, q = read_input()
temp = [[0] * num_teachers for _ in range(num_thesises)]

for i, val in enumerate(q):
    temp[i][val - 1] = 1
q = temp

# Binary integer variables
p, h = [], []  # h - đồ án i nằm ở hội đồng j
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
print(num_thesises)
for i in range(num_thesises):
    for j in range(num_councils):
        if solver.Value(h[i][j]) == 1:
            print(j + 1, end=" ")
print()
print(num_teachers)
for i in range(num_teachers):
    for j in range(num_councils):
        if solver.Value(p[i][j]) == 1:
            print(j + 1, end=" ")
print()
