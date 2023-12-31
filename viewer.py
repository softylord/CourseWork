
import sys, pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pywavefront

 
# IMPORT OBJECT LOADER
from objloader import *

 
pygame.init()
viewport = (800,600)
hx = viewport[0]
hy = viewport[1]
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)
 
glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)        # most obj files expect to be smooth-shaded
 
# LOAD OBJECT AFTER PYGAME INIT
obj = OBJ(sys.argv[1], hx, hy, swapyz=True)
 
clock = pygame.time.Clock()
 
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
width, height = viewport
gluPerspective(45.0, width/float(height), 0.1, 100.0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)
 
rx, ry = (0,0)
tx, ty = (0,0)
mx=0
my=0
mz=0
zpos = 5
rotate = move = False
while 1:
    clock.tick(30)
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                sys.exit()
            if e.key == pygame.K_LEFT:
                mx+=-0.5
            if e.key == pygame.K_RIGHT:
                mx+=0.5
            if e.key == pygame.K_UP:
                my+=1
            if e.key == pygame.K_DOWN:
                my-=1
            if e.key == pygame.K_q:
                mz+=1
            if e.key == pygame.K_e:
                mz-+1
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 4: zpos = max(1, zpos-1)
            elif e.button == 5: zpos += 1
            elif e.button == 1: rotate = True
            elif e.button == 3: move = True
        elif e.type == MOUSEBUTTONUP:
            if e.button == 1: rotate = False
            elif e.button == 3: move = False
        elif e.type == MOUSEMOTION:
            i, j = e.rel
            if rotate:
                rx += i
                ry += j
            if move:
                tx += i
                ty -= j
 
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
 
    # RENDER OBJECT
    glTranslate(tx/20., ty/20., - zpos)
    glRotate(ry, 1, 0, 0)
    glRotate(rx, 0, 1, 0)
    glTranslatef(mx, my, mz)

    glCallList(obj.gl_list)
 
    pygame.display.flip()