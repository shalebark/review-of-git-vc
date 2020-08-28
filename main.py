
"""
    Core Functions:


    Branches expect all commits to come nicely as one node next to another,
    When going back and then commiting to a node that already has a descendent, it will create a new node that exists outside of the branch.

    So far, haven't done the workspace updates yet
"""

# also file minus
def file_add(filepath):
    index.add(filepath)

def commit(message: str, description: Optional[str]):
    repository.commit(index.compile_changes(), message, description)

def update_workspace(commit: Commit):
    workspace.set_to_commit(commit)

def branch(branch_name: str) -> None:
    assert(not repository.has_branch(branch_name))
    branch = repository.find_branch(branch_name)
    repository.checkout(branch.head())

def merge(com1: Commit, com2: Commit) -> None:
    try:
        com1.merge(com2)
        repository.commit(, 'merge', '')
    except MergeException as err:
        print(err)
        index.mark_conflicts(err.conflicts)

def merge_by_id(rev1: str, rev2: str) -> None:
    com1 = repository.find_revision(rev_id1)
    assert(com1 is not None)
    com2 = repository.find_revision(rev_id2)
    assert(com2 is not None)
    merge(com1, com2)

def merge_branch(branch_name: str) -> None:
    branch = repository.find_branch(branch_name)
    assert(branch is not None)
    merge(repository.current_commit(), branch.head())

def checkout_by_revision(rev: str) -> None:
    commit = revision.find_revision(rev)
    repository.checkout(commit)

def reset() -> None:
    update_workspace(repository.current_commit())

"""

---MAIN



*utility:
    get_all_files_inside_directory() # recursively get all files in directory (txt files only for now)
    get_ignore_patterns() # uses .bvcignore to retrieve all ignore patterns

    # shows the changes to be commited, and shows the list of files that have changes but not staged to commit
    get_status():

*workspace:
    # only the CURRENT changeset knows what files are tracked,
    # only the index knows file meta data for each of the tracked files
    # use the repository, index, and os to determine which files are untracked
    find_all_untracked_files():
        directory_files = util.get_all_files_inside_directory()
        tracked_files = repo.get_current().get_tracked_files()
        ignore_patterns = util.get_ignore_patterns()

        # all directory files that does not match any of the ignore patterns and not in tracked_files
        return [ file for file in directory_files if file not match ignore_patterns if file not in tracked_files ]

    # all tracked files
    find_all_tracked_files():
        # only the CURRENT changeset knows what files are tracked,
        return repository.get_current().get_tracked_files()

    # all changed tracked files
    find_all_changed_files():
        # the index knows the meta data for the tracked files, it should be able to figure out which has changed
        return index.get_changed_files()

    # shows the diffs of workspace and CURRENT
    show_file_diff(filepath):
        buffer = read(filepath)
        diff = differ.diff( repository.get_current().get_file_snapshot(filepath), buffer)
        stdout(diff)

    # shows all the diffs for all tracked files
    show_all_diffs():
        current = repository.get_current()
        tracked_files = current.get_tracked_files()
        buffers = [ differ.diff(current.get_file_snapshot(filepath), read(filepath)) for filepath in tracked_files ].join('-------------')
        stdout(buffers)

    # adds a file to index(stage)
    add_file_to_index(filepath):
        return index.add_file(filepath)

    # remove select a specific file to index
    remove_file_from_index(filepath):
        return index.remove_file(filepath)

    # revert file to whatever is in the index
    revert_file(filepath):
        write(filepath, repository.get_current().get_file_snapshot(filepath))

    # reverts everything to the current changeset
    reset_hard():
        util.checkout(repository.get_current())

*index:
    #
    # the index contains the list of tracked files, along with information such as size, creation_time, and last_modified_time
    #
    self.tracked_files = [] # ( size, creation_time, last_modified_time, filepath )

    fetch_meta(filepath):


    add_file(filepath):
        self.fetch_meta(filepath)

    get_tracked_files():
        return list(self.tracked_files)

    # returns list of diffs for tracked files
    get_changed_files():
        for file in self.get_tracked_files():

    get_changes_preview()
    stage_file()
    remove_file_from_index()
    get_file_snapshot()

*stage:
    # shows the status of the staged commit ()
    get_status():


"""

