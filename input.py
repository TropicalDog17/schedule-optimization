def read_input():
    num_thesises, num_teachers, num_councils = map(int, input().split())

    a, b, c, d, e, f = map(int, input().split())
    s, g, q = [], [], []
    for _ in range(num_thesises):
        row = list(map(int, input().split()))
        s.append(row)

    for _ in range(num_thesises):
        row = list(map(int, input().split()))
        g.append(row)

    q = list(map(int, input().split()))

    return num_thesises, num_teachers, num_councils, a, b, c, d, e, f, s, g, q
