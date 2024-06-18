import pygame
from archivos import *
from Classpokemon import *
from Classbotones import *
import random
import os

NEGRO = (0,0,0)
ROJO = (255,0,0)
VERDE = (0,255,0)
AZUL = (0,0,255)
AZUL_CLARO = (0,150,255)
BLANCO = (255,255,255)

ANCHO_VENTANA = 650 
ALTO_VENTANA = 900
VELOCIDAD = 10
TAMANO_VENTANA =  (ANCHO_VENTANA,ALTO_VENTANA)

FPS = 30

pygame.init()

lista_pokemons = cargar_lista_pokemons('Pokemons.csv')

ventana = pygame.display.set_mode(TAMANO_VENTANA)
pygame.display.set_caption("Who's That Pokemon?")

icono = pygame.image.load('Recursos\Pokeball.png')
pygame.display.set_icon(icono)

ventana.fill(AZUL_CLARO)

fuente = pygame.font.SysFont('Arial',20)
fuente_titulo = pygame.font.SysFont('Arial',40)

input = pygame.Rect(0,0,200,32)
input.center = (ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 5)

texto = ''

texto_superior = fuente_titulo.render("Who's That Pokemon?",True,BLANCO)

boton = pygame.Rect(ANCHO_VENTANA // 2 - 50, ALTO_VENTANA - 100, 100, 50)
mostrar_boton = False

tiempo_inicial = 0
contador_tiempo = 0
TIEMPO_MAXIMO = 3000 

ruta_frames = r'Recursos\frames-gif'
contador_frames = []
for i in range(1, 31):
    filename = f'frame-{i:02d}.gif'
    frame = pygame.image.load(os.path.join(ruta_frames, filename))
    frame = pygame.transform.scale(frame, (70, 70))
    contador_frames.append(frame)

frame_actual = 0
tiempo_por_frame = TIEMPO_MAXIMO / len(contador_frames)

botonin = BotonGeneraciones()

pokemon_actual = random.choice(lista_pokemons)
mostrar_silueta = True
siguiente = False
activo = False
flag = True
while flag == True:
    lista_eventos = pygame.event.get()
    tiempo_actual = pygame.time.get_ticks()

    if siguiente:
        pokemon_actual = random.choice(lista_pokemons)
        mostrar_silueta = True
        siguiente = False
        tiempo_inicial = 0
        contador_tiempo = 0

    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            flag = False

        elif evento.type == pygame.KEYDOWN:
            if activo:
                if evento.key == pygame.K_BACKSPACE:
                    texto = texto[:-1]
                elif evento.key == pygame.K_RETURN:
                    if pokemon_actual.nombre == texto:
                        mostrar_silueta = False
                        mostrar_boton = True
                        tiempo_inicial = tiempo_actual
                    texto = ""
                else:
                    texto += evento.unicode

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if input .collidepoint(evento.pos):
                activo = not activo
            else:
                activo = False
            
            if mostrar_boton and boton.collidepoint(evento.pos):
                pokemon_actual = random.choice(lista_pokemons)
                mostrar_silueta = True
                mostrar_boton = False

            generacion_seleccionada = botonin.detectar_click(evento.pos)
            if generacion_seleccionada:
                print(f"Generación seleccionada: {generacion_seleccionada}")

    ventana.fill(AZUL_CLARO)

    pokemon_actual.dibujar(ventana, mostrar_silueta)

    pygame.draw.rect(ventana, BLANCO, input)

    superficie_texto = fuente.render(texto, True, NEGRO)

    ventana.blit(superficie_texto,(input.x + 5, input.y + (input.height - superficie_texto.get_height()) // 2))
    ventana.blit(texto_superior,(ANCHO_VENTANA // 2 - texto_superior.get_width() // 2, 50))

    if tiempo_inicial > 0:
        contador_tiempo = tiempo_actual - tiempo_inicial

        frame_actual = int((contador_tiempo / tiempo_por_frame) % len(contador_frames))

        ventana.blit(contador_frames[frame_actual], (input.right + 50, input.y + (input.height - 90) // 2))

        if contador_tiempo >= TIEMPO_MAXIMO:
            siguiente = True
            mostrar_boton = False

    botonin.dibujar_botones(ventana)
    
    pygame.display.update()

pygame.quit()