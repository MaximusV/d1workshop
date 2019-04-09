Advanced
********

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

Among the most popular protocols are UART, I²C and SPI. We are going to have
examples of each of them, but we are not going to get into details of how they
work internally. It's enough to know that they let you send bytes to the
device, and receive bytes in response.

Temperature and Humidity
========================

The SHT30 sensor shield provides an accurate temperature and humidity sensor
which communicates over the I2C protocol, the same as the OLED shield. This
only needs two pins aside from ground and power; a clock pin (SCL) and a data
pin (SDA). Multiple devices can use the same pins by having a different address
on the bus (more on this later). A library for controlling the SHT30 has been
built into the firmware already::

    from sht30 import SHT30
    sensor = SHT30()
    temperature, humidity = sensor.measure()

Note that another cheaper and less accurate sensor is often used for this
purpose as well, the DHT11/12. These are described in the 'extra' section for
reference.

OLED
====

A small, 64×48 monochrome display. It uses pins ``gpio4`` and ``gpio5`` to talk
with the board with the I²C protocol. It will conflict with any other shield
that uses those pins, but doesn't use I²C, like the neopixel shield or the
relay shield. It can coexist with other shields that use I²C, like the motor
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
    display.show()



Network
=======

The ESP8266 has wireless networking support. It can act as a WiFi access point
to which you can connect, and it can also connect to the Internet.

To configure it as an access point, run code like this (use your own name and password)::

    import network
    # AP_IF stands for Access Point Interface
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid="network-name", authmode=network.AUTH_WPA_WPA2_PSK, password="abcdabcdabcd")

To scan for available networks (and also get additional information about their
signal strength and details), use::

    import network
    # STA_IF stands for Standard Interface
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    print(sta.scan())

To connect to an existing network, use::

    import network
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    # Don't call this with a non-existent network
    # sta.connect("micropi", "pyconlimerick")

Once the board connects to a network, it will remember it and reconnect after
every restart. To get details about connection, use::

    sta.ifconfig()
    sta.status()
    sta.isconnected()

.. note::
    If you accidentally input a bad WiFi ssid or password, the device will get
    stuck trying to connect to it and will spam network debug output to the
    terminal. You can still actually type code despite this so you just need to
    disable the interface by copying and pasting the following code::

        import network
        sta = network.WLAN(network.STA_IF)
        sta.active(False)

HTTP Requests
=============

Once you are connected to a network, you can talk to servers and interact with
web services. The easiest example is to do a HTTP request to a simple webserver.
After the last section, you should be connected to a network, probably the 'micropi'
network hosted for the wokshop. Make sure the AP network is disabled now because
it will conflict with the 'micropi' network::

    import network
    ap = network.WLAN(network.AP_IF)
    ap.active(False)

Let's define a convenient function for making a HTTP request. This function is
intentionally quite low level, there are of course libraries that provide a
more simple inteface but this nicely demonstrates what a HTTP request is. When
you open a website in your browser, the same sequence of calls in made within
the browser engine.::

    def http_req(host, path, verb="GET", json_data=""):
        # this call resolves the DNS name into an IP address
        addr = socket.getaddrinfo(host, 80)[0][-1]
        # this instantiates a socket to use.
        s = socket.socket()
        s.connect(addr)

        if verb == "GET":
            req = '{} /{} HTTP/1.0\r\nHost: {}\r\n\r\n'
            # send the formatted HTTP 1.0 request
            s.send(bytes(req.format(verb, path, host), 'utf8'))
        else:
            req = '{} /{} HTTP/1.0\r\nHost: {}\r\nContent-Type:application/json\r\n{}\r\n'
            s.send(bytes(req.format(verb, path, host, json_data), 'utf8'))

        # read the response data from the socket and print it out.
        while True:
            data = s.recv(100)
            if data:
                print(str(data, 'utf8'), end='')
            else:
                break
        s.close()

Now to make a request::

    # This is the IP address of the Raspberry Pi server. If you're using another
    # network, try putting a website address like 'www.harsh-enough.com' instead.
    http_req("192.168.4.1", "")

    # the webserver also exposes an endpoint to GET a user's score.
    http_req("192.168.4.1", "user/test")

    # if we try to get a user that doesn't exists, we get a 404 HTTP error:
    http_req("192.168.4.1", "user/coolboi360")

    # we can use the POST verb to create or update a user
    import json
    data = json.dumps({"score": 10})
    # come up with a username to create and put it in the path
    name = "example"
    http_req("192.168.4.1", "user/" + name, "POST", data)

    # now let's get that user data to check that it was created
    http_req("192.168.4.1", "user/" + name)

It's also possible to make more advanced requests, adding special headers to
them etc. However, keep in mind that our board has very little memory for
storing the answer, and you can easily get a ``MemoryError``.


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

In order to connect to your board, you have to know its address. If the board
works in access point mode, it uses the default address. If it's connected to
WiFi, you can check it with this code::

    import network
    sta = network.WLAN(network.STA_IF)
    print(sta.ifconfig())

You will see something like ``XXX.XXX.XXX.XXX`` -- that's the IP address. Enter
it in the WebREPL's address box at the top like this
``ws://XXX.XXX.XXX.XXX:8266/``.

To connect to your board, you first have to setup the webrepl. You do this
by running the following code and following the instructions. Please use 'pycon'
as the password for consistency ::

    import webrepl_setup

You might have to physically reconnect the board to get the webREPL running.
Now you can go back to the browser and click "connect".

Filesystem
==========

Writing in the console is all fine for experimenting, but when you actually
build something, you want the code to stay on the board, so that you don't have
to connect to it and type the code every time. For that purpose, there is a
file storage on your board, where you can put your code and store data.

You can see the list of files in that storage with this code::

    import os
    print(os.listdir())

You should see something like ``['boot.py']`` -- that's a list with just one
file name in it. ``boot.py`` and later ``main.py`` are two special files that
are executed when the board starts. ``boot.py`` is for configuration, and you
can put your own code in ``main.py``.

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

You can use the WebREPL to upload files to the board from your computer. To do
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
