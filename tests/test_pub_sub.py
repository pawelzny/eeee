#!/usr/bin/env python
# -*- coding: utf-8 -*-
from eeee import Event, subscribe
from eeee.event import EventLoop, Publisher

__author__ = 'Paweł Zadrożny'
__copyright__ = 'Copyright (c) 2018, Pawelzny'


def test_standalone_decorator():
    event = Event('sub_standalone')
    assert len(event.pub_sub) == 0

    @subscribe(event)
    async def simple_handler():
        return 'simple_handler'

    assert len(event.pub_sub) == 1
    assert event.pub_sub[0].publisher is None
    assert event.pub_sub[0].subscriber == simple_handler


def test_decorator_with_set_publisher():
    event = Event('sub_to_publisher')
    assert len(event.pub_sub) == 0

    @event.subscribe(publisher='my_choice')
    async def nice_handler():
        return 'nice_handler'

    assert len(event.pub_sub) == 1
    assert event.pub_sub[0].publisher == 'my_choice'
    assert event.pub_sub[0].subscriber == nice_handler


def test_builtin_decorator():
    event = Event('builtin_decorator')
    assert len(event.pub_sub) == 0

    @event.subscribe()
    async def better_handler():
        return 'better_handler'

    assert len(event.pub_sub) == 1
    assert event.pub_sub[0].publisher is None
    assert event.pub_sub[0].subscriber == better_handler


def test_publish_to_all():
    event = Event('publish_to_all')

    # noinspection PyShadowingNames,PyUnusedLocal
    @event.subscribe()
    async def first_all(message, publisher, event):
        return [message, publisher, event]

    # noinspection PyShadowingNames,PyUnusedLocal
    @event.subscribe()
    async def second_all(message, publisher, event):
        return [message, publisher, event]

    with EventLoop(event.publish('test message')) as loop:
        result = loop.run_until_complete()

    assert len(result) == 2
    for r in result:
        assert r[0] == 'test message'
        assert r[1] is None
        assert r[2] == 'publish_to_all'


def test_publish_to_specific():
    event = Event('publish_to_secret')

    # noinspection PyShadowingNames,PyUnusedLocal
    @event.subscribe(publisher='omit')
    async def first_sp(message, publisher, event):
        return ['omitted', publisher, event]

    # noinspection PyShadowingNames,PyUnusedLocal
    @event.subscribe(publisher='secret')
    async def second_sp(message, publisher, event):
        return ['received', publisher, event]

    with EventLoop(event.publish('secret message', Publisher('secret'))) as loop:
        result = loop.run_until_complete()

    assert len(result) == 1
    result = result.pop()
    assert result[0] == 'received'
    assert result[1] == Publisher('secret')
    assert result[2] == 'publish_to_secret'


def test_publish_to_all_but_specific():
    event = Event('publish_to_all_but_omit')

    # noinspection PyShadowingNames,PyUnusedLocal
    @event.subscribe(publisher=Publisher('omit'))
    async def first_sp(message, publisher, event):
        return ['omitted', publisher, event]

    # noinspection PyShadowingNames,PyUnusedLocal
    @event.subscribe()
    async def second_sp(message, publisher, event):
        return ['received', publisher, event]

    with EventLoop(event.publish('secret message', Publisher('broadcast'))) as loop:
        result = loop.run_until_complete()

    assert len(result) == 1
    result = result.pop()
    assert result[0] == 'received'
    assert result[1] == Publisher('broadcast')
    assert result[2] == 'publish_to_all_but_omit'


def test_unsubscribe():
    event = Event('unsubscribe_me')

    # noinspection PyShadowingNames,PyUnusedLocal
    @event.subscribe()
    async def i_will_do_it(message, publisher, event):
        return ['received', publisher, event]

    assert len(event.pub_sub) == 1

    event.unsubscribe(i_will_do_it)
    assert len(event.pub_sub) == 0
