#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
from typing import Any, Union

__author__ = 'Paweł Zadrożny'
__copyright__ = 'Copyright (c) 2018, Pawelzny'


def run_until_complete(futures: Union[list, "asyncio.Future", "asyncio.coroutine"]) -> Any:
    loop = asyncio.get_event_loop()

    if type(futures) is list:
        futures = asyncio.gather(*futures, loop=loop, return_exceptions=True)
    return loop.run_until_complete(futures)
