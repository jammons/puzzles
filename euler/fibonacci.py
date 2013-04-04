def next_fib(first, second, max):
    next = first + second
    if next >= max:
        return []
    else:
        return [next] + next_fib(second, next, max)


def gen_fibonacci(max):
    ''' generate all fibonacci numbers less than max '''
    return [1, 2] + next_fib(1, 2, max)

def is_even(num):
    if num%2 == 0:
        return True
    else:
        return False

def sum_evens(max):
    fibs = gen_fibonacci(max)
    evens = [f for f in fibs if is_even(f)]
    return sum(evens)
