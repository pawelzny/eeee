#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from eeee import Event

__author__ = 'Paweł Zadrożny'
__copyright__ = 'Copyright (c) 2018, Pawelzny'


class TestEvent(unittest.TestCase):
    def test_enable_by_default(self):
        event = Event('Enable by default')
        self.assertTrue(event.is_enable)

    def test_enable(self):
        event = Event('Enable manually')
        event._Event__is_enable = False  # force override __is_enable property
        self.assertFalse(event.is_enable)

        event.enable()
        self.assertTrue(event.is_enable)

    def test_disable(self):
        event = Event('Disable manually')
        self.assertTrue(event.is_enable)

        event.disable()
        self.assertFalse(event.is_enable)

    def test_toggle(self):
        event = Event('Toggle event')
        self.assertTrue(event.is_enable)

        event.toggle()
        self.assertFalse(event.is_enable)

        event.toggle()
        self.assertTrue(event.is_enable)

    def test_new_event_without_name(self):
        event = Event()
        self.assertEqual(event.name, 'Event')
