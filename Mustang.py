import pygame

class Mustang():
    def _init_(self, x, y, velocidad, ancho=200, alto=200, frames=None):
        # Inicialización de posición y dimensiones
        self.x = float(x)  # Usamos float para movimientos suaves y precisos
        self.y = float(y)
        self.ancho = int(ancho)
        self.alto = int(alto)
        
        # Velocidad: Si es positiva va a la derecha, negativa a la izquierda
        self.velocidad = velocidad 
        self.color = (255, 255, 255) # Color blanco por defecto (si no hay imágenes)

        # Crea el rectángulo (hitbox) para colisiones y posicionamiento.
        # Es importante tener esto para interactuar con otros objetos en Pygame.
        self.rect = pygame.Rect(int(self.x), int(self.y), self.ancho, self.alto)

        
        # Guardamos la lista de imágenes (frames). Si no pasan ninguna, creamos una lista vacía.
        self.frames = list(frames) if frames else []
        
        # OPTIMIZACIÓN: Pre-calculamos las imágenes invertidas (mirando a la izquierda).
        # Hacemos esto aquí una sola vez en lugar de hacerlo en cada frame del juego (lo cual sería lento).
        # pygame.transform.flip(imagen, flip_x, flip_y) -> True en X voltea horizontalmente.
        self.frames_flipped = [pygame.transform.flip(f, True, False) for f in self.frames] if self.frames else []
        
        self.frame_index = 0  # Índice para saber qué imagen de la lista mostrar (0, 1, 2...)
        self.frame_time = pygame.time.get_ticks() # Marca de tiempo del último cambio de imagen
        self.frame_cooldown = 150  # Tiempo en milisegundos que debe pasar antes de cambiar al siguiente frame

    def dibujar(self, ventana):
        # Si existen imágenes (frames), usamos la lógica de animación
        if self.frames:
            now = pygame.time.get_ticks() # Tiempo actual en ms
            
            # Decidimos qué lista de imágenes usar según la dirección:
            # Si velocidad >= 0 (derecha/quieto) usa self.frames
            # Si velocidad < 0 (izquierda) usa self.frames_flipped
            seq = self.frames if self.velocidad >= 0 else (self.frames_flipped or [pygame.transform.flip(f, True, False) for f in self.frames])
            
            # Obtenemos la imagen actual usando el operador módulo (%) para que el índice
            # siempre se mantenga dentro del rango de la lista (ej: si llega al final, vuelve a 0).
            img = seq[self.frame_index % len(seq)]
            
            # Dibujamos la imagen en la pantalla (ventana)
            ventana.blit(img, (int(self.x), int(self.y)))
            
            # --- Sincronización ---
            # Es CRUCIAL actualizar la posición del rectángulo invisible (hitbox)
            # para que coincida con donde acabamos de dibujar la imagen.
            self.rect.topleft = (int(self.x), int(self.y))
            
            # Nos aseguramos de que el rect tenga el tamaño correcto
            self.rect.width = self.ancho
            self.rect.height = self.alto
            
            # --- Control de tiempo de animación ---
            # Si ha pasado suficiente tiempo (150ms) desde el último frame...
            if now - self.frame_time > self.frame_cooldown:
                self.frame_index = (self.frame_index + 1) % len(seq) # Pasamos a la siguiente imagen
                self.frame_time = now # Reseteamos el contador de tiempo
        
        # Si NO hay imágenes (frames), dibujamos un rectángulo simple
        else:
            # Actualizamos la posición del rect
            self.rect.topleft = (int(self.x), int(self.y))
            self.rect.width = self.ancho
            self.rect.height = self.alto
            
            # Dibujamos el rectángulo de color sólido
            pygame.draw.rect(ventana, self.color, self.rect)

    def movimiento(self):
        # Actualiza la posición X sumando la velocidad.
        # Al ser float, permite velocidades decimales (ej: 2.5 pixeles por frame).
        self.x += float(self.velocidad)