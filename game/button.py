import pygame
# Colores (RGB)
PURPLE = (147, 112, 219)
AQUA = (127, 255, 212)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 182, 193)  # Color rosa para botones
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)  # Color verde para respuestas correctas
class Button:
    def __init__(self, x: int, y: int, width: int, height: int,text,base_color,hovering_color,font, image):
        #en caso de que el boton tenga imagen de fondo
        self.image = image
        self.x_pos = x
        self.y_pos = y
        
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

        #color base y color de hooving (mouse encima del boton)
        self.base_color, self.hovering_color = base_color, hovering_color
       
        self.font = font
        self.textd = self.font.render(self.text, True, self.base_color)
       
        if self.image is None:
            self.image = self.textd
            
        self.radius = 20
        self.is_hovered = False
        
        #contorno o hitbox del boton creado para comprobar clicks
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.textd_rect = self.textd.get_rect(center=(self.x_pos, self.y_pos))

    def draw(self, screen: pygame.Surface):
        color = RED if self.is_hovered else PINK  # Cambiado a rosa/rojo

        pygame.draw.rect(screen, color, self.rect, border_radius=self.radius)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def update_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def checkForInput(self, screen):
        action = False
        # obtenemos constantemente la posicion del mouse en ventana
        position = pygame.mouse.get_pos()

        #cambia color si se sobrepone el cursor en el boton
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            # Si las coordenadas del mouse están dentro del rectángulo definido por self.rect,
            # cambia el color del texto a self.hovering_color.
            self.textd = self.font.render(self.text, True, self.hovering_color)
        else:
                # Si las coordenadas del mouse no están dentro del rectángulo,
            # cambia el color del texto a self.base_color.
            self.textd = self.font.render(self.text, True, self.base_color)
    

        # comprueba si hizo click sobre el boton
        if self.rect.collidepoint(position):
            # Verifica si la posición actual del mouse está dentro del rectángulo definido por self.rect.
            if pygame.mouse.get_pressed()[0] == 1:
                # Si el botón izquierdo del mouse se presiono y self.clicked es False (es decir, no se ha hecho click previamente),
                # establece self.clicked en True y action se cambia a True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            # Si el botón izquierdo del mouse se presiono, establece self.clicked en False.
            self.clicked = False

        # dibujamos en pantalla
        screen.blit(self.textd, self.textd_rect)
        return action