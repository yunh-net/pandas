#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import with_statement  # support python 2.5
import pandas as pd
import unittest
import warnings
import nose

class TestConfig(unittest.TestCase):

    def __init__(self,*args):
        super(TestConfig,self).__init__(*args)

        from copy import deepcopy
        self.cf = pd.core.config
        self.gc=deepcopy(getattr(self.cf, '__global_config'))
        self.do=deepcopy(getattr(self.cf, '__deprecated_options'))
        self.ro=deepcopy(getattr(self.cf, '__registered_options'))

    def setUp(self):
        setattr(self.cf, '__global_config', {})
        setattr(self.cf, '__deprecated_options', {})
        setattr(self.cf, '__registered_options', {})

    def tearDown(self):
        setattr(self.cf, '__global_config',self.gc)
        setattr(self.cf, '__deprecated_options', self.do)
        setattr(self.cf, '__registered_options', self.ro)

    def test_api(self):

        #the pandas object exposes the user API
        self.assertTrue(hasattr(pd, 'get_option'))
        self.assertTrue(hasattr(pd, 'set_option'))
        self.assertTrue(hasattr(pd, 'reset_option'))
        self.assertTrue(hasattr(pd, 'reset_options'))
        self.assertTrue(hasattr(pd, 'describe_options'))

    def test_register_option(self):
        self.cf.register_option('a', 1, 'doc')

        # can't register an already registered option
        self.assertRaises(KeyError, self.cf.register_option, 'a', 1, 'doc')

        # can't register an already registered option
        self.assertRaises(KeyError, self.cf.register_option, 'a.b.c.d1', 1,
                          'doc')
        self.assertRaises(KeyError, self.cf.register_option, 'a.b.c.d2', 1,
                          'doc')

        # we can register options several levels deep
        # without predefining the intermediate steps
        # and we can define differently named options
        # in the same namespace
        self.cf.register_option('k.b.c.d1', 1, 'doc')
        self.cf.register_option('k.b.c.d2', 1, 'doc')

    def test_describe_options(self):
        self.cf.register_option('a', 1, 'doc')
        self.cf.register_option('b', 1, 'doc2')
        self.cf.deprecate_option('b')

        self.cf.register_option('c.d.e1', 1, 'doc3')
        self.cf.register_option('c.d.e2', 1, 'doc4')
        self.cf.register_option('f', 1)
        self.cf.register_option('g.h', 1)
        self.cf.deprecate_option('g.h',rkey="blah")

        # non-existent keys raise KeyError
        self.assertRaises(KeyError, self.cf.describe_options, 'no.such.key')

        # we can get the description for any key we registered
        self.assertTrue('doc' in self.cf.describe_options('a',_print_desc=False))
        self.assertTrue('doc2' in self.cf.describe_options('b',_print_desc=False))
        self.assertTrue('precated' in self.cf.describe_options('b',_print_desc=False))

        self.assertTrue('doc3' in self.cf.describe_options('c.d.e1',_print_desc=False))
        self.assertTrue('doc4' in self.cf.describe_options('c.d.e2',_print_desc=False))

        # if no doc is specified we get a default message
        # saying "description not available"
        self.assertTrue('vailable' in self.cf.describe_options('f',_print_desc=False))
        self.assertTrue('vailable' in self.cf.describe_options('g.h',_print_desc=False))
        self.assertTrue('precated' in self.cf.describe_options('g.h',_print_desc=False))
        self.assertTrue('blah' in self.cf.describe_options('g.h',_print_desc=False))

    def test_get_option(self):
        self.cf.register_option('a', 1, 'doc')
        self.cf.register_option('b.a', 'hullo', 'doc2')
        self.cf.register_option('b.b', None, 'doc2')

        # gets of existing keys succeed
        self.assertEqual(self.cf.get_option('a'), 1)
        self.assertEqual(self.cf.get_option('b.a'), 'hullo')
        self.assertTrue(self.cf.get_option('b.b') is None)

        # gets of non-existent keys fail
        self.assertRaises(KeyError, self.cf.get_option, 'no_such_option')

    def test_set_option(self):
        self.cf.register_option('a', 1, 'doc')
        self.cf.register_option('b.a', 'hullo', 'doc2')
        self.cf.register_option('b.b', None, 'doc2')

        self.assertEqual(self.cf.get_option('a'), 1)
        self.assertEqual(self.cf.get_option('b.a'), 'hullo')
        self.assertTrue(self.cf.get_option('b.b') is None)

        self.cf.set_option('a', 2)
        self.cf.set_option('b.a', 'wurld')
        self.cf.set_option('b.b', 1.1)

        self.assertEqual(self.cf.get_option('a'), 2)
        self.assertEqual(self.cf.get_option('b.a'), 'wurld')
        self.assertEqual(self.cf.get_option('b.b'), 1.1)

        self.assertRaises(KeyError, self.cf.set_option, 'no.such.key', None)

    def test_validation(self):
        self.cf.register_option('a', 1, 'doc', validator=self.cf.is_int)
        self.cf.register_option('b.a', 'hullo', 'doc2',
                                validator=self.cf.is_text)
        self.assertRaises(ValueError, self.cf.register_option, 'a.b.c.d2',
                          'NO', 'doc', validator=self.cf.is_int)

        self.cf.set_option('a', 2)  # int is_int
        self.cf.set_option('b.a', 'wurld')  # str is_str

        self.assertRaises(ValueError, self.cf.set_option, 'a', None)  # None not is_int
        self.assertRaises(ValueError, self.cf.set_option, 'a', 'ab')
        self.assertRaises(ValueError, self.cf.set_option, 'b.a', 1)

    def test_reset_option(self):
        self.cf.register_option('a', 1, 'doc', validator=self.cf.is_int)
        self.cf.register_option('b.a', 'hullo', 'doc2',
                                validator=self.cf.is_str)
        self.assertEqual(self.cf.get_option('a'), 1)
        self.assertEqual(self.cf.get_option('b.a'), 'hullo')

        self.cf.set_option('a', 2)
        self.cf.set_option('b.a', 'wurld')
        self.assertEqual(self.cf.get_option('a'), 2)
        self.assertEqual(self.cf.get_option('b.a'), 'wurld')

        self.cf.reset_option('a')
        self.assertEqual(self.cf.get_option('a'), 1)
        self.assertEqual(self.cf.get_option('b.a'), 'wurld')
        self.cf.reset_option('b.a')
        self.assertEqual(self.cf.get_option('a'), 1)
        self.assertEqual(self.cf.get_option('b.a'), 'hullo')

    def test_reset_options(self):
        self.cf.register_option('a', 1, 'doc', validator=self.cf.is_int)
        self.cf.register_option('b.a', 'hullo', 'doc2',
                                validator=self.cf.is_str)
        self.assertEqual(self.cf.get_option('a'), 1)
        self.assertEqual(self.cf.get_option('b.a'), 'hullo')

        self.cf.set_option('a', 2)
        self.cf.set_option('b.a', 'wurld')
        self.assertEqual(self.cf.get_option('a'), 2)
        self.assertEqual(self.cf.get_option('b.a'), 'wurld')

        self.cf.reset_options()
        self.assertEqual(self.cf.get_option('a'), 1)
        self.assertEqual(self.cf.get_option('b.a'), 'hullo')


    def test_deprecate_option(self):
        import sys
        self.cf.deprecate_option('c')  # we can deprecate non-existent options

        # testing warning with catch_warning was only added in 2.6
        if sys.version_info[:2]<(2,6):
            raise nose.SkipTest()

        self.assertTrue(self.cf._is_deprecated('c'))
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            try:
                self.cf.get_option('c')
            except KeyError:
                pass
            else:
                self.fail("Nonexistent option didn't raise KeyError")

            self.assertEqual(len(w), 1)  # should have raised one warning
            self.assertTrue('deprecated' in str(w[-1]))  # we get the default message

        self.cf.register_option('a', 1, 'doc', validator=self.cf.is_int)
        self.cf.register_option('b.a', 'hullo', 'doc2')
        self.cf.register_option('c', 'hullo', 'doc2')

        self.cf.deprecate_option('a', removal_ver='nifty_ver')
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            self.cf.get_option('a')

            self.assertEqual(len(w), 1)  # should have raised one warning
            self.assertTrue('eprecated' in str(w[-1]))  # we get the default message
            self.assertTrue('nifty_ver' in str(w[-1]))  # with the removal_ver quoted

            self.assertRaises(KeyError, self.cf.deprecate_option, 'a')  # can't depr. twice

        self.cf.deprecate_option('b.a', 'zounds!')
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            self.cf.get_option('b.a')

            self.assertEqual(len(w), 1)  # should have raised one warning
            self.assertTrue('zounds!' in str(w[-1]))  # we get the custom message

        # test rerouting keys
        self.cf.register_option('d.a', 'foo', 'doc2')
        self.cf.register_option('d.dep', 'bar', 'doc2')
        self.assertEqual(self.cf.get_option('d.a'), 'foo')
        self.assertEqual(self.cf.get_option('d.dep'), 'bar')

        self.cf.deprecate_option('d.dep', rkey='d.a')  # reroute d.dep to d.a
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            self.assertEqual(self.cf.get_option('d.dep'), 'foo')

            self.assertEqual(len(w), 1)  # should have raised one warning
            self.assertTrue('eprecated' in str(w[-1]))  # we get the custom message

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            self.cf.set_option('d.dep', 'baz')  # should overwrite "d.a"

            self.assertEqual(len(w), 1)  # should have raised one warning
            self.assertTrue('eprecated' in str(w[-1]))  # we get the custom message

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            self.assertEqual(self.cf.get_option('d.dep'), 'baz')

            self.assertEqual(len(w), 1)  # should have raised one warning
            self.assertTrue('eprecated' in str(w[-1]))  # we get the custom message

    def test_config_prefix(self):
        with self.cf.config_prefix("base"):
            self.cf.register_option('a',1,"doc1")
            self.cf.register_option('b',2,"doc2")
            self.assertEqual(self.cf.get_option('a'), 1)
            self.assertEqual(self.cf.get_option('b'), 2)

            self.cf.set_option('a',3)
            self.cf.set_option('b',4)
            self.assertEqual(self.cf.get_option('a'), 3)
            self.assertEqual(self.cf.get_option('b'), 4)

        self.assertEqual(self.cf.get_option('base.a'), 3)
        self.assertEqual(self.cf.get_option('base.b'), 4)
        self.assertTrue('doc1' in self.cf.describe_options('base.a',_print_desc=False))
        self.assertTrue('doc2' in self.cf.describe_options('base.b',_print_desc=False))

        self.cf.reset_option('base.a')
        self.cf.reset_option('base.b')

        with self.cf.config_prefix("base"):
            self.assertEqual(self.cf.get_option('a'), 1)
            self.assertEqual(self.cf.get_option('b'), 2)


# fmt.reset_printoptions and fmt.set_printoptions were altered
# to use core.config, test_format exercises those paths.
