from itertools import islice
def trangle():
    result = [1,]
    while True:
        yield result
        result.append(2)
        yield result
        result.append(3)
        yield result
t = trangle()
for i in range(10):
    print(next(t))

