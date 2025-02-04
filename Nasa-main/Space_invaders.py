import pygame
import random
from quiz_handler import QuizHandler

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 16*60, 9*60
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders Quiz")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fuente para el texto
font = pygame.font.SysFont("Arial", 20)

# Cargar la imagen de la nave
nave_image = pygame.image.load('images/nave.png')
nave_image = pygame.transform.scale(nave_image, (100, 100))  # Escalar la imagen a un tamaño adecuado

# Cargar varias imágenes de transición para respuestas correctas
correct_images = [
    pygame.image.load('images/IMG1.jpg'),
    pygame.image.load('images/IMG2.jpg'),
    pygame.image.load('images/IMG3.jpg'),
    pygame.image.load('images/IMG4.jpg'),
    pygame.image.load('images/IMG5.jpg'),
    pygame.image.load('images/IMG6.jpg')
]
# Escalar todas las imágenes al tamaño de la ventana
correct_images = [pygame.transform.scale(img, (WIDTH, HEIGHT)) for img in correct_images]

# Cargar varias imágenes de transición para respuestas incorrectas
incorrect_images = [
    pygame.image.load('images/IMGX1.jpg'),
    pygame.image.load('images/IMGX2.jpg'),
    pygame.image.load('images/IMGX3.jpg'),
    pygame.image.load('images/IMGX4.jpg'),
    pygame.image.load('images/IMGX5.jpg'),
    pygame.image.load('images/IMGX6.jpg')
]
# Escalar todas las imágenes al tamaño de la ventana
incorrect_images = [pygame.transform.scale(img, (WIDTH, HEIGHT)) for img in incorrect_images]

# Inicializar el índice de imagen correcta/incorrecta
current_image_index = 0

# Inicializar el manejador de preguntas
quiz = QuizHandler()

# Clase para la nave del jugador
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, nave_image.get_width(), nave_image.get_height())
        self.lasers = []
        self.lives = 3  # Número de vidas iniciales
        self.shoot_cooldown = 0  # Cooldown para disparar

    def move(self, dx):
        self.rect.x += dx
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width

    def shoot(self):
        if self.shoot_cooldown == 0:  # Solo dispara si el cooldown ha terminado
            laser = pygame.Rect(self.rect.centerx - 2, self.rect.y - 10, 4, 10)
            self.lasers.append(laser)
            self.shoot_cooldown = 20  # Cooldown de 20 frames entre disparos

    def draw(self, surface):
        surface.blit(nave_image, (self.rect.x, self.rect.y))
        for laser in self.lasers:
            pygame.draw.rect(surface, RED, laser)  # Cambiar el color del láser a rojo

    def update_cooldown(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

# Clase para los enemigos
class Enemy:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.lasers = []
        self.shoot_cooldown = random.randint(50, 150)  # Cooldown inicial aleatorio

    def shoot(self):
        if self.shoot_cooldown == 0:  # Dispara solo si el cooldown ha terminado
            laser = pygame.Rect(self.rect.centerx - 2, self.rect.y + self.rect.height, 4, 10)
            self.lasers.append(laser)
            self.shoot_cooldown = random.randint(30, 100)  # Cooldown entre disparos aleatorio

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)
        text_surface = font.render(self.text, True, BLACK)
        surface.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))
        # Dibujar los láseres de los enemigos
        for laser in self.lasers:
            pygame.draw.rect(surface, GREEN, laser)  # Cambiar el color del láser a verde

    def update_cooldown(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

# Inicializar la nave del jugador
player = Player(WIDTH // 2 - 25, HEIGHT - 100)

# Inicializar los enemigos
enemies = []

# Pregunta actual
quiz.get_next_question()

# Colocar las respuestas en los "invaders"
def place_enemies():
    enemies.clear()  # Limpiar los enemigos
    for i, answer in enumerate(quiz.current_answers):
        x_pos = 100 + i * 150
        enemies.append(Enemy(x_pos, 100, 100, 50, answer))

place_enemies()

# Velocidad de los enemigos
enemy_dx = 2
enemy_dy = 20

# Función para mostrar las vidas en la pantalla
def draw_lives(surface, lives):
    lives_text = font.render(f'Vidas: {lives}', True, WHITE)
    surface.blit(lives_text, (10, 10))

# Función para mostrar la pregunta en la pantalla
def draw_question(surface, question):
    question_text = font.render(question, True, WHITE)
    surface.blit(question_text, (WIDTH // 2 - question_text.get_width() // 2, 20))

# Función para mostrar la pantalla de Game Over
def draw_game_over(surface):
    game_over_text = font.render("Game Over!", True, RED)
    surface.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 20))

# Función para mostrar la pantalla de inicio
def show_start_screen():
    # Cargar la imagen de la pantalla de inicio
    start_image = pygame.image.load('images/start_screen.jpg')
    start_image = pygame.transform.scale(start_image, (WIDTH, HEIGHT))  # Escalar la imagen a la ventana
    while True:
        win.fill(BLACK)
        win.blit(start_image, (0, 0))  # Dibujar la imagen de la pantalla de inicio
        
        # Mostrar el mensaje "Presione S para iniciar"
        start_message = font.render("Presione S para iniciar", True, WHITE)
        win.blit(start_message, (WIDTH // 2 - start_message.get_width() // 2, HEIGHT - 40))  # Centrar en la parte inferior
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:  # Esperar a que el jugador presione 'S'
                return  # Salir de la pantalla de inicio

# Llamar a la pantalla de inicio antes de comenzar el juego
show_start_screen()

# Juego principal
running = True
game_over = False
show_image = False  # Estado para mostrar la imagen
image_type = "correct"  # Define el tipo de imagen a mostrar
while running:
    pygame.time.delay(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    # Solo permite mover la nave y disparar si no hay Game Over
    if not game_over:
        if keys[pygame.K_LEFT]:
            player.move(-10)
        if keys[pygame.K_RIGHT]:
            player.move(10)
        if keys[pygame.K_SPACE]:
            player.shoot()
    
    if game_over and keys[pygame.K_r]:  # Reiniciar el juego
        player.lives = 3
        enemy_dx = 2
        place_enemies()
        quiz.get_next_question()
        game_over = False
        show_image = False  # Reiniciar estado de imagen

    if show_image and keys[pygame.K_s]:  # Avanzar a la siguiente pregunta
        show_image = False
        quiz.get_next_question()
        place_enemies()

    # Actualizar cooldown de disparo del jugador
    player.update_cooldown()

    # Mover los láseres del jugador
    for laser in player.lasers[:]:
        laser.y -= 10
        if laser.y < 0:
            player.lasers.remove(laser)

    # Mover los enemigos
    for enemy in enemies:
        enemy.rect.x += enemy_dx
        enemy.update_cooldown()  # Actualizar cooldown de los enemigos
        enemy.shoot()  # Hacer que el enemigo dispare

    # Si alguno de los enemigos toca los bordes, todos cambian de dirección y bajan
    if any(enemy.rect.x <= 0 or enemy.rect.x >= WIDTH - enemy.rect.width for enemy in enemies):
        enemy_dx *= -1
        for enemy in enemies:
            enemy.rect.y += enemy_dy

    # Comprobar colisiones entre los disparos del jugador y los enemigos
    for laser in player.lasers[:]:
        for i, enemy in enumerate(enemies[:] ):
            if laser.colliderect(enemy.rect):
                if quiz.check_answer(i):
                    # Respuesta correcta
                    show_image = True
                    image_type = "correct"
                    current_image_index = random.randint(0, len(correct_images) - 1)
                    place_enemies()  # Colocar nuevos enemigos (puedes ajustar según sea necesario)
                    # Aumentar la velocidad de los enemigos cada vez que se responde correctamente
                    enemy_dx += 0.5
                    enemy_dy += 1
                else:
                    # Respuesta incorrecta
                    show_image = True 
                    image_type = "incorrect"
                    current_image_index = quiz.get_current_question_number() % len(incorrect_images)
                    place_enemies()
                    player.lives -= 1  # Restar una vida
                player.lasers.remove(laser)
                break

    # Comprobar si el jugador se queda sin vidas
    if player.lives <= 0:
        game_over = True

    # Comprobar colisiones entre los disparos enemigos y la nave del jugador
    for enemy in enemies:
        for laser in enemy.lasers[:]:
            laser.y += 5
            if laser.colliderect(player.rect):  # Verifica colisión con la nave del jugador
                player.lives -= 1  # Resta una vida si hay colisión
                enemy.lasers.remove(laser)  # Elimina el láser después de la colisión
            # Eliminar láseres fuera de la pantalla
            if laser.y > HEIGHT:
                enemy.lasers.remove(laser)

    # Dibujar en la ventana
    win.fill(BLACK)
    if show_image:
        # Mostrar la imagen correcta o incorrecta
        if image_type == "correct":
            win.blit(correct_images[current_image_index], (0, 0))
        else:
            win.blit(incorrect_images[current_image_index], (0, 0))
    else:
        # Dibujar el estado del juego
        draw_lives(win, player.lives)
        draw_question(win, quiz.current_question)
        player.draw(win)
        for enemy in enemies:
            enemy.draw(win)

    if game_over:
        draw_game_over(win)

    pygame.display.update()

pygame.quit()
