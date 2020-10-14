import math
import time
from helper import *
import matplotlib.pyplot as plt

# Laurel Dernbach
# CS31: Algorithms 20S
# Coding Assignment 3

# global counters to compare the number of elementary
# operations (i.e. simple multiplication) each function takes
naive_count = 0
karatsuba_count = 0

# naive algorithm for polynomial multiplication
def naive_mult(P, Q):
    global naive_count
    R = list()
    n = len(P)-1
    for k in range(0, (2*n)+1):
        if k <= n:
            sum1 = 0
            for i in range(0, k+1):
                sum1 += P[i]*Q[k-i]
                naive_count += 1
            R.append(sum1)
        if n < k <= 2*n:
            sum2 = 0
            for i in range((k-n), n+1):
                sum2 += P[i]*Q[k-i]
                naive_count += 1
            R.append(sum2)
    return R

# karatsuba algorithm for polynomial multiplication
def karatsuba(P, Q):
    global karatsuba_count
    n = len(P)-1

    # base cases
    if n == 1 or n == 0:
        karatsuba_count += 1
        return naive_mult(P, Q)

    # generate P' and Q'
    pPrime = []
    qPrime = []
    m = math.ceil(n/2)
    for i in range(0, m):
        pPrime.append(P[i] + P[m+i])
        qPrime.append(Q[i] + Q[m+i])
    if n > (2*m - 1):
        pPrime.append(P[n])
        qPrime.append(Q[n])
    else:
        pPrime.append(0)
        qPrime.append(0)

    r1 = karatsuba(P[0:m], Q[0:m])
    r2 = karatsuba(P[m:n+1], Q[m:n+1])
    r3 = karatsuba(pPrime[0:m+1], qPrime[0:m+1])

    # pad with 0s to ensure equal length
    r1.extend([0] * (2 * m - len(r1)+1))
    r2.extend([0] * (2 * m - len(r2)+1))
    r3.extend([0] * (2 * m - len(r3)+1))

    r4 = []
    for i in range(0, 2*m):
        karatsuba_count += 1
        r4.append(r3[i] - r1[i] - r2[i])
    r4.extend([0] * (2 * m - len(r4) + 1))  # padding with 0s

    R = []
    # R[i] = r1[i] + r4[i-m] + r2[i-2m]
    # if an index is out of range, "return" 0
    for i in range(0, 2 * n + 1):
        karatsuba_count += 1        # each case is one addition
        if i < 2 * m:
            # r1 in range, r4 neg index, r2 neg index
            if i < m:
                R.append(r1[i])
            # r1 in range, r4 pos index, r2 neg index
            else:
                R.append(r1[i] + r4[i - m])
        elif i > len(r1)-1:
            if i < 2 * m:
                # r1 out of range, r4 neg index, r2 neg index
                if i < m:
                    R.append(0)
                # r1 out of range, r4 pos index, r2 neg index
                else:
                    R.append(r4[i - m])
            # r1 out of range, r4 pos index in range, r2 pos index
            elif i > m and i-m < len(r2):
                R.append(r4[i-m] + r2[i - 2 * m])
            # r1 out of range, r4 out of range, r2 pos index
            else:
                R.append(r2[i - 2 * m])
        # r1 in range, r4 pos index, r2 pos index
        else:
            R.append(r1[i] + r4[i - m] + r2[i - 2 * m])

    return R

# calculates the sum of squares of coefficients of the polynomial that results from
# multiplying two n degree polynomials whose coefficients are the first n digits of pi
def SN(n):
    poly = read_pi(n+1)
    square = karatsuba(poly, poly)
    sum = 0
    for num in square:
        sum += num*num
    return sum

# graphs runtime based on actual time
def graph_plot(n):
    # X-axis: integers n,  1 to 2000 increasing in jumps of 50
    # Y1: time taken by naive_mult(P, Q) to square a n degree polynomial
    # with coefficient being the first n digits of pi
    # Y1: time taken by karatsuba(P, Q) to square a n degree polynomial
    # with coefficient being the first n digits of pi
    X = list()
    Y1 = list()
    Y2 = list()

    for i in range(1, n+1, 50):
        nums = read_pi(i)
        X.append(i)

        t1 = time.time()
        naive_mult(nums, nums)
        t2 = time.time()
        print("NMC", naive_count)
        Y1.append(t2 - t1)

        t3 = time.time()
        karatsuba(nums, nums)
        t4 = time.time()
        print("KC", karatsuba_count)
        Y2.append(t4 - t3)

        if (t4-t3) < (t2-t1):
            print("karatsuba wins when n =", i)

    # red is naive
    # green is karatsuba
    plt.plot(X, Y1, 'r', X, Y2, 'g')
    plt.show()

# graphs runtime based on global counters for elementary operations
def graph_plot_counters(n):
    # X-axis: integers n,  1 to 2000 increasing in jumps of 50
    # Y1: time taken by naive_mult(P, Q) to square a n degree polynomial
    # with coefficient being the first n digits of pi
    # Y1: time taken by karatsuba(P, Q) to square a n degree polynomial
    # with coefficient being the first n digits of pi
    X = list()
    Y1 = list()
    Y2 = list()

    for i in range(1, n+1, 50):
        nums = read_pi(i)
        X.append(i)

        naive_mult(nums, nums)
        Y1.append(naive_count)

        karatsuba(nums, nums)
        Y2.append(karatsuba_count)

    # red is naive
    # green is karatsuba
    plt.plot(X, Y1, 'r', X, Y2, 'g')
    plt.show()

graph_plot_counters(2000)






