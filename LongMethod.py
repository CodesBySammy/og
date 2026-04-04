def long_method():
    total = 0
    for i in range(100):
        for j in range(100):
            if i % 2 == 0:
                total += i * j
    print(total)
