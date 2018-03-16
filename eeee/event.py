#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
from collections import namedtuple
from inspect import iscoroutinefunction
from typing import Any, Union

from eeee import exceptions

__author__ = 'Paweł Zadrożny'
__copyright__ = 'Copyright (c) 2018, Pawelzny'


def subscribe(event: "Event", publisher: Union["Publisher", str] = None):
    """Decorator function which subscribe callable to event.

    :Example:
        Create event, and use decorator to subscribe any callable::

            >>> my_event = Event('MyEvent')
            >>> @subscribe(my_event, publisher='incoming webhook')
            ... async def incoming_webhook_handler(message, publisher, event):
            ...    pass # doo something

    :param event: Event Event object
    :type event: eeee.event.Event
    :param publisher: Optional name or instance of Publisher
    :type publisher: eeee.event.Publisher, str
    :return: decorator wrapper
    """
    if publisher is not None:
        publisher = Publisher(publisher)

    def wrapper(subscriber: callable):
        """Register subscriber to event.

        :param subscriber: Callable handler.
        :type subscriber: callable
        :return: subscriber
        """
        subscriber = Subscriber(subscriber)
        # noinspection PyProtectedMember
        event._reg_sub(subscriber, publisher)
        return subscriber

    return wrapper


class Event:
    """Async event emitter.

    Register subscribers to this event and publish message asynchronously.

    :Example:
        Create new Event called 'MyEvent',
        and publish dict as message::

            >>> my_event = Event('MyEvent')
            >>> result = await my_event.publish({'message': 'secret'})

        Result will contain list with values returned by handlers.
    """

    RETURN_EXCEPTIONS = False
    """If set to True will return handler's exception as result instead of raise it."""

    _PubSub = namedtuple('PubSub', ['subscriber', 'publisher'])

    def __init__(self, name: str = None):
        if name is None:
            name = self.__class__.__name__
        self.name = name
        self.pub_sub = tuple()
        self.__is_enable = True

    @property
    def is_enable(self):
        """Check if Event emitter is enabled.

        :return: Boolean
        """
        return self.__is_enable

    async def publish(self, message: Any, publisher: Union["Publisher", str] = None):
        """Propagate message to all interested in subscribers.

        If publisher is not set, then broadcast is meant for all subscribers.
        Any subscriber can listen to all or only to one publisher within event.

        :Example:
            Secret message will be passed to handlers which listen to 'secret publisher'
            or to handlers which set publisher to None (default)::

                >>> my_event = Event('MyEvent')
                >>> result = await my_event.publish({'message': 'secret'},
                ...                                 Publisher('secret publisher'))

            When publisher is set to None, message will be passed only to
            handlers which set publisher to None (default)::

                >>> broadcast = Event('Broadcast')
                >>> result = await broadcast.publish({'message': 'non secret'})

        :param message: Literally anything.
        :type message: Any
        :param publisher: Optional Publisher.
        :type publisher: eeee.event.Publisher
        :return: List of results from subscribed handlers or None if event is disabled.
        """
        if self.is_enable:
            if publisher is not None:
                publisher = Publisher(publisher)
            coros = []
            for ps in self.pub_sub:
                if ps.publisher is None or (publisher is not None and ps.publisher == publisher):
                    coros.append(ps.subscriber(message, publisher, event=self.name))
            if coros:
                return await asyncio.gather(*coros, return_exceptions=self.RETURN_EXCEPTIONS)
        return None

    def subscribe(self, publisher: Union["Publisher", str] = None):
        """Subscribe decorator integrated within Event object.

        :Example:
            Can be used instead of standalone @subscribe decorator::

                >>> my_event = Event('MyEvent')
                >>> @my_event.subscribe(publisher='incoming_webhook')
                ... async def incoming_webhook_handler(message, publisher, event):
                ...     pass # doo something

            Subscribe method must be called to decorate handler.

        :param publisher: Optional publisher instance.
        :type publisher: eeee.event.Publisher, str
        :return: subscribe decorator
        """
        return subscribe(self, publisher)  # delegate to subscribe decorator

    def unsubscribe(self, subscriber: Union["Subscriber", callable],
                    publisher: Union["Publisher", str] = None):
        """Unsubscribe subscribed handler from event.

        If publisher had been set on subscribe, then must be provided as well.

        :Example:
            Unsubscribe existing handler::

                >>> my_event = Event('MyEvent')
                >>> my_event.unsubscribe(event_handler, 'secret publisher')

        :param subscriber: Callable handler.
        :type subscriber: callable
        :param publisher: Optional name or instance of Publisher
        :type publisher: eeee.event.Publisher, str
        """
        subscriber = Subscriber(subscriber)
        if publisher is not None:
            publisher = Publisher(publisher)
        pub_sub = self._PubSub(subscriber=subscriber, publisher=publisher)
        self.pub_sub = tuple(ps for ps in self.pub_sub if ps != pub_sub)

    def enable(self):
        """Enable event.

        Idempotent method which set Event as enabled.

        :return: self
        """
        self.__is_enable = True
        return self

    def disable(self):
        """Disable event.

        Idempotent method which set Event as disabled.

        :return: self
        """
        self.__is_enable = False
        return self

    def toggle(self):
        """Toggle event enable-disable.

        Change state of Event to opposite.

        :return: self
        """
        self.__is_enable = not self.__is_enable
        return self

    def _reg_sub(self, subscriber: Union["Subscriber", callable],
                 publisher: Union["Publisher", str] = None):
        """Append subscriber to list of subscribers.

        :param subscriber: Callable handler.
        :type subscriber: callable
        :param publisher: Optional name or instance of Publisher
        :type publisher: eeee.event.Publisher, str
        """
        self.pub_sub += (self._PubSub(subscriber=subscriber, publisher=publisher),)


class Publisher:
    """Event publisher.

    Publisher is a wrapper which provides unified interface.
    Instead of using plain strings which may be error prone,
    It is recommended to use Publisher instance.

    Two instances of the same name are considered equal but not the same.
    Publisher is not a singleton.

    :Example:
        Create publisher and use multiple times or in case of import clash
        create new instance of the same name::

            >>> broadcaster = Publisher('Broadcaster')
            >>> broadcaster_clone = Publisher('Broadcaster')
            >>> broadcaster == broadcaster_clone
            True

            >>> broadcaster == 'Broadcaster'
            True

            >>> broadcaster is broadcaster_clone
            False

        One instance may be input for new one which creates a copy::

            >>> fancy = Publisher('Fancy')
            >>> fancy_clone = Publisher(fancy)
            >>> fancy is fancy_clone
            False

            >>> fancy.name == fancy_clone.name
            True

    """
    def __init__(self, name: Union["Publisher", str]):
        if isinstance(name, self.__class__):
            name = name.name
        elif type(name) is str:
            name = name
        else:
            raise exceptions.NamingError(types=[self.__class__, str], wrong=str(type(name)))
        self.name = name
        self.__template = str(self.__class__) + '{name}</class>'
        self.__id = self.__template.format(name=self.name)

    def __str__(self):
        return str(self.id)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        if type(other) is str:
            return self.id == self.__template.format(name=other)
        return False

    @property
    def id(self):
        """Publisher identification.

        :return: string ID
        """
        return self.__id


class Subscriber:
    """Event subscriber.

    Subscriber is a wrapper which provides unified interface.
    Instead of using event handlers directly which may be error prone,
    It is recommended to use Subscriber instance.

    Subscriber is not meant to be used outside of Event context.

    Two instances of the same name are considered equal but not the same.
    Subscriber is not a singleton.

    :Example:
        Create subscriber with coroutine::

            >>> async def default_handler(message, publisher, event):
            ...     pass
            ...
            >>> sub = Subscriber(default_handler)
            >>> sub_clone = Subscriber(default_handler)
            >>> sub == 'default_handler'
            True

            >>> sub == sub_clone
            True

            >>> sub is sub_clone
            False

            >>> result = await sub('a message', Publisher('global'), 'mock event')
        """
    def __init__(self, handler: Union["Subscriber", callable]):
        if isinstance(handler, self.__class__):
            self.handler = handler.handler
            self.name = handler.name
        elif callable(handler):
            try:
                self.name = handler.__name__
                self.handler = handler
                is_coro = iscoroutinefunction(handler)
            except AttributeError:
                # assume instance of callable class
                self.name = handler.__class__.__name__
                self.handler = handler
                is_coro = iscoroutinefunction(handler.__call__)

            if not is_coro:
                raise exceptions.NotCoroutineError
        else:
            raise exceptions.NotCallableError

        self.__template = str(self.__class__) + '{name}</class>'
        self.__id = self.__template.format(name=self.name)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        if type(other) is str:
            return self.id == self.__template.format(name=other)
        return False

    async def __call__(self, *args, **kwargs):
        return await self.handler(*args, **kwargs)

    @property
    def id(self):
        """Subscriber identification.

        :return: string ID
        """
        return self.__id
