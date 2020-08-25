import sys
import diff
import os
import re

def diff_apply(filebuffer, deltas):
    file_lines = filebuffer.split(os.linesep)
    index = 0
    for delta in deltas:
        if delta[0:2] == '@@':
            index = int(re.search('.*\+(\d+)', delta).group(1)) - 1
            continue
        elif delta[0:1] == '-':
            file_lines.pop(index)
        elif delta[0:1] == '+':
            file_lines.insert(index, delta[1:])
            index += 1

    return os.linesep.join(file_lines)

def diff_apply_file(file, deltafile):
    filebuffer = None
    deltas = None
    with open(file) as f, open(deltafile) as df:
        filebuffer = f.read()
        deltas = diff.read_deltas_buffer(df.read())
    return diff_apply(filebuffer, deltas)

if __name__ == '__main__':
    sys.stdout.write(diff_apply_file(sys.argv[1], sys.argv[2]))
