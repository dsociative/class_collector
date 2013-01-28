# -*- coding: utf8 -*-
from os.path import abspath, basename
from unittest import TestCase

from class_collector import ClassCollector
from tests import test_env
from tests.test_env.base_command import BaseCommand
from tests.test_env.user import auth
from tests.test_env.user.auth import Authorization


def names(cmds):
    return [cmd.__name__ for cmd in cmds]


def filenames(paths):
    return [basename(p) for p in paths]


class CollectorTest(TestCase):

    def setUp(self):
        path = abspath('tests/test_env')
        self.collector = ClassCollector(path, BaseCommand)

    def test_path_not_found(self):
        self.assertRaises(ValueError, ClassCollector, 'notfoundpath',
                          BaseCommand)

    def test_iscommand(self):
        self.assertTrue(self.collector.iscommand(Authorization))

    def test_inmodule(self):
        self.assertTrue(self.collector.inmodule(Authorization, auth))
        self.assertFalse(self.collector.inmodule(Authorization, test_env))

    def test_python_files(self):
        self.assertEqual(filenames(self.collector.python_files()),
                         ['__init__.py', 'auth.py', '__init__.py',
                          'base_command.py'])

    def test_classes(self):
        classes = list(self.collector.classes())
        self.assertEqual(names(classes), ['Authorization', 'BaseCommand'])

    def test_commands_gen(self):
        commands = self.collector.commands_gen()
        self.assertEqual(names(commands), ['Authorization'])

    def test_commands(self):
        self.assertEqual(names(self.collector.commands()),
                         names(self.collector.commands_gen()))

    def test_mapper(self):
        mapper = self.collector.mapper()
        self.assertEqual(mapper['user.authorization'].__name__,
                         'Authorization')

    def test_mapper_custom_key(self):
        mapper = self.collector.mapper(lambda cls: cls.__name__)
        self.assertEqual(mapper['Authorization'].__name__, 'Authorization')
