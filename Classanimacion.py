import pygame
import os

class Animacion:
    def __init__(self, ruta_frames, tiempo_maximo, tamano=(70, 70)):
        self.frames = []
        self.cargar_frames(ruta_frames, tamano)
        self.tiempo_maximo = tiempo_maximo
        self.tiempo_por_frame = tiempo_maximo / len(self.frames)
        self.frame_actual = 0
        self.tiempo_inicial = 0

    def cargar_frames(self, ruta_frames, tamano):
        for i in range(1, 31):
            filename = f'frame-{i:02d}.gif'
            frame = pygame.image.load(os.path.join(ruta_frames, filename))
            frame = pygame.transform.scale(frame, tamano)
            self.frames.append(frame)

    def iniciar(self, tiempo_actual):
        self.tiempo_inicial = tiempo_actual

    def actualizar(self, tiempo_actual):
        if self.tiempo_inicial > 0:
            contador_tiempo = tiempo_actual - self.tiempo_inicial
            self.frame_actual = int((contador_tiempo / self.tiempo_por_frame) % len(self.frames))
            if contador_tiempo >= self.tiempo_maximo:
                self.tiempo_inicial = 0

    def dibujar(self, ventana, posicion):
        if self.tiempo_inicial > 0:
            ventana.blit(self.frames[self.frame_actual], posicion)