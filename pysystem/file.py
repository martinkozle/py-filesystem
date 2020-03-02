from copy import deepcopy
from pysystem import exceptions


class BaseFile:
    def __init__(self, name):
        self.name = name
        self.parent = None

    @staticmethod
    def create_copy_from_file(file):
        return deepcopy(file)

    def __str__(self) -> str:
        return self.get_path()

    def get_path(self, limit=None):
        display_name = self.name + '/' if type(self) is Folder else self.name
        if self.parent is None or self.parent is limit:
            return display_name
        return self.parent.get_path() + display_name


class File(BaseFile):
    def __init__(self, name, *, contents=""):
        super().__init__(name)
        self.contents = contents

    def cat(self):
        return self.contents


class Folder(BaseFile):
    def __init__(self, name, *, child_files=None):
        super().__init__(name)
        if child_files is None:
            child_files = {}
        self.child_files = child_files

    def add_child(self, file):
        tmp_name = file.name
        counter = 1
        while tmp_name in self.child_files:
            tmp_name = file.name + '({})'.format(counter)
            counter += 1
        file.name = tmp_name
        self.child_files[file.name] = file
        file.parent = self
        return file

    def remove_child(self, file):
        if file.name not in self.child_files:
            raise exceptions.NoSuchFileException()
        del self.child_files[file.name]

    def cat(self):
        return exceptions.InvalidDirectoryOperationException()

    def get_sub_file(self, file_name):
        for child_file in self.child_files.values():
            if child_file.name == file_name:
                return child_file
        return None
