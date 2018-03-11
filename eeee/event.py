#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum
from typing import Generic, Union

from . import types

__author__ = 'Paweł Zadrożny'
__copyright__ = 'Copyright (c) 2018, Pawelzny'


class PubSub(Generic[types.PubSub]):
    def __init__(self, publisher: Union[types.Publisher, None],
                 subscriber: types.Subscriber, is_pause=False):
        self.publisher = publisher
        self.subscriber = subscriber
        self.is_pause = is_pause

    def pause(self):
        self.is_pause = True

    def resume(self):
        self.is_pause = False


class Event(Generic[types.Event]):
    # noinspection PyArgumentList
    Toggle = Enum('Toggle', (('PAUSE', 'pause'), ('RESUME', 'resume')), module=__name__)

    def __init__(self):
        self.pub_sub = tuple()
        self.__enable = True

    async def publish(self, publisher: types.Publisher):
        if self.__enable:
            for ps in self.pub_sub:
                if (not ps.is_pause) and (ps.publisher is None or ps.publisher == publisher):
                    await ps.subscriber.receive(publisher.message)

    def subscribe(self, publisher: Union[types.Publisher, None], subscriber: types.Subscriber):
        self.pub_sub += (PubSub(publisher, subscriber),)

    def enable(self):
        self.__enable = True
        return self

    def disable(self):
        self.__enable = False
        return self

    def _toggle(self, method: 'Toggle', *publisher: types.Publisher):
        for pub in (p for p in publisher if p is not None):
            for ps in (pub_sub for pub_sub in self.pub_sub if pub_sub.publisher is not None):
                if ps.publisher == pub:
                    getattr(ps.publisher, method.value)()

    def pause(self, *publisher: types.Publisher):
        self._toggle(self.Toggle.PAUSE, *publisher)

    def resume(self, *publisher: types.Publisher):
        self._toggle(self.Toggle.RESUME, *publisher)
