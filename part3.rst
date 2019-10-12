Part 3
******

Game Programming
================

In this section we're going to look at some basic games programming concepts,
using the OLED shield and its buttons to implement a basic game. You should have
setup the WebREPL in part2 as we will need to be able to upload our game file
multiple times throughout this example.

Getting Started
===============

On your laptop, open a text editor and start a new file, named 'game.py' or
similar (you'll just have to import your specific name in the examples later).
Copy the code examples into this file in your editor and save it. When you want
to test your code, you'll have to upload this file to your device using the WebREPL
or ampy and then import the class and instantiate it. Note you'll need to soft
reset MicroPython with `Ctrl+d` for every subsequent upload. Why do you think
this is? Hint: we discussed the reason back in Modules section in Python Basics.


Game Structure
==============

First we'll have to import the libraries we need and setup some basic framework
for the game, constants and so on::

    from time import sleep
    from machine import I2C, Pin, Timer, disable_irq, enable_irq
    from micropython import const, alloc_emergency_exception_buf

    import ssd1306
    from i2c_button import I2C_BUTTON

    alloc_emergency_exception_buf(100)

    B_WIDTH = const(7)
    B_HEIGHT = const(3)
    B_STEP = const(2)

    BUT_LEFT = 0
    BUT_RIGHT = 2

    UPDATE_PERIOD = 50

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

        class Game():

            def __init__(self):
                self.dirty = 0

                i2c = I2C(sda=Pin(4), scl=Pin(5))
                self.display = ssd1306.SSD1306_I2C(64, 48, i2c)
                self.display.poweron()

                self.buttons = I2C_BUTTON(i2c)

                self.blocks = [Block((x*9)+2, (y * 5)+2, self.display)
                    for x in range(0, 8)
                    for y in range(0, 3)
                    ]
                self.draw()

                self.tim = Timer(-1)
                self.tim.init(period=UPDATE_PERIOD, mode=Timer.PERIODIC,
                              callback=self.set_dirty)

                self.game_loop()

            def game_loop(self):
                  while True:
                      if self.dirty:
                          self.update()
                          self.draw()
                          # critical section
                          state = disable_irq()
                          self.dirty = 0
                          enable_irq(state)

            def draw(self):
                self.display.fill(0)

                for block in self.blocks:
                    block.draw()
                self.display.show()

            def update(self):
                pass

Ok, that's a lot of code! Take some time to read through it and understand as
much as you can. Don't worry if some of it doesn't make sense now, there are some
MicroPython interrupt specific and so on that may not make sense.

The Block class defines a basic rectangle component that we can use for various
bits of the game. It basically just contains some coordinates and a reference to
a display where it can 'draw' itself.

The Game class is responsible for containing all of the game components and logic.
The __init__ instantiates the display and buttons and does an initial draw. A
classic game structure is to have an update function that handles updating the
game state and a draw function that renders the interface for the player. These
get called in a loop, often at the rate of the maximum refresh that the display
device can handle (the frame rate e.g 60 Frames Per Second (FPS)). It is also
possible to update the game logic more often than it is drawn if  necessary.

In this example, the game uses a Timer to control the update rate, mostly for
the sake of demonstrating the use of interrupts (and because that is how I wrote
it at the time to be honest). You'll notice the game loop is an infinite while
loop which is often how game loops are implemented. You could not bother with a
timer and just update/draw as fast as the main loop can run but I wanted to control
the framerate more specifically. The update function should generally be called
before the draw function for good practise, can you guess why this might be?

The timer just sets a dirty flag which the next game loop iteration will detect
and run update/draw before resetting the flag in a 'critical section'. This just
means that we disable the interrupt while we make this change so that the Timer
doesn't fire and try to access/update the flag at the same time.

Let's test the code, upload the file to your board with the WebREPL and run::

    from game import Game
    g = Game()

You should see the blocks appear on the screen. Nothing else is happening though
which is a bit boring. Let's add a ball!

The Ball
========

Let's add a Ball class. You'll notice it is very similar to the Block class and
could be a good place to use inheritance (if your familiar with OO concepts, if
not don't worry about it). Inheritance behaviour was a little broken in
MicroPython when I wrote the game so for now let's just duplicate code :( ::

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

            self.y += self.v_y

        def draw(self):
            self.display.fill_rect(self.x, self.y, self.width, self.height, 1)

In the init of the Game class we need to instantiate the Ball now like so::

    self.ball = Ball(32, 24, self.display, 2, 2)

In the previously empty update function replace the 'pass' with a call to update
the ball::

    self.ball.update()

The ball's update function updates the ball's x,y coordinates by v_x and v_y every
update. The 'v' stands for velocity here. It also enforces the screen bounds so
the ball doesn't wrap around through the screen edges, instead it reverses the
appropriate velocity value to give the impression of bouncing.

Now let's test again, uploading the new version of the game file and instantiating
the Game class in the REPL. You should see a ball boucing around now. Uh oh, looks
like there is a bug (well there are several actually), the ball is only bouncing up and down.
Can you see what is missing from the ball's update function to make the ball move
in the X-axis? How would you increase the ball's speed if you had to?

The Paddle
==========

So now we have something that looks kind of like a game but really it's more like
a screensaver at this point, the player can't actually interact with it at all.
Let's add the paddle and allow some user input. We'll need to instantiate the
paddle and store it as a variable in the Game class and detect button presses in
the update function::

    # in the Game init
    self.paddle = Block(26, 44, self.display)

    # in the Game draw function
    self.paddle.draw()

    # in the Game update, before the ball update() call
    self.buttons.get()
        if self.buttons.BUTTON_A > 0:
            self.paddle.move_left()
        if self.buttons.BUTTON_B > 0:
            self.paddle.move_right()


Ok, time to test again. Does this work as you expect, can you think of any
improvements? The paddle moves a bit slowly maybe? The ball is still not interacting
with the blocks or the paddle though, so let's add that.

Collision Detection
===================

We need to be able to tell when the ball hits against another game object like
the paddle or the blocks. This bit involves a bit of basic coordinate maths to
figure out if the rectangles intersect or not. We need a function that takes two
objects and checks if they collide::

    def collision(self, rect1, rect2):
        # note this function doesn't use the self parameter so it could be static
        # or defined outside the Game class if we wanted.
        return (rect1.x < rect2.x + rect2.width &&
                rect1.x + rect1.width > rect2.x &&
                rect1.y < rect2.y + rect2.height &&
                rect1.y + rect1.height > rect2.y)

Now we need to call this fucntion on the ball and other objects on every update.
This could be a bit expensive to calculate all the time so we should ideally only
call it when necessary. For example, no point checking collisions when the Ball
is in the empty space in the middle which we can check with a simple Y value
check. For now, let's not worry about it. We need to add a function to the ball
class to make it react to a collision with the paddle::

    def hit_paddle(self):
        self.v_y *= -1

Then in the Game update function we can check for the collision and make the Ball
react::

    if self.collision(self.ball, self.paddle):
        self.ball.hit_paddle()


Draw the rest of the Owl
========================

That is as much of the Game example that I've written, I'll leave the rest as an exercise
for the reader! We still need to add a score tracking system, collision with
the blocks and a Game Over for when the ball hits the bottom too many times. If
you have time then try to implement these features!

That's all, folks!
==================

You've reached the end of the content of the workshop for now! If there is time
left then just play around with things!
