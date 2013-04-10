import math

def calc_prime_factors(num):
    ''' returns a list of prime factors for the given num '''
    # one of the factors has to be less than sqrt(num)
    possible_primes = get_primes(int(math.sqrt(num)+1))

    return test_factors(num, possible_primes)


def test_factors(num, possible_primes):
    for prime in possible_primes:
        if num % prime == 0:
            print prime
            if num == prime:
                # end case
                return [prime]
            else:
                next = num/prime
                return [prime] + test_factors(next, possible_primes)

def get_primes(num):
    prime_list = []
    marked_list = [False]*(num+1)
    for factor in range(2, num+1):
        if not marked_list[factor]:
            prime_list.append(factor)
            for m in range(factor**2, num+1, factor):
                marked_list[m] = True
    return prime_list


'''
# this is slower than the above
def get_primes(num):
    nums = set([i for i in range(1, num+1)])

    # remove non-primes
    for factor in range(2, int(math.sqrt(num)+1)):
        factor_set = set([factor*i for i in range(2, (num/factor)+1)])
        nums = nums - factor_set

    return nums
'''

#t = timeit.Timer('prime_set(10000)', 'from __main__ import prime_set')
#t1 = timeit.Timer('alt_prime_set(10000)', 'from __main__ import alt_prime_set')
