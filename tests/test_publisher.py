#!/usr/bin/env python
# -*- coding: utf-8 -*-
from eeee.event import Publisher

__author__ = 'Paweł Zadrożny'
__copyright__ = 'Copyright (c) 2018, Pawelzny'


def test_publisher_identification():
    pub = Publisher('some name')
    assert pub.id == "<class 'eeee.event.Publisher'>some name</class>"


def test_publisher_comparison_difference():
    assert Publisher('first') != Publisher('second')
    assert Publisher('first') != 'second'
    assert Publisher('first') is not Publisher('first')


def test_publisher_comparison_the_same():
    assert Publisher('one another') == Publisher('one another')
    assert Publisher('one another') == 'one another'
