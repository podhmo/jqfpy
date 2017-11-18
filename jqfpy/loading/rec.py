def consume_rec(xs, fn, n=0):
    if n <= 0:
        fn(xs)
    else:
        for x in xs:
            consume_rec(x, fn, n=n - 1)
