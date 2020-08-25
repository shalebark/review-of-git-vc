import sys
import os
import difflib

def diff(buff1, buff2):
    lines1 = buff1.split(os.linesep)
    lines2 = buff2.split(os.linesep)
    return list(difflib.unified_diff(lines1, lines2, n=0))[2:]

def diff_files(file1, file2):
    buff1 = None
    buff2 = None
    with open(file1) as f1, open(file2) as f2:
        buff1 = f1.read()
        buff2 = f2.read()
    return diff(buff1, buff2)

def diff_buff(deltas):
    return os.linesep.join(deltas)

def diff_out(deltas):
    sys.stdout.write(diff_buff(deltas))

def read_deltas_buffer(buff):
    return list(filter(lambda x: x != '', buff.split(os.linesep)))

if __name__ == "__main__":
    diff_out(diff_files(sys.argv[1], sys.argv[2]))
