import pathlib, os
from .PathTrie import PathTrie

class WatcherPath:
    def __init__(self, path: str, recursive=False, ignore: list["str"] = []):
        """
            path is the core path
            ignore is the relative paths to the path
        """
        self.path = pathlib.Path(path)
        self.recursive = recursive
        self._ignore_trie = PathTrie()
        for ignored_path in ignore:
            ignored_full_path = (self.path / ignored_path).resolve()
            self._ignore_trie.insert(str(ignored_full_path))


    def _check_rules(self):
        if not self.path.is_dir():
            raise Exception("Only dirs are supported")

    def get_dirs(self):
        base_dir = [str(self.path.resolve())]
        if self.recursive:
            sub_dirs = self._get_recursive_dirs()
            base_dir.extend(sub_dirs)

        return base_dir

    def _get_recursive_dirs(self):
            sub_dirs = []
            for dirpath, dirnames, _ in os.walk(self.path):
                for dirname in dirnames:
                    full_path = pathlib.Path(dirpath) / dirname  # Join and normalize
                    full_path = full_path.resolve()  # Convert to absolute path
                    
                    if not self.is_ignored(str(full_path)):  # Check full path in Trie
                        sub_dirs.append(str(full_path))
            return sub_dirs

    def is_ignored(self, path: str):
        return self._ignore_trie.search(str(pathlib.Path(path).resolve())) 
