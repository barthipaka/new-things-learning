def f1():
    yield 1
    yield 2
    yield 3


result = f1()
for value in result:
    print(value)


def f1():
    for x in range(1,4):
        yield x

result = f1()
for value in result:
    print(value)

    