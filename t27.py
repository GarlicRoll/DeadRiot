N = int(input())
S = 0
d = 1001

for i in range(N):
    a,b = map(int, input().split())
    if a > b:
        S += a
    else:
        S += b
    if abs(a - b) < d and abs(a - b) % 7 == 0:
        d = abs(a - b)

print(d)
if S % 7 == 0:
    print(S)
else:
    print(S - d)