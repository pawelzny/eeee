#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
from typing import Union

__author__ = 'Paweł Zadrożny'
__copyright__ = 'Copyright (c) 2018, Pawelzny'


class EventLoop:
    def __init__(self, *futures: Union["asyncio.Future", "asyncio.coroutine"]):
        self.loop = asyncio.get_event_loop()
        if len(futures) > 1:
            self.futures = asyncio.gather(*futures, loop=self.loop, return_exceptions=True)
        else:
            self.futures = futures[0]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def run_until_complete(self):
        return self.loop.run_until_complete(self.futures)
