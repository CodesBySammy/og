def main():
    data = {"a": 1, "b": 2}
    result = 0
    for k in data:
        if data[k] > 0:
            result += data[k]
    print(result)

main()
