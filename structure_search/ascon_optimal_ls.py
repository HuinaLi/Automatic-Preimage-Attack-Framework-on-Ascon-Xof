#-------------------------------------------------------------------------------
# Name:     Ascon permutation
# Purpose:  Model initialization: generate initial state CNF
#           All CNF consists of three parts: 
#           1. initial state CNF (generete using ascon_optimal_ls.py), 
#           2. sbox and Constraint CNF (using get_allcons_cnf_ascon.py), 
#           3. Objective Function CNF (using PySat,https://pysathq.github.io/) 
# Author:   Anonymous
# Created:  12-12-2022
# Version:  1st
#-------------------------------------------------------------------------------
from sage.all import *
from copy import copy, deepcopy
from sage.rings.polynomial.pbori.pbori import *
from sage.rings.polynomial.pbori import *
from random import randint
from sage.sat.boolean_polynomials import solve as solve_sat
from sage.sat.converters.polybori import CNFEncoder
from sage.sat.solvers.dimacs import DIMACS
import sys
import logging
import argparse


# create logger
logger = logging.getLogger("XOR model: Ascon")
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter("c:%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)

def SingleMatrix(X, r0, r1):
    """SingleMatrix transform X

    Args:
        X (list): 64 bit input
        r0 (int): shift bits r0
        r1 (int): shift bits r1

    Returns:
        list: 64 bit output
    """
    Y = []
    for i in range(64):
        # the SingleMatrix transform
        Y.append(X[i] + X[(i + (64 - r0)) % 64] + X[(i + (64 - r1)) % 64])
    return Y

def InvSingleMatrix(X, r0, r1):
    """Inverse of the SingleMatrix transform

    Args:
        X (list): 64 bit input
        r0 (int): shift bits r0
        r1 (int): shift bits r1

    Returns:
        list: 64 bit output
    """
    # convert X to sage matrix(use self defined ring)
    tempX = matrix(R, 1, 64, X)
    tempX = tempX.transpose()
    # convert SingleMatrix to sage matrix(use GF2 ring)
    m = matrix(GF(2), 64, 64)  # a 64*64 matrix with all zeroes
    # construct the matrix
    for i in range(64):
        temp = [0] * 64
        # set the i th, i-r0 th, i-r1 th bits to 1
        temp[i], temp[(i - r0) % 64], temp[(i - r1) % 64] = 1, 1, 1
        m[i] = temp
    # compute inverse of SingleMatrix
    m = m.inverse()
    # compute output after inverse of SingleMatrix
    Y = m * tempX
    # convert sage matrix to python list
    return Y.list()

def Matrix(X):
    """Matrix transform

    Args:
        X (list): 320 bit input

    Returns:
        list: 320 bit output
    """
    # 64 bits as a block, each block uses different transform shift r0, r1
    X[0  : 64] = SingleMatrix(X[0  : 64], 19, 28)
    X[64 :128] = SingleMatrix(X[64 :128], 61, 39)
    X[128:192] = SingleMatrix(X[128:192], 1, 6)
    X[192:256] = SingleMatrix(X[192:256], 10, 17)
    X[256:320] = SingleMatrix(X[256:320], 7, 41)
    return X
    
def InvMatrix(X):
    """Inverse of the Matrix transform

    Args:
        X (list): 320 bit input

    Returns:
        list: 320 bit output
    """
    X[0  : 64] = InvSingleMatrix(X[0  : 64], 19, 28)
    X[64 :128] = InvSingleMatrix(X[64 :128], 61, 39)
    X[128:192] = InvSingleMatrix(X[128:192], 1, 6)
    X[192:256] = InvSingleMatrix(X[192:256], 10, 17)
    X[256:320] = InvSingleMatrix(X[256:320], 7, 41)
    return X

def SingleSbox(y0, y1, y2, y3, y4):
    """5-bits sbox

    Args:
        y0 (int): 1 bit input, 0 or 1
        y1 (int): 1 bit input, 0 or 1
        y2 (int): 1 bit input, 0 or 1
        y3 (int): 1 bit input, 0 or 1
        y4 (int): 1 bit input, 0 or 1

    Returns:
        list: 5 bits output
    """
    x0 = y4*y1 + y3 + y2*y1 + y2 + y1*y0 + y1 + y0
    x1 = y4 + y3*y2 + y3*y1 + y3 + y2*y1 + y2 + y1 + y0
    x2 = y4*y3 + y4 + y2 + y1 + 1
    x3 = y4*y0 + y4 + y3*y0 + y3 + y2 + y1 + y0
    x4 = y4*y1 + y4 + y3 + y1*y0 + y1
    return x0, x1, x2, x3, x4

def InvSingleSbox(y0, y1, y2, y3, y4):
    """inverse of the 5-bits sbox

    Args:
        y0 (int): 1 bit input, 0 or 1
        y1 (int): 1 bit input, 0 or 1
        y2 (int): 1 bit input, 0 or 1
        y3 (int): 1 bit input, 0 or 1
        y4 (int): 1 bit input, 0 or 1

    Returns:
        list: 5 bits output
    """
    x0 = y4*y3*y2 + y4*y3*y1 + y4*y3*y0 + y3*y2*y0 + y3*y2 + y3 + y2 + y1*y0 + y1 + 1
    x1 = y4*y2*y0 + y4 + y3*y2 + y2*y0 + y1 + y0
    x2 = y4*y3*y1 + y4*y3 + y4*y2*y1 + y4*y2 + y3*y1*y0 + y3*y1 + y2*y1*y0 + y2*y1 + y2 + 1 + x1
    x3 = y4*y2*y1 + y4*y2*y0 + y4*y2 + y4*y1 + y4 + y3 + y2*y1 + y2*y0 + y1
    x4 = y4*y3*y2 + y4*y2*y1 + y4*y2*y0 + y4*y2 + y3*y2*y0 + y3*y2 + y3 + y2*y1 + y2*y0 + y1*y0
    return x0, x1, x2, x3, x4

def Sbox(Y):
    """320 bits sbox

    Args:
        Y (list): 320 bits input

    Returns:
        list: 320 bits output
    """
    Z = [R(0) for i in range(320)]
    # 5 bits as a block, each block uses a 5-bits sbox
    for j in range(64):
        Z[0 + j], Z[64 + j], Z[128 + j], Z[192 + j] , Z[256 + j] = SingleSbox(Y[0 + j], Y[64 + j], Y[128 + j], Y[192 + j], Y[256+j])
    return Z

def InvSbox(Y):
    """inverse of the 320 bits sbox

    Args:
        Y (list): 320 bits input

    Returns:
        list: 320 bits output
    """
    Z = [R(0) for i in range(320)]
    # 5 bits as a block, each block uses a 5-bits sbox
    for j in range(64):
        Z[0 + j], Z[64 + j], Z[128 + j], Z[192 + j] , Z[256 + j] = InvSingleSbox(Y[0 + j], Y[64 + j], Y[128 + j], Y[192 + j], Y[256+j])
    return Z

def addConst(X, r):
    """add a const to input X

    Args:
        X (list): 320 bits input
        r (int): const index

    Returns:
        list: 320 bits output
    """
    # the chosen list of the consts
    constant = [0xf0, 0xe1, 0xd2, 0xc3, 0xb4, 0xa5, 0x96, 0x87, 0x78, 0x69,
            0x5a, 0x4b]
    base = 184
    for i in range(8):
        # choose the const according to the index r
        if constant[r] >> (7 - i) & 0x1:
            X[base + i] += 1
    return X

def round(X, r):
    """round function

    Args:
        X (list): 320 bits input
        r (int): the number of rounds

    Returns:
        list: 320 bits output
    """
    # n rounds
    for i in range(r):
        # a round contains 3 parts
        X = addConst(X, i)
        X = Sbox(X)
        X = Matrix(X)
    return X
    
def Invround(X):
    """inverse of the round function

    Args:
        X (list): 320 bits input

    Returns:
        list: 320 bits output
    """
    # 2 rounds
    for i in range(2):
        # a round contains 3 parts
        X = InvMatrix(X)
        X = InvSbox(X)
        X = addConst(X, (i + 1) % 2) 
    return X

def print_state(X):
    """print a gimli state in a logger in hex form

    Args:
        X (list): input gimli state
        logger (logging.Logger): the logger to log the state
        gimli (Gimli): the gimli object related to the input X
    """
    for i in range(5):
        # print a row at a time
        # now start convert binary state to hex form
        # get the binary state
        state_binary = X[64*i : 64*i + 64]
        # the length of a word should be the multiple of 4
        if len(state_binary) % 4 != 0:
            logger.error("the length of a word should be the multiple of 4")
            exit(1)
        # compute hex every 4 bits
        state_hex = []
        for k in range(len(state_binary) // 4):
            # compute 4 bits int value
            tmp = 0
            for bit in range(4):
                tmp += (int(state_binary[k * 4 + bit]) << (3-bit))
            # convert in value to hex and remove "0x", then add to the state
            state_hex.append(hex(tmp)[2:])
        # padding "0x"
        for k in range(16):
            print(state_hex[k],end="")
        print('\n')

def index_xy(x: int, y: int) -> int:
    """return the index of coordinates x, y

    Args:
        x (int): x coordinate
        y (int): y coordinate

    Returns:
        int: index of x, y
    """
    x, y = x%64, y%5
    return 64 * y + x


if __name__ == '__main__':
    state = 320
    rate = 64
    ROUNDS = 4
    R = declare_ring([Block('x', ROUNDS*state + (ROUNDS-1)*state + state + (ROUNDS-2)*state + rate + state)], globals())
    A = [[R(x(i + r*state)) for i in range(state) ] for r in range(ROUNDS) ]               
    B = [[R(x(i + ROUNDS*state + r*state)) for i in range(state) ] for r in range(ROUNDS-1) ]         
    D = [[R(x(i + ROUNDS*state + (ROUNDS-1)*state + r*state)) for i in range(state) ] for r in range(1) ]  
    Q = [[R(x(i + ROUNDS*state + (ROUNDS-1)*state + state + r*state)) for i in range(state) ] for r in range(ROUNDS-2) ]  
    B0 = [R(x(i + ROUNDS*state + (ROUNDS-1)*state + state + (ROUNDS-2)*state)) for i in range(rate) ]
    k = [R(x(i + ROUNDS*state + (ROUNDS-1)*state + state + (ROUNDS-2)*state + rate)) for i in range(state) ]
    Qq = set()
################INV#########################
    # 3r: numvars A0--pspc-->B0--pl-->A1--pspc-->B1--pl-->A2
    # A[0]      v 1 -  320
    # A[1]      v 321 -  640
    # A[2]      v 641 -  960
    # B[0]      v 961 -  1280
    # B[1]      v 1281 - 1600
    # D[0]      v 1601 - 1920
    # Q[0]      v 1921 - 2240
    # B0        v 2241 - 2304
############################################
 # 4r: numvars A0--pspc-->B0--pl-->A1--pspc-->B1--pl-->A2--pspc-->B2--pl-->A3
    # A[0]      v 1 -  320
    # A[1]      v 321 -  640
    # A[2]      v 641 -  960
    # A[3]      v 961 -  1280
    # B[0]      v 1281 - 1600
    # B[1]      v 1601 - 1920
    # B[2]      v 1921 - 2240
    # D[0]      v 2241 - 2560
    # Q[0]Qb1   v 2561 - 2880
    # Q[1]Qa2   v 2881 - 3200
    # B0        v 3201 - 3264
    # k         v 3265 - 3584
############################################
## Since the last c=256 bits of the initial state are all fixed constants, 
## we initialize their corresponding model variables as 0
    for y in range(5):
        for x in range(rate):
            if y in [1,2,3,4]:
                Qq.add(A[0][index_xy(x,y)])
    solver = DIMACS(filename = "/home/n2107349e/SAT/Ascon_tools/Ascon_ls/4r/ascon_ls_inv.cnf")
    e = CNFEncoder(solver, R)
    e(list(Qq))
    solver.write()
    logger.info("finished")
    ## note that we make all 320 variables of D[0] equal to 0 in our model, so another 320 clauses will add into  anscon_ls_inv.cnf
