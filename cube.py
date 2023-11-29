import pygame
import OpenGL
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pywavefront
from PIL import Image
import numpy



scene = pywavefront.Wavefront('cube.obj', collect_faces=True)

scene_box = (scene.vertices[0], scene.vertices[0])
for vertex in scene.vertices:
    min_v = [min(scene_box[0][i], vertex[i]) for i in range(3)]
    max_v = [max(scene_box[1][i], vertex[i]) for i in range(3)]
    scene_box = (min_v, max_v)

scene_size     = [scene_box[1][i]-scene_box[0][i] for i in range(3)]
max_scene_size = max(scene_size)
scaled_size    = 5
scene_scale    = [scaled_size/max_scene_size for i in range(3)]
scene_trans    = [-(scene_box[1][i]+scene_box[0][i])/2 for i in range(3)]



def Model():
    glPushMatrix()
    #glRotatef(1, 5, 15, 1)
    glScalef(*scene_scale)
    glTranslatef(*scene_trans)

    for mesh in scene.mesh_list:
        glBegin(GL_TRIANGLES)
        for face in mesh.faces:
            for vertex_i in face:
                glVertex3f(*scene.vertices[vertex_i])
        glEnd()

    glPopMatrix()

def main():
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        gluPerspective(45, (display[0] / display[1]), 1, 500.0)
        glTranslatef(0.0, 0.0, -10)
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        # Set the texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # Set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        image = Image.open("cube.jpg")
        flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = numpy.array(list(flipped_image.getdata()), numpy.uint8)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        glEnable(GL_TEXTURE_2D)

        rx, ry = (0,0)
        tx, ty = (0,0)
        zpos = 5
        rotate = move = False
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_LEFT:
                        glTranslatef(-0.5,0,0)
                    if e.key == pygame.K_RIGHT:
                        glTranslatef(0.5,0,0)
                    if e.key == pygame.K_UP:
                        glTranslatef(0,1,0)
                    if e.key == pygame.K_DOWN:
                        glTranslatef(0,-1,0)
                elif e.type==MOUSEBUTTONDOWN:
                    if e.button == 4: zpos=max(1, zpos-1)
                    elif e.button ==5: zpos+=1
                    elif e.button==1: rotate = True
                    elif e.button==3: move=True
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
            glTranslate(tx/20., ty/20., - zpos)
            glRotate(ry, 1, 0, 0)
            glRotate(rx, 0, 1, 0)

            #glRotatef(1, 5, 1, 1)
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

            #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            Model()

            pygame.display.flip()
            pygame.time.wait(10)

main()