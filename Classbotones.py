import pygame

pygame.init()

fuente = pygame.font.SysFont('Arial',20)

NEGRO = (0,0,0)
GRIS = (128, 128, 128)
BLANCO = (255,255,255)

class Botones:
    def __init__(self):
        self.botones = []
        self.color_botones = {}
        self.generaciones_seleccionadas = []

    def crear_botones_generaciones(self):
        ancho_boton = 50
        alto_boton = 30
        espaciado = 2.5
        filas = 3
        columnas = 3
        matriz_botones_generacion = [[None for _ in range(columnas)] for _ in range(filas)]

        for i in range(filas):
            for j in range(columnas):
                x = 50 + j * (ancho_boton + espaciado)
                y = 775 + i * (alto_boton + espaciado)
                boton_rectangulo = pygame.Rect(x, y, ancho_boton, alto_boton)
                numero_generacion = i * columnas + j + 1
                matriz_botones_generacion[i][j] = (boton_rectangulo, numero_generacion)
                self.color_botones[(i,j)] = BLANCO
            
        self.botones = matriz_botones_generacion

    def dibujar_botones(self, ventana):
        for i in range(len(self.botones)):
            fila = self.botones[i]
            for j in range(len(fila)):
                boton_rect, num_generacion = fila[j]
                color = self.color_botones[(i, j)]
                pygame.draw.rect(ventana, color, boton_rect)
                texto = fuente.render(str(num_generacion), True, NEGRO)
                ventana.blit(texto, (boton_rect.x + (boton_rect.width - texto.get_width()) // 2, boton_rect.y + (boton_rect.height - texto.get_height()) // 2))

    def actualizar_color_boton(self, pos):
        i = 0
        for fila in self.botones:
            j = 0
            for boton_rect, num_generacion in fila:
                if boton_rect.collidepoint(pos):
                    if self.color_botones[(i, j)] == BLANCO:
                        self.color_botones[(i, j)] = GRIS
                        self.generaciones_seleccionadas.append(num_generacion)
                    else:
                        self.color_botones[(i, j)] = BLANCO
                        self.generaciones_seleccionadas.remove(num_generacion)
                j += 1
            i += 1
        
    def obtener_generaciones_seleccionadas(self):
        return self.generaciones_seleccionadas