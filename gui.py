import pygame
import json
import random
import os
from typing import Dict, List, Tuple

# Inicialización de Pygame
pygame.init()

# Constantes
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

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
    def __init__(self, x: int, y: int, width: int, height: int, text: str):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.radius = 20
        self.is_hovered = False

    def draw(self, screen: pygame.Surface):
        color = RED if self.is_hovered else PINK  # Cambiado a rosa/rojo
        pygame.draw.rect(screen, color, self.rect, border_radius=self.radius)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def update_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

class Question:
    def __init__(self, question: str, image_path: str, options: List[str], correct_answer: str, category: str):
        self.question = question
        self.image_path = image_path
        self.options = options
        self.correct_answer = correct_answer
        self.category = category
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (200, 200))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Juego Educativo")
        self.clock = pygame.time.Clock()
        
        # Timer
        self.timer = 10 * FPS  # 10 segundos en frames
        self.current_time = self.timer
        self.timer_active = False  # Nueva variable para controlar el timer
        
        # Jugadores
        self.player1_score = 0
        self.player2_score = 0
        self.current_player = None
        self.show_turn_announcement = False
        self.announcement_timer = 0
        
        # Mensaje de retroalimentación
        self.feedback_message = ""
        self.feedback_color = WHITE
        self.feedback_timer = 0
        
        # Botones
        self.buttons = []
        self.update_buttons([])
        
        # Cargar preguntas
        self.questions = self.load_questions()
        self.current_question = None
        
        # Estado del juego
        self.game_state = "playing"
        self.winner = None

    def update_buttons(self, options: List[str]):
        """Actualiza los botones con nuevas opciones"""
        self.buttons = []
        button_width = 150
        button_height = 50
        spacing = (WINDOW_WIDTH - (button_width * 4)) // 5
        for i, option in enumerate(options):
            x = spacing + (i * (button_width + spacing))
            self.buttons.append(Button(x, 500, button_width, button_height, option))

    def show_feedback(self, is_correct: bool):
        """Muestra mensaje de retroalimentación"""
        self.feedback_message = "¡Correcto!" if is_correct else "Incorrecto"
        self.feedback_color = GREEN if is_correct else RED
        self.feedback_timer = 2 * FPS  # Mostrar por 2 segundos
    
    def load_questions(self) -> List[Question]:
        """Carga las preguntas desde un archivo JSON"""
        questions = []
        try:
            with open('questions.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                for q in data['questions']:
                    questions.append(Question(
                        q['question'],
                        q['image_path'],
                        q['options'],
                        q['correct_answer'],
                        q['category']
                    ))
        except FileNotFoundError:
            print("Archivo de preguntas no encontrado")
        return questions

    def select_random_question(self):
        """Selecciona una pregunta aleatoria"""
        if self.questions:
            self.current_question = random.choice(self.questions)
            self.update_buttons(self.current_question.options)
            self.current_time = self.timer
            self.current_player = None
            self.show_turn_announcement = False
            self.timer_active = False  # El timer se detiene al cambiar la pregunta
    
    def check_answer(self, answer: str) -> bool:
        """Verifica si la respuesta es correcta"""
        if self.current_question and answer == self.current_question.correct_answer:
            if self.current_player == 1:
                self.player1_score += 10
            else:
                self.player2_score += 10
            self.show_feedback(True)
            return True
        self.show_feedback(False)
        return False
    
    def draw_turn_announcement(self):
        """Dibuja el anuncio del turno del jugador"""
        if self.show_turn_announcement and self.current_player:
            # Semi-transparente overlay
            s = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            s.set_alpha(128)
            s.fill((255, 255, 255))
            self.screen.blit(s, (0,0))
            
            font = pygame.font.Font(None, 48)
            player_color = RED if self.current_player == 1 else BLUE
            
            text_player = font.render("Jugador", True, player_color)
            text_number = font.render(str(self.current_player), True, player_color)
            
            text_rect_player = text_player.get_rect(center=(WINDOW_WIDTH//2 - 50, WINDOW_HEIGHT//2))
            text_rect_number = text_number.get_rect(center=(WINDOW_WIDTH//2 + 50, WINDOW_HEIGHT//2))
            
            self.screen.blit(text_player, text_rect_player)
            self.screen.blit(text_number, text_rect_number)

    def draw_game_over(self):
        """Dibuja la pantalla de fin de juego"""
        s = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        s.set_alpha(128)
        s.fill((0, 0, 0))
        self.screen.blit(s, (0,0))

        font = pygame.font.Font(None, 74)
        if self.winner:
            text = font.render(f"¡Jugador {self.winner} Gana!", True, RED if self.winner == 1 else BLUE)
        else:
            text = font.render("¡Empate!", True, WHITE)
        
        text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        self.screen.blit(text, text_rect)

        # Instrucciones para reiniciar
        font_small = pygame.font.Font(None, 36)
        restart_text = font_small.render("Presiona ESPACIO para jugar de nuevo", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
    def draw(self):
        """Dibuja todos los elementos en pantalla"""
        # Fondo
        self.screen.fill(AQUA)
        
        # Barra superior
        pygame.draw.rect(self.screen, PURPLE, (0, 0, WINDOW_WIDTH, 60))
        
        # Timer bar
        timer_width = (self.current_time / self.timer) * WINDOW_WIDTH
        pygame.draw.rect(self.screen, PURPLE, (0, 70, timer_width, 10))
        
        # Puntuaciones
        font = pygame.font.Font(None, 36)
        score1 = font.render(f"Jugador 1: {self.player1_score}", True, BLACK)
        score2 = font.render(f"Jugador 2: {self.player2_score}", True, BLACK)
        self.screen.blit(score1, (50, 20))
        self.screen.blit(score2, (WINDOW_WIDTH - 200, 20))
        
        if self.current_question:
            # Pregunta
            question_font = pygame.font.Font(None, 40)
            question_text = question_font.render(self.current_question.question, True, BLACK)
            question_rect = question_text.get_rect(center=(WINDOW_WIDTH//2, 120))
            self.screen.blit(question_text, question_rect)
            
            # Imagen
            image_rect = self.current_question.image.get_rect(center=(WINDOW_WIDTH//2, 280))
            self.screen.blit(self.current_question.image, image_rect)
        
        # Botones
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update_hover(mouse_pos)
            button.draw(self.screen)
        
        # Mensaje de retroalimentación
        if self.feedback_timer > 0:
            feedback_font = pygame.font.Font(None, 48)
            feedback_text = feedback_font.render(self.feedback_message, True, self.feedback_color)
            feedback_rect = feedback_text.get_rect(center=(WINDOW_WIDTH//2, 400))
            self.screen.blit(feedback_text, feedback_rect)
        
        # Anuncio de turno
        if self.show_turn_announcement:
            self.draw_turn_announcement()
            
        # Pantalla de fin de juego
        if self.game_state == "game_over":
            self.draw_game_over()
        
        pygame.display.flip()

    def reset_game(self):
        """Reinicia el juego"""
        self.player1_score = 0
        self.player2_score = 0
        self.current_player = None
        self.game_state = "playing"
        self.winner = None
        self.select_random_question()
    
    def run(self):
        """Loop principal del juego"""
        running = True
        self.select_random_question()
        
        while running:
            if self.game_state == "playing":
                # Solo actualizar el timer si está activo
                if self.timer_active:
                    self.current_time -= 1
                    if self.current_time <= 0:
                        self.select_random_question()
                
                # Actualizar tiempo de anuncio
                if self.show_turn_announcement:
                    self.announcement_timer -= 1
                    if self.announcement_timer <= 0:
                        self.show_turn_announcement = False
                
                # Actualizar timer de feedback
                if self.feedback_timer > 0:
                    self.feedback_timer -= 1
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if self.game_state == "playing":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q and self.current_player is None:
                            self.current_player = 1
                            self.show_turn_announcement = True
                            self.announcement_timer = 2 * FPS
                            self.timer_active = True  # Activar el timer cuando el jugador 1 toma su turno
                        elif event.key == pygame.K_RIGHTBRACKET and self.current_player is None:
                            self.current_player = 2
                            self.show_turn_announcement = True
                            self.announcement_timer = 2 * FPS
                            self.timer_active = True  # Activar el timer cuando el jugador 2 toma su turno
                    
                    if event.type == pygame.MOUSEBUTTONDOWN and self.current_player is not None:
                        mouse_pos = pygame.mouse.get_pos()
                        for button in self.buttons:
                            if button.rect.collidepoint(mouse_pos):
                                correct = self.check_answer(button.text)
                                
                                # Verificar si alguien ganó
                                if self.player1_score >= 50 or self.player2_score >= 50:
                                    self.game_state = "game_over"
                                    if self.player1_score > self.player2_score:
                                        self.winner = 1
                                    elif self.player2_score > self.player1_score:
                                        self.winner = 2
                                    else:
                                        self.winner = None
                                else:
                                    self.select_random_question()
                
                elif self.game_state == "game_over":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.reset_game()
            
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

def main():
    # Verificar que existe el directorio de imágenes
    if not os.path.exists('images'):
        os.makedirs('images')
        print("Se ha creado el directorio 'images'. Por favor, coloca las imágenes de las preguntas en él.")
    
    # Verificar que existe el archivo de preguntas
    if not os.path.exists('questions.json'):
        print("No se encuentra el archivo 'questions.json'. Por favor, créalo con el formato correcto.")
        return
    
    # Iniciar el juego
    game = Game()
    game.run()

if __name__ == "__main__":
    main()