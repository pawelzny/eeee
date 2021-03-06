==========
Public API
==========

.. contents:: :local:


*****************
Publish/Subscribe
*****************


Event
=====

.. py:module:: eeee.event
.. autoclass:: Event
   :member-order: bysource
   :members:


Publisher
=========

.. py:module:: eeee.event
.. autoclass:: Publisher
   :member-order: bysource
   :members:


Subscriber
==========

.. py:module:: eeee.event
.. autoclass:: Subscriber
   :member-order: bysource
   :members:


**********
Exceptions
**********

.. py:module:: eeee.exceptions
.. autoexception:: EeeeException
   :members:

.. autoexception:: EeeeTypeError
   :members:

.. autoexception:: NamingError
   :members:

.. autoexception:: HandlerError
   :members:

.. autoexception:: NotCallableError
   :members:

.. autoexception:: NotCoroutineError
   :members:

.. inheritance-diagram:: eeee.exceptions


*********
Utilities
*********


Subscribe decorator
===================

.. py:module:: eeee.event
.. autofunction:: subscribe


Asyncio context manager
=======================

.. _`Context Loop`: http://context-loop.readthedocs.com/

Provided by `Context Loop`_ can be imported from `eeee` as well.
Context loop allow to execute asynchronous code ad-hoc.

.. code-block:: python

   import eeee import Loop

   >>> my_event = Event('MyEvent')
   >>> with Loop(my_event.publish({'message': 'secret'})) as loop:
   ...   result = loop.run_until_complete()
   ...


