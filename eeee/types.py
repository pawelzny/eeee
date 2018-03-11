#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import TypeVar

__author__ = 'Paweł Zadrożny'
__copyright__ = 'Copyright (c) 2018, Pawelzny'
__all__ = ['Event', 'Message', 'Publisher', 'PubSub', 'Subscriber']

Event = TypeVar('Event')
Message = TypeVar('Message')
Publisher = TypeVar('Publisher')
PubSub = TypeVar('PubSub')
Subscriber = TypeVar('Subscriber')
