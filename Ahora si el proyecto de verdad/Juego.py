import pygame
import Constantes
from Personaje import Personaje
import os
from Obstaculos import Ladrillo

pygame.init() # Inicializa todos los módulos de Pygame necesarios

def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height() # Corregido: antes tenías image.get_width() aquí también
    nueva_imagen = pygame.transform.scale(image, (w * scale, h * scale))
    return nueva_imagen

# Configuración de la ventana del juego
def pantalla_muerte(ventana):
    """Muestra la pantalla de muerte y devuelve True si el usuario quiere reiniciar.
    Teclas: R = reiniciar, Q o ESC = salir."""
    fuente_grande = pygame.font.SysFont(None, 72)
    fuente_peq = pygame.font.SysFont(None, 30)
    reloj_muerte = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    return False

        ventana.fill(Constantes.COLOR_BG)
        texto = fuente_grande.render("¡Has muerto!", True, (255, 0, 0))
        subt = fuente_peq.render("Presiona R para reiniciar  Q o ESC para salir", True, (255, 255, 255))
        ventana.blit(texto, texto.get_rect(center=(Constantes.ANCHO//2, Constantes.ALTO//2 - 30)))
        ventana.blit(subt, subt.get_rect(center=(Constantes.ANCHO//2, Constantes.ALTO//2 + 30)))
        pygame.display.update()
        reloj_muerte.tick(30)


def game_loop():
    # inicializaciones por partida
    ventana = pygame.display.set_mode((Constantes.ANCHO, Constantes.ALTO))
    pygame.display.set_caption("Mi primer juego")

    # --- CARGA DE RECURSOS ---
    
    # 1. Fondo
    try:
        imagen_fondo = pygame.image.load("Ahora si el proyecto de verdad/assets/images/calle.PNG")
        imagen_fondo = pygame.transform.scale(imagen_fondo, (Constantes.ANCHO, Constantes.ALTO))
    except (pygame.error, FileNotFoundError):
        print("ADVERTENCIA: No se pudo cargar la imagen de fondo. Usando fondo sólido.")
        imagen_fondo = None

    img_corazon_lleno = None
    img_corazon_vacio = None
    try:
        raw_lleno = pygame.image.load("Ahora si el proyecto de verdad/assets/Corazon.webp")
        raw_vacio = pygame.image.load("Ahora si el proyecto de verdad/assets/Sinvida.webp")
        # Escalamos a un tamaño pequeño (ej. 40x40 pixeles) para el HUD
        img_corazon_lleno = pygame.transform.scale(raw_lleno, (40, 40))
        img_corazon_vacio = pygame.transform.scale(raw_vacio, (40, 40))
    except (pygame.error, FileNotFoundError) as e:
        print(f"ADVERTENCIA: No se pudieron cargar los corazones ({e}). Se usarán cuadros de color.")

    # Personaje 
    animaciones = []
    try:
        for i in range(6):
            # Asegúrate de que esta ruta sea correcta en tu carpeta
            img = pygame.image.load(f"Borradores/assets/images/characters/sprite{i}.png")
            img = escalar_img(img, Constantes.SCALA_PERSONAJE)
            animaciones.append(img)
    except (pygame.error, FileNotFoundError):
        print("Error cargando sprites del personaje. Revisa la ruta.")
        # Generar cuadros negros de emergencia si falla la carga para que no crashee
        surf = pygame.Surface((50,50))
        surf.fill((255,255,255))
        animaciones = [surf] * 6

    suelo_inicial_y = 430
    jugador = Personaje(50, suelo_inicial_y, animaciones)

    y_obstaculo = suelo_inicial_y - Constantes.ALTO_OBS
    obstaculo_actual = Ladrillo(600, y_obstaculo, Constantes.ANCHO_OBS, Constantes.ALTO_OBS)

    mover_arriba = False
    mover_abajo = False
    mover_izquierda = False
    mover_derecha = False
    saltar = False

    # Vidas / HUD
    max_vidas = 3
    vidas = max_vidas
    hit_cooldown_ms = 1000  # tiempo de invulnerabilidad tras recibir daño
    last_hit_time = -hit_cooldown_ms

    reloj = pygame.time.Clock()
    run = True

    # --- BUCLE PRINCIPAL DEL JUEGO ---
    while run:
        reloj.tick(Constantes.FPS)

        # Lógica de Scroll
        if mover_derecha:
            Constantes.scroll_x -= Constantes.scroll_speed

        if abs(Constantes.scroll_x) > Constantes.ANCHO:
            Constantes.scroll_x = 0

        # Dibujar Fondo
        if imagen_fondo:
            ventana.blit(imagen_fondo, (Constantes.scroll_x, 0))
            ventana.blit(imagen_fondo, (Constantes.scroll_x + Constantes.ANCHO, 0))
        else:
            ventana.fill(Constantes.COLOR_BG)

        delta_x = 0
        delta_y = 0

        # Lógica de Teclas
        if not jugador.en_el_aire:
            if mover_arriba:
                delta_y = -5
            if mover_abajo:
                delta_y = 5

        if saltar:
            jugador.salto()

        jugador.corriendo = mover_izquierda or mover_derecha

        # Actualización Jugador
        jugador.movimiento(delta_x, delta_y)
        jugador.update()
        jugador.dibujar(ventana)

        # Obstáculos
        obstaculo_actual.forma.x = obstaculo_actual.initial_x + Constantes.scroll_x
        pygame.draw.rect(ventana, Constantes.Blue, obstaculo_actual.forma)
        
        # Colisión con obstáculo
        if jugador.forma.colliderect(obstaculo_actual.forma):
            ahora = pygame.time.get_ticks()
            if ahora - last_hit_time > hit_cooldown_ms:
                vidas -= 1
                jugador.forma.center = (50, suelo_inicial_y)
                jugador.en_el_aire = False
                jugador.velocidad_y = 0
                Constantes.scroll_x = 0
                
                if vidas <= 0:
                    run = False

        # Eventos (Teclado / Salir)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    mover_derecha = True
                if event.key == pygame.K_w:
                    mover_arriba = True
                if event.key == pygame.K_s:
                    mover_abajo = True
                if event.key == pygame.K_SPACE:
                    saltar = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    mover_derecha = False
                if event.key == pygame.K_w:
                    mover_arriba = False
                if event.key == pygame.K_s:
                    mover_abajo = False
                if event.key == pygame.K_SPACE:
                    saltar = False

        for i in range(max_vidas):
            x = 10 + i * 45  # Separación horizontal
            y = 10           # Separación vertical desde arriba
            
            # Determinar qué imagen usar
            imagen_a_dibujar = None
            if i < vidas:
                imagen_a_dibujar = img_corazon_lleno
            else:
                imagen_a_dibujar = img_corazon_vacio
            
            # Dibujar la imagen si existe
            if imagen_a_dibujar:
                ventana.blit(imagen_a_dibujar, (x, y))
            else:
                # Fallback: dibujar un cuadro si la imagen falló al cargar
                color = (255, 0, 0) if i < vidas else (100, 100, 100)
                pygame.draw.rect(ventana, color, (x, y, 30, 30))

        pygame.display.update()

    # Al salir del while, mostramos pantalla de muerte
    return pantalla_muerte(ventana)

if __name__ == "__main__":
    try:
        while True:
            reiniciar = game_loop()
            if not reiniciar:
                break
            # Reset global state for a fresh start
            Constantes.scroll_x = 0
    finally:
        pygame.quit()