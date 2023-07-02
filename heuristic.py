import random
import sys
from input import read_input

# check operating system
if sys.platform == "win32":
    sys.stdin = open(".\\testcase\\example.txt", "r")
else:
    sys.stdin = open("./testcase/example.txt", "r")


num_theses, num_teachers, num_councils, a, b, c, d, e, f, s, g, q = read_input()

temp = [[0] * num_teachers for _ in range(num_theses)]

for i, val in enumerate(q):
    temp[i][val - 1] = 1
q = temp

p = [[0 for _ in range(num_councils)] for _ in range(num_teachers)]
h = [[0 for _ in range(num_councils)] for _ in range(num_theses)]

# Randomly assign teachers to councils
for i in range(num_teachers):
    p[i][random.randint(0, num_councils - 1)] = 1

# Randomly assign theses to councils
for i in range(num_theses):
    h[i][random.randint(0, num_councils - 1)] = 1

# Heuristic optimization
# Reassign based on the heuristic to satisfy the constraints


# function to get the total similarity score within a council
def get_council_similarity(council):
    score = 0
    for i in range(num_theses):
        for j in range(i + 1, num_theses):
            if h[i][council] == 1 and h[j][council] == 1:
                score += s[i][j]
    return score


# function to get the total similarity score between theses and teachers within a council
def get_council_teacher_similarity(council):
    score = 0
    for i in range(num_theses):
        for j in range(num_teachers):
            if h[i][council] == 1 and p[j][council] == 1:
                score += g[i][j]
    return score


# Optimize the assignments for each council
for k in range(num_councils):
    council_theses = [i for i in range(num_theses) if h[i][k] == 1]
    council_teachers = [j for j in range(num_teachers) if p[j][k] == 1]

    # Ensure the number of theses in the council is within [a, b]
    while len(council_theses) < a:
        i = random.choice([i for i in range(num_theses) if h[i][k] == 0])
        h[i][k] = 1
        council_theses.append(i)

    while len(council_theses) > b:
        i = random.choice([i for i in council_theses])
        h[i][k] = 0
        council_theses.remove(i)

    # Ensure the number of teachers in the council is within [c, d]
    while len(council_teachers) < c:
        j = random.choice([j for j in range(num_teachers) if p[j][k] == 0])
        p[j][k] = 1
        council_teachers.append(j)

    while len(council_teachers) > d:
        j = random.choice([j for j in council_teachers])
        p[j][k] = 0
        council_teachers.remove(j)

    # Ensure each thesis is assigned to exactly one council
    for i in range(num_theses):
        if h[i][k] == 1 and sum(h[i]) > 1:
            other_council = random.choice([c for c in range(num_councils) if c != k])
            h[i][k] = 0
            h[i][other_council] = 1

    # Ensure each teacher is assigned to exactly one council
    for j in range(num_teachers):
        if p[j][k] == 1 and sum(p[j]) > 1:
            other_council = random.choice([c for c in range(num_councils) if c != k])
            p[j][k] = 0
            p[j][other_council] = 1

    # for i in range(num_theses):
    #     if h[i][k] == 1:
    #         for j in range(num_teachers):
    #             if p[j][k] == 1:
    #                 if g[i][j] < e:
    #                     p[j][k] = 1 - p[j][k]
    #                     break
    #         if sum(p[j]) > 1:
    #             p[j][k] = 1 - p[j][k]
    #             break
    # for j in range(num_teachers):
    #     if p[j][k] == 1:
    #         for i in range(num_theses):
    #             if h[i][k] == 1:
    #                 if g[i][j] < f:
    #                     h[i][k] = 1 - h[i][k]
    #                     break
    #         if sum(h[i]) > 1:
    #             h[i][k] = 1 - h[i][k]
    #             break
    # Similarity score between each pair of thesis in each council is at least e
    # s[i][j] >= e * h[i, k] * h[j, k]
    for i in range(num_theses):
        for j in range(i + 1, num_theses):
            if h[i][k] == 1 and h[j][k] == 1 and s[i][j] < e:
                h[i][k] = 1 - h[i][k]
                break
        if sum(h[i]) > 1:
            h[i][k] = 1 - h[i][k]
            break

    # Similarity score between each pair of thesis and teacher in each council is at least f
    # g[i][j] >= f * h[i, k] * p[j, k]
    for i in range(num_theses):
        for j in range(num_teachers):
            if h[i][k] == 1 and p[j][k] == 1 and g[i][j] < f:
                p[j][k] = 1 - p[j][k]
                break
        if sum(p[j]) > 1:
            p[j][k] = 1 - p[j][k]
            break


def calc_score():
    score = 0
    for i in range(num_theses):
        for j in range(i + 1, num_theses):
            for k in range(num_councils):
                score += s[i][j] * h[i][k] * h[j][k]
    for i in range(num_theses):
        for j in range(num_teachers):
            for k in range(num_councils):
                score += g[i][j] * h[i][k] * p[j][k]
    return score


# Print the results
print(num_theses)
for i in range(num_theses):
    for j in range(num_councils):
        if h[i][j] == 1:
            print(j + 1, end=" ")
print()

print(num_teachers)
for i in range(num_teachers):
    for j in range(num_councils):
        if p[i][j] == 1:
            print(j + 1, end=" ")
print()
print("Objective value", calc_score())
