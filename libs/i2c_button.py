import ustruct
from time import sleep

PRODUCT_ID_I2C_BUTTON = 0x01
DEFAULT_I2C_BUTTON_ADDRESS = 0x31

OLED_I2C_ADDRESS_1 = 0x3C
OLED_I2C_ADDRESS_2 = 0x3D

GET_SLAVE_STATUS = 0x01
RESET_SLAVE = 0x02
CHANGE_I2C_ADDRESS = 0x03
GET_KEY_VALUE = 0x04
CHANGE_KEY_A_LONG_PRESS_TIME = 0x05
CHANGE_KEY_B_LONG_PRESS_TIME = 0x06
CHANGE_KEY_A_DOUBLE_PRESS_INTERVAL = 0x07
CHANGE_KEY_B_DOUBLE_PRESS_INTERVAL = 0x08

KEY_VALUE_NONE = 0x00
KEY_VALUE_SHORT_PRESS = 0x01
KEY_VALUE_LONG_PRESS = 0x02
KEY_VALUE_DOUBLE_PRESS = 0x03
KEY_VALUE_HOLD = 0x04

class I2C_BUTTON:

    def __init__(self, i2c, addr=DEFAULT_I2C_BUTTON_ADDRESS):
        self.BUTTON_A = 0
        self.BUTTON_B = 0

        self._address = addr
        self.i2c = i2c

        self.get_data = bytearray(2)
        self.send_data = bytearray(2)

        self.key = ["None", "Press", "Long Press", "Double Press", "Hold"]

    def get(self):
        self.send_data[0] = GET_KEY_VALUE
        result = self.sendData(self.send_data, 1)

        if result == 0:
            self.BUTTON_A = (self.get_data[0] >> 4)
            self.BUTTON_B = (self.get_data[0] & 0x0f);
        else:
            self.BUTTON_A = 0
            self.BUTTON_B = 0

        return result

    def reset(self):
        self.send_data[0] = RESET_SLAVE
        result = self.sendData(self.send_data, 1)
        return result

    def changeAddress(self, address):
        self.send_data[0] = CHANGE_I2C_ADDRESS
        self.send_data[1] = address

        result = self.sendData(self.send_data, 2)
        if result == 0:
            self._address = address
        return result

    def getInfo(self):

        pass

    def sendData(self, data, len):
        if not (self._address == 49):
            return 1
        else:
            t = bytes(data[:len])
            self.i2c.writeto(self._address, t)
            sleep(0.05)
            ## self.i2c.writeto(self._address, bytes(data)
            if data[0] == GET_SLAVE_STATUS:
                self.get_data = ustruct.unpack('<BB', self.i2c.readfrom(self._address, 2))
                ##self.get_data = self.i2c.readfrom(self._address, 2)
            else:
                self.get_data[0] = ustruct.unpack('<B', self.i2c.readfrom(self._address, 1))[0]
                ### ustruct.unpack(">h", self.i2c.readfrom(self._address, 1))[0]
        return 0
        #ustruct.unpack("<")
##
# from i2c_button import I2C_BUTTON
# b = I2C_BUTTON(i)
# b.get()
# >>>
#

  # private:
	# unsigned char _address;
	# unsigned char send_data[2] = {0};
	# unsigned char get_data[2]={0};
	# unsigned char sendData(unsigned char *data, unsigned char len);
