#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
from collections import namedtuple
from typing import Any, Union

__author__ = 'Paweł Zadrożny'
__copyright__ = 'Copyright (c) 2018, Pawelzny'


def subscribe(event: "Event", publisher: "Publisher" = None):
    """Decorator function which subscribe callable to event.

    :example:
        my_event = Event('MyEvent')

        @subscribe(my_event, publisher='incoming_webhook')
        async def incoming_webhook_handler(message, publisher, event):
            # doo something
            pass
    :param event: Event Event object
    :param publisher: str Name of message publisher
    :return: decorator wrapper
    """

    def wrapper(subscriber: callable):
        """Register subscriber to event.

        :param subscriber:
        :return: subscriber
        """
        # noinspection PyProtectedMember
        event._reg_sub(subscriber, publisher)
        return subscriber

    return wrapper


class Event:
    """Async event emitter.

    Register subscribers to this event and publish message asynchronously.

    :example:
        my_event = Event('MyEvent')
        result = await my_event.publish({'message': 'secret'}, 'secret publisher')
    """

    PubSub = namedtuple('PubSub', ['subscriber', 'publisher'])

    def __init__(self, name: str = None):
        if name is None:
            name = self.__class__.__name__
        self.name = name
        self.pub_sub = tuple()
        self.__is_enable = True

    @property
    def is_enable(self):
        return self.__is_enable

    async def publish(self, message: Any, publisher: "Publisher" = None):
        """Propagate message to all interested in subscribers.

        If publisher is not set, then broadcast is meant for all subscribers.
        Any subscriber can listen to all or only to one publisher within event.

        :param message: Any data type.
        :param publisher: Name of publisher which sign a message.
        :return: list or None if event is disabled.
        """
        if self.is_enable:
            result = []
            for ps in self.pub_sub:
                if ps.publisher is None or (publisher is not None and ps.publisher == publisher):
                    result.append(await ps.subscriber(message=message,
                                                      publisher=publisher,
                                                      event=self.name))
            return result
        return None

    def subscribe(self, publisher: "Publisher" = None):
        return subscribe(self, publisher)  # delegate to subscribe decorator

    def enable(self):
        self.__is_enable = True
        return self

    def disable(self):
        self.__is_enable = False
        return self

    def toggle(self):
        self.__is_enable = not self.__is_enable
        return self

    def _reg_sub(self, subscriber: callable, publisher: "Publisher" = None):
        """Append subscriber to list of subscribers.

        :param subscriber: Callable subscriber.
        :param publisher: Optional name of publisher to listen to.
        :return:
        """
        self.pub_sub += (self.PubSub(subscriber=subscriber, publisher=publisher),)


class Publisher:
    def __init__(self, name: str):
        if not type(name) is str:
            raise AttributeError(f'Attribute "name" must be type of String, '
                                 f'{type(name)} was given.')
        self.name = name
        self.__id = f'{self.__class__}:{self.name}'
        self.__id = str(self.__class__).replace("'>", f":{name}'>")

    def __str__(self):
        return str(self.id)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        return str(self.id) == other

    @property
    def id(self):
        return self.__id


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
