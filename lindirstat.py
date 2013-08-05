
base_dir = '/'

import subprocess, os

class RootDirectory(object):
    pass

class DirEntry(object):

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.children = []
        self.fullpath = self.parent + os.path.sep + self.name

    def disk_usage(self):
        pass

    def listdir(self):
        for name in os.listdir(self.fullpath):
            self.children.append(DirEntry(name, self.fullpath))

    def __repr__(self):
        return self.fullpath

top = DirEntry('home', '/')

print top.children

top.listdir()

print top.children
