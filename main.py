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
boton_salir = Botones()
boton_reiniciar = Botones()
botones_generaciones.crear_botones_generacion(75, 45, 3, 3, (50, 550), 1)
botones_dificultad.crear_botones_dificultad(110, 45, 3, 1, (500, 550), 1)
boton_salir.crear_boton(ANCHO_VENTANA - 250, ALTO_VENTANA // 2 - 100, 200, 50, NEGRO, "Salir")
boton_reiniciar.crear_boton(ANCHO_VENTANA - 250, ALTO_VENTANA // 2 - 170, 200, 50, NEGRO, "Volver a jugar")

# Seleccionar Pokémon inicial
pokemon_actual = random.choice(lista_pokemons)

# Contadores
contador_tiempo = 0
contador_pokemons = 0
tiempo_inicial = pygame.time.get_ticks()
aciertos = 0
lista_tiempos = []
pokemons_adivinados = []
tiempo_ultima_respuesta = 0
aciertos = 0
max_aciertos = record_aciertos('./record_aciertos.txt', aciertos)


# Banderas
mostrar_silueta = True
siguiente = False
activo = False
flag = True
aplicar_filtro = False
mostrar_nombres = False 
juego = True
juego_terminado = False

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
                        animacion.iniciar(tiempo_actual)
                        tiempo_inicial = tiempo_actual + 3000
                        lista_tiempos.append(contador_tiempo)
                        tiempo_ultima_respuesta = contador_tiempo
                        contador_pokemons += 1
                        aciertos += 1
                        pokemons_adivinados.append({'nombre': pokemon_actual.nombre, 'generacion': pokemon_actual.generacion})
                        if aciertos > max_aciertos:
                            max_aciertos = aciertos
                            record_aciertos('./record_aciertos.txt', aciertos)
                        
                        juego = True
                    elif pokemon_actual.nombre.lower() != texto.lower():
                        juego = False

                    tiempo_inicial = tiempo_actual + 3000
                    texto = ""
                    mostrar_silueta = False
                    mostrar_nombres = True

                else:
                    texto += evento.unicode

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_salir.boton_clickeado(evento.pos):
                flag = False
            elif boton_reiniciar.boton_clickeado(evento.pos):
                contador_tiempo = 0
                contador_pokemons = 0
                tiempo_inicial = pygame.time.get_ticks()
                aciertos = 0
                lista_tiempos = []
                pokemons_adivinados = []
                tiempo_ultima_respuesta = 0
                aciertos = 0
                juego = True
                juego_terminado = False
                print('reiniciar')
            elif input_rect.collidepoint(evento.pos):
                activo = not activo
            else:
                activo = False

            pos = evento.pos
            botones_generaciones.actualizar_color_boton(pos)
            botones_dificultad.actualizar_color_boton(pos)
            aplicar_filtro = True


    if juego and aciertos < 10:
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

        texto_ultima_respuesta = fuente.render(f'Tiempo última respuesta: {tiempo_ultima_respuesta}s', True, NEGRO)
        ventana.blit(texto_ultima_respuesta, (2, 2))

        if lista_tiempos:
            tiempo_promedio_actual = sum(lista_tiempos) / len(lista_tiempos)
        else:
            tiempo_promedio_actual = 0

        texto_promedio_actual = fuente.render(f'Tiempo promedio: {tiempo_promedio_actual:.2f}s', True, NEGRO)
        ventana.blit(texto_promedio_actual, (2, 22))

        texto_aciertos = fuente.render(f'Aciertos: {aciertos}', True, NEGRO)
        ventana.blit(texto_aciertos, (420, 22))

        texto_record_aciertos = fuente.render(f'Record Aciertos: {max_aciertos}', True, NEGRO)
        ventana.blit(texto_record_aciertos, (420, 2))

    else:
        if juego_terminado == False:
            juego_terminado = True
            ventana.fill(AZUL_CLARO)
            guardar_estadisticas('./estadisticas.json', aciertos, lista_tiempos)

        rect_x = 30
        rect_y = 30
        rect_width = 600
        rect_height = 650
        pygame.draw.rect(ventana, BLANCO, (rect_x, rect_y, rect_width, rect_height))

        mejor_tiempo, peor_tiempo, tiempo_promedio = calcular_estadisticas(lista_tiempos)
        texto_resultados = fuente_titulo.render("Resultados del Juego", True, NEGRO)
        texto_aciertos = fuente.render(f'Aciertos: {aciertos}', True, NEGRO)
        texto_mejor_tiempo = fuente.render(f'Mejor tiempo: {mejor_tiempo:.2f}s', True, NEGRO)
        texto_peor_tiempo = fuente.render(f'Peor tiempo: {peor_tiempo:.2f}s', True, NEGRO)
        texto_tiempo_promedio = fuente.render(f'Tiempo promedio: {tiempo_promedio:.2f}s', True, NEGRO)

        ventana.blit(texto_resultados, (ANCHO_VENTANA // 2 - texto_resultados.get_width() // 2, 50))
        ventana.blit(texto_aciertos, (50, 150))
        ventana.blit(texto_mejor_tiempo, (50, 200))
        ventana.blit(texto_peor_tiempo, (50, 250))
        ventana.blit(texto_tiempo_promedio, (50, 300))

        y = 350
        for pokemon in pokemons_adivinados:
            texto_pokemon_adivinado = fuente.render(f'{pokemon["nombre"]} (Generacion {pokemon["generacion"]})', True, NEGRO)
            ventana.blit(texto_pokemon_adivinado, (50, y))
            y += 30

        boton_salir.dibujar_boton(ventana,fuente)
        boton_reiniciar.dibujar_boton(ventana,fuente)

    pygame.display.update()

pygame.quit()