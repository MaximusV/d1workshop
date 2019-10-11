Misc
====

This is just a dumping ground of old material that may still be useful and
I wanted to keep just in case.



Mac
---

MacOS should have the device driver installed as well but we have seen varying
levels of success at previous workshop sessions. Normally connecting with 'screen'
should look similar to the Linux example but the device name will vary depending
on the driver::

    screen /dev/tty.SLAB_USBtoUART 115200

To check if the device is being detected and the driver is working, do `ls /dev/tty*`
to list tty devices on the filesystem with the device disconnected first. Reconnect
the board and do the ```ls /dev/tty*`` again to spot the difference.

This website has some good general troubleshooting instructions for mac serial drivers,
just ignore any bits specific to their paid drivers https://www.mac-usb-serial.com/docs/support/troubleshooting.html.
If the default driver doesn't work, then try to follow the instructions here to
uninstall that and install a new one: https://github.com/MPParsley/ch340g-ch34g-ch34x-mac-os-x-driver

Once the driver is working and you connect with a terminal emulator like screen,
you should get a blank screen and if you hit enter a few times, you should see
the usual python REPL prompt '>>>'. You might see some gibberish characters or
get a SyntaxError when you first connect, that is just the initial serial
connection. To exit screen just disconnect the cable.
Skip to the :ref:`hello-world` section.
