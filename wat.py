def compare_lists(list_a, list_b, comparator):

    iter_a = iter(list_a)
    iter_b = iter(list_b)

    added = []
    modified = []
    removed = []

    while True:
        val_a = [None, True]
        val_b = [None, True]
        try:
            val_a[0] = next(iter_a)
        except StopIteration:
            val_a[1] = False
        try:
            val_b[0] = next(iter_b)
        except StopIteration:
            val_b[1] = False

        print(val_a, val_b)

        if val_a[1] is False and val_b[1] is False:
            break
        if val_a[1] is False:
            removed.append(val_b[0])
            continue
        if val_b[1] is False:
            added.append(val_a[0])
            continue

        if comparator(val_a, val_b):
            modified.append(val_a[0])

    return (added, modified, removed)

from pprint import pprint

if __name__ == "__main__":

    # modifiedset = [1,2,3]
    # originalset = [2,3,4]

    # modified = (list(modifiedset), modifiedset)
    # original = (list(originalset), originalset)

    # def comparator(idx_a, idx_b):
    #     nonlocal modifiedset
    #     nonlocal originalset
    #     if idx_a is not originalset
    #     [idx_b]

    first = {'1': "one", '2': "2", '4': "four", '5': "five"}
    second = {'2': "two", '3': "three", '5': "five"}

    # added
    added = set(second) - set(first)
    print(added)
    # removed
    removed = set(first) - set(second)
    print(removed)

    done = set(list(added) + list(removed))

    modified = [ i[0] for i in set(first.items()) - set(second.items()) if i[0] not in done ]
    print( modified )
