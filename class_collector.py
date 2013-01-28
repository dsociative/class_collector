# -*- coding: utf8 -*-
from os import walk
from os.path import join, isdir
from inspect import getmembers, isclass

from import_file import import_file


def get_default_key(command):
    return command.name


class ClassCollector(object):

    def __init__(self, path, base_cls):
        self.path = path
        self.base_cls = base_cls

        if not isdir(path):
            raise ValueError, 'path %s not found or not is dir' % path

    def files(self):
        for root, dirs, files in walk(self.path, topdown=False):
            for file in files:
                yield join(root, file)

    def python_files(self):
        for filename in self.files():
            if filename.endswith('.py'):
                yield filename

    def inmodule(self, cls, module):
        return cls.__module__ == module.__name__

    def iscommand(self, cls):
        return issubclass(cls, self.base_cls)

    def import_file(self, path):
        return import_file(path)

    def classes(self):
        for path in self.python_files():
            module = self.import_file(path)
            for name, cls in getmembers(module, isclass):
                if self.inmodule(cls, module):
                    yield cls

    def commands_gen(self):
        for cls in self.classes():
            if self.iscommand(cls):
                yield cls

    def commands(self):
        return list(self.commands_gen())

    def mapper_gen(self, get_key=get_default_key):
        for command in self.commands_gen():
            yield get_key(command), command

    def mapper(self, get_key=get_default_key):
        return dict(self.mapper_gen(get_key))
