from ortools.sat.python import cp_model
import sys
from input import read_input


if sys.platform == "win32":
    sys.stdin = open(".\\testcase\\example.txt", "r")
else:
    sys.stdin = open("./testcase/example.txt", "r")

model = cp_model.CpModel()

num_thesises, num_teachers, num_councils, a, b, c, d, e, f, s, g, q = read_input()

for i in range(len(q)):
    q[i] = q[i] - 1


p, h = [0] * num_thesises, [0] * num_teachers
for i in range(num_thesises):
    p[i] = model.NewIntVar(0, num_councils - 1, f"p_{i}")
for i in range(num_teachers):
    h[i] = model.NewIntVar(0, num_councils - 1, f"h_{i}")

# Implement teacher in council constraints, each council teacher count must be in [c, d]
for i in range(num_councils):
    teacher_in_council = []
    for j in range(num_teachers):
        teacher_j_in_council_i = model.NewBoolVar(f"teacher_{j}_in_council_{i}")
        model.Add(h[j] == i).OnlyEnforceIf(teacher_j_in_council_i)
        model.Add(h[j] != i).OnlyEnforceIf(teacher_j_in_council_i.Not())
        teacher_in_council.append(teacher_j_in_council_i)
    model.Add(sum(teacher_in_council) >= c)
    model.Add(sum(teacher_in_council) <= d)
# Implement thesis in council constraints, each council teacher count must be in [a, b]
for i in range(num_councils):
    thesis_in_council = []
    for j in range(num_thesises):
        thesis_j_in_council_i = model.NewBoolVar(f"thesis_{j}_in_council_{i}")
        model.Add(p[j] == i).OnlyEnforceIf(thesis_j_in_council_i)
        model.Add(p[j] != i).OnlyEnforceIf(thesis_j_in_council_i.Not())
        thesis_in_council.append(thesis_j_in_council_i)
    model.Add(sum(thesis_in_council) >= a)
    model.Add(sum(thesis_in_council) <= b)
# Implement thesis and teacher not in same council constraints
for i in range(num_thesises):
    for j in range(num_teachers):
        # only if thesis i has advisor j
        thesis_i_teacher_j = model.NewBoolVar(f"thesis_{i}_teacher_{j}")
        model.Add(q[i] == j).OnlyEnforceIf(thesis_i_teacher_j)
        model.Add(q[i] != j).OnlyEnforceIf(thesis_i_teacher_j.Not())
        # thesis i and teacher j not in same council
        not_same_council = model.NewBoolVar(f"not_same_council_{i}_{j}")
        model.Add(p[i] != h[j]).OnlyEnforceIf(not_same_council)
        model.Add(p[i] == h[j]).OnlyEnforceIf(not_same_council.Not())
        # thesis i and teacher j not in same council only if thesis i has advisor j
        model.AddBoolAnd([thesis_i_teacher_j, not_same_council]).OnlyEnforceIf(
            thesis_i_teacher_j
        )

# Similarity of thesis i and thesis j must be greater than e if they are in the same council
for i in range(num_thesises):
    for j in range(i + 1, num_thesises):
        thesis_i_and_j_in_same_council = model.NewBoolVar(
            f"thesis_{i}_and_{j}_in_same_council"
        )
        model.Add(p[i] == p[j]).OnlyEnforceIf(thesis_i_and_j_in_same_council)
        model.Add(p[i] != p[j]).OnlyEnforceIf(thesis_i_and_j_in_same_council.Not())
        model.Add(s[i][j] >= e).OnlyEnforceIf(thesis_i_and_j_in_same_council)

# Similarity of thesis i and teacher j must be greater than f, if they are in the same council
for i in range(num_thesises):
    for j in range(num_teachers):
        thesis_i_and_teacher_j_in_same_council = model.NewBoolVar(
            f"thesis_{i}_and_teacher_{j}_in_same_council"
        )
        model.Add(p[i] == h[j]).OnlyEnforceIf(thesis_i_and_teacher_j_in_same_council)
        model.Add(p[i] != h[j]).OnlyEnforceIf(
            thesis_i_and_teacher_j_in_same_council.Not()
        )
        model.Add(g[i][j] >= f).OnlyEnforceIf(thesis_i_and_teacher_j_in_same_council)
obj = []
# check if thesis i and thesis j are in the same council
for i in range(num_thesises):
    for j in range(i + 1, num_thesises):
        thesis_i_and_j_in_same_council = model.NewBoolVar(
            f"thesis_{i}_and_{j}_in_same_council"
        )
        model.Add(p[i] == p[j]).OnlyEnforceIf(thesis_i_and_j_in_same_council)
        model.Add(p[i] != p[j]).OnlyEnforceIf(thesis_i_and_j_in_same_council.Not())
        obj.append(thesis_i_and_j_in_same_council * s[i][j])
# check if thesis i and teacher j are in the same council
for i in range(num_thesises):
    for j in range(num_teachers):
        thesis_i_and_teacher_j_in_same_council = model.NewBoolVar(
            f"thesis_{i}_and_teacher_{j}_in_same_council"
        )
        model.Add(p[i] == h[j]).OnlyEnforceIf(thesis_i_and_teacher_j_in_same_council)
        model.Add(p[i] != h[j]).OnlyEnforceIf(
            thesis_i_and_teacher_j_in_same_council.Not()
        )
        obj.append(thesis_i_and_teacher_j_in_same_council * g[i][j])
model.Maximize(sum(obj))
# Solve the model
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 60.0
status = solver.Solve(model)

# Check if a feasible solution was found
if status == cp_model.OPTIMAL:
    # Retrieve the assignments of theses and teachers to councils
    thesis_assignments = [solver.Value(p[i]) + 1 for i in range(num_thesises)]
    teacher_assignments = [solver.Value(h[i]) + 1 for i in range(num_teachers)]

    print("Thesis assignments:", thesis_assignments)
    print("Teacher assignments:", teacher_assignments)
    # Print the objective value
    print("Objective value:", solver.ObjectiveValue())
else:
    print("No feasible solution found.")
