#-------------------------------------------------------------------------------
# Name:     Ascon permutation
# Purpose:  Generate all contraints of n rounds in CNF form -->list
#           All CNF consists of three parts: 
#           1. initial state CNF (generete using ascon_optimal_ls.py), 
#           2. sbox and Constraint CNF (using get_allcons_cnf_ascon.py), 
#           3. Objective Function CNF (using PySat,https://pysathq.github.io/) 
# Author:   Anonymous
# Created:  30-11-2022
# Version:  1st
#-------------------------------------------------------------------------------
import sys
import math

ROUNDS = 4
state = 320

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

## 11 clauses
cnf_free_inv = [
    [-2], 
    [-3], 
    [-4], 
    [-5], 
    [-8], 
    [1, -7], 
    [1, -9], 
    [7, -6], 
    [7, -10], 
    [-6, -10], 
    [6, 10, -1]
]


#CNF_bad: [B0 B1 B2 A D]  7 clauses
cnf_bad = [
    [-4, -5], 
    [4, 5, -2], 
    [4, 5, -3], 
    [1, 2, -5], 
    [4, 1, 3, -2], 
    [4, 2, 3, -1], 
    [1, 2, 3, -4]
]

##CNF_baq: [B0 B1 B2 A Q]  7 clauses
cnf_baq = [
    [4, -5], 
    [1, 5, -4], 
    [2, 5, -4], 
    [3, 5, -4], 
    [1, 2, 3, -5], 
    [4, -1, -2, -3], 
    [-1, -2, -3, -5]
]


#A_to_B: [A0 A1 A2 A3 A4 B0 B1 B2 B3 B4 ] 16 clauses
cnf_atob = [
    [-3], 
    [1, 9], 
    [2, 7], 
    [2, 10], 
    [4, 7], 
    [4, 8], 
    [5, 8], 
    [6, -10], 
    [1, 5, 10], 
    [4, 5, 9], 
    [-1, -2, -6], 
    [-1, -4, -9], 
    [-1, -5, -9], 
    [-2, -4, -7], 
    [-2, -5, -6], 
    [-4, -5, -8]
]


## CNF_a02b0: [A0 A1 A2 A3 A4 B0 B1 B2 B3 B4 ]
## 11 clauses
cnf_a02b0 = [
    [-2], 
    [-3], 
    [-4], 
    [-5], 
    [-8], 
    [-9], 
    [1, -7], 
    [7, -6], 
    [7, -10], 
    [-6, -10], 
    [6, 10, -1]
]

## A1_to_B1 : A1,B1,Qa1b1
## CNF_a12b1: [A0 A1 A2 A3 A4 B0 q0 B1 q1 B2 q2 B3 q3 B4 q4 ]
## 20 cluases
cnf_a12b1 = [
    [-6,-12],
    [-12,-14],
    [1,5,-6],
    [1,5,-14],
    [12,15],
    [6,-7,-8,14],
    [-1,8],
    [-5,8],
    [1,5,15],
    [7,-15],
    [-2,12],
    [10,-12],
    [2,-10],
    [-6,-14],
    [-1,-5],
    [13],
    [11],
    [9], 
    [-4],
    [-3]
]

## B1_to_A2: B1,A2,Qb1, Qa2
## [B0 q0 B1 q1  B2 q2 A0 Q0] 

## 8 clauses
cnf_b12a2_r3 = [
    [1, 3, 5, -7], 
    [-5, 7], 
    [-3, 7], 
    [-1, 7], 
    [8], 
    [6], 
    [4], 
    [2]
]

## 12 clauses
cnf_b12a2_r2 = [
    [-1, 7, -8], 
    [-3, 7, -8], 
    [-5, 7, -8], 
    [-7, 8], 
    [-2, -4, -6, 8], 
    [1, 3, 5, -7], 
    [6, -8], 
    [4, -8], 
    [-3, 4], 
    [-5, 6], 
    [2, -8], 
    [-1, 2]
]

## A2_to_B2: A2,B2,Qa2
## [A0 q0 A1 q1 A2 q2 A3 q3 A4 q4 B0  B1  B2  B3  B4 ]
## 43 clauses
cnf_a22b2 = [
    [2, 10, -15], 
    [10, -11, -15], 
    [2, -11, -15], 
    [-3, 5, 11, -15], 
    [2, 13, -14], 
    [-5, 11, -12], 
    [2, 10, -11], 
    [-2, -10, -11, 15], 
    [-2, 7, 9, -10, 14], 
    [-2, 5, 7, -10, 12], 
    [-1, -3, -15], 
    [2, -7, -14], 
    [7, -11, 12, -15], 
    [-3, -11, 15], 
    [3, 5, -11, 12, -15], 
    [-3, -9, -15], 
    [-2, 3, -10, 11], 
    [-1, -11, 15], 
    [7, -10, 13], 
    [3, -10, 11, 15], 
    [2, -12], 
    [1, -2, -10, 14], 
    [10, -12], 
    [1, -2, 3, 11, 15], 
    [1, -2, 9, -10, 15], 
    [-1, -7, -14], 
    [-1, 10, -14], 
    [2, 10, -13], 
    [-5, -7, -12], 
    [-7, -9, -13], 
    [9, -10, 13], 
    [-1, -9, -14], 
    [-7, 10, -13], 
    [2, -9, -14], 
    [-3, -7, -12], 
    [-3, -5, -11], 
    [2, -3, -15], 
    [-3, 10, -15], 
    [-9, 10], 
    [-1, 2], 
    [8], 
    [6], 
    [4]

]

## CNF_b22a3: [B0 B1 B2 A]
## [b0,b1,b2,a0]: 4 clauses
cnf_b22a3 = [
    [1,-4],
    [2,-4],
    [3,-4],
    [4,-1,-2,-3]
]

## 11 clauses
cnf_n2 = [
    [-3],
    [-4],
    [1, -6], 
    [-1, -5], 
    [-1, -7], 
    [-2, -6], 
    [2, 5, -7], 
    [2, 6, -1], 
    [2, 7, -5], 
    [1, 5, 7, -2], 
    [-2, -5, -7]
]

## 37 clauses
cnf_n3 = [
    [6, 8, -10, 11], 
    [-5, 6, 9, 10, -11], 
    [5, -6, -8, 12], 
    [5, -6, -8, -9, 13], 
    [5, -8, -10, 12], 
    [5, -8, -9, -10, 13], 
    [5, -8, -9, 12], 
    [-7, 8, 10], 
    [11, -12], 
    [6, 9, -10, 11], 
    [-5, 6, 10, -12], 
    [1, 8, -9], 
    [1, -6, -10], 
    [-6, -9, -11, 12], 
    [-9, -10, -11, 12], 
    [-7, -11], 
    [-5, 9, -12], 
    [-5, -13], 
    [-6, 10, 11], 
    [1, 5, -11], 
    [5, -6, -10], 
    [-1, -5, -11], 
    [6, 8, 9, 10, -11], 
    [6, 9, 10, -12], 
    [6, 8, 10, -12], 
    [8, 9, -12], 
    [1, -7], 
    [5, -8, 11], 
    [6, -7, -10], 
    [6, 10, -13], 
    [5, -9, 11], 
    [1, -9, 11], 
    [9, -13], 
    [8, -13], 
    [4], 
    [3], 
    [2]
]

##CNF_Hash_3r_3: [A0 A1 A2 A3 A4 B0]  4 clauses
cnf_hash_3r_3 = [
    [1, -6], 
    [3, -6], 
    [4, -6], 
    [6, -1, -3, -4]
]
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
    # cnf_bad: [B0 B1 B2 A D] : row
    # cnf_baq: [B0 B1 B2 A Q] : row
    # cnf_hash_3r: [A0 A1 A2 A3 A4 B0 B1]:column
    # cnf_free_inv: [A0 A1 A2 A3 A4 B0 B1 B2 B3 B4 ]:column
    # cnf_atob: [A0 A1 A2 A3 A4 B0 B1 B2 B3 B4 ]:column
################INV#########################
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
    # cnf_a02b0: [A0 A1 A2 A3 A4 B0 B1 B2 B3 B4 ]
    # cnf_bad: [B0 B1 B2 A D] : row
    # cnf_a12b1:[A0 A1 A2 A3 A4 B0 q0 B1 q1 B2 q2 B3 q3 B4 q4 ]
    # cnf_b12a2_r3: [B0 q0 B1 q1  B2 q2 A0 Q0]
    # cnf_b12a2_r2: [B0 q0 B1 q1  B2 q2 A0 Q0]
    # cnf_a22b2: [A0 q0 A1 q1 A2 q2 A3 q3 A4 q4 B0  B1  B2  B3  B4 ]
    # cnf_b22a3: [B0 B1 B2 A] 
    # cnf_n2: [a0 a1 a2 a3 a4 k0 k1]
    # cnf_n3:[q0,q1,q2,q3,q4,b0,b1,b2,b3,b4,k2,k3,k4] 
############################################
## cnf_free_inv: 11 clauses only add in the first round
## cnf_a02b0: 11 clauses
row = [0]*10
for r in range(1): 
    for x in range (64):    
        # [A0 A1 A2 A3 A4 B0 B1 B2 B3 B4 ] 
        row = [index_xy(x,0),index_xy(x,1),index_xy(x,2),index_xy(x,3),index_xy(x,4),ROUNDS*state + r*state + index_xy(x,0),ROUNDS*state + r*state  + index_xy(x,1),ROUNDS*state + r*state + index_xy(x,2),ROUNDS*state + r*state + index_xy(x,3),ROUNDS*state + r*state + index_xy(x,4)]
        for i in range (len(cnf_a02b0)):
            CNF_clause= ""
            for j in range(len(cnf_a02b0[i])):
                temp = int(cnf_a02b0[i][j])
                if temp > 0 :
                    CNF_clause += str(row[ temp-1] + 1) + " "
                else:
                    CNF_clause += str(-1 * row[abs(temp+1)]-1) + " "
            CNF_clause += '0'
            print(CNF_clause)   
 

## cnf_bad: 7 clauses 
row = [0]*5
for r in range(1): 
    for y in range (5):
        for x in range (64):   
            # row [B0 B1 B2 A D]
            if y == 0:
                row = [ROUNDS*state + r*state + index_xy(x,y), ROUNDS*state + r*state + index_xy(x-19,y), ROUNDS*state + r*state + index_xy(x-28,y), (r+1)*state + index_xy(x,y), ROUNDS*state + (ROUNDS-1)*state  + r*state + index_xy(x,y)]
            if y == 1:
                row = [ROUNDS*state + r*state + index_xy(x,y), ROUNDS*state + r*state + index_xy(x-61,y), ROUNDS*state + r*state + index_xy(x-39,y), (r+1)*state + index_xy(x,y), ROUNDS*state + (ROUNDS-1)*state  + r*state + index_xy(x,y)]
            if y == 2:
                row = [ROUNDS*state + r*state + index_xy(x,y), ROUNDS*state + r*state + index_xy(x-1,y), ROUNDS*state + r*state + index_xy(x-6,y), (r+1)*state + index_xy(x,y), ROUNDS*state + (ROUNDS-1)*state  + r*state + index_xy(x,y)]
            if y == 3:
                row = [ROUNDS*state + r*state + index_xy(x,y), ROUNDS*state + r*state + index_xy(x-10,y), ROUNDS*state + r*state + index_xy(x-17,y), (r+1)*state + index_xy(x,y), ROUNDS*state + (ROUNDS-1)*state  + r*state + index_xy(x,y)]
            if y == 4:
                row = [ROUNDS*state + r*state + index_xy(x,y), ROUNDS*state + r*state + index_xy(x-7,y), ROUNDS*state + r*state + index_xy(x-41,y), (r+1)*state + index_xy(x,y), ROUNDS*state + (ROUNDS-1)*state  + r*state + index_xy(x,y)]
            
            for i in range (len(cnf_bad)):
                CNF_clause= ""
                for j in range(len(cnf_bad[i])):
                    temp = int(cnf_bad[i][j])
                    if temp > 0 :
                        CNF_clause += str(row[ temp-1] + 1) + " "
                    else:
                        CNF_clause += str(-1 * row[abs(temp+1)]-1) + " "
                CNF_clause += '0'
                print(CNF_clause)

## cnf_atob: 16 clauses only add in the second round
## cnf_a12b1: 20 clauses
row = [0]*15
for r in range(1): 
    for x in range (64):    
        # [A0 A1 A2 A3 A4 B0 B1 B2 B3 B4 ] 
        # [A0 A1 A2 A3 A4 B0 q0 B1 q1 B2 q2 B3 q3 B4 q4 ]
        row = [(r+1)*state + index_xy(x,0),(r+1)*state + index_xy(x,1),(r+1)*state + index_xy(x,2),(r+1)*state + index_xy(x,3),(r+1)*state + index_xy(x,4),ROUNDS*state + (r+1)*state + index_xy(x,0),ROUNDS*state + (ROUNDS-1)*state + state + index_xy(x,0),ROUNDS*state + (r+1)*state  + index_xy(x,1),ROUNDS*state + (ROUNDS-1)*state + state + index_xy(x,1),ROUNDS*state + (r+1)*state + index_xy(x,2),ROUNDS*state + (ROUNDS-1)*state + state + index_xy(x,2),ROUNDS*state + (r+1)*state + index_xy(x,3),ROUNDS*state + (ROUNDS-1)*state + state + index_xy(x,3),ROUNDS*state + (r+1)*state + index_xy(x,4),ROUNDS*state + (ROUNDS-1)*state + state + index_xy(x,4)]
        for i in range (len(cnf_a12b1)):
            CNF_clause= ""
            for j in range(len(cnf_a12b1[i])):
                temp = int(cnf_a12b1[i][j])
                if temp > 0 :
                    CNF_clause += str(row[ temp-1] + 1) + " "
                else:
                    CNF_clause += str(-1 * row[abs(temp+1)]-1) + " "
            CNF_clause += '0'
            print(CNF_clause)   


## cnf_baq: 7 clauses 
#  B1_to_A2: B1,A2,Qb1, Qa2
#  cnf_b12a2_r2: 12 clauses
row = [0]*8
for r in range(1): 
    for y in range (5):
        for x in range (64):   
            # column [B0 B1 B2 A Q]
            # [B0 q0 B1 q1  B2 q2 A0 Q0] 
            if y in [0,4]:
                if y == 0:
                    row = [ROUNDS*state + (r+1)*state + index_xy(x,y), ROUNDS*state + (ROUNDS-1)*state + state + r*state + index_xy(x,y), ROUNDS*state + (r+1)*state + index_xy(x-19,y),ROUNDS*state + (ROUNDS-1)*state + state + r*state + index_xy(x-19,y), ROUNDS*state + (r+1)*state + index_xy(x-28,y),ROUNDS*state + (ROUNDS-1)*state + state + r*state + index_xy(x-28,y), (r+2)*state + index_xy(x,y), ROUNDS*state + (ROUNDS-1)*state  + state + (r+1)*state + index_xy(x,y)]
                if y == 4:
                    row = [ROUNDS*state + (r+1)*state + index_xy(x,y), ROUNDS*state + (ROUNDS-1)*state + state + r*state + index_xy(x,y), ROUNDS*state + (r+1)*state + index_xy(x-7,y),ROUNDS*state + (ROUNDS-1)*state + state + r*state + index_xy(x-7,y), ROUNDS*state + (r+1)*state + index_xy(x-41,y), ROUNDS*state + (ROUNDS-1)*state + state + r*state + index_xy(x-41,y),(r+2)*state + index_xy(x,y), ROUNDS*state + (ROUNDS-1)*state  + state + (r+1)*state + index_xy(x,y)]
                
                for i in range (len(cnf_b12a2_r2)):
                    CNF_clause= ""
                    for j in range(len(cnf_b12a2_r2[i])):
                        temp = int(cnf_b12a2_r2[i][j])
                        if temp > 0 :
                            CNF_clause += str(row[ temp-1] + 1) + " "
                        else:
                            CNF_clause += str(-1 * row[abs(temp+1)]-1) + " "
                    CNF_clause += '0'
                    print(CNF_clause)

## [B0 q0 B1 q1  B2 q2 A0 Q0] 
# cnf_b12a2_r3: 8 clauses
row = [0]*8
for r in range(1): 
    for y in range (5):
        for x in range (64):   
            # column [B0 B1 B2 A Q]
            # [B0 q0 B1 q1  B2 q2 A0 Q0] 
            if y in [1,2,3]:
                if y == 1:
                    row = [ROUNDS*state + (r+1)*state + index_xy(x,y), ROUNDS*state + (ROUNDS-1)*state + state + r*state + index_xy(x,y), ROUNDS*state + (r+1)*state + index_xy(x-61,y),ROUNDS*state + (ROUNDS-1)*state + state + r*state + index_xy(x-61,y), ROUNDS*state + (r+1)*state + index_xy(x-39,y), ROUNDS*state + (ROUNDS-1)*state + state + r*state + index_xy(x-39,y),(r+2)*state + index_xy(x,y), ROUNDS*state + (ROUNDS-1)*state  + state + (r+1)*state + index_xy(x,y)]
                if y == 2:
                    row = [ROUNDS*state + (r+1)*state + index_xy(x,y), ROUNDS*state + (ROUNDS-1)*state + state + r*state + index_xy(x,y), ROUNDS*state + (r+1)*state + index_xy(x-1,y),ROUNDS*state + (ROUNDS-1)*state + state + r*state + index_xy(x-1,y), ROUNDS*state + (r+1)*state + index_xy(x-6,y),ROUNDS*state + (ROUNDS-1)*state + state + r*state + index_xy(x-6,y), (r+2)*state + index_xy(x,y), ROUNDS*state + (ROUNDS-1)*state  + state + (r+1)*state + index_xy(x,y)]
                if y == 3:
                    row = [ROUNDS*state + (r+1)*state + index_xy(x,y), ROUNDS*state + (ROUNDS-1)*state + state + r*state + index_xy(x,y), ROUNDS*state + (r+1)*state + index_xy(x-10,y),ROUNDS*state + (ROUNDS-1)*state + state + r*state + index_xy(x-10,y), ROUNDS*state + (r+1)*state + index_xy(x-17,y),ROUNDS*state + (ROUNDS-1)*state + state + r*state + index_xy(x-17,y), (r+2)*state + index_xy(x,y), ROUNDS*state + (ROUNDS-1)*state  + state + (r+1)*state + index_xy(x,y)]
                
                for i in range (len(cnf_b12a2_r3)):
                    CNF_clause= ""
                    for j in range(len(cnf_b12a2_r3[i])):
                        temp = int(cnf_b12a2_r3[i][j])
                        if temp > 0 :
                            CNF_clause += str(row[ temp-1] + 1) + " "
                        else:
                            CNF_clause += str(-1 * row[abs(temp+1)]-1) + " "
                    CNF_clause += '0'
                    print(CNF_clause)


## A2_to_B2: A2,B2,Qa2
## [A0 q0 A1 q1 A2 q2 A3 q3 A4 q4 B0  B1  B2  B3  B4 ]
## cnf_a22b2: 44 clauses
row = [0]*15
for r in range(1): 
    for x in range (64):    
        # [A0 q0 A1 q1 A2 q2 A3 q3 A4 q4 B0  B1  B2  B3  B4 ]
        row = [(r+2)*state + index_xy(x,0),ROUNDS*state + (ROUNDS-1)*state  + state + (r+1)*state + index_xy(x,0), (r+2)*state + index_xy(x,1),ROUNDS*state + (ROUNDS-1)*state  + state + (r+1)*state + index_xy(x,1),(r+2)*state + index_xy(x,2),ROUNDS*state + (ROUNDS-1)*state  + state + (r+1)*state + index_xy(x,2),(r+2)*state + index_xy(x,3),ROUNDS*state + (ROUNDS-1)*state  + state + (r+1)*state + index_xy(x,3),(r+2)*state + index_xy(x,4),ROUNDS*state + (ROUNDS-1)*state  + state + (r+1)*state + index_xy(x,4),ROUNDS*state + (r+2)*state + index_xy(x,0),ROUNDS*state + (r+2)*state + index_xy(x,1),ROUNDS*state + (r+2)*state + index_xy(x,2),ROUNDS*state + (r+2)*state + index_xy(x,3),ROUNDS*state + (r+2)*state + index_xy(x,4)]
        for i in range (len(cnf_a22b2)):
            CNF_clause= ""
            for j in range(len(cnf_a22b2[i])):
                temp = int(cnf_a22b2[i][j])
                if temp > 0 :
                    CNF_clause += str(row[ temp-1] + 1) + " "
                else:
                    CNF_clause += str(-1 * row[abs(temp+1)]-1) + " "
            CNF_clause += '0'
            print(CNF_clause)   

## CNF_b22a3: [B0 B1 B2 A]
## cnf_b22a3: 4 clauses
row = [0]*4
for r in range(1): 
    for y in range (5):
        for x in range (64):   
            # column [B0 B1 B2 A]
            if y == 0:
                row = [ROUNDS*state + (r+2)*state + index_xy(x,y), ROUNDS*state + (r+2)*state + index_xy(x-19,y), ROUNDS*state + (r+2)*state + index_xy(x-28,y), (r+3)*state + index_xy(x,y)]
            if y == 1:
                row = [ROUNDS*state + (r+2)*state + index_xy(x,y), ROUNDS*state + (r+2)*state + index_xy(x-61,y), ROUNDS*state + (r+2)*state + index_xy(x-39,y), (r+3)*state + index_xy(x,y)]
            if y == 2:
                row = [ROUNDS*state + (r+2)*state + index_xy(x,y), ROUNDS*state + (r+2)*state + index_xy(x-1,y), ROUNDS*state + (r+2)*state + index_xy(x-6,y), (r+3)*state + index_xy(x,y)]
            if y == 3:
                row = [ROUNDS*state + (r+2)*state + index_xy(x,y), ROUNDS*state + (r+2)*state + index_xy(x-10,y), ROUNDS*state + (r+2)*state + index_xy(x-17,y), (r+3)*state + index_xy(x,y)]
            if y == 4:
                row = [ROUNDS*state + (r+2)*state + index_xy(x,y), ROUNDS*state + (r+2)*state + index_xy(x-7,y), ROUNDS*state + (r+2)*state + index_xy(x-41,y), (r+3)*state + index_xy(x,y)]
            
            for i in range (len(cnf_b22a3)):
                CNF_clause= ""
                for j in range(len(cnf_b22a3[i])):
                    temp = int(cnf_b22a3[i][j])
                    if temp > 0 :
                        CNF_clause += str(row[ temp-1] + 1) + " "
                    else:
                        CNF_clause += str(-1 * row[abs(temp+1)]-1) + " "
                CNF_clause += '0'
                print(CNF_clause)

## cnf_hash_3r_3: 4 clauses only add in A[2]&B0

row = [0]*6
for r in range(1): 
    for x in range (64):   
        # [A0 A1 A2 A3 A4 B0] : column 
        row = [(r+3)*state + index_xy(x,0), (r+3)*state + index_xy(x,1), (r+3)*state + index_xy(x,2), (r+3)*state + index_xy(x,3), (r+3)*state + index_xy(x,4),ROUNDS*state + (ROUNDS-1)*state + (ROUNDS-1)*state + x]

        for i in range (len(cnf_hash_3r_3)):
            CNF_clause= ""
            for j in range(len(cnf_hash_3r_3[i])):
                temp = int(cnf_hash_3r_3[i][j])
                if temp > 0 :
                    CNF_clause += str(row[ temp-1] + 1) + " "
                else:
                    CNF_clause += str(-1 * row[abs(temp+1)]-1) + " "
            CNF_clause += '0'
            print(CNF_clause)  

## cnf_n2:10 clauses
row = [0]*7
for r in range(1): 
    for x in range (64):   
        # [A0 A1 A2 A3 A4 k0,k1] : column 
        row = [(r+1)*state + index_xy(x,0), (r+1)*state + index_xy(x,1), (r+1)*state + index_xy(x,2), (r+1)*state + index_xy(x,3), (r+1)*state + index_xy(x,4),ROUNDS*state + (ROUNDS-1)*state + (ROUNDS-1)*state + 64 + index_xy(x,0),ROUNDS*state + (ROUNDS-1)*state + (ROUNDS-1)*state + 64 + index_xy(x,1)]

        for i in range (len(cnf_n2)):
            CNF_clause= ""
            for j in range(len(cnf_n2[i])):
                temp = int(cnf_n2[i][j])
                if temp > 0 :
                    CNF_clause += str(row[ temp-1] + 1) + " "
                else:
                    CNF_clause += str(-1 * row[abs(temp+1)]-1) + " "
            CNF_clause += '0'
            print(CNF_clause)  

## cnf_n3: 37 clauses
row = [0]*13
for r in range(1): 
    for x in range (64):    
        # [q0 q1 q2 q3 q4 B0  B1  B2  B3  B4 k2 k3 k4 ]
        row = [ROUNDS*state + (ROUNDS-1)*state  + state + (r+1)*state + index_xy(x,0), ROUNDS*state + (ROUNDS-1)*state  + state + (r+1)*state + index_xy(x,1),ROUNDS*state + (ROUNDS-1)*state  + state + (r+1)*state + index_xy(x,2),ROUNDS*state + (ROUNDS-1)*state  + state + (r+1)*state + index_xy(x,3),ROUNDS*state + (ROUNDS-1)*state  + state + (r+1)*state + index_xy(x,4),ROUNDS*state + (r+2)*state + index_xy(x,0),ROUNDS*state + (r+2)*state + index_xy(x,1),ROUNDS*state + (r+2)*state + index_xy(x,2),ROUNDS*state + (r+2)*state + index_xy(x,3),ROUNDS*state + (r+2)*state + index_xy(x,4),ROUNDS*state + (ROUNDS-1)*state + (ROUNDS-1)*state + 64 + index_xy(x,2),ROUNDS*state + (ROUNDS-1)*state + (ROUNDS-1)*state + 64 + index_xy(x,3),ROUNDS*state + (ROUNDS-1)*state + (ROUNDS-1)*state + 64 + index_xy(x,4)]
        for i in range (len(cnf_n3)):
            CNF_clause= ""
            for j in range(len(cnf_n3[i])):
                temp = int(cnf_n3[i][j])
                if temp > 0 :
                    CNF_clause += str(row[ temp-1] + 1) + " "
                else:
                    CNF_clause += str(-1 * row[abs(temp+1)]-1) + " "
            CNF_clause += '0'
            print(CNF_clause) 
