#!/usr/bin/env python
# -*- coding: utf-8 -*-
from eeee import Event

__author__ = 'Paweł Zadrożny'
__copyright__ = 'Copyright (c) 2018, Pawelzny'


def test_enable():
    event = Event('test_enable')
    assert event.is_enable is True


def test_disable():
    event = Event('test_disable')
    assert event.is_enable is True
    event.disable()
    assert event.is_enable is False


def test_toggle():
    event = Event('test_toggle')
    assert event.is_enable is True
    event.toggle()
    assert event.is_enable is False
    event.toggle()
    assert event.is_enable is True
