# assign02_김은혜

import turtle
import random

swidth = 600
sheight = 600

turtle.setup(swidth, sheight)
turtle.colormode(255)

t = turtle.Turtle()

for i in range(80):
    t.shape('turtle')
    t.setheading(30 + 30 * i)
    t.forward(5 + i)
    t.color(random.randrange(256), random.randrange(256), random.randrange(256))

turtle.done()
