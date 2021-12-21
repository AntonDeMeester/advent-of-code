from collections import defaultdict

c = defaultdict(int)

for i in range(1, 4):
    for j in range(1, 4):
        for k in range(1, 4):
            c[i + j + k] += 1

print(c)
