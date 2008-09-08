# std lib
import math
import random

# 3rd party libs
import pyglet
from pyglet.gl import *
from pyglet.window.key import *

import cocos
from cocos.director import director
from cocos.sprite import *
import pymunk as pm

# locals
from primitives import *
import HUD

COLL_TYPE_IGNORE, COLL_TYPE_HEAD, COLL_TYPE_BODY, COLL_TYPE_GOAL = range(4)


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



class GameLayer(cocos.layer.Layer):
    is_event_handler = True     #: enable pyglet's events

    def __init__(self):
        super(GameLayer,self).__init__()

        self.schedule( self.step )

        pm.init_pymunk()
        self.space = pm.Space( iterations=10)
        self.space.gravity = (0, 0.0)

        self.chain = []

        self.add_segments()
        self.add_balls()
        self.add_goal()

        self.space.add_collisionpair_func( COLL_TYPE_HEAD, COLL_TYPE_GOAL, self.collision_head_goal, None)


    def step(self, dt):
        balls_to_remove = []
        for elem in self.space.shapes:
            if isinstance(elem, pm.Circle):
                elem.data.position = elem.body.position
                elem.data.rotation = -math.degrees( elem.body.angle )


        for body in self.chain:
            body.reset_forces()

        for i,b in enumerate( self.chain):
            if i > 0:
                self.chain[i-1].damped_spring( self.chain[i], (0,0), (0,0), 30.0, 30.0, 150.0, dt)

        self.space.step(dt)


    # collision detection
    def collision_head_goal(self, shapeA, shapeB, contacts, normal_coef, data):
        print shapeA, shapeB
        body,shape,sprite = self.create_body_ball()
        body.position = self.chain[-1].position + (5,5)
        self.attach_ball(body)
        self.chain.append( body )
        return True

    def draw( self ):
#        for elem in self.elements:
#            if isinstance(elem, pm.Circle):
#                self.draw_ball( elem )
#            elif isinstance(elem, pm.Segment):
#                self.draw_segment( elem )
        pass

    def draw_ball( self, ball ):
#        d = ball.body.position + ball.center.cpvrotate(ball.body.rotation_vector)
#        Circle( d.x, d.y, width=ball.radius*2, color=(1.0,1.0,1.0,1.0)).render()
#        Line( ball.body.position, d, color=(0.5,0.5,1.0,1.0), rotation=0.0 ).render()
        drawCircleShape(ball)

    def draw_segment( self, s ):
        a = s.body.position + s.a 
        b = s.body.position + s.b
        glPushAttrib(GL_CURRENT_BIT)
        Polygon( v=[ a, b ], color=(1.0,0.5,0.5,1.0), stroke=1.0 ).render()
        glPopAttrib()

    def add_segments(self):
        x,y = director.get_window_size()
        
        body = pm.Body(pm.inf, pm.inf)           # mass, inertia
        body.position = (0,0)               #     

        l0 = pm.Segment(body, (0,1), (x,1), 1.0)
        l1 = pm.Segment(body, (0,0), (0,y), 1.0)
        l2 = pm.Segment(body, (x,1), (x,y), 1.0)
        l3 = pm.Segment(body, (0,y), (x,y), 1.0)
        l0.friction = 1.0
        l1.friction = 1.0
        l2.friction = 1.0
        l3.friction = 1.0
        l0.elasticity = 0.7
        l1.elasticity = 0.7
        l2.elasticity = 0.7
        l3.elasticity = 0.7
        
        self.space.add_static(l0,l1,l2,l3)

    def add_balls(self):
        """Add a ball to the space space at a random position"""

        for i in xrange(8):
            if i==0:
                body,shape,sprite = self.create_head_ball()
            else:
                body,shape,sprite = self.create_body_ball()
            body.position = (320+i*20,50)


            if len( self.chain) > 0:
                self.attach_ball( body )

            self.chain.append( body )

    def attach_ball( self, body ):
#        joint = pm.SlideJoint(self.chain[-1], body, (0,0), (0,0), 25, 40)
#        self.space.add( joint )
        pass

    def add_goal(self):
        body,shape,sprite = self.create_goal_ball()
        body.position = 400,400
        self.add( sprite, z=-1)
        self.space.add(body, shape)

    def create_body_ball(self):
        mass = 0.5
        radius = 12
        inertia = pm.moment_for_circle(mass, 0, radius, (0,0))
        body = pm.Body(mass, inertia)
        shape = pm.Circle(body, radius, (0,0))
        shape.friction  = 1.5
        shape.elasticity = 1.0
        sprite = Sprite('ball.png')
        shape.collision_type = COLL_TYPE_BODY
        shape.data = sprite

        self.space.add(body, shape)
        self.add( sprite, z=-1 )
        return (body,shape,sprite)

    def create_head_ball(self):
        mass = 5
        radius = 15
        inertia = pm.moment_for_circle(mass, 0, radius, (0,0))
        body = pm.Body(mass, inertia)
        shape = pm.Circle(body, radius, (0,0))
        shape.friction  = 1.5
        shape.elasticity = 1.0
        sprite = Sprite('ball_head.png')
        shape.collision_type = COLL_TYPE_HEAD
        shape.data = sprite

        self.space.add(body, shape)
        self.add( sprite, z=-1 )
        return (body,shape,sprite)

    def create_goal_ball(self):
        mass = 20
        radius = 45/2
        inertia = pm.moment_for_circle(mass, 0, radius, (0,0))
        body = pm.Body(mass, inertia)
        shape = pm.Circle(body, radius, (0,0))
        shape.friction  = 1.5
        shape.elasticity = 1.0
        sprite = Sprite('ball_goal.png')
        shape.data = sprite
        shape.collision_type = COLL_TYPE_GOAL

        self.space.add(body, shape)
        self.add( sprite, z=-1 )
        return (body,shape,sprite)

    def on_key_press (self, key, modifiers):
        if key in (LEFT, RIGHT, UP, DOWN):
            force_value = 50
            force = (0,0)
            if key == UP:
                force = (0,force_value)
            elif key == DOWN:
                force = (0,-force_value)
            elif key == LEFT:
                force = (-force_value,0)
            elif key == RIGHT:
                force = (force_value,0)
            elif key == KEY_R:
                force = (0,0)
                self.chain[0].reset_forces()
#            self.chain[0].apply_force(force, (0,0) )
            self.chain[0].apply_impulse(force, (0,0) )
            return True 
        return False 


def get_game_scene():
    s = cocos.scene.Scene()
    s.add( GameLayer(), z=0)
    s.add( HUD.BackgroundLayer(), z=-1)
    s.add( HUD.HUD(), z=1 )
    return s
