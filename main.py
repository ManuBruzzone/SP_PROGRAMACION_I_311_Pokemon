import pygame
from archivos import *
from Classpokemon import *
from Classbotones import *
from Classanimacion import *
import random
import os

NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AZUL_CLARO = (0, 150, 255)
BLANCO = (255, 255, 255)

# Configuración de la ventana
ANCHO_VENTANA = 650 
ALTO_VENTANA = 900
TAMANO_VENTANA = (ANCHO_VENTANA, ALTO_VENTANA)

# Inicialización de Pygame
pygame.init()

# Cargar la lista de Pokemons
lista_pokemons = cargar_lista_pokemons('pokemons.csv')

# Configurar la ventana
ventana = pygame.display.set_mode(TAMANO_VENTANA)
pygame.display.set_caption("Who's That Pokemon?")
icono = pygame.image.load('Recursos\Icono\Pokeball.png')
pygame.display.set_icon(icono)
ventana.fill(AZUL_CLARO)

# Fuentes
fuente = pygame.font.SysFont('consolas', 20)
fuente_titulo = pygame.font.SysFont('Arial', 40)

# Input
input_rect = pygame.Rect(0, 0, 200, 32)
input_rect.center = (ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 5)
texto = ''

# Textos
texto_superior = fuente_titulo.render("Who's That Pokemon?", True, BLANCO)
texto_generaciones = fuente.render('Generation', True, NEGRO)
texto_dificultad = fuente.render('Difficulty', True, NEGRO)

# Ruta y configuración de la animación
ruta_frames = 'Recursos/frames-gif'
animacion = Animacion(ruta_frames, 3000)

# Botones
botones_generaciones = Botones()
botones_dificultad = Botones()
botones_generaciones.crear_botones(75,45,3,3,(50,720),1)
botones_dificultad.crear_botones(75,45,3,1,(300,720),1)

# Seleccionar Pokémon inicial
pokemon_actual = random.choice(lista_pokemons)

# Inicializar generaciones seleccionadas y lista filtrada
generaciones_seleccionadas = botones_generaciones.obtener_generaciones_seleccionadas()
lista_pokemons_filtrada = pokemon_actual.filtrar_pokemons(lista_pokemons, generaciones_seleccionadas)
pokemon_actual = random.choice(lista_pokemons_filtrada) if lista_pokemons_filtrada else None

# Banderas
mostrar_silueta = True
siguiente = False
activo = False
flag = True
aplicar_filtro = False

while flag:
    lista_eventos = pygame.event.get()
    tiempo_actual = pygame.time.get_ticks()

    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            flag = False

        elif evento.type == pygame.KEYDOWN:
            if activo:
                if evento.key == pygame.K_BACKSPACE:
                    texto = texto[:-1]
                elif evento.key == pygame.K_RETURN:
                    if pokemon_actual.nombre.lower() == texto.lower():
                        mostrar_silueta = False
                        animacion.iniciar(tiempo_actual)
                    texto = ""
                else:
                    texto += evento.unicode

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(evento.pos):
                activo = not activo
            else:
                activo = False

            pos = evento.pos
            botones_generaciones.actualizar_color_boton(pos)
            aplicar_filtro = True

    if siguiente:
        if aplicar_filtro:
            generaciones_seleccionadas = botones_generaciones.obtener_generaciones_seleccionadas()
            lista_pokemons_filtrada = pokemon_actual.filtrar_pokemons(lista_pokemons, generaciones_seleccionadas)
            aplicar_filtro = False

        if lista_pokemons_filtrada:
            pokemon_actual = random.choice(lista_pokemons_filtrada)
        mostrar_silueta = True
        siguiente = False


    if not mostrar_silueta and tiempo_actual - animacion.tiempo_inicial >= animacion.tiempo_maximo:
        pokemon_actual = random.choice(lista_pokemons)
        mostrar_silueta = True 
        animacion.tiempo_inicial = 0
        siguiente = True


    generaciones_seleccionadas = botones_generaciones.obtener_generaciones_seleccionadas()

    ventana.fill(AZUL_CLARO)

    botones_generaciones.dibujar_botones(ventana,NEGRO,fuente)
    botones_dificultad.dibujar_botones(ventana,NEGRO,fuente)
    pokemon_actual.dibujar(ventana, mostrar_silueta)

    pygame.draw.rect(ventana, BLANCO, input_rect)
    nombre_pokemon = fuente.render(f'{pokemon_actual.nombre} {pokemon_actual.generacion}',True,NEGRO)
    superficie_texto = fuente.render(texto, True, NEGRO)
    ventana.blit(superficie_texto, (input_rect.x + 5, input_rect.y + (input_rect.height - superficie_texto.get_height()) // 2))
    ventana.blit(texto_superior, (ANCHO_VENTANA // 2 - texto_superior.get_width() // 2, 50))
    ventana.blit(texto_generaciones, (49,695))
    ventana.blit(texto_dificultad, (350,695))
    ventana.blit(nombre_pokemon, (50,50))
    

    animacion.actualizar(tiempo_actual)
    animacion.dibujar(ventana, (input_rect.right + 50, input_rect.y + (input_rect.height - 90) // 2))

    pygame.display.update()

pygame.quit()