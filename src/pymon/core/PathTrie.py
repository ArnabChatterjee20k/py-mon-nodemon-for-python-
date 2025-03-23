import pathlib
class Node:
    def __init__(self):
        self.children = {}
        self.is_end = False
    

class PathTrie:
    def __init__(self):
        self.root = Node()

    def __contains__(self,path):
        return self.search(path)

    def insert(self,path:str):
        parts = pathlib.Path(path).parts
        node = self.root
        for part in parts:
            if part not in node.children:
                node.children[part] = Node()
            node = node.children[part]
        node.is_end = True

    def search(self,path:str):
        node = self.root
        parts = pathlib.Path(path).parts
        for part in parts:
            if part not in node.children:
                return False
            node = node.children[part]
            if node.is_end:
                return True
        
        return node.is_end
    
    def print_trie(self, node=None, prefix="", level=0):
        """
        Recursively prints the trie in a tree-like structure.
        """
        if node is None:
            node = self.root

        for key, child in node.children.items():
            print("  " * level + "|-- " + key + ("/" if child.children else ""))
            self.print_trie(child, prefix + key + "/", level + 1)