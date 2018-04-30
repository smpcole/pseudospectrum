import numpy as np
import random
import matplotlib.pyplot as plt
import sys

def unif(a, b):
    return lambda: random.uniform(a, b)
    
def random_matrix(m, n, symmetric = False, distr = unif(-1, 1)):
    A = np.zeros((m, n))
    if symmetric and m != n:
        raise ValueError("Dimensions of a symmetric matrix must be equal.")
    for i in range(n):
        for j in range(n):
            if symmetric and j < i:
                A[i, j] = A[j, i]
            else:
                A[i, j] = distr()
    return A            

def random_symmetric_matrix(n, distr = unif(-1, 1)):
    return random_matrix(n, n, True, distr)

# Append all eigenvalues of A to the lists x and y
# x = real components, y = imaginary components
def get_eigs(A, x, y):
    for z in np.linalg.eigvals(A):
        x.append(z.real)
        y.append(z.imag)

def test_pseudospectrum(A = None, symmetric = False, epsilons = (.1, .01, .0001, .000001), T = 100):
    random.seed()
    if A is None:
        A = random_matrix(5, 5)
    m, n = A.shape
    if m != n:
        raise ValueError("Matrix dimensions must be equal.")
    Ax = []
    Ay = []
    get_eigs(A, Ax, Ay)
    i = 1
    for epsilon in epsilons:
        x = []
        y = []
        for t in range(T):
            B = A + epsilon * random_matrix(n, n, symmetric)
            get_eigs(B, x, y)
        plt.figure(i)
        plt.plot(x, y, ".")
        plt.plot(Ax, Ay, "+")
        plt.title(r"$\epsilon$ = %f, $T$ = %d" % (epsilon, T))
        plt.savefig("output%d.pdf" % i)
        i += 1

def test_a():
    test_pseudospectrum()

def test_b():
    A = np.zeros((5, 5))
    A[:4, :4] = .1 * random_matrix(4, 4)
    A[4, 4] = -.5
    print(A)
    test_pseudospectrum(A)

def test_ci():
    test_pseudospectrum(random_symmetric_matrix(5, unif(-.25, .25)))

def test_cii():
    test_pseudospectrum(random_symmetric_matrix(5, unif(-.25, .25)), True)
    

if __name__ == "__main__":        
    test = sys.argv[1]
    if test == "a":
        test_a()
    elif test == "b":
        test_b()
    elif test == "ci":
        test_ci()
    elif test == "cii":
        test_cii()
    else:
        print("Invalid test: %s" % test)
