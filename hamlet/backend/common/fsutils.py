import os
import json
import pathlib


class Search:
    @staticmethod
    def split_path(path):
        parts = os.path.normpath(path).split(os.path.sep)
        if len(parts) > 0 and parts[0] == "":
            parts[0] = os.path.sep
        return parts

    @staticmethod
    def exists(directory, name, up=0):
        if up < 0:
            raise ValueError("up parameter must be >= 0")
        search_dir_parts = Search.split_path(directory)
        up = min(len(search_dir_parts), up)
        up = len(search_dir_parts) - up
        search_path = os.path.join(*search_dir_parts[:up], name)
        return search_path if os.path.exists(search_path) else None

    @staticmethod
    def isfile(directory, name, up=0):
        filename = Search.exists(directory, name, up)
        return filename if filename is not None and os.path.isfile(filename) else None

    @staticmethod
    def isdir(directory, name, up=0):
        dirname = Search.exists(directory, name, up)
        return dirname if dirname is not None and os.path.isdir(dirname) else None

    @staticmethod
    def upwards(directory, name):
        parts = Search.split_path(directory)
        for up in range(len(parts)):
            up = len(parts) - up
            search_path = os.path.join(*parts[:up], name)
            if os.path.exists(search_path):
                return search_path
        return None

    @staticmethod
    def downwards(directory, name):
        found = []
        for root, dirs, files in os.walk(directory, topdown=True):
            for filename in files:
                if filename == name:
                    found.append(os.path.join(root, filename))
            for dirname in dirs:
                if dirname == name:
                    found.append(os.path.join(root, dirname))
        return found

    @staticmethod
    def basename(path, up=0):
        parts = Search.split_path(path)
        up = min(len(parts), up)
        up = len(parts) - up - 1
        return parts[up]

    @staticmethod
    def parent(path, up=0):
        parts = Search.split_path(path)
        up = min(len(parts), up)
        up = len(parts) - up
        return os.path.join(*parts[:up])

    @staticmethod
    def cut(path, prefix="", suffix=""):
        path = Search.split_path(path)
        if prefix:
            prefix = Search.split_path(prefix)
            if path[: len(prefix)] == prefix:
                path = path[len(prefix) :]
        if suffix:
            suffix = Search.split_path(suffix)
            if path[-len(suffix) :] == suffix:
                path = path[: -len(suffix)]
        return os.path.join(*path)

    @staticmethod
    def match(*patterns, root=None):
        root = root or os.getcwd()
        root = pathlib.Path(root)
        matches = []
        for pattern in patterns:
            matches_gen = root.glob(pattern)
            matches += [str(match) for match in matches_gen]
        # removing duplicates
        return list(set(matches))

    def match_dirs(*patterns, root=None, include_file_dirs=False):
        matches = Search.match(*patterns, root=root)
        filtered_matches = []
        for match in matches:
            if os.path.isfile(match):
                if include_file_dirs:
                    filtered_matches.append(os.path.dirname(match))
            else:
                filtered_matches.append(match)
        # removing duplicates
        return list(set(filtered_matches))

    def match_files(*patterns, root=None):
        matches = Search.match(*patterns, root=root)
        return [match for match in matches if os.path.isfile(match)]

    def list_all(dirname):
        return [name for name in os.listdir(dirname)]

    def list_files(dirname):
        return [
            name
            for name in os.listdir(dirname)
            if os.path.isfile(os.path.join(dirname, name))
        ]

    def list_dirs(dirname):
        return [
            name
            for name in os.listdir(dirname)
            if os.path.isdir(os.path.join(dirname, name))
        ]


class ContextSearch:
    def __init__(self, cwd):
        self.cwd = cwd

    @property
    def cwd(self):
        return self.__cwd

    @cwd.setter
    def cwd(self, value):
        if not os.path.isabs(value):
            raise ValueError("{} is not abs path".format(value))
        if not os.path.exists(value):
            raise ValueError("{} does not exist".format(value))
        if not os.path.isdir(value):
            raise ValueError("{} is not directory".format(value))
        self.__cwd = value

    def exists(self, name, up=0):
        return Search.exists(self.cwd, name, up=up)

    def isfile(self, name, up=0):
        return Search.isfile(self.cwd, name, up=up)

    def isdir(self, name, up=0):
        return Search.isdir(self.cwd, name, up=up)

    def upwards(self, name):
        return Search.upwards(self.cwd, name)

    def downwards(self, name):
        return Search.downwards(self.cwd, name)

    def basename(self, up=0):
        return Search.basename(self.cwd, up=up)

    def parent(self, up=0):
        return Search.parent(self.cwd, up=up)


# TODO: Needs to be splitted into several subclasses like JSONFile, TXTFile, ByteFile
# Then File may be used as an automated type resolver.
class File:
    def __init__(self, path):
        self.path = path
        self.data = None
        name, ext = os.path.splitext(self.path)
        self.ext = ext

    def load(self):
        if self.data is not None:
            return self.data
        if self.ext == ".json":
            with open(self.path, "rb") as f:
                self.data = json.load(f)
        else:
            with open(self.path, "rt") as f:
                self.data = f.read()
        return self.data

    def reload(self):
        self.data = None
        return self.load()

    def write(self):
        if self.ext == ".json":

            def serialize():
                return json.dumps(self.data)

        else:

            def serialize():
                return self.data

        with open(self.path, "wt+") as f:
            f.write(serialize())

    def __getitem__(self, key):
        try:
            self.load()
            return self.data[key]
        except TypeError as e:
            raise TypeError("Unstructured data") from e


class Directory:
    def __init__(self, path):
        self.path = path

    def __getitem__(self, key):
        path = os.path.join(self.path, key)
        if not os.path.exists(path):
            raise KeyError("Path {} does not exist".format(path))
        if os.path.isfile(path):
            return File(path)
        else:
            return self.__class__(os.path.join(self.path, key))

    def __iter__(self):
        for path in os.listdir(self.path):
            fullpath = os.path.join(self.path, path)
            if os.path.isfile(fullpath):
                yield File(fullpath)
            elif os.path.isdir(fullpath):
                yield self.__class__(fullpath)
            else:
                yield fullpath
