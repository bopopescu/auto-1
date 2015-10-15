# -*- coding: cp936 -*-

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import time
import sys
import numpy

# Set the  width, height, and axis ranges of the window
width = 800
height = 550
centerX = width / 2
centerY = height / 2
radius = 300

# define the features of ground and step
step = 40
xGround = 400
zGround = 400

#define the features of camera 
cameraPosition = [500, 400, 500]
lookRef =[0, 0, 0]

#record the begin coordinate and end coordinate of mouse when the mouse is moving on the screen 
startPoint = [0, 0, 0]
endPoint = [0, 0, 0]
normalVector= [0, 1, 0]
lastVector = [0, 1, 0]
lastAngle = 0.0
#The flag variable records the mouse button state. If the button is pressed, It's True 
flag = False

def init():
    global radius, startPoint, endPoint

    glClearColor(0, 0, 0, 0)
    glLineWidth(1.5)

    if centerX > centerY:
        radius = centerY
    else:
        radius = centerX

    startPoint[0] = -radius
    startPoint[1] = 0
    startPoint[2] = 0
    endPoint[0]   = 0
    endPoint[1]   = 0
    endPoint[2]   =radius

def drawGround():

    glBegin(GL_LINES)
    #draw the x axis
    for x in numpy.arange(-xGround, xGround, step):
        glVertex3f(x, 0, zGround)
        glVertex3f(x, 0, -zGround)
    glVertex3f(x + step, 0, zGround)
    glVertex3f(x + step, 0, -zGround)
    #draw the y axis
    for z in numpy.arange(-zGround, zGround, step):
        glVertex3f(xGround, 0, z)
        glVertex3f(-xGround, 0, z)
    glVertex3f(xGround, 0, z + step)
    glVertex3f(-xGround, 0, z + step)

    glEnd()

def draw():
    #calculate the FPS
    global normalVector, startPoint, endPoint, cameraPosition, lookRef, lastAngle, lastVector, flag
    beginPoint = [startPoint[0], startPoint[1], startPoint[2]]

    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.5, 0.7, 0.1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    #calculate the angle and normal vector

    lengthBegin = math.sqrt( beginPoint[0]**2+beginPoint[1]**2+beginPoint[2]**2)
    lengthEnd   = math.sqrt( endPoint[0]**2 + endPoint[1]**2 + endPoint[2]**2)
    dotSum = 0
    #normalize the vector
    for i in range(3):
        beginPoint[i] /= lengthBegin
        endPoint[i]   /= lengthEnd
        dotSum       +=beginPoint[i]*endPoint[i]
    if dotSum > 1:
        dotSum = 1
    theta = math.acos( dotSum ) * 180 / math.pi

    normalVector[0] = beginPoint[1]*endPoint[2] - beginPoint[2]*endPoint[1]
    normalVector[1] = endPoint[0]*beginPoint[2] - endPoint[2]*beginPoint[0]
    normalVector[2] = beginPoint[0]*endPoint[1] - beginPoint[1]*endPoint[0]
    #gluLookAt will build a view matrix
    gluLookAt( cameraPosition[0], cameraPosition[1], cameraPosition[2], lookRef[0], lookRef[1], lookRef[2], 0, 1, 0)

    #Be carefully, here We can't use glLoadIdentity()
    if flag == True and normalVector[0] != 0 and normalVector[1] != 0 and normalVector[2]!=0:
        glRotatef(theta, normalVector[0], normalVector[1], normalVector[2])

    glRotatef(lastAngle, lastVector[0], lastVector[1], lastVector[2])

    if flag == True and normalVector[0] != 0 and normalVector[1] != 0 and normalVector[2]!=0:
        lastAngle = theta
        for i in range(3):
            lastVector[i] = normalVector[i]

    glPushMatrix()
    drawGround()
    glPopMatrix()
    glFlush()

    glutSwapBuffers()

def reshape( w, h):
    # To ensure we don't have a zero height
    if h==0:
        h = 1
    # Fill the entire graphics window!
    glViewport(0, 0, w, h)
    #define the projection method
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w/h, 0.1, 2000)
    #define the modelview
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def keyboard(key, x, y):
    # Allows us to quit by pressing 'Esc' or 'q'
    if key == chr(27):
        sys.exit()
    if key == "q":
        sys.exit()

#This function is called when the mouse click the window screen
def mouse(key, state, x, y):

    y = glutGet(GLUT_WINDOW_HEIGHT) - y
    global centerX
    global centerY
    global radius
    global startPoint
    global flag
    x = x - centerX
    y = y - centerY
    R2 = x**2 + y**2

    if key == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            flag = True
            if R2 >radius**2:
                startPoint[0] = radius*x*1.0/math.sqrt(R2)
                startPoint[1] = radius*y*1.0/math.sqrt(R2)
                startPoint[2] = 0
            else:
                startPoint[0] = x
                startPoint[1] = y
                startPoint[2] = math.sqrt(radius**2 - R2)
        else:
            flag = False

#The x, y record the mouse path coordinate
def motion(x, y):

    y = glutGet(GLUT_WINDOW_HEIGHT) - y
    global centerX
    global centerY
    global radius
    global endPoint

    x = x - centerX
    y = y - centerY
    R2 = x**2 + y**2
    if R2 > radius**2:
        endPoint[0] = radius*x*1.0/math.sqrt(R2)
        endPoint[1] = radius*y*1.0/math.sqrt(R2)
        endPoint[2] = 0
    else:
        endPoint[0] = x
        endPoint[1] = y
        endPoint[2] = math.sqrt(radius**2 - R2)
    glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB|GLUT_DOUBLE)
    glutInitWindowPosition(100,100)
    glutInitWindowSize(width,height)
    glutCreateWindow("Mesh grid")
    glutReshapeFunc(reshape)
    glutDisplayFunc(draw)

    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    init()
    glutMainLoop()

#begin to run the program
main()
#End of Program