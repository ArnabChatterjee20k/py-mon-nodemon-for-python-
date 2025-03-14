import pathlib, os


class WatcherPath:
    """Currently supported for directories not individual files"""

    def __init__(
        self, location: str, recursive=False, ignore: list["WatcherPath"] = []
    ):
        self._path = pathlib.Path(location)
        self.recursive = recursive
        self.ignore = ignore
        self._check_exceptions

    def _check_exceptions(self):
        if not self._path.is_dir():
            raise Exception("We only support directories")

    def get_dirs(self):
        if self.recursive:
            paths = []
            for path in self._get_all_dirs():
                paths.append(path)
            return paths
        return [self._path.resolve()]

    def _get_all_dirs(self):
        if self._path.is_dir():
            for dirpath, _, _ in os.walk(self._path, followlinks=True):
                dirpath_watcher_instance = WatcherPath(dirpath)
                for ignored in self.ignore:
                    if dirpath_watcher_instance.contains(ignored):
                        continue
                    yield pathlib.Path(dirpath).resolve()

    def contains(self, path: "WatcherPath"):
        # getting the absolute path of _path and path
        # then string comparison
        return str(path._path.resolve()).startswith(str(self._path.resolve()))