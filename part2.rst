Part 2
******

Communication Protocols
=======================

So far all devices we connected to the board were relatively simple and only
required a single pin. More sophisticated devices are controlled with multiple
pins, and often have very elaborate ways in which you have to change the pins
to make them do something, like sending a character to them, or retrieving a
value. Those ways are often standardized, and already implemented for you, so
that you don't have to care about all the gory details -- you just call
high-level commands, and the libraries and/or hardware in your board handles it
all for you.

Among the most popular protocols are UART, I²C and SPI. We are going to look
at examples of I²C in particular, but we are not going to get into details of how it
work internally. It's enough to know that they let you send bytes to the
device, and receive bytes in response.

Temperature and Humidity
========================

The SHT30 sensor shield provides an accurate temperature and humidity sensor
which communicates over the I²C protocol, the same as the OLED shield. This
only needs two pins aside from ground and power; a clock pin (SCL) and a data
pin (SDA). Multiple devices can use the same pins by having a different address
on the bus (more on this later). A library for controlling the SHT30 has been
built into the firmware already::

    from sht30 import SHT30
    sensor = SHT30()
    temperature, humidity = sensor.measure()

Note that another cheaper and less accurate sensor is often used for this
purpose as well, the DHT11/22. These are described in the 'extra' section for
reference.

OLED
====

A small, 64×48 monochrome display. It uses pins ``gpio4`` and ``gpio5`` to talk
with the board with the I²C protocol. It will conflict with any other shield
that uses those pins, but doesn't use I²C, like the neopixel shield or the
relay shield. It can coexist with other shields that use I²C, like the SHT30
shield.

Up to two such displays can be connected at the same time, provided they have
different addresses set using the jumper on the back.

You can control the display using the ``ssd1306`` library::

    import ssd1306
    from machine import I2C, Pin
    i2c = I2C(-1, Pin(5), Pin(4))
    display = ssd1306.SSD1306_I2C(64, 48, i2c)

    display.fill(0)
    display.text("Hello", 0, 0)
    display.text("world!", 0, 8)
    display.pixel(20, 20, 1)
    # You have to call show to actually display your changes.
    display.show()

The display driver "implements" the `Framebuffer interface <https://docs.micropython.org/en/latest/library/framebuf.html#class-framebuffer>`_
so you can use the methods documented on the linked page. Framebuf provides a
common interface for display drivers so that you can use the same drawing code
with multiple different hardware screens. This is a common concept used in programming.

Network
=======

The ESP8266 has wireless networking support. It can act as a WiFi access point
to which you can connect, and it can also connect to the Internet.

First let's try set it up with the standard interface and connect to an existing
network. We'll try the Access Point in the WebREPL section later. To scan for
available networks (and also get additional information about their signal
strength and details), use::

    import network
    # STA_IF stands for Standard Interface
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    print(sta.scan())

To connect to an existing network, use::

    import network
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    sta.connect("micropi", "pyladies")

Once the board connects to a network, it will remember it and reconnect after
every restart. To get details about connection, use::

    sta.ifconfig()
    sta.status()
    sta.isconnected()


HTTP Requests
=============

Once you are connected to a network, you can talk to servers and interact with
web services. The easiest example is to do a HTTP request to a simple webserver.
After the last section, you should be connected to a network, probably the 'micropi'
network hosted for the workshop. Make sure the AP network is disabled now because
it will conflict with the 'micropi' network::

    import network
    ap = network.WLAN(network.AP_IF)
    ap.active(False)

urequests Library
-----------------

You might be familiar with the popular `requests` python library for making HTTP
requests, it defines a much simpler interface than the builtin standard libraries
for HTTP and is pretty much the de facto standard. There is a micropython version
that implements the basic interface which is very nice for simple requests. This
is included in the build on the board so let's try that::

    # we can use this import alias so that the code
    # could be portable with standard python
    import urequests as requests

    # This is the IP address of the Pi serving the 'micropi' network
    resp = requests.get("http://192.168.4.1")
    resp.status_code
    resp.text

`HTTP status-codes <https://www.w3schools.com/tags/ref_httpmessages.asp>`_ tell the client whether the request was successful or some
kind of error was encountered. As you've just seen, 200 means success. Read more
about error codes from the link provided. The server provides a ``/user`` endpoint
for creating, updating or viewing a score value for a user. If we try to query a user that
doesn't exist, we should get a 404::

    import urequests as requests
    resp = requests.get("http://192.168.4.1/user/abcd")
    resp.status_code

`HTTP verbs <https://www.w3schools.com/tags/ref_httpmethods.asp>`_ like 'GET', 'POST', 'DELETE' are used to distinguish between requests
that are purely informational e.g GET and requests that expect the server to make
a change like saving some form data e.g POST. By convention, a GET request is
expected to be 'safe' in that it won't change or delete data. Let's try PUT
some data to the example server to create a score entry for a user::

    import urequests as requests
    import json

    data = json.dumps({"score": 10})
    # come up with a username yourself to create and put it in the path
    name = ""
    resp = requests.put("http://192.168.4.1/user/" + name, data=data)
    resp.status_code
    resp.text
    # What happens if you make the same request again?

Now let's say our user got a new high score and we want to update their entry. We
should use the POST method for this, as the PUT method doesn't allow us to change
existing users::

    import urequests as requests
    import json

    data = json.dumps({"score": 25})
    name = "" # same as your username from the last example.
    resp = requests.post("http://192.168.4.1/user/" + name, data=data)
    resp.status_code
    resp.text

Now you should have an idea of how HTTP web applications work and see how online
game services could be implemented! The `server code <https://github.com/MaximusV/d1workshop/blob/master/libs/server.py>`_
might be interesting to read through but it is just a quick example and may not
make a lot of sense.

WebREPL
=======

The command console in which you are typing all the code is called "REPL" --
an acronym of "read-evaluate-print-loop". It works over a serial connection
over USB. However, once you have your board connected to network, you can
use the command console in your browser, over network. That is called WebREPL.

First, you will need to download the web page for the WebREPL to your computer.
Get the file from https://github.com/micropython/webrepl/archive/master.zip and
unpack it somewhere on your computer, then click on the ``webrepl.html`` file
to open it in the browser.

.. note::

    We should make sure to disable the other interface, since it is configured
    with a similar IP and may cause weird conflicts with the AP network::

        import network
        sta = network.WLAN(network.STA_IF)
        sta.active(False)

In order to connect to your board, you have to know its address. If the board
works in access point mode, it uses the default address. To configure it as an
access point, run code like this (use your own name and password)::

    import network
    # AP_IF stands for Access Point Interface
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid="network-name", authmode=network.AUTH_WPA_WPA2_PSK, password="abcdabcdabcd")
    print(ap.ifconfig())

For either interface you can check the connection details with the ``ifconfig()``
function. You will see a number like ``XXX.XXX.XXX.XXX`` -- that's the IP address
(probably 192.168.4.1 which is a standard address for Access Point networks).
Enter this in the WebREPL's address box at the top like this
``ws://XXX.XXX.XXX.XXX:8266/``.

To connect to your board, you first have to setup the webrepl. You do this
by running the following code and following the instructions. Please use 'pyladies'
as the password for consistency ::

    import webrepl_setup

You have to turn off and on the board to get the webREPL running after first setup
despite what it says about rebooting itself. Now you can go back to the browser
and click "connect".

Filesystem
==========

Writing in the console is all fine for experimenting, but when you actually
build something, you want the code to stay on the board, so that you don't have
to connect to it and type the code every time. For that purpose, there is a
file storage on your board, where you can put your code and store data.

You can see the list of files in that storage with this code::

    import os
    print(os.listdir())

You should see something like ``[]`` or ``['example.py']`` -- that's a list with
just one file name in it, the example we created in the Setup section.
Note that ``boot.py`` and later ``main.py`` are two special filenames that
are executed automatically when the board starts. ``boot.py`` is for configuration,
and you can put your own app code in ``main.py``.

You can create, write to and read from files like you would with normal Python::

    with open("myfile.txt", "w") as f:
        f.write("Hello world!")
    print(os.listdir())
    with open("myfile.txt", "r") as f:
        print(f.read())

Please note that since the board doesn't have much memory, you can't put large
files on it.


Uploading Files
===============

You can use the WebREPL to upload files to the board from your computer. Either
with the web interface or else with the Command Line tool provided. To do
that, you need to open a terminal in the directory where you unpacked the
WebREPL files, and run the command:

.. code-block:: bash

    python webrepl_cli.py yourfile.xxx XXX.XXX.XXX.XXX:

Where ``yourfile.xxx`` is the file you want to send, and ``XXX.XXX.XXX.XXX`` is
the address of your board.

.. note::
    You have to have Python installed on your computer for this to work.

This requires you to setup a network connection on your board first. However,
you can also upload files to your board using the same serial connection that
you use for the interactive console. You just need to install a small utility
program::

    pip install adafruit-ampy

And then you can use it to copy files to your board::

    ampy --port=/dev/ttyUSB0 put yourfile.xxx

.. warning::
    The serial connection can be only used by a single program at a time.
    Make sure that your console is discobbected while you use ampy, otherwise
    you may get a cryptic error about it not having the access rights.


OLED Shield Buttons
===================
The OLED shield has two buttons at the bottom which we can use to interact with
the screen to create menus etc. These buttons are controlled over I2C (for
version 2.1.0 of the shield, version 2.0.0 just has simple pins) which means
the shield only needs 2 pins to control both. However, this means that you need
a driver to interact with the buttons.

Let's upload the driver as a file through the WebREPL. Copy the contents of the
file from https://github.com/MaximusV/d1workshop/raw/master/libs/i2c_button.py
into a file locally and save it. Upload the file through the WebREPL as described
earlier. Then you should be able to use the driver like so::

    from time import sleep
    from machine import Pin, I2C
    from i2c_button import I2C_BUTTON

    i2c = I2C(-1, Pin(5), Pin(4))
    buttons = I2C_BUTTON(i2c)
    buttons.get()

    while True:
        sleep(0.5)
        buttons.get()
        print("A:" + buttons.key[buttons.BUTTON_A])
        print("B:" + buttons.key[buttons.BUTTON_B])


That's all, folks!
==================

You've reached the end of the content of the workshop for now! If there is time
left then just play around with things, set yourself a task for example:

Can you get the screen to display the temperature and humidity, updating every
30 seconds?
