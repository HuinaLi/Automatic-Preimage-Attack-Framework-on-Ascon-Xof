
# open file
f1 = open("/home/n2107349e/SAT/Ascon_tools/Ascon_ls/4r/ascon_ls_inv.cnf", "r")
f2 = open("/home/n2107349e/SAT/Ascon_tools/Ascon_ls/4r/allcons.cnf", "r")
# file to write
f4 = open("/home/n2107349e/SAT/Ascon_tools/Ascon_ls/4r/ascon_4r.cnf", "w")
# buf to write
buf = ""
# read file
buf = f1.read()
buf += f2.read()
#buf += f3.read()
# find the end of the first line
index_1st = buf.find("\n")
# modify first line
line_1st = buf[:index_1st + 1].split()

# compute the number of lines of file1/2/3
f2.seek(0)
line_num2 = len(f2.readlines())
line_1st[3] = str(int(line_1st[3]) + line_num2 )
print(line_num2)
buf = " ".join(line_1st) + "\n" + buf[index_1st + 1:]
f4.write(buf)
# close
f1.close()
f2.close()
#f3.close()
f4.close()
