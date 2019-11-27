"""
Author: RedFantom
License: GNU GPLv3
Source: The ttkwidgets repository
"""
from unittest import TestCase
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk
from ttkwidgets.hook import hook_ttk_widgets, generate_hook_name, is_hooked


class TestHooks(TestCase):

    def setUp(self):
        self.expected = {None: None}
        self.updated = False
        self.user_hook_called = False
        self.second_updated = False

    def basic_updater(self, widget, option, value):
        self.assertTrue(option in self.expected)
        self.assertEquals(value, self.expected[option])
        self.updated = True

    def second_updater(self, widget, option, value):
        self.second_updated = True

    def has_been_updated(self):
        updated = self.updated
        self.updated = False
        return updated

    def has_been_second_updated(self):
        updated = self.second_updated
        self.second_updated = False
        return updated

    def test_basic_hook(self):
        self.expected = {"tooltip": "Hello World"}
        options = {"tooltip": "Default Value"}
        hook_ttk_widgets(self.basic_updater, options)
        ttk.Button(tooltip="Hello World")
        self.assertTrue(self.has_been_updated())

        self.assertTrue(is_hooked(options))
        self.assertTrue(hasattr(ttk.Button, generate_hook_name(options)))

    def test_user_hook_and_defaults(self):
        self.expected = {"not_user": "Hello World"}
        hook_ttk_widgets(self.basic_updater, self.expected.copy())

        button_init = ttk.Button.__init__

        def __init__(self_widget, *args, **kwargs):
            self.user_hook_called = True
            button_init(self_widget, *args, **kwargs)

        ttk.Button.__init__ = __init__

        ttk.Button()
        self.assertTrue(self.user_hook_called)
        self.assertTrue(is_hooked(self.expected))
        self.assertTrue(self.has_been_updated())

    def test_multi_hooks(self):
        options1 = {"hook1": "Default One"}
        options2 = {"hook2": "Default Two"}
        self.expected = {"hook1": "Custom One"}

        name = hook_ttk_widgets(self.basic_updater, options1)
        hook_ttk_widgets(self.second_updater, options2)
        self.assertEquals(name, generate_hook_name(options1))

        self.assertTrue(is_hooked(options1))
        self.assertTrue(is_hooked(options2))

        ttk.Button(hook1="Custom One")

        self.assertTrue(is_hooked(options1))
        self.assertTrue(is_hooked(options2))

        self.assertTrue(self.has_been_updated())
        self.assertTrue(self.has_been_second_updated())
