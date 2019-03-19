from machine import I2C, Pin, Timer, disable_irq, enable_irq
from micropython import const, alloc_emergency_exception_buf
from time import sleep

import ssd1306

alloc_emergency_exception_buf(100)

B_WIDTH = const(7)
B_HEIGHT = const(3)
B_STEP = const(2)

BUT_LEFT = 0
BUT_RIGHT = 2

class Block():
    
    def __init__(self, x, y, display, width=B_WIDTH, height=B_HEIGHT):
        self.x = x
        self.y = y
        self.display = display
        self.width = width
        self.height = height

        self.draw()
    
    def draw(self):
        self.display.fill_rect(self.x, self.y, self.width, self.height, 1)
        
    def move_left(self, pin):
        self.x -= B_STEP
    
    def move_right(self, pin):
        self.x += B_STEP

class Ball():
    
    def __init__(self, x, y, display, width=B_WIDTH, height=B_HEIGHT):
        self.x = x
        self.y = y
        self.display = display
        self.width = width
        self.height = height
        self.v_x = 1
        self.v_y = 2
        self.draw()

    def update(self):
        if self.x == 64 or self.x == 0:
            self.v_x *= -1

        if self.y == 48 or self.y == 0:
            self.v_y *= -1
        self.x += self.v_x
        self.y += self.v_y

    def draw(self):
        self.display.fill_rect(self.x, self.y, self.width, self.height, 1)
    
class Breakout():

    def __init__(self):
        self.dirty = 0

        i2c = I2C(sda=Pin(4), scl=Pin(5))
        self.display = ssd1306.SSD1306_I2C(64, 48, i2c)
        self.display.poweron()
        
        self.blocks = [Block((x*9)+2, (y * 5)+2, self.display)
            for x in range(0, 8)
            for y in range(0,3)
            ]
        self.ball = Ball(32, 24, self.display, 2, 2)
        self.paddle = Block(26, 44, self.display)
        self.draw()
        
        self.l_but = Pin(BUT_LEFT, Pin.IN)
        self.r_but = Pin(BUT_RIGHT, Pin.IN)

        self.l_but.irq(trigger=Pin.IRQ_FALLING, handler=self.paddle.move_left)
        self.r_but.irq(trigger=Pin.IRQ_FALLING, handler=self.paddle.move_right)
        
        self.tim = Timer(-1)
        self.tim.init(period=50, mode=Timer.PERIODIC, callback=self.set_dirty)
        
        self.game_loop()

    def set_dirty(self, tim):
        self.dirty = 1
    
    def game_loop(self):
        while True:
            if self.dirty:
                self.ball.update()
                self.draw()
                # critical section
                state = disable_irq()
                self.dirty = 0
                enable_irq(state)

    def draw(self):
        self.display.framebuf.fill(0)
        self.ball.draw()
        self.paddle.draw()
        for block in self.blocks:
            block.draw()
        self.display.show()

    def update(self):
        self.ball.update()
        self.draw()
