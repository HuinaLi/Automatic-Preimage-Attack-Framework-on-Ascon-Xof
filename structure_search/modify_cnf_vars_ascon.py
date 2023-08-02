"""
add offsets to cnf variables
"""
import argparse
parse = argparse.ArgumentParser(description="add offsets to cnf variables")
parse.add_argument("-f1", "--file1", type=str, help="cons cnf file")
parse.add_argument("-f2", "--file2", type=str, help="AS cnf file")
parse.add_argument("-o", "--output", type=str, help="output cnf file")
parse.add_argument("-r", "--rounds", type=int, help="number of rounds")
args = parse.parse_args()

rounds = args.rounds
# number of AS vars ;64>=3/4/7/8: 265; 63>=9/8: 261; 63>=3/4/7: 262;320=3: 2656; 64>29: 242; 64>=32/30: 241; 320<=45:1323;64=19:499;64>=23/26/27/28:250; 64>=19/20/21: 251; 320<=20:1239; 320<=24: 1254;64<=24:254;64=24:504;64_eq32: 482; 320=32: 3039; 64>=25: 250; 64>=62: 189;64>=60:220;64>=50:217; 64>=34: 241;320=64:3104; 128<=33: 494; 320>=31: 1698; 960<=95: 4365; 64<=8: 250; 64>=8/6: 265; 128>=9: 577; 640<=55: 2738; 320<=30: 1365; 128>=34: 558; 320<=60:1369; 128>=4:586;
vars_num = 320
SUM_A_aux = 265 + 261 
offsets = []
# file to modify
path_r = args.file1
path_as = args.file2
# process offsets 
offsets.append(320)
f = open(path_r, "r")
first_line = f.readline().split()
offsets.append(int(first_line[2]) - vars_num + SUM_A_aux)
f.close()

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    return False

def add_offset(num: int, offset: int) -> int:
    if num < 0:
        num -= offset
    elif num > 0:
        num += offset
    return num

def process_num(num: int) -> int:
    if abs(num) <= vars_num:
        num = add_offset(num, offsets[0])
    else:
        num = add_offset(num, offsets[1])
    return num


if __name__ == "__main__":
    f = open(path_as, "r")

    lines = f.readlines()
    buf = ""
    for line in lines:
        line_nums = line.split()
        if not is_number(line_nums[0]):
            continue
        # each num adds an offset according to its value
        for num in line_nums:
            num = process_num(int(num))
            buf += str(num) + " "
        # each line ends with "0"
        buf += "0"
        buf += "\n"
    f.close()
    f = open(args.output, "w")
    f.write(buf)