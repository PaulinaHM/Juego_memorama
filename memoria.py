import pygame
import sys
import math
import time
import random
from detalles import *
from detalles import SONIDOS
pygame.mixer.Sound.play(SONIDOS["clic"])


#Iniciamos todo lo de Pygame para poder usar sonido, pantalla, imagenes y efectos


pygame.init()
pygame.font.init()
pygame.mixer.init()

# Lo siguiente configura la parte trasera de cada tarjeta
nombre_imagen_oculta = "archivos/oculta.png"
imagen_oculta = pygame.image.load(nombre_imagen_oculta)
segundos_mostrar_pieza = 2  # Segundos para ocultar la pieza si no es la correcta


class Cuadro:
    def __init__(self, fuente_imagen):
        self.mostrar = True
        self.descubierto = False
        self.fuente_imagen = fuente_imagen
        self.imagen_real = pygame.image.load(fuente_imagen)


#Toda la configuración del juego que al final se toma como un arreglo de objetos

cuadros = [
    [Cuadro("archivos/coco.png"), Cuadro("archivos/coco.png"),
     Cuadro("archivos/manzana.png"), Cuadro("archivos/manzana.png")],
    [Cuadro("archivos/limón.png"), Cuadro("archivos/limón.png"),
     Cuadro("archivos/naranja.png"), Cuadro("archivos/naranja.png")],
    [Cuadro("archivos/pera.png"), Cuadro("archivos/pera.png"),
     Cuadro("archivos/piña.png"), Cuadro("archivos/piña.png")],
    [Cuadro("archivos/plátano.png"), Cuadro("archivos/plátano.png"),
     Cuadro("archivos/sandía.png"), Cuadro("archivos/sandía.png")],
]



# Calculamos el tamaño de la pantalla en base al tamaño de los cuadrados
anchura_pantalla = len(cuadros[0]) * medida_cuadro
altura_pantalla = (len(cuadros) * medida_cuadro) + altura_boton
anchura_boton = anchura_pantalla

def mostrar_menu():
    pantalla_menu = pygame.display.set_mode((anchura_pantalla, altura_pantalla))
    pygame.display.set_caption('Menú - Memorama en Python')
    fuente_menu = pygame.font.SysFont("Arial", 40)

    boton_jugar = pygame.Rect(100, 150, 200, 50)
    boton_salir = pygame.Rect(100, 250, 200, 50)

    ejecutando_menu = True
    while ejecutando_menu:
        pantalla_menu.fill(color_blanco)

        pygame.draw.rect(pantalla_menu, color_azul, boton_jugar)
        pygame.draw.rect(pantalla_menu, color_gris, boton_salir)

        texto_jugar = fuente_menu.render("Iniciar Juego", True, color_blanco)
        texto_salir = fuente_menu.render("Salir", True, color_negro)

        pantalla_menu.blit(texto_jugar, (120, 160))
        pantalla_menu.blit(texto_salir, (160, 260))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(event.pos):
                    ejecutando_menu = False  # Sale del menú y comienza el juego
                elif boton_salir.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

# >>> IMPLEMENTADO: Mostrar menú antes de iniciar el juego
mostrar_menu()

# La fuente que estará sobre el botón
tamanio_fuente = 20
fuente = pygame.font.SysFont("Arial", tamanio_fuente)
xFuente = int((anchura_boton / 2) - (tamanio_fuente / 2))
yFuente = int(altura_pantalla - altura_boton)

# El botón, que al final es un rectángulo
boton = pygame.Rect(0, altura_pantalla - altura_boton,
                    anchura_boton, altura_pantalla)

# Bandera para saber si se debe ocultar la tarjeta dentro de N segundos
ultimos_segundos = None
puede_jugar = True  # Bandera para saber si reaccionar a los eventos del usuario

# Saber si el juego está iniciado; así sabemos si ocultar o mostrar piezas, además del botón
juego_iniciado = False

# Banderas de las tarjetas cuando se busca una pareja. Las necesitamos como índices para el arreglo de cuadros
# x1 con y1 sirven para la primer tarjeta
x1 = None
y1 = None

# Y las siguientes para la segunda tarjeta
x2 = None
y2 = None


# Ocultar todos los cuadros al inicio del juego
def ocultar_todos_los_cuadros():
    for fila in cuadros:
        for cuadro in fila:
            cuadro.mostrar = False
            cuadro.descubierto = False


def aleatorizar_cuadros():
    # Elegir X e Y aleatorios
    cantidad_filas = len(cuadros)
    cantidad_columnas = len(cuadros[0])
    for y in range(cantidad_filas):
        for x in range(cantidad_columnas):
            x_aleatorio = random.randint(0, cantidad_columnas - 1)
            y_aleatorio = random.randint(0, cantidad_filas - 1)
            cuadro_temporal = cuadros[y][x]
            cuadros[y][x] = cuadros[y_aleatorio][x_aleatorio]
            cuadros[y_aleatorio][x_aleatorio] = cuadro_temporal


def comprobar_si_gana():
    if gana():
        pygame.mixer.Sound.play(SONIDOS["exito"])
        reiniciar_juego()


# Regresa False si al menos un cuadro NO está descubierto.
# True en caso de que absolutamente todos estén descubiertos
def gana():
    for fila in cuadros:
        for cuadro in fila:
            if not cuadro.descubierto:
                return False
    return True


def reiniciar_juego():
    global juego_iniciado
    juego_iniciado = False


def iniciar_juego():
    pygame.mixer.Sound.play(SONIDOS ["clic"])
    global juego_iniciado
    # Aleatorizar 3 veces
    for i in range(3):
        aleatorizar_cuadros()
    ocultar_todos_los_cuadros()
    juego_iniciado = True


#Iniciamos la pantalla con las medidas previamente calculadas, colocamos título y reproducimos el sonido de fondo

pantalla_juego = pygame.display.set_mode((anchura_pantalla, altura_pantalla))
pygame.display.set_caption('Memorama en Python')
pygame.mixer.Sound.play(SONIDOS["fondo"], -1)  # El -1 indica un loop infinito
# Ciclo infinito...
while True:
    # Escuchar eventos, pues estamos en un ciclo infinito que se repite varias veces por segundo
    for event in pygame.event.get():
        # Si quitan el juego, salimos
        if event.type == pygame.QUIT:
            sys.exit()
        # cuando detecta el clic, el usuario puede jugar...
        elif event.type == pygame.MOUSEBUTTONDOWN and puede_jugar:

            # Si el click fue sobre el botón y el juego no se ha iniciado, entonces iniciamos el juego
            xAbsoluto, yAbsoluto = event.pos
            if boton.collidepoint(event.pos):
                if not juego_iniciado:
                    iniciar_juego()

            else:
                # Si no hay juego iniciado, ignoramos el clic
                if not juego_iniciado:
                    continue
                
                x = math.floor(xAbsoluto / medida_cuadro)
                y = math.floor(yAbsoluto / medida_cuadro)
                # Si  ya está mostrada o descubierta, no hacemos nada
                cuadro = cuadros[y][x]
                if cuadro.mostrar or cuadro.descubierto:
                    # continue ignora lo de abajo y deja que el ciclo siga
                    continue
                # Si es la primera vez que tocan la imagen (es decir, no están buscando el par de otra, sino apenas están descubriendo la primera)
                if x1 is None and y1 is None:
                    # Entonces la actual es en la que acaban de dar clic, la mostramos
                    x1 = x
                    y1 = y
                    cuadros[y1][x1].mostrar = True
                    pygame.mixer.Sound.play(SONIDOS["voltear"])
                else:
                    # En caso de que ya hubiera una clickeada anteriormente y estemos buscando el par, comparamos...
                    x2 = x
                    y2 = y
                    cuadros[y2][x2].mostrar = True
                    cuadro1 = cuadros[y1][x1]
                    cuadro2 = cuadros[y2][x2]
                    # Si coinciden, entonces a ambas las ponemos en descubiertas:
                    if cuadro1.fuente_imagen == cuadro2.fuente_imagen:
                        cuadros[y1][x1].descubierto = True
                        cuadros[y2][x2].descubierto = True
                        x1 = None
                        x2 = None
                        y1 = None
                        y2 = None
                        pygame.mixer.Sound.play(SONIDOS["clic"])
                    else:
                        pygame.mixer.Sound.play(SONIDOS["fracaso"])
                        # Si no coinciden, tenemos que ocultarlas en el plazo de [segundos_mostrar_pieza] segundo(s). Así que establecemos
                        # la bandera. Como esto es un ciclo infinito y asíncrono, podemos usar el tiempo para saber
                        # cuándo fue el tiempo en el que se empezó a ocultar
                        ultimos_segundos = int(time.time())
                        # Hasta que el tiempo se cumpla, el usuario no puede jugar
                        puede_jugar = False
                comprobar_si_gana()

    ahora = int(time.time())
    # Y aquí usamos la bandera del tiempo, de nuevo. Si los segundos actuales menos los segundos
    # en los que se empezó el ocultamiento son mayores a los segundos en los que se muestra la pieza, entonces
    # se ocultan las dos tarjetas y se reinician las banderas
    if ultimos_segundos is not None and ahora - ultimos_segundos >= segundos_mostrar_pieza:
        cuadros[y1][x1].mostrar = False
        cuadros[y2][x2].mostrar = False
        x1 = None
        y1 = None
        x2 = None
        y2 = None
        ultimos_segundos = None
        # En este momento el usuario ya puede hacer clic de nuevo pues las imágenes ya estarán ocultas
        puede_jugar = True

    # Hacer toda la pantalla blanca
    pantalla_juego.fill(color_blanco)
    # Banderas para saber en dónde dibujar las imágenes, pues al final
    # la pantalla de PyGame son solo un montón de pixeles
    x = 0
    y = 0
    # Recorrer los cuadros
    for fila in cuadros:
        x = 0
        for cuadro in fila:
            """
            Si está descubierto o se debe mostrar, dibujamos la imagen real. Si no,
            dibujamos la imagen oculta
            """
            if cuadro.descubierto or cuadro.mostrar:
                pantalla_juego.blit(cuadro.imagen_real, (x, y))
            else:
                pantalla_juego.blit(imagen_oculta, (x, y))
            x += medida_cuadro
        y += medida_cuadro

    # También dibujamos el botón
    if juego_iniciado:
        # Si está iniciado, entonces botón blanco con fuente gris para que parezca deshabilitado
        pygame.draw.rect(pantalla_juego, color_blanco, boton)
        pantalla_juego.blit(fuente.render(
            "Iniciar juego", True, color_gris), (xFuente, yFuente))
    else:
        pygame.draw.rect(pantalla_juego, color_azul, boton)
        pantalla_juego.blit(fuente.render(
            "Iniciar juego", True, color_blanco), (xFuente, yFuente))

    # Actualizamos la pantalla
    pygame.display.update()