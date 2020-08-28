"""
bvc:
    status
    add(file|directory)
    rm(file|directory)
    commit
    checkout(file|revision|branch)
    branch(make|None)
    merge(revision|branch)
    diff(file|revision|stage)
"""



"""

How BVC Works:



"""

"""
    workspace (basically the filesystem)
    index (a data structure that contains filepath, filesize, creation_time, modified_time for all tracked files)
        whenever a file gets added use bvc add, it adds it to the index
        when a commit happens, it reads the index file, and then compares it to the workspace for changes
            my guess for changes
            newly added files
    repository ()


    ALL FILE PATHS SHOULD BE RELPATHS
"""

