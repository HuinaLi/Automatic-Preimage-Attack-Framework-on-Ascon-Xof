import argparse

solution_sign = "s SATISFIABLE"
line_split = "v"
state_x = 64
state_y = 5
state = state_x*state_y



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

"""shift symmetry"""
def shiftZ(X: list, r0: int) -> list:
    Y = []
    for y in range(state_y):
        for x in range(state_x):
            # shift (x)
            Y.append(X[state_x * y + (x-r0) % state_x])
    return Y

"""read solution from solution file"""
def read_sol_ls(sol_path: str, ROUNDS: int) -> list:
    # var number of A,B,D,Q,B0 
    var_num = ROUNDS*state + (ROUNDS-1)*state + (ROUNDS-1)*state  + state_x + state
    # extract the solution from cnf solution file
    f = open(sol_path, "r")
    contents = f.read()
    # find solution_sign "s SATISFIABLE"
    i = contents.find(solution_sign)
    if i < 0:
        return None

    i += len(solution_sign) + 1
    # get the contents after "s SATISFIABLE"
    lines = contents[i:].split(line_split)
    sol = []
    # get the solution of A,B,D,Q,B0
    for line in lines:
        vars = line.split()
        for var in vars:
            v = 0 if int(var) < 0 else 1
            sol.append(v)
        if len(sol) >= var_num:
            break
    sol = sol[:var_num]
    #print("sol"+ str(sol))
    # return A,B,D,Q,B0
    A = []
    B = []
    D = []
    Q = []
    n0 = []
    B0 = []
    Ko = []
    for r in range(ROUNDS):
        A.append(sol[r*state : (r+1)*state])
    for r in range(ROUNDS-1):
        B.append(sol[ROUNDS*state + r*state : ROUNDS*state + (r+1)*state])
    for r in range(ROUNDS-1):    
        if r < 1:
            D.append(sol[ROUNDS*state + (ROUNDS-1)*state + r*state : ROUNDS*state + (ROUNDS-1)*state + (r+1)*state])
        else:
            Q.append(sol[ROUNDS*state + (ROUNDS-1)*state +  r*state : ROUNDS*state + (ROUNDS-1)*state +  (r+1)*state])
    
    cons_n0 = sol[ROUNDS*state + 3*64: ROUNDS*state + 4*64]
    B0 = sol[ROUNDS*state + (ROUNDS-1)*state + (ROUNDS-1)*state : ROUNDS*state + (ROUNDS-1)*state + (ROUNDS-1)*state + state_x]
    Ko = sol[ROUNDS*state + (ROUNDS-1)*state + (ROUNDS-1)*state + state_x : ROUNDS*state + (ROUNDS-1)*state + (ROUNDS-1)*state + state_x + state]
    print("---------------------------------------------------")
    k = 0
    for i in range(state):
        if A[0][i] == 1:
            k += 1
    print("Var_num = " + str(k))
    
    d = 0
    for r in range(1):
        for i in range(state):
            if D[r][i] == 1:
                d += 1
    print("D_num = " + str(d))
    print("DF_num = " + str(k-d))

    b0 = 0
    for i in range(state_x):
        if B0[i] == 1:
            b0 += 1
        
    print("B = " + str(b0))

    if ROUNDS ==3:
        q = 0
        for r in range(ROUNDS-2):
            for i in range(state):
                if Q[r][i] == 1:
                    q += 1
        print("Q = " + str(q))

        n0 = 0
        for i in range(state_x):
            if cons_n0[i] == 1:
                n0 += 1
            
        print("n0 = " + str(n0))
   
    n2 = 0
    for i in range(128):
        if Ko[i] == 1:
            n2 += 1
        
    print("n2_'1' = " + str(n2))

    dr_cost_n20 = 0
    dr_cost_n21 = 0
    dr_cost_n2 = 0
    for i in range(64):
        if Ko[i] == 1:
            dr_cost_n20 += 1
        if Ko[i+64] == 1:
            dr_cost_n21 += 1
    dr_cost_n2 = 2*dr_cost_n20 + 3*dr_cost_n21
    print("dr_cost_n2 = " + str(dr_cost_n2))

    dr_cost_n3 = 0
    for i in range(128,320):
        if Ko[i] == 1:
            dr_cost_n3 += 1
    print("n3_'1' = dr_cost_n3 = " + str(dr_cost_n3))

    print("dr_cost = " + str(dr_cost_n2 + dr_cost_n3))

    # print("Complexity = " + str(128-(k-d)))
    print("Complexity = " + str(128-(k-d)*0.585))
    print("---------------------------------------------------")

    print("A{}: ".format(0))
    print_state(A[0])

    print("B{}: ".format(0))
    print_state(B[0])

    print("D{}: ".format(0))
    print_state(D[0])

    print("A{}: ".format(1))
    print_state(A[1])

    print("B{}: ".format(1))
    print_state(B[1])
        
    if ROUNDS ==3:
        print("Q{}: ".format(0))
        print_state(Q[0])

        print("A{}: ".format(2))
        print_state(A[2])
    elif ROUNDS ==4:
        print("Q{}: ".format(0))
        print_state(Q[0])

        print("A{}: ".format(2))
        print_state(A[2])

        print("Q{}: ".format(1))
        print_state(Q[1])

        print("B{}: ".format(2))
        print_state(B[2])

        print("A{}: ".format(3))
        print_state(A[3])

    print("K:")
    print_state(Ko) 

    print("B0:")
    print_x(B0)    

    print("---------------------------------------------------")
    return A,B

"""get banned solution list"""
def ban_sol(a:list,b:list) -> list:
    # shift the solution
    ban_list = []

    for r in range(state_x):
        ban = []
        for ai in a:
            ban.append(shiftZ(ai, r))
        for bi in b:
            ban.append(shiftZ(bi, r))
        ban_list.append(ban)
    #print(ban_list[0])
    # we got 64 solutions to ban
    return ban_list

"""add ban solution list to cnf"""
def add_ban2cnf(cnf_path: str, ban_list: list) -> None:
    # add 64 ban solutions to cnf
    # line_cnt = 64
    line_cnt = len(ban_list)
    #print (line_cnt)
    # ban cnf string
    ban_cnf = ""
    # add each solution
    for ban in ban_list:
        # each solution is A,B.
        for r in range(len(ban)):
            if r < 3:
                ai = ban[r]
                # the first index of ai in cnf
                # a0: 1 - 320
                # a1: 321 - 640
                # b: 641 - 960
                offset = r*state + 1
                for i in range(len(ai)):
                    v = ai[i]
                    if v:
                        ban_cnf += "-" + str(i + offset) + " "
                    else:
                        ban_cnf += str(i + offset) + " "
            else:
                bi = ban[r]
                offset = r*state + 1
                for i in range(len(bi)):
                    v = bi[i]
                    if v:
                        ban_cnf += "-" + str(i + offset) + " "
                    else:
                        ban_cnf += str(i + offset) + " "
        ban_cnf += "0\n"
    # read previous cnf
    f = open(cnf_path, "r")
    pre_cnf = f.read()
    f.close()
    # find the first line
    index_1st = pre_cnf.find("\n")
    line_1st = pre_cnf[:index_1st + 1].split()
    # modify first line
    line_1st[3] = str(int(line_1st[3]) + line_cnt)
    line_1st = " ".join(line_1st) + "\n"
    new_cnf = line_1st + pre_cnf[index_1st + 1:] + ban_cnf
    # write ban to cnf
    f = open(cnf_path, "w")
    f.write(new_cnf)
    f.close()

def print_state(X: list) -> None:
    """print a state in column form

    Args:
        X (list): input state
    """
    # print 5*64 columns
    for y in range(state_y):
        #print("\n")
        lane_print = ""
        for x in range(state_x):
            # now start convert binary column to int
            # get the binary column
            lane_print += str(X[index_xy(x,y)]) if X[index_xy(x,y)] else "0"
        print(lane_print)
    print("------")

def print_x(X: list) -> None:
    """print a state in column form

    Args:
        X (list): input row
    """
    # print a row
    lane_print = ""
    for x in range(state_x):
        lane_print += str(X[x]) if X[x] else "0"
    print(lane_print)
    print("------")

    
if __name__ == "__main__":
    parse = argparse.ArgumentParser(description="add banned solutions to cnf")
    parse.add_argument("-c", "--cnf", type=str, help="cnf file")
    parse.add_argument("-s", "--solution", type=str, help="solution file")
    parse.add_argument("-r", "--rounds", type=int, help="rounds of the solution")
    args = parse.parse_args()

    a,b = read_sol_ls(args.solution, args.rounds)
    
    if not a:
        raise ValueError("solution not found")
    ban_list = ban_sol(a,b)
    add_ban2cnf(args.cnf, ban_list)