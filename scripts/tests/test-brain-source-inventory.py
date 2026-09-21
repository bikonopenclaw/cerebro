#!/usr/bin/env python3
"""Regression tests for incomplete inventory traversal; fixture files only."""
import errno
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

MODULE_PATH = Path(os.environ.get('INVENTORY_UNDER_TEST', str(Path(__file__).resolve().parents[1] / 'brain-source-inventory.py')))
spec = importlib.util.spec_from_file_location('inventory_under_test', MODULE_PATH)
inventory_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inventory_module)

class InventoryErrors(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.history = self.base / 'agents' / 'main' / 'sessions'
        self.history.mkdir(parents=True)
        self.agents = patch.object(inventory_module, 'AGENTS', ('main',))
        self.agents.start()
        self.addCleanup(self.agents.stop)

    def run_inventory(self):
        return inventory_module.inventory(base=self.base, profiles={'main': self.base})

    def assert_unreviewed(self, result):
        self.assertIs(result['coverage_complete'], False)
        self.assertTrue(all(row['coverage'] == 'unreviewed' and row['content_read'] is False for row in result['sources']))

    def test_walk_permission_error_recorded_and_sibling_is_inventoried(self):
        denied = self.history / 'unreadable'
        denied.mkdir()
        (denied / 'hidden.jsonl').write_text('hidden fixture')
        allowed = self.history / 'readable'
        allowed.mkdir()
        good = allowed / 'good.jsonl'
        good.write_text('readable fixture')
        real_scandir = os.scandir
        def scandir(path):
            if Path(path) == denied:
                raise PermissionError(errno.EACCES, 'fixture denied directory', str(path))
            return real_scandir(path)
        # Real os.walk handles this scandir failure internally and calls onerror.
        with patch.object(inventory_module.os, 'scandir', side_effect=scandir):
            result = self.run_inventory()
        self.assertEqual(result['errors'], [{'path': str(denied), 'error': 'PermissionError'}])
        self.assertEqual([row['path'] for row in result['sources']], [str(good)])
        self.assert_unreviewed(result)

    def test_individual_stat_error_records_file_and_continues_same_directory(self):
        bad = self.history / 'first.jsonl'
        good = self.history / 'second.jsonl'
        bad.write_text('fixture not readable')
        good.write_text('fixture readable')
        real_stat = Path.stat
        def ordered_walk(path, **kwargs):
            self.assertEqual(Path(path), self.history)
            yield str(self.history), [], [bad.name, good.name]
        for exception in (FileNotFoundError, PermissionError):
            with self.subTest(exception=exception.__name__):
                def stat_file(path, *args, **kwargs):
                    if path == bad and kwargs.get('follow_symlinks', True):
                        raise exception(errno.ENOENT if exception is FileNotFoundError else errno.EACCES, 'fixture stat error', str(path))
                    return real_stat(path, *args, **kwargs)
                with patch.object(inventory_module.os, 'walk', side_effect=ordered_walk), patch.object(Path, 'stat', stat_file):
                    result = self.run_inventory()
                self.assertEqual(result['errors'], [{'path': str(bad), 'error': exception.__name__}])
                self.assertEqual([row['path'] for row in result['sources']], [str(good)])
                self.assert_unreviewed(result)

    def test_filters_and_metadata_only_contract_survive(self):
        good = self.history / 'good.jsonl'
        good.write_text('sensitive fixture body must not be read')
        (self.history / 'ignored.txt').write_text('irrelevant')
        (self.history / 'linked.jsonl').symlink_to(good)
        old = self.history / 'old.jsonl'
        old.write_text('old')
        os.utime(old, (1, 1))
        with patch.object(Path, 'read_text', side_effect=AssertionError('inventory must not read contents')):
            result = self.run_inventory()
        self.assertEqual(result['errors'], [])
        self.assertEqual([row['path'] for row in result['sources']], [str(good)])
        self.assert_unreviewed(result)

if __name__ == '__main__':
    unittest.main(verbosity=2)
