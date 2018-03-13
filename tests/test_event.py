#!/usr/bin/env python
# -*- coding: utf-8 -*-
from eeee.event import Event, subscribe
from eeee.loop import run_until_complete

__author__ = 'Paweł Zadrożny'
__copyright__ = 'Copyright (c) 2018, Pawelzny'


class TestEvent:
    def test_enable(self):
        event = Event('test_enable')
        assert event.is_enable is True

    def test_disable(self):
        event = Event('test_disable')
        assert event.is_enable is True
        event.disable()
        assert event.is_enable is False

    def test_toggle(self):
        event = Event('test_toggle')
        assert event.is_enable is True
        event.toggle()
        assert event.is_enable is False
        event.toggle()
        assert event.is_enable is True


class TestSubscribe:
    def test_standalone_decorator(self):
        event = Event('sub_standalone')
        assert len(event.pub_sub) == 0

        @subscribe(event)
        async def simple_handler():
            return 'simple_handler'

        assert len(event.pub_sub) == 1
        assert event.pub_sub[0].publisher is None
        assert event.pub_sub[0].subscriber == simple_handler

    def test_decorator_with_set_publisher(self):
        event = Event('sub_to_publisher')
        assert len(event.pub_sub) == 0

        @event.subscribe(publisher='my_choice')
        async def nice_handler():
            return 'nice_handler'

        assert len(event.pub_sub) == 1
        assert event.pub_sub[0].publisher == 'my_choice'
        assert event.pub_sub[0].subscriber == nice_handler

    def test_builtin_decorator(self):
        event = Event('builtin_decorator')
        assert len(event.pub_sub) == 0

        @event.subscribe()
        async def better_handler():
            return 'better_handler'

        assert len(event.pub_sub) == 1
        assert event.pub_sub[0].publisher is None
        assert event.pub_sub[0].subscriber == better_handler


class TestPublish:
    def test_publish_to_all(self):
        event = Event('publish_to_all')

        @event.subscribe()
        async def first_all(message, publisher, event):
            return [message, publisher, event]

        @event.subscribe()
        async def second_all(message, publisher, event):
            return [message, publisher, event]

        result = run_until_complete(event.publish('test message'))
        assert len(result) == 2
        for r in result:
            assert r[0] == 'test message'
            assert r[1] is None
            assert r[2] == 'publish_to_all'

    def test_publish_to_specific(self):
        event = Event('publish_to_secret')

        @event.subscribe(publisher='omit')
        async def first_sp(message, publisher, event):
            return ['omitted', publisher, event]

        @event.subscribe(publisher='secret')
        async def second_sp(message, publisher, event):
            return ['received', publisher, event]

        result = run_until_complete(event.publish('secret message', 'secret'))
        assert len(result) == 1
        result = result.pop()
        assert result[0] == 'received'
        assert result[1] == 'secret'
        assert result[2] == 'publish_to_secret'

    def test_publish_to_all_but_specific(self):
        event = Event('publish_to_all_but_omit')

        @event.subscribe(publisher='omit')
        async def first_sp(message, publisher, event):
            return ['omitted', publisher, event]

        @event.subscribe()
        async def second_sp(message, publisher, event):
            return ['received', publisher, event]

        result = run_until_complete(event.publish('secret message', 'broadcast'))
        assert len(result) == 1
        result = result.pop()
        assert result[0] == 'received'
        assert result[1] == 'broadcast'
        assert result[2] == 'publish_to_all_but_omit'
