import pathlib, os


class WatcherPath:
    def __init__(self, path: str, recursive=False, ignore: list["WatcherPath"] = []):
        self.path = pathlib.Path(path)
        self.recursive = recursive
        self.ignore = ignore

    def _check_rules(self):
        if not self.path.is_dir():
            raise Exception("Only dirs are supported")

    def get_dirs(self):
        if self.recursive:
            self._get_recursive_dirs()

        return [str(self.path.resolve())]

    def _get_recursive_dirs(self):
        dirs = os.walk(self.path)
        # TODO: use trie or path matching data structure
        # problem -> for every path we are iterating every ignore files to match
        # we can reduce it with some kind of path level cache
        # cause ignore itself can be recursive path itself
        # or a file(may be)
        for dirpath, _, _ in dirs:
            print(dirpath)
            raise Exception("Recursive Not supported")

    def is_ignored(self, path: "WatcherPath"):
        pass
