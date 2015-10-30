__author__ = 'connor'
with open("output/rand_trunc.log") as f:
    content = f.readlines()
    for i in range(len(content)):
        if content[i] == '\n':
            stripped_line = content[i-1].split()
            print(str(stripped_line[3]) + "\t" + str(stripped_line[4]))