"""
---DictionaryTree
"""
class DictionaryNode:
    # identifier must be unique to the tree
    def __init__(self, identifier: Optional[str], parent=None, item=None: Any):
        self.identifier = identifer
        self.parent = parent
        self.children = []
        self.item = item

    def get_identifier():
        return self.identifier

    def get_item():
        return self.item

    def set_item(item=None: Any):
        self.item = item

    def childrens():
        return len(self.children)

class DictionaryTree:
    def __init__(self):
        self.root = DictionaryNode()
        self.identifier_dict = {}

    def get_root():
        return self.root

    def is_in_tree(identifier: str):
        return not not self.identifier

    def get(identifier):
        return self.identifier_dict[identifier]

    def descend_from(node: DictionaryNode, identifer: str, item=None: Any) -> DictionaryNode:
        assert(not self.is_in_tree(identifier))
        child = Node(str, node, item)
        node.children.append(child)
        self.identifier_dict[identifier] = child
        return child



"""
---EOL Dictionary Tree
"""

"""
---Branch

Branches are a list of nodes that all descend from the previous one. A branch itself cannot contain other branches, its a path from one node to another end node
The list of nodes in a branch cannot be duplicated
"""
class Branch:
    def __init__(self, name: str, root: Node, end: Node):
        self.name = name
        self.root = root
        self.end = end
        self.nodes = [root]

class BranchManager:
    def __init__(self):
        self.branches = {}
        self.current = current

    def add(self, branch: Branch):
        self.branches[branch.name] = branch

    def remove(self, branch: Branch):
        self.branches[branch.name] = branch

    def has(self, name: str):
        return self.branches.has_key(name)

    def get(self, name: str):
        return self.branches[str]

    def set_current(branch: Branch):
        self.current = branch

    def get_current(): Branch:
        return self.current

    def is_current_head(revision: str) -> bool:
        return self.current.get_head().get_revision() == revision

    # def update_head(revision: str):
    #     self.current.(revision)

    # def is_current_endnode(node: Node) -> bool:
    #     return self.current.end is node

    # def update_current_endnode(node: Node):
    #     self.current.end = node

"""
---EOL Branch
"""

"""
---Changeset
"""

class Changeset:
    def __init__(self, file_deltas: Index.Delta, hash: str, message: str, description: Optional[str]):
        self.file_deltas = file_deltas
        self.hash = hash
        self.message = message
        self.description = description

"""
---EOL Changeset
"""

"""
---Repository
"""

class Repository:
    def __int__(self):
        self.tree = DictionaryTree()
        self.bmgr = BranchManager()
        self.current_node = self.tree.get_root()

    def load():
        # loads the repository from some data
        return


    def commit(changeset: Changeset) -> str:
        new_node = self.tree.descend_from(self.current_node, changeset.get_hash(), changeset)
        # if the new node is the end node of the current branch, then set that as the new end node foro the branch
        if self.bgmr.is_current_endnode(self.current_node):
            self.bgmr.update_current_endnode(new_node)
        return new_node.get_item().hash()

    # name is the unique identifier for branch
    def branch(name):
        branch = self.bgmr.get_or_create(name)
        self.checkout(branch.get_endnode())

    # only switches the node to the node, does not affect the workspace
    def checkout_by_revision(revision: str) -> Changeset:
        self.checkout(self.tree.get(revision))

    # only switches the node to the node, does not affect the workspace
    def checkout(changeset: Changeset) -> Changeset:
        self.current_node = self.tree.get(changeset.get_hash())
        self.bgmr.find_branch_of_node()
        ()

"""
count as in dev or master, depending on if you are in dev or master, but if you come from neither and checkout to this commit directly, you belong into none of them
commit f6a89a79f229f12efd2eb5a92a60ab74d7dcef3d (HEAD -> dev, master)
Merge: 8998d86 2a18c14
Author: U-kenneth-PC\kenneth <cremling@protonmail.com>
Date:   Tue Aug 25 16:55:40 2020 -0400

    merge


"""


"""
---EOL Repository
"""


