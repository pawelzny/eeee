#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Generic

from . import types

__author__ = 'Paweł Zadrożny'
__copyright__ = 'Copyright (c) 2018, Pawelzny'


class Message(Generic[types.Message]):
    def __init__(self, *args, **kwargs):
        self.args = args,
        self.kwargs = kwargs


class Publisher(Generic[types.Publisher]):
    message: types.Message = None

    def __init__(self):
        self.clear()

    def set_payload(self, message: types.Message):
        self.message = message

    def clear(self):
        self.message = None
