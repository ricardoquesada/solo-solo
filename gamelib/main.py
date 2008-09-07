
# This code is so you can run the samples without installing the package
import sys
import os
#sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import pymunk as pm
from pymunk.vec2d import Vec2d
import math
import random
from primitives import *

from pyglet.gl import *



import cocos
from cocos.director import director

import pyglet


def drawCircle(x, y, r, a):
    segs = 15
    coef = 2.0*math.pi/segs;
    
    glBegin(GL_LINE_LOOP)
    for n in range(segs):
        rads = n*coef
        glVertex2f(r*math.cos(rads + a) + x, r*math.sin(rads + a) + y)
    glVertex2f(x,y)
    glEnd()


def drawCircleShape(circle):
    body = circle.body
    c = body.position + circle.center.cpvrotate(body.rotation_vector)
    drawCircle(c.x, c.y, circle.radius, body.angle)



class PMLayer(cocos.layer.Layer):
    is_event_handler = True     #: enable pyglet's events

    def __init__(self):
        super(PMLayer,self).__init__()

        self.schedule( self.step )


        pm.init_pymunk()
        self.space = pm.Space( iterations=10)
        self.space.gravity = (0, -500.0)

        self.elements=[]

        self.head = None

        self.add_segments()
        self.add_ball()


    def step(self, dt):
        balls_to_remove = []
        for elem in self.elements:
            if isinstance(elem, pm.Circle) and elem.body.position.y < 0:
                balls_to_remove.append(elem)
        
        for ball in balls_to_remove:
            self.space.remove(ball, ball.body)
            self.elements.remove(ball)

            self.add_ball()

        self.space.step(dt)

    def draw( self ):
        for elem in self.elements:
            if isinstance(elem, pm.Circle):
                self.draw_ball( elem )
            elif isinstance(elem, pm.Segment):
                self.draw_segment( elem )

    def draw_ball( self, ball ):
#        d = ball.body.position + ball.center.cpvrotate(ball.body.rotation_vector)
#        Circle( d.x, d.y, width=ball.radius*2, color=(1.0,1.0,1.0,1.0)).render()
#        Line( ball.body.position, d, color=(0.5,0.5,1.0,1.0), rotation=0.0 ).render()
        drawCircleShape(ball)

    def draw_segment( self, s ):
        a = s.body.position + s.a 
        b = s.body.position + s.b
        Polygon( v=[ a, b ], color=(1.0,0.5,0.5,1.0), stroke=1.0 ).render()

    def add_segments(self):
        x,y = director.get_window_size()
        
        body = pm.Body(pm.inf, pm.inf)           # mass, inertia
        body.position = Vec2d(0,0)               #     

        l0 = pm.Segment(body, (0,1), (x,1), 1.0)
        l1 = pm.Segment(body, (0,0), (0,y), 1.0)
        l2 = pm.Segment(body, (x,1), (x,y), 1.0)
        l3 = pm.Segment(body, (0,y), (x,y), 1.0)
        l0.friction = 1.0
        l1.friction = 1.0
        l2.friction = 1.0
        l3.friction = 1.0
        l0.elasticity = 0.8
        l1.elasticity = 1.2
        l2.elasticity = 1.2
        l3.elasticity = 1.2
        
        self.space.add_static(l0,l1,l2,l3)
        self.elements += (l0,l1,l2,l3)

    def add_ball(self):
        """Add a ball to the space space at a random position"""

        last = None
        for i in xrange(5):
            body,shape = self.create_ball()
            body.position = (320+i*20,200+i*20)
            shape.data = i

            self.space.add(body, shape)
            self.elements.append( shape )

            if i == 0:
                self.head = body

            if last:
                joint = pm.SlideJoint(last, body, (0,0), (0,0), 0, 40)
#                joint = pm.PinJoint(last, body, last.position, last.position, 10, 40)
                self.space.add( joint )

            last = body

    def create_ball(self):
        mass = 1
        radius = 10
        inertia = pm.moment_for_circle(mass, 0, radius, (0,0))
        body = pm.Body(mass, inertia)
        shape = pm.Circle(body, radius, (0,0))
        shape.friction  = 1.5
        shape.elasticity = 1.0

        return (body,shape)

    def on_key_press (self, key, modifiers):
        i = ord('i')
        j = ord('j')
        k = ord('k')
        l = ord('l')
        r = ord('r')
        if key in (i,j,k,l,r):
            force = (0,0)
            if key == i:
                force = (0,100)
            elif key == k:
                force = (0,-100)
            elif key == j:
                force = (-100,0)
            elif key == l:
                force = (100,0)
            elif key == r:
                force = (0,0)
                self.head.reset_forces()
            self.head.apply_force(force, (0,0) )
            return True 
        return False 

if __name__ == "__main__":
    director.init()
    test_layer = PMLayer()
    main_scene = cocos.scene.Scene (test_layer)
    director.run (main_scene)
'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "gamelib"
package.
'''

import data

def main():
    director.init()
    test_layer = PMLayer()
    main_scene = cocos.scene.Scene (test_layer)
    director.run (main_scene)

if __name__ == "__main__":
    main()
