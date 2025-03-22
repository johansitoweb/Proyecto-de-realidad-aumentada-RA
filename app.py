import cv2
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

pygame.init()
ventana = pygame.display.set_mode((640, 680), pygame.OPENGL | pygame.DOUBLEBUF)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def cargar_textura(archivo_imagen):
    try:
        imagen = pygame.image.load(archivo_imagen)
        imagen_datos = pygame.image.tostring(imagen, "RGBA", 1) # Cambiado a RGBA
        textura_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textura_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, imagen.get_width(), imagen.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, imagen_datos) # Cambiado a RGBA
        return textura_id
    except pygame.error as e:
        print(f"Error al cargar la imagen: {e}")
        return None

textura_id = cargar_textura("pato.png")
if textura_id is None:
    quit()

captura = cv2.VideoCapture(0)
textura_camara_id = glGenTextures(1)

while True:
    ret, frame = captura.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_data = frame_rgb.tobytes()
    glBindTexture(GL_TEXTURE_2D, textura_camara_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, frame.shape[1], frame.shape[0], 0, GL_RGB, GL_UNSIGNED_BYTE, frame_data)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluPerspective(45, (640 / 480), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5.0)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textura_camara_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-2.0, -1.5, -1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(2.0, -1.5, -1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(2.0, 1.5, -1.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-2.0, 1.5, -1.0)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, textura_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0, -1.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0, -1.0, 0.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0, 1.0, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0, 1.0, 0.0)
    glEnd()
    glDisable(GL_TEXTURE_2D)

    pygame.display.flip()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            captura.release()
            cv2.destroyAllWindows()
            quit()