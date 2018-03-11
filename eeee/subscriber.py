#!/usr/bin/env python
# -*- coding: utf-8 -*-
import abc
from typing import Generic

from . import types

__author__ = 'Paweł Zadrożny'
__copyright__ = 'Copyright (c) 2018, Pawelzny'


class Subscriber(Generic[types.Subscriber]):
    async def __call__(self, message):
        await self.receive(message)

    @abc.abstractmethod
    async def receive(self, message):
        raise NotImplemented
