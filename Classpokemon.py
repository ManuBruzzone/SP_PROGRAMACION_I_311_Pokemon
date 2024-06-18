import pygame

class Pokemon:
    def __init__(self, nombre, origen, dimensiones, imagen, generacion, dificultad):
        self.nombre = nombre
        self.imagen = pygame.image.load(imagen)
        self.imagen = pygame.transform.scale(self.imagen, dimensiones)
        self.rectangulo = self.imagen.get_rect()
        self.rectangulo.center = origen
        self.generacion = generacion
        self.dificultad = dificultad

    def dibujar(self, pantalla, mostrar_silueta):
        if mostrar_silueta:
            silueta = self.imagen.copy()
            silueta.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
            pantalla.blit(silueta, self.rectangulo)
        else:
            pantalla.blit(self.imagen, self.rectangulo)