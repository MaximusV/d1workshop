from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from sht30 import SHT30

try:
    i = I2C(-1, Pin(5), Pin(4))

    devices = i.scan()
    if not devices:
        print("No I2C devices detected")

    if 60 in devices and 49 in devices:
        s = SSD1306_I2C(64, 48, i)

        s.text("Pycon", 0, 5)
        s.text("Limerick", 0, 20)
        s.text("March 23", 0, 35)
        s.show()
    else:
        print("OLED shield not found")
    if 69 in devices:
        t = SHT30()
        if not t.is_present():
            print("SHT not present")
        else:
            t.measure()
    else:
        print("SHT30 shield not found")
except Exception:
    p = Pin(2, Pin.OUT)
    raise
