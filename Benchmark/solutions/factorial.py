fact = lambda n : 1 if n <= 1 else n * fact(n-1)
for _ in range(int(input())): print(fact(int(input())))