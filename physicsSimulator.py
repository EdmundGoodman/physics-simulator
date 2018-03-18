#Edmund Goodman - Creative Commons Attribution-NonCommercial-ShareAlike 2.5
#Physics Simulator
from turtle import *
import math, os, colorsys

class body:
    def __init__(self, name, position, velocity, acceleration, radius, mass, charge):
        #Initialise all the variables
        self.name = name #name
        self.radius = radius #radius
        self.mass = mass #mass
        self.charge = charge

        self.position = position #(x, y)
        self.velocity = velocity #(x, y)
        self.acceleration = acceleration #(x, y)

    def displayBody(self):
        #Print various attributes of the body
        print("{}".format(self.name))
        print("{} {} {}".format(self.position, self.velocity, self.acceleration))
        print("{} {} {}".format(self.radius, self.mass, self.charge))

    def updateAcceleration(self, otherBodies):
        #Calculate and update acceleration bases upon gravity
        self.acceleration = [0 for i in self.acceleration]

        for o in otherBodies:
            #Calculate the vector & the hypotenuse between the bodies (dist & hyp)
            dist, hyp = [], 0
            for i in range(0, len(self.acceleration)):
                dist.append(self.position[i]-o.position[i])
                hyp += dist[i]**2
            hyp = math.sqrt(hyp)

            #Update the acceleration due to gravity
            if self.mass != 0:
                gravitationalConstant = 0.1 #6.67*(10**−11)
                force = -1*gravitationalConstant*((self.mass*o.mass)/hyp)
                acceleration = force/self.mass
                for i in range(0, len(self.acceleration)):
                    self.acceleration[i] += (acceleration*dist[i]/hyp)

            #Update the acceleration due to electostatic attraction
            if self.charge != 0:
                coulombsConstant = 0.1 #8.99*(10**9)
                force = coulombsConstant*((self.charge*o.charge)/hyp)
                acceleration = force/self.mass
                for i in range(0, len(self.acceleration)):
                    self.acceleration[i] += (acceleration*dist[i]/hyp)

    def updateVelocity(self):
        #Update velocity based off of acceleration
        for i in range(0, len(self.velocity)):
            self.velocity[i] += self.acceleration[i]

    def updatePosition(self):
        #Update position based off of velocity
        for i in range(0, len(self.position)):
            self.position[i] += self.velocity[i]*timeStep

    def getCollisions(self, otherBodies):
        #Get all the collisions
        collisions = []
        for o in otherBodies:
            #Calculate the hypotenuse between the bodies self and o (hyp)
            hyp = 0
            for i in range(0, len(self.acceleration)):
                hyp += (self.position[i]-o.position[i])**2
            hyp = math.sqrt(hyp)
            #If there is a collision
            if hyp < (self.radius + o.radius):
                collisions.append([self, o])
        return collisions

    def showBody(self):
        #Given a body, blit it to the screen at its relevant position
        goto([self.position[i] for i in range(0, len(self.acceleration))])
        pendown(); dot(self.radius*2); penup()

    def getOtherBodies(self, allBodies):
        #Return all bodies other than self
        otherBodies = allBodies[:]
        otherBodies.remove(self)
        return otherBodies


#Initialise window
os.system('clear'); title('Physics Simulator')
#Initialise variables
loopCount, displayStep, blitStep, timeStep, coloring = 50000, 20, 20, .05, "speed"

#Initialise celestial bodies
body1 = body("body1", [-475,-100], [1,0], [0,0], 5, 5, 0)
body2 = body("body2", [-475,0], [2,0], [0,0], 5, 5, 0)
body3 = body("body3", [-475,100], [-1,0], [0,0], 5, 5, 0)
allBodies = [body1, body2, body3]

#Turtle prettiness code
speed(0)
penup()
ht()
setup(1000,700)
tracer(len(allBodies)*blitStep,0)

#Animate the bodies for loopCount # steps
for iterations in range(loopCount):
    #Find all collisions in among the bodies
    collisions = []
    for b in allBodies:
        collisions += b.getCollisions(b.getOtherBodies(allBodies))
    #Sort the contents of the contents of the list, so you can remove duplicates, even if they are opposite ways round
    collisions = list(set([tuple(sorted(c, key=lambda x: x.name, reverse=True)) for c in collisions]))
    #if collisions != []: [print([print(x.name, end=" ") for x in y]) for y in collisions]

    #Enact all the collisions
    for c in collisions:
        #Update the velocities relative to the bodies masses
        for i in range(0, len(c[0].velocity)):
            c[0].velocity[i] = ((c[0].velocity[i]*c[0].mass)+(c[1].velocity[i]*c[1].mass))/(c[0].mass+c[1].mass)
        #Average the positions
        for i in range(0, len(c[0].position)):
            c[0].position[i] = (c[0].position[i]+c[1].position[i])/2
        #Combine the masses & radii
        c[0].mass += c[1].mass
        c[0].radius += c[1].radius
        #Remove the second body
        allBodies.remove(c[1])
        #Replace all instances of the second body with the first body in collisions
        for i,y in enumerate(collisions):
            if c[1] in y:
                collisions[i] = [c[0] if x==c[1] else x for x in y]

    #Update the acceleration for b relative to the other bodies
    for b in allBodies:
        b.updateAcceleration(b.getOtherBodies(allBodies))

    for b in allBodies:
        #Display the bodies every displayStep number of iterations
        if iterations%displayStep==0:
            #Calculate the coloring of each body
            if coloring=="speed":
                colorValue = sum([abs(x) for x in b.velocity])*.2
            elif coloring=="3d":
                colorValue = abs(b.position[-1])/1000
            elif coloring=="mass":
                colorValue = b.mass/100
            elif coloring=="charge":
                colorValue = b.charge/100
            else: #iterations
                colorValue = (float(iterations)/1000)*.5
            color(colorsys.hsv_to_rgb(colorValue,1.0,1.0))
            b.showBody()

        #Update the velocity and position of body
        b.updateVelocity()
        b.updatePosition()

exitonclick()
