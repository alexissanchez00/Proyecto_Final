Documentación del Proyecto: Juego de Plataformas 2D en Pygame

1. Descripción General

Este proyecto es un videojuego de plataformas de desplazamiento lateral (Side-scroller) desarrollado en Python utilizando la biblioteca Pygame. El juego presenta a un personaje animado que debe esquivar obstáculos, gestionar sus vidas y navegar a través de un escenario con movimiento (scrolling).

2. Requisitos del Sistema

Lenguaje: Python 3.x

Librerías: pygame, os

Instalación de dependencias:

pip install pygame


3. Estructura del Proyecto

El código está modularizado en cuatro archivos principales para separar la lógica, las constantes y las entidades del juego.

/Directorio_Juego
│
├── main.py          # Punto de entrada y bucle principal del juego
├── Constantes.py    # Variables globales de configuración
├── Personaje.py     # Lógica del jugador (física y animación)
├── Obstaculos.py    # Lógica de los bloques/enemigos
│
└── assets/          # (Carpeta inferida) Imágenes y recursos


4. Descripción de Módulos y Clases

A. Constantes.py

Este archivo actúa como un archivo de configuración centralizado. Contiene variables que no cambian durante la ejecución.

Pantalla: ANCHO, ALTO, COLOR_BG, FPS.

Física/Juego: VELOCIDAD, SCALA_PERSONAJE (0.6), scroll_speed (velocidad del fondo).

Colores: Definiciones RGB (ej. Blue para obstáculos).

B. Personaje.py

Define la clase Personaje, que encapsula toda la lógica del avatar del jugador.

Clase: Personaje

__init__(self, x, y, animaciones):

Inicializa la posición y carga las imágenes.

Ajuste de Hitbox: Reduce el rectángulo de colisión (self.forma) al 30% del tamaño de la imagen original para hacer las colisiones más precisas y justas para el jugador.

Inicializa variables físicas: gravedad (0.7) y fuerza de salto (-18).

update(self):

Gestiona la animación del sprite. Alterna frames cada 100ms si el personaje corre o salta.

Si está quieto, resetea al frame 0.

dibujar(self, interfaz):

Dibuja el sprite en pantalla.

Debug: Dibuja un rectángulo rojo alrededor del personaje para visualizar la hitbox.

movimiento(self, delta_x, delta_y):

Aplica gravedad (velocidad_y).

Detecta colisiones con el suelo (self.suelo_y).

Actualiza la posición x e y del rectángulo.

salto(self):

Aplica una velocidad vertical negativa para elevar al personaje, solo si en_el_aire es False.

C. Obstaculos.py

Define los elementos que el jugador debe esquivar.

Clase: Ladrillo

__init__(self, x, y, ancho, alto):

Crea un pygame.Rect.

Almacena initial_x para calcular su posición relativa al desplazamiento del fondo (scroll).

D. main.py

Es el núcleo del juego, encargado de ensamblar todas las piezas.

Funciones Principales:

escalar_img(image, scale): Función utilitaria para redimensionar sprites.

pantalla_muerte(ventana):

Bucle secundario que se activa cuando las vidas llegan a 0.

Permite reiniciar con R o salir con Q/ESC.

game_loop(): Bucle principal.

Carga de Recursos: Fondo y sprites del personaje.

Instanciación: Crea objetos Personaje y Ladrillo.

Sistema de Vidas: Implementa un contador de vidas (3) y un sistema de "Cooldown" (invulnerabilidad temporal) de 1 segundo tras recibir daño.

Scroll Infinito: Mueve el fondo y resetea la posición cuando sale de pantalla.

Inputs: Mapea teclas a booleanos de movimiento.

Colisiones: Detecta jugador.forma.colliderect(obstaculo) y aplica daño/reinicio de posición.

5. Controles

Acción

Tecla

Mover Arriba (Debug)

W

Mover Abajo (Debug)

S


Mover Derecha

D

Saltar

ESPACIO

Reiniciar (en Game Over)

R

Salir

Q o ESC