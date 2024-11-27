import pygame
from typing import Dict, List, Tuple
class Question:
    def __init__(self, question: str, image_path: str, options: List[str], correct_answer: str, category: str):
        self.question = question
        self.image_path = image_path
        self.options = options
        self.correct_answer = correct_answer
        self.category = category
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (200, 200))
        
        def __str__(self):
            return f"Pregunta: {self.question}, Opciones: {self.options}, Respuesta Correcta: {self.correct_answer}, Categoría: {self.category}"