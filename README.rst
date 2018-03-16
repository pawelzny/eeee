****************************
Extremely Easy Event Emitter
****************************

:Info: Extremely Easy Event Emitter.
:Author: Paweł Zadrożny @pawelzny <pawel.zny@gmail.com>


Features
========

* Asynchronous Event emitter based on asyncio
* Subscribe any callable handler
* Filter events by Publisher
* Easy enable-disable events on runtime
* Subscribe handlers using decorator


Installation
============

.. code:: bash

    pip install eeee


**Package**: https://pypi.org/project/eeee/


Quick Example
=============

.. code:: python

    from eeee import Event, Publisher

    my_event = Event('MyEvent')

    # Subscribe takes publisher instance or name as optional argument.
    # If publisher is defined handler will be triggered only when that
    # particular publisher send a message.
    # Leave empty to listen to all publishers within this event.
    @my_event.subscribe()
    async def custom_handler(message, publisher, event):
        print(message, publisher, event)

    result = await my_event.publish('New message arrived!', Publisher('global'))
