#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Paweł Zadrożny'
__copyright__ = 'Copyright (c) 2018, Pawelzny'


class EeeeException(Exception):
    pass


class EeeeTypeError(EeeeException):
    pass


class NamingError(EeeeTypeError):
    message = 'Argument "name" type mismatch.'

    def __init__(self, message: str = None, types: list = None, wrong: str = None):
        if message is not None:
            self.message = message
        elif types and wrong:
            self.message = f'{self.message} Must be one of type: {types}, got {wrong} instead.'
        super().__init__(self.message)


class HandlerError(EeeeTypeError):
    message = 'Argument "handler" must be function or class with __call__ method.'

    def __init__(self, message: str = None):
        if message is not None:
            self.message = message
        super().__init__(self.message)


class NotCallableError(HandlerError):
    pass


class NotCoroutineError(HandlerError):
    message = 'Argument "handler" must be coroutine.'
