import os


class Search:

    @staticmethod
    def split_path(path):
        parts = os.path.normpath(path).split(os.path.sep)
        if len(parts) > 0 and parts[0] == '':
            parts[0] = os.path.sep
        return parts

    @staticmethod
    def exists(directory, name, up=0):
        if up < 0:
            raise ValueError('up parameter must be >= 0')
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
        return dirname if dirname is not None and os.path.isfile(dirname) else None

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
    def cut(path, prefix='', suffix=''):
        path = Search.split_path(path)
        if prefix:
            prefix = Search.split_path(prefix)
            if path[:len(prefix)] == prefix:
                path = path[len(prefix):]
        if suffix:
            suffix = Search.split_path(suffix)
            if path[-len(suffix):] == suffix:
                path = path[:-len(suffix)]
        return os.path.join(*path)


class ContextSearch:
    def __init__(self, cwd):
        self.cwd = cwd

    @property
    def cwd(self):
        return self.__cwd

    @cwd.setter
    def cwd(self, value):
        if not os.path.isabs(value):
            raise ValueError('{} is not abs path'.format(value))
        if not os.path.exists(value):
            raise ValueError('{} does not exist'.format(value))
        if not os.path.isdir(value):
            raise ValueError('{} is not directory'.format(value))
        self.__cwd = value

    def exists(self, name, up=0):
        return Search.exists(self.cwd, name, up=up)

    def isfile(self, name, up=0):
        return Search.isfile(self.cwd, name, up=up)

    def isdir(self, name, up=0):
        return Search.isdir(self.cwd, name, up=up)

    def upwards(self, name):
        return Search.upwards(self.cwd, name)

    def basename(self, up=0):
        return Search.basename(self.cwd, up=up)

    def parent(self, up=0):
        return Search.parent(self.cwd, up=up)


class File:
    def __init__(self, name):
        pass


class Directory:
    def __init__(self, dir):
        self.dir = dir

    def __getitem__(self, key):
        path = os.path.join(self._dir, key)
        if not os.path.exists(path):
            raise ValueError('{} does not exist'.format(path))
        if os.path.isfile(path):
            return File(path)
        else:
            return self.__class__(os.path.join(self.dir, key))

    def __iter__(self):
        for name in os.listdir(self.dir):
            yield name
