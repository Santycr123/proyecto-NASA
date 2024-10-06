# quiz_handler.py
import random

class QuizHandler:
    def __init__(self):
        self.questions = [
            {
                "question": "¿Cuántos planetas hay en el sistema solar?",
                "answers": ["4", "6", "8", "10"],
                "correct": 2
            },
            {
                "question": "¿Cuántas estrellas hay en el sistema solar?",
                "answers": ["5", "1", "500", "245"],
                "correct": 1
            },
            {
                "question": "¿?",
                "answers": ["Incorrecta", "Incorrecta", "Incorrecta", "Correcta"],
                "correct": 3
            },
            {
                "question": "¿Cuántos planetas emiten luz en el sistema solar?",
                "answers": ["Ninguno", "Todos", "Los más grandes", "Los más pequeños"],
                "correct": 0
            },
            {
                "question": "¿Todos los planetas en el universo giran alrededor del sol?",
                "answers": ["SI", "NO", "Si, porque el sol es el centro del universo", "No, porque hay más estrellas como el sol"],
                "correct": 3
            }]
        '''
        ,
            {
                "question": "¿Pregunta 6?",
                "answers": ["Incorrecta", "Correcta", "Incorrecta", "Incorrecta"],
                "correct": 1
            },
            {
                "question": "¿Pregunta 7?",
                "answers": ["Incorrecta", "Incorrecta", "Correcta", "Incorrecta"],
                "correct": 2
            },
            {
                "question": "¿Pregunta 8?",
                "answers": ["Correcta", "Incorrecta", "Incorrecta", "Incorrecta"],
                "correct": 0
            },
            {
                "question": "¿Pregunta 9?",
                "answers": ["Incorrecta", "Incorrecta", "Incorrecta", "Correcta"],
                "correct": 3
            },
            {
                "question": "¿Pregunta 10?",
                "answers": ["Correcta", "Incorrecta", "Incorrecta", "Incorrecta"],
                "correct": 0
            }'''
        self.current_question_index = -1
        self.current_answers = []
        self.current_question = ""

    def get_next_question(self):
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.current_question = self.questions[self.current_question_index]["question"]
            self.current_answers = self.questions[self.current_question_index]["answers"]
        else:
            self.current_question = "¡Fin del juego!"
            self.current_answers = []

    def check_answer(self, answer_index):
        if self.current_question_index < len(self.questions):
            correct_index = self.questions[self.current_question_index]["correct"]
            return answer_index == correct_index
        return False

    def get_current_question_number(self):
        return self.current_question_index  # Devuelve el índice de la pregunta actual
