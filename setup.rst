Setup
*****

Prerequisites
=============

To participate in the workshop, you will need the following:

  * A laptop with Linux, Mac OS or Windows and at least one free USB port.
  * If it's Windows or Mac OS, make sure to install `drivers`_ for the CH340
    UBS2TTL chip.
  * A micro-USB cable with data lines that fits your USB port.
  * You will need a terminal application installed. For Linux and Mac you can
    use ``screen``, which is installed by default. For Windows we recommend
    `PuTTy`_ or `CoolTerm`_.
  * Please note that the workshop will be in English.

.. _drivers: http://www.wemos.cc/downloads/
.. _PuTTy: http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html
.. _CoolTerm: http://freeware.the-meiers.org/

In addition, at the workshop, you will receive:
  * WeMos D1 Mini development board with ESP8266 on it,
  * WeMos OLED shield,
  * WeMos SHT30 shield,
  * Blue LED,
  * Push button,
  * LDR light sensor (sharing is caring)

The firmware that is flashed on the boards is also available at
https://github.com/MaximusV/d1workshop/raw/master/libs/firmware-combined.bin


Notes on Handling
=================
The board can be disconnected and reconnected at any time, there is no power
off or shut down command you need to issue first. This is typical of
microcontrollers and embedded devices in general, they have to operate in
conditions where power may be unreliable and need to be able to handle sudden
restarts.

**Always disconnect the board from power before adding or removing the shields or
components**. Be careful to align the pins correctly, use the RST pin on top
left for reference. Gently rock the shield back and forth while pulling upwards
to remove it, try not to bend the pins. Sometimes the pins won't fully insert
on some shields or boards so don't try to force it flush.

Note that the pins are exposed on the bottom of the board so don't let that
touch any metal or water as it might short circuit the pins. When plugging in
the components double check you're connecting the right pins, if in doubt ask
somebody to check for you. All that aside, don't worry too much, these devices
are fairly robust and worst case they are cheap replaceable components.
Accidents happen and that's ok!


Development Board
=================

The board we are using is called "WeMos D1 Mini" and has an ESP8266 module
on it, which we will be programming. It comes with the latest version of
MicroPython already setup on it, together with all the drivers we are going
to use.

.. note::
    The D0, D1, D2, ... numbers printed on the board are different from what
    Micropython uses -- because originally those boards were made for a
    different software. Make sure to refer to the image below to determine
    which pins are which.

.. image:: ./images/board.png
    :width: 512px


It has a micro-USB socket for connecting to the computer. On the side is
a button for resetting the board. Along the sides of the board are two rows
of pins, to which we will be connecting cables.

The symbols meaning is as follows:

  * ``3v3`` - this is a fancy way to write 3.3V, which is the voltage that the
    board runs on internally. You can think about this pin like the plus side
    of a battery.
  * ``gnd``, ``G`` - this is the ground. Think about it like the minus side of
    the battery.
  * ``gpioXX`` - "gpio" stands for "general purpose input output". Those are
    the pins we will be using for sending and receiving signals to and from
    various devices that we will connect to them. They can act as output --
    pretty much like a switch that you can connect to plus or to minus with
    your program.  Or they can act as input, telling your program whether they
    are connected to plus or minus.
  * ``a0`` - this is the analog pin. It can measure the voltage that is applied
    to it, but it can only handle up to 3.3V.
  * ``5V`` - this pin is connected with the 5V from your computer. You can
    also use it to power your board with a battery when it's not connected to
    the computer. The voltage applied here will be internally converted to the
    3.3V that the board needs.
  * ``rst`` - this is a reset button (and a corresponding pin, to which you can
    connect external button).

Many of the gpio pins have an additional function, we will cover them separately.


Connecting
==========

The board you got should already have MicroPython with all the needed libraries
flashed on it. In order to access its console, you will need to connect it to
your computer with the micro-USB cable, and access the serial interface that
appears with a terminal program.


Linux and MacOS
---------------

Simply open a terminal and run the following commands. On Linux::

    screen /dev/ttyUSB0 115200

On MacOS::

    screen /dev/tty.SLAB_USBtoUART 115200

To exit screen, press ctrl+A and then capital K.


Windows
-------

For the serial interface to appear in your system, you will need to install the
drivers_ for CH340. Once you have that, you can use either Hyper Terminal,
PuTTy or CoolTerm to connect to it, following this guide_.

The parameters for the connection are: 115200 baud rate, 8 data bits, no
parity, 1 stop bit, no flow control.


Hello world!
------------

Once you are connected, press "enter" and you should see the Micropython
prompt, that looks like this::

    >>>

It's traditional to start with a "Hello world!" program, so type this and press
"enter"::

    print("Hello world!")

If you see "Hello world!" displayed in the next line, then congratulations, you
got it working.

.. _guide: https://techawarey.wordpress.com/tag/serial-port-communication-in-windows-7-using-hyper-terminal-and-putty/


Official Documentation and Support
==================================

The official documentation for this port of Micropython is available at
http://micropython.org/resources/docs/en/latest/esp8266/. There is a also a
forum on which you can ask questions and get help, located at
http://forum.micropython.org/. Finally, there are ``#esp8266`` and
``#micropython`` channels on http://freenode.net IRC network, where people chat
in real time. Remember that all people there are just users like you, but
possibly more experienced, and not employees who get paid to help you.
