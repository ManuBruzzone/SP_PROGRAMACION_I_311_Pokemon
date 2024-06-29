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
ALTO_VENTANA = 720
TAMANO_VENTANA = (ANCHO_VENTANA, ALTO_VENTANA)

# Inicialización de Pygame
pygame.init()

# Cargar la lista de Pokemons
lista_pokemons = cargar_lista_pokemons('pokemons.csv')
lista_nombre = cargar_nombre_pokemons('pokemon_names_multilang.csv')

# Configurar la ventana
ventana = pygame.display.set_mode(TAMANO_VENTANA)
pygame.display.set_caption("Who's That Pokemon?")
icono = pygame.image.load('Recursos\Icono\Pokeball.png')
pygame.display.set_icon(icono)
ventana.fill(AZUL_CLARO)

# Banderas
reino_unido = pygame.image.load(r'Recursos\Banderas\Reino_Unido.png')
reino_unido = pygame.transform.scale(reino_unido, (25,25))
francia = pygame.image.load(r'Recursos\Banderas\Francia.png')
francia = pygame.transform.scale(francia, (25,25))
italia = pygame.image.load(r'Recursos\Banderas\Italia.png')
italia = pygame.transform.scale(italia, (25,25))
alemania = pygame.image.load(r'Recursos\Banderas\Alemania.png')
alemania = pygame.transform.scale(alemania, (25,25))

# Fuentes
fuente = pygame.font.SysFont('consolas', 20)
fuente_titulo = pygame.font.SysFont('Arial', 40)

# Input
input_rect = pygame.Rect(0, 0, 200, 32)
input_rect.center = (ANCHO_VENTANA // 2, ALTO_VENTANA // 1.7 + 1)
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
botones_generaciones.crear_botones_generacion(75, 45, 3, 3, (50, 550), 1)
botones_dificultad.crear_botones_dificultad(110, 45, 3, 1, (500, 550), 1)

# Seleccionar Pokémon inicial
pokemon_actual = random.choice(lista_pokemons)

# Contadores
contador_tiempo = 0
contador_pokemons = 0
tiempo_inicial = pygame.time.get_ticks()
aciertos = 0

# Banderas
mostrar_silueta = True
siguiente = False
activo = False
flag = True
aplicar_filtro = False
mostrar_nombres = False 

while flag:
    lista_eventos = pygame.event.get()
    tiempo_actual = pygame.time.get_ticks()
    contador_tiempo = (tiempo_actual - tiempo_inicial)// 1000

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
                        mostrar_nombres = True
                        animacion.iniciar(tiempo_actual)
                        contador_pokemons += 1
                        tiempo_inicial = tiempo_actual + 3000
                        aciertos += 1
                    elif pokemon_actual.nombre.lower() != texto.lower():
                        mostrar_silueta = False
                        mostrar_nombres = True
                        tiempo_inicial = tiempo_actual + 3000
                        aciertos = 0
                        guardar_datos_json('./estadisticas.json',datos_a_guardar)
                    else:
                        pass
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
            botones_dificultad.actualizar_color_boton(pos)
            aplicar_filtro = True

    if siguiente:
        if aplicar_filtro:
            generaciones_seleccionadas = botones_generaciones.obtener_generaciones_seleccionadas()
            lista_pokemons_filtrada = pokemon_actual.filtrar_pokemons(lista_pokemons, generaciones_seleccionadas)
            aplicar_filtro = False

        if lista_pokemons_filtrada:
            pokemon_actual = random.choice(lista_pokemons_filtrada)
        mostrar_silueta = True
        mostrar_nombres = False
        siguiente = False

    if not mostrar_silueta and tiempo_actual - animacion.tiempo_inicial >= animacion.tiempo_maximo:
        tiempo_inicio_respuesta = pygame.time.get_ticks()
        pokemon_actual = random.choice(lista_pokemons)
        mostrar_silueta = True 
        animacion.tiempo_inicial = 0
        siguiente = True
        mostrar_nombres = False

    ventana.fill(AZUL_CLARO)

    botones_generaciones.dibujar_botones_generacion(ventana, NEGRO, fuente)
    botones_dificultad.dibujar_botones_dificultad(ventana, NEGRO, fuente)
    dificultad_seleccionada = botones_dificultad.obtener_dificutlad_seleccioanda()
    
    pokemon_actual.dibujar(ventana, mostrar_silueta, dificultad_seleccionada)

    pygame.draw.rect(ventana, BLANCO, input_rect)
    superficie_texto = fuente.render(texto, True, NEGRO)
    contador_aciertos = fuente.render(f'{aciertos}/10', True, NEGRO)
    ventana.blit(superficie_texto, (input_rect.x + 5, input_rect.y + (input_rect.height - superficie_texto.get_height()) // 2))
    ventana.blit(texto_superior, (ANCHO_VENTANA // 2 - texto_superior.get_width() // 2, 50))
    ventana.blit(texto_generaciones, (110, 515))
    ventana.blit(texto_dificultad, (498, 515))
    ventana.blit(contador_aciertos, (ANCHO_VENTANA // 2 - 20, ALTO_VENTANA // 2 + 85))


    # Pruebas
    nombre_pokemon = fuente.render(f'{pokemon_actual.nombre} {pokemon_actual.generacion}', True, NEGRO)
    ventana.blit(nombre_pokemon, (50, 50))

    animacion.actualizar(tiempo_actual)
    animacion.dibujar(ventana, (input_rect.right + 50, input_rect.y + (input_rect.height - 90) // 2))
 
    if mostrar_nombres:
        pokemon_actual.nombres(lista_nombre, fuente, NEGRO, ventana)
        ventana.blit(reino_unido, (0,168))
        ventana.blit(francia, (0,218))
        ventana.blit(italia, (0,268))
        ventana.blit(alemania, (0,318))

    texto_contador_tiempo = fuente.render(f'Time: {contador_tiempo}s', True, NEGRO)
    texto_contador_pokemons = fuente.render(f'Pokemons: {contador_pokemons}', True, NEGRO)
    ventana.blit(texto_contador_tiempo, (ANCHO_VENTANA - texto_contador_tiempo.get_width() - 10, 10))
    ventana.blit(texto_contador_pokemons, (ANCHO_VENTANA - texto_contador_pokemons.get_width() - 10, 40))

    datos_a_guardar = {
    "aciertos": aciertos,
    "contador_tiempo": contador_tiempo,
    "contador_pokemons": contador_pokemons,
    }

    pygame.display.update()

pygame.quit()