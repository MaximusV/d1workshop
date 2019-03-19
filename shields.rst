Shields
*******

There is a number of ready to use "shields" -- add-on boards -- for the WeMos
D1 Mini, containing useful components together with all the necessary
connections and possible additional components. All you have to do is plug such
a "shield" on top or bottom of the WeMos D1 Mini board, and load the right code
to use the components on it.

.. warning::
    These shields are not provided as part of this workshop but are included
    here for reference.


Button
======

This is a very basic shield that contains a single pushbutton. The button is
connected to pin ``gpio0`` and to ``gnd``, so you can read its state with this
code::

    from machine import Pin
    button = Pin(0)
    if button.value():
        print("The button is not pressed.")
    else:
        print("The button is pressed.")

Of course everything we learned about buttons and debouncing applies here as
well.


DHT and DHT Pro
===============

Those two shield have temperature and humidity sensors on them. The first one,
DHT, has DHT11 sensor, the second one, DHT Pro, has DHT22, which is more
accurate and has better precision.

In both cases the sensors are available on the pin ``gpio2``, and you can
access them with code like this::

    from machine import Pin
    import dht
    sensor = dht.DHT11(Pin(2))
    sensor.measure()
    print(sensor.temperature())
    print(sensor.humidity())

(Use ``DHT22`` class for the DHT Pro shield.)

It is recommended to use this shield with the "dual base", so that the
temperature sensor is not right above or below the ESP8266 module, which tends
to become warm during work and can affect temperature measurements.


Neopixel
========

That shield has a single addressable RGB LED on it, connected to pin ``gpio4``.
Unfortunately, that means that this shield conflicts with any other shield that
uses the I²C protocol, such as the OLED shield or the motor shield. You can use
it with code lik this::

    from machine import Pin
    import neopixel
    pixels = neopixel.NeoPixel(Pin(4, Pin.OUT), 1)
    pixels[0] = (0xff, 0x00, 0x22)
    pixels.write()


Relay
=====

This shield contains a relay switch, together with a transistor and a couple of
other components required to reliably connect it to the board. It uses pin
``gpio5``, which unfortunately makes it incompatible with any other shields
using the I²C protocol, such as the OLED shield or the motor shield. You can
control the relay with the following code::

    from machine import Pin
    relay = Pin(5, Pin.OUT)
    relay.low() # Switch off
    relay.high() # Switch on


Motor
=====

The motor shield contains a H-bridge) and a PWM chip, and it's able to drive up
to two small DC motors. You can control it using I²C on pins ``gpio4`` and
``gpio5``. It will conflict with any shields that use those pins but don't use
I²C, such as the relay shield and the neopixel shield. It will work well
together with other shields using I²C.

Up to four such shields can be connected at the same time, provided they have
different addresses selected using the jumpers at their backs.

In order to use this shield, use the ``d1motor`` library::

    import d1motor
    from machine import I2C, Pin
    i2c = I2C(-1, Pin(5), Pin(4), freq=10000)
    m0 = d1motor.Motor(0, i2c)
    m1 = d1motor.Motor(1, i2c)
    m0.speed(5000)


Micro SD
========

This shield lets you connect a micro SD card to your board. It connects to pins
``gpio12``, ``gpio13``, ``gpio14`` and ``gpio15`` and uses SPI protocol. It can
be used together with other devices using the SPI protocol, as long as they
don't use pin ``gpio15`` as CS.

You can mount an SD card in place of the internal filesystem using the
following code::

    import os
    from machine import SPI, Pin
    import sdcard
    sd = sdcard.SDCard(SPI(1), Pin(15))
    os.umount()
    os.VfsFat(sd, "")

Afterwards you can use ``os.listdir()``, ``open()`` and all other normal file
functions to manipulate the files on the SD card. In order to mount the
internal filesystem back, use the following code::

    import flashbdev
    os.umount()
    os.VfsFat(flashbdev.bdev, "")


Battery
=======

This shield lets you power your board from a single-cell LiPo battery. It
connects to the ``5V`` pin, and doesn't require any communication from your
board to work. You can simply plug it in and use it.


Servo (Custom)
==============

There is an experimental 18-channel servo shield. It uses the I²C protocol on
pins ``gpio4`` and ``gpio5`` and is compatible with other I²C shields.

In order to power the servos, you need to either provide external power to the
pin marked with ``+`` next to the ``5V`` pin, or connect it with the ``5V`` pin
to make the servos share power with the board.

You can set the servo positions using the following code::

    from servo import Servos
    from machine import I2C, Pin
    i2c = I2C(-1, Pin(5), Pin(4))
    servos = Servos(i2c)
    servos.position(0, degrees=45)


TFT Screen (Custom)
===================

There is an experimental breakout board for the ST7735 TFT screen. It uses the
SPI interface on pins ``gpio12``, ``gpio13``, ``gpio14``, and ``gpio15``.

You can use it with the following example code::

    from machine import Pin, SPI
    import st7735

    display = st7735.ST7735(SPI(1), dc=Pin(12), cs=None, rst=Pin(15))
    display.fill(0x7521)
    display.pixel(64, 64, 0)

If you have a display with a red tab, you need to use a different initialization::

    display = st7735.ST7735R(SPI(1, baudrate=40000000), dc=Pin(12), cs=None, rst=Pin(15))
