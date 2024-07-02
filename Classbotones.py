import pygame

pygame.init()

NEGRO = (0,0,0)
GRIS = (128, 128, 128)
ROJO = (255, 0, 0)
BLANCO = (255,255,255)

class Botones:
    def __init__(self):
        self.botones_generacion = []
        self.botones_dificultad = []
        self.medidas_botones_fondo = ()
        self.color_botones_generacion = {}
        self.color_botones_dificultad = {}
        self.generaciones_seleccionadas = []
        self.dificultades_seleccionadas = []
        self.boton = None
        self.color_boton = ROJO
        self.texto_boton = ""


    def crear_botones_generacion(self, ancho_boton, alto_boton, filas, columnas, pos_inicial, espaciado):
        matriz_botones_generacion = [[None for _ in range(columnas)] for _ in range(filas)]

        for i in range(filas):
            for j in range(columnas):
                x = pos_inicial[0] + j * (ancho_boton + espaciado)
                y = pos_inicial[1] + i * (alto_boton + espaciado)
                boton_rectangulo = pygame.Rect(x, y, ancho_boton, alto_boton)
                numero_generacion = i * columnas + j + 1
                matriz_botones_generacion[i][j] = (boton_rectangulo, numero_generacion)
                self.color_botones_generacion[(i,j)] = BLANCO
            
        self.botones_generacion = matriz_botones_generacion
        self.medidas_botones_fondo = pygame.Rect(pos_inicial[0] -10, pos_inicial[1] -10, (columnas * (ancho_boton + espaciado) - espaciado) + 20, (filas * (alto_boton + espaciado) - espaciado) + 20)


    def crear_botones_dificultad(self, ancho_boton, alto_boton, filas, columnas, pos_inicial, espaciado):
        matriz_botones_generacion = [[None for _ in range(columnas)] for _ in range(filas)]
        dificultades = ['Easy','Normal', 'Hard']
        dificultad_index = 0

        for i in range(filas):
            for j in range(columnas):
                x = pos_inicial[0] + j * (ancho_boton + espaciado)
                y = pos_inicial[1] + i * (alto_boton + espaciado)
                boton_rectangulo = pygame.Rect(x, y, ancho_boton, alto_boton)
                texto_dificultad = dificultades[dificultad_index % len(dificultades)]
                dificultad_index += 1
                matriz_botones_generacion[i][j] = (boton_rectangulo, texto_dificultad)
                self.color_botones_dificultad[(i,j)] = BLANCO
            
        self.botones_dificultad = matriz_botones_generacion
        self.medidas_botones_fondo = pygame.Rect(pos_inicial[0] -10, pos_inicial[1] -10, (columnas * (ancho_boton + espaciado) - espaciado) + 20, (filas * (alto_boton + espaciado) - espaciado) + 20)
    
    def crear_boton(self, x, y, ancho, alto, color, texto):
        self.boton = pygame.Rect(x, y, ancho, alto)
        self.color_boton = color
        self.texto_boton = texto

    def dibujar_botones_generacion(self, ventana, color_texto, fuente):
        if self.medidas_botones_fondo:
            pygame.draw.rect(ventana, GRIS, self.medidas_botones_fondo)

        for i in range(len(self.botones_generacion)):
            fila = self.botones_generacion[i]
            for j in range(len(fila)):
                boton_rect, num_generacion = fila[j]
                color = self.color_botones_generacion[(i, j)]
                pygame.draw.rect(ventana, color, boton_rect)
                texto = fuente.render(str(num_generacion), True, color_texto)
                ventana.blit(texto, (boton_rect.x + (boton_rect.width - texto.get_width()) // 2, boton_rect.y + (boton_rect.height - texto.get_height()) // 2))

    def dibujar_botones_dificultad(self, ventana, color_texto, fuente):
        if self.medidas_botones_fondo:
            pygame.draw.rect(ventana, GRIS, self.medidas_botones_fondo)

        for i in range(len(self.botones_dificultad)):
            fila = self.botones_dificultad[i]
            for j in range(len(fila)):
                boton_rect, texto_dificultad = fila[j]
                color = self.color_botones_dificultad[(i, j)]
                pygame.draw.rect(ventana, color, boton_rect)
                texto = fuente.render(texto_dificultad, True, color_texto)
                ventana.blit(texto, (boton_rect.x + (boton_rect.width - texto.get_width()) // 2, boton_rect.y + (boton_rect.height - texto.get_height()) // 2))

    def dibujar_boton(self, ventana, fuente):
        if self.boton:
            pygame.draw.rect(ventana, self.color_boton, self.boton)
            texto = fuente.render(self.texto_boton, True, BLANCO)
            ventana.blit(texto, (self.boton.x + (self.boton.width - texto.get_width()) // 2, self.boton.y + (self.boton.height - texto.get_height()) // 2))

    def actualizar_color_boton(self, pos):
        i_gen = 0
        for fila in self.botones_generacion:
            j_gen = 0
            for boton_rect, num_generacion in fila:
                if boton_rect.collidepoint(pos):
                    if self.color_botones_generacion[(i_gen, j_gen)] == BLANCO:
                        self.color_botones_generacion[(i_gen, j_gen)] = GRIS
                        self.generaciones_seleccionadas.append(num_generacion)
                    else:
                        self.color_botones_generacion[(i_gen, j_gen)] = BLANCO
                        self.generaciones_seleccionadas.remove(num_generacion)
                j_gen += 1
            i_gen += 1

        i_dif = 0
        for fila in self.botones_dificultad:
            j_dif = 0
            for boton_rect, texto_dificultad in fila:
                if boton_rect.collidepoint(pos):
                    if self.color_botones_dificultad[(i_dif, j_dif)] == BLANCO:
                        self.color_botones_dificultad[(i_dif, j_dif)] = GRIS
                        self.dificultades_seleccionadas.append(texto_dificultad)
                    else:
                        self.color_botones_dificultad[(i_dif, j_dif)] = BLANCO
                        self.dificultades_seleccionadas.remove(texto_dificultad)
                j_dif += 1
            i_dif += 1

    def obtener_generaciones_seleccionadas(self):
        return self.generaciones_seleccionadas
    
    def obtener_dificutlad_seleccioanda(self):
        return self.dificultades_seleccionadas
    
    def boton_clickeado(self, pos):
        clickeado = False
        if self.boton and self.boton.collidepoint(pos):
            clickeado = True
        
        return clickeado 