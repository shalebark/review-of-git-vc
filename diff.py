class Differ:

    def __init__(self, original, modified):
        self.buffers = {'original': original, 'modified': modified}

        self.lines = {'original': self.buffers['original'].split('\n'), 'modified': self.buffers['modified'].split('\n')}
        self.pointer = { 'original': { 'position': -1, 'line': None, 'eol': False }, 'modified': { 'position': -1, 'line': None, 'eol': False } }

        self.changes = []

    # --- GETTER HELPERS
    def get_buffer_lines(self, buffer_name):
        return self.lines[buffer_name]

    def get_buffer_length(self, buffer_name):
        return len(self.get_buffer_lines(buffer_name))

    def get_pointer_position(self, buffer_name):
        return self.pointer[buffer_name]['position']

    def get_pointer_line(self, buffer_name):
        return self.pointer[buffer_name]['line']

    def get_pointer_eol(self, buffer_name):
        return self.pointer[buffer_name]['eol']
    # --- EOF GETTER HELPERS

    def read_next_line(self, buffer_name):
        if self.get_pointer_eol(buffer_name) == True:
            return self.pointer

        self.pointer[buffer_name]['position'] += 1

        if self.get_pointer_position(buffer_name) >= self.get_buffer_length(buffer_name):
            self.pointer[buffer_name]['line'] = None
            self.pointer[buffer_name]['eol'] = True
            return self.pointer

        self.pointer[buffer_name]['line'] = None if self.get_pointer_position(buffer_name) < 0 else self.get_buffer_lines(buffer_name)[self.get_pointer_position(buffer_name)]
        return self.pointer

    def read_line(self):
        self.read_next_line('original')
        self.read_next_line('modified')
        return not (self.get_pointer_eol('original') or self.get_pointer_eol('modified'))

    def line_is_changed(self):
        return self.get_pointer_line('original') != self.get_pointer_line('modified')

    def seek_pointer_position(self, buffer_name, index):
        self.pointer[buffer_name]['eol'] = False
        self.pointer[buffer_name]['position'] = index - 1;
        self.read_next_line(buffer_name)

    def find_next_line_position(self, buffer_name, lookup_line):
        starting_position = self.get_pointer_position(buffer_name)
        for position in range(starting_position, self.get_buffer_length(buffer_name)):
            if self.get_buffer_lines(buffer_name)[position] == lookup_line:
                return position
        return None

    def delete_by_position_range(self, start_position, end_position):
        self.changes.append({'type': 'sub', 'start_position': start_position, 'length': end_position - start_position})

    def add_by_position_range(self, start_position, end_position):
        for position in range(start_position, end_position):
            self.changes.append({'type': 'add', 'position': position, 'line': self.get_buffer_lines('modified')[position] })

    def delete_remaining_original_lines(self):
        self.delete_by_position_range(self.get_pointer_position('original'), self.get_buffer_length('original'))

    def add_remaining_modified_lines(self):
        while True:
            self.add(self.get_pointer_position('modified'), self.get_pointer_line('modified'))
            self.read_next_line('modified')
            if self.get_pointer_eol('modified'):
                break


def diff(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        differ = Differ(f1.read(), f2.read())

        while True:
            differ.read_next_line('original')
            differ.read_next_line('modified')

            # end condition: both files has finally been exhausted, exit
            if differ.get_pointer_eol('original') and differ.get_pointer_eol('modified'):
                break

            # end condition: the original file is larger than the modified, remaining originals must have been deleted
            if differ.get_pointer_eol('modified'):
                differ.delete_by_position_range(differ.get_pointer_position('original'), differ.get_buffer_length('original'))
                break

            # end condition: the modified file is larger than the original, remaining modified must be new additions
            if differ.get_pointer_eol('original'):
                differ.add_by_position_range(differ.get_pointer_position('modified'), differ.get_pointer_position('modified'))
                break

            if differ.get_pointer_line('original') != differ.get_pointer_line('modified'):
                found_position = differ.find_next_line_position('original', differ.get_pointer_line('modified'))

                # Nothing is Found, then this is a new line, add
                if found_position is None:
                    differ.add_by_position_range(differ.get_pointer_position('modified'), differ.get_pointer_position('modified') + 1)
                    # Shift Up the original pointer by 1, so we can go back to this same original line for next check
                    differ.seek_pointer_position('original', differ.get_pointer_position('original') - 1)

                # If a position is found, then we've deleted all the previous lines
                else:
                    differ.delete_by_position_range(differ.get_pointer_position('original'), found_position)
                    # Move the original pointer to the new position, the current modified matches this one, so move the pointer so they both match, next loop will increment both
                    differ.seek_pointer_position('original', found_position)


        # while differ.read_line():
        #     if differ.line_is_changed():
        #         print('preindex lookup',
        #             differ.get_buffer_length('original'), differ.get_buffer_length('modified'),
        #             differ.get_buffer_lines('original'), differ.get_buffer_lines('modified'),
        #             differ.get_pointer_position('original'), differ.get_pointer_line('original'),
        #             differ.get_pointer_position('modified'), differ.get_pointer_line('modified'),
        #         )

        #         original_index = differ.get_pointer_position('original')
        #         found_index = differ.lookup_next_instance(differ.get_pointer_line('modified'))

        #         print('postindex lookup',
        #             differ.get_buffer_length('original'), differ.get_buffer_length('modified'),
        #             differ.get_buffer_lines('original'), differ.get_buffer_lines('modified'),
        #             differ.get_pointer_position('original'), differ.get_pointer_line('original'),
        #             differ.get_pointer_position('modified'), differ.get_pointer_line('modified'),
        #         )

        #         if found_index is not -1:
        #             differ.delete_by_position_range(original_index, found_index)
        #         else:
        #             differ.add(differ.get_pointer_position('modified'), differ.get_pointer_line('modified'))
        #             differ.set_pointer_position('original', original_index - 1)
        #     else:
        #         print( 'no change',
        #             differ.get_buffer_length('original'), differ.get_buffer_length('modified'),
        #             differ.get_buffer_lines('original'), differ.get_buffer_lines('modified'),
        #             differ.get_pointer_eol('original'), differ.get_pointer_eol('modified'),
        #             differ.get_pointer_position('original'), differ.get_pointer_line('original'),
        #             differ.get_pointer_position('modified'), differ.get_pointer_line('modified'),
        #         )
        #     print('------------------------')

        # print('here')

        # if differ.get_pointer_eol('modified'):
        #     differ.delete_remaining_original_lines()
        # if differ.get_pointer_eol('original'):
        #     differ.add_remaining_modified_lines()

    return {'changes': differ.changes, 'original_lines': differ.get_buffer_lines('original'), 'modified_lines': differ.get_buffer_lines('modified')}

def diff_buff(file1, file2):
    diff_results = diff(file1, file2)

    changes = diff_results['changes']
    original_lines = diff_results['original_lines']
    modified_lines = diff_results['modified_lines']

    buffer = ''

    def add_set_to_buffer():
        nonlocal buffer
        nonlocal current_add_set

        if current_add_set:
            buffer += '+%s,%s\n' %(current_add_set[0]['position'] + 1, len(current_add_set))
            for add_change in current_add_set:
                buffer += '>%s\n' %(add_change['line'])
            current_add_set.clear()

    current_add_set = []
    for change in changes:
        if change['type'] == 'add':
            if not ( current_add_set and ( current_add_set[len(current_add_set) -1]['position'] + 1 == change['position'] ) ):
                add_set_to_buffer()
            current_add_set.append(change)
        # change['type] == 'sub':
        else:
            add_set_to_buffer()
            buffer += '-%s,%s\n' %(change['start_position'] + 1, change['length'])
            for idx in range(change['start_position'], change['start_position'] + change['length']):
                print('idx check', idx, original_lines[idx], original_lines)
                buffer += '<%s\n' %(original_lines[idx])

    add_set_to_buffer()

    return buffer

def diff_out(file1, file2):
    print(diff(file1, file2))
    # print(diff_buff(file1, file2))

if __name__ == "__main__":
    import sys
    # for i in range(0, 1):
    #     print(i)
    diff_out(sys.argv[1], sys.argv[2])