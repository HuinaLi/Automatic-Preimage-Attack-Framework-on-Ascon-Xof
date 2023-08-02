import argparse
parse = argparse.ArgumentParser(description="combine 2 cnfs")
parse.add_argument("-f1", "--file1", type=str, help="cons cnf file1")
parse.add_argument("-f2", "--file2", type=str, help="cnf file2")
parse.add_argument("-f3", "--file3", type=str, help="cnf file3")
parse.add_argument("-f4", "--file4", type=str, help="cnf file4")
parse.add_argument("-f5", "--file5", type=str, help="cnf file5")
parse.add_argument("-o", "--output", type=str, help="output cnf file")
parse.add_argument("-r", "--rounds", type=int, help="number of rounds")
args = parse.parse_args()

path1 = args.file1
path2 = args.file2
path3 = args.file3
path4 = args.file4
path5 = args.file5
path6 = args.output
rounds = args.rounds
# open file
f1 = open(path1, "r")
f2 = open(path2, "r")
f3 = open(path3, "r")
f4 = open(path4, "r")
f5 = open(path5, "r")
# file to write
f6 = open(path6, "w")
# buf to write
buf = ""
# read file
buf = f1.read()
buf += f2.read()
buf += f3.read()
buf += f4.read()
buf += f5.read()
# find the end of the first line
index_1st = buf.find("\n")
# combine
buf = buf[:index_1st + 1]  + buf[index_1st + 1:]
# modify first line
line_1st = buf[:index_1st + 1].split()
#320<=32:1365; 128<=30/32:493; 63>=9/8: 261; 63>=3/4/7: 262; 64>=3: 265; 63>=3: 262; 64=11:474; 64>=9/10/11:264; 64>=6/7/8:265; 320=10: 2845; 320<=45: 1323; 320<=10: 1146;64_eq32: 482; 64_eq40: 504;320=32: 3039; 64>=30:241; 64>=62: 189;64>=60:220;64>=50:217; 64>=34: 241; 64>=8/6: 265; 320=64:3104; 320<=64: 1432; 128<=33: 494; 320>=31: 1698; 320>=120: 1610; 960<=95: 4365;64>=8: 265; 128>=9: 577; 640<=55: 2738;  # number of AS vars ; 320<=30: 1365; 128>=34: 558；320<=60:1369; 128>=4:586;
line_1st[2] = str(int(line_1st[2]) + 261 + 265 + 1365 )
# compute the number of lines of file2
f2.seek(0)
line_num2 = len(f2.readlines())
# compute the number of lines of file3
f3.seek(0)
line_num3 = len(f3.readlines())
# compute the number of lines of file4
f4.seek(0)
line_num4 = len(f4.readlines())
# compute the number of lines of file5
f5.seek(0)
line_num5 = len(f5.readlines())
line_1st[3] = str(int(line_1st[3]) + line_num2+ line_num3 + line_num4 +  line_num5)
print(line_num2)
print(line_num3)
print(line_num4)
print(line_num5)
buf = " ".join(line_1st) + "\n" + buf[index_1st + 1:]

f6.write(buf)
# close
f1.close()
f2.close()
f3.close()
f4.close()
f5.close()
f6.close()