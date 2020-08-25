import sys
import diff
import os
import re

def diff_revert(filebuffer, deltas):
    file_lines = filebuffer.split(os.linesep)
    index = 0
    last_instruction = None
    for delta in deltas:
        if delta[0:2] == '@@':
            index = int(re.search('.*\-(\d+)', delta).group(1)) - 1
            last_instruction = 'jump'
            continue
        # insert on -
        elif delta[0:1] == '-':
            last_instruction = 'add'
            file_lines.insert(index, delta[1:])
            index += 1
        # remove on +
        elif delta[0:1] == '+':
            if last_instruction == 'jump':
                index += 1
            last_instruction = 'sub'
            file_lines.pop(index)

    return os.linesep.join(file_lines)

def diff_revert_file(file, deltafile):
    filebuffer = None
    deltas = None
    with open(file) as f, open(deltafile) as df:
        filebuffer = f.read()
        deltas = diff.read_deltas_buffer(df.read())
    return diff_revert(filebuffer, deltas)

if __name__ == '__main__':
    sys.stdout.write(diff_revert_file(sys.argv[1], sys.argv[2]))
