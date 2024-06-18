import pygame

pygame.init()

fuente = pygame.font.SysFont('Arial',20)

NEGRO = (0,0,0)
ROJO = (255,0,0)
VERDE = (0,255,0)
AZUL = (0,0,255)
AZUL_CLARO = (0,150,255)
BLANCO = (255,255,255)

class BotonGeneraciones:
    def __init__(self):
        self.botones = []
        self.crear_botones()

    def crear_botones(self):
        ancho_boton = 60
        alto_boton = 30
        espaciado = 3
        for i in range(3):
            fila = []
            for j in range(3):
                x = 50 + j * (ancho_boton + espaciado)
                y = 700 + i * (alto_boton + espaciado)
                rect = pygame.Rect(x, y, ancho_boton, alto_boton)
                num_generacion = i * 3 + j + 1
                fila.append((rect, num_generacion))
            self.botones.append(fila)

    def dibujar_botones(self, ventana):
        for fila in self.botones:
            for boton_rect, num_generacion in fila:
                pygame.draw.rect(ventana, BLANCO, boton_rect)
                texto = fuente.render(str(num_generacion), True, NEGRO)
                ventana.blit(texto, (boton_rect.x + (boton_rect.width - texto.get_width()) // 2,boton_rect.y + (boton_rect.height - texto.get_height()) // 2))

    def detectar_click(self, pos):
        for fila in self.botones:
            for boton_rect, num_generacion in fila:
                if boton_rect.collidepoint(pos):
                    return num_generacion