import pygame
from archivos import *
from Classpokemon import *
import random

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
input.center = (ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 200)

color_activo = BLANCO
color_inactivo = NEGRO
color = color_inactivo

texto = ''

activo = False
encontro = False
siguiente = False

texto_superior = fuente_titulo.render("Who's That Pokemon?",True,BLANCO)

boton = pygame.Rect(ANCHO_VENTANA // 2 - 50, ALTO_VENTANA - 100, 100, 50)
mostrar_boton = False

pokemon_actual = random.choice(lista_pokemons)
mostrar_silueta = True
flag = True
while flag == True:
    lista_eventos = pygame.event.get()
    if siguiente:
        pokemon_actual = random.choice(lista_pokemons)
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

    if activo == True:
        color = color_activo
    else:
        color = color_inactivo

    ventana.fill(AZUL_CLARO)

    pokemon_actual.dibujar(ventana, mostrar_silueta)

    pygame.draw.rect(ventana, color, input)

    superficie_texto = fuente.render(texto, True, NEGRO)

    ventana.blit(superficie_texto,(input.x + 5, input.y + (input.height - superficie_texto.get_height()) // 2))
    ventana.blit(texto_superior,(ANCHO_VENTANA // 2 - texto_superior.get_width() // 2, 50))

    if mostrar_boton:
        pygame.draw.rect(ventana, (0, 255, 0), boton)
        texto_boton = fuente.render("Siguiente", True, NEGRO)
        ventana.blit(texto_boton, (boton.x + 10, boton.y + 10))

    pygame.display.update()

pygame.quit()