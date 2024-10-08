import pygame
import random
from collections import deque, Counter


# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Card Counting Trainer")
font = pygame.font.Font(None, 36)

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Definir los rank y los suits
rank = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
suits = ['diamonds', 'clubs', 'hearts', 'spades']


def draw_menu():
    # Create the main menu with configuration options and their color (RGB)
    screen.fill((0, 0, 0))
    title = font.render("Deckout", True, (201, 52, 52))
    
    # Split the description into multiple lines
    desc_lines = [
        "Get a stack of 5 cards, each turn draw a new card",
        "and get the best combinations luck/probability can give you"
    ]
    
    goal = font.render("The rarer your hand, the most points you get!", True, (150, 100, 130))
    text = font.render("Points per hand:", True, (255, 255, 255))
    
    # Split the points text into multiple lines
    points_lines = [
        "Royal Flush +9  ~  Straight Flush +8  ~  Poker +7",
        "Full House +6  ~  Flush +5  ~  Straight +4",
        "Three OaK +3  ~  Two Pair +2  ~  Pair +1"
    ]
    
    play_button = font.render("Play", True, (0, 255, 0))
    
    # Add the text to the menu and its position (horizontal, vertical)
    screen.blit(title, (340, 100))
    
    # Render and blit each line of the description
    #y_offset = 200
    #for line in desc_lines:
    #    desc = font.render(line, True, (66, 166, 252))
    #    screen.blit(desc, (120-y_offset/3, y_offset))
    #    y_offset += 40  # Adjust the vertical spacing as needed
    
    #screen.blit(goal, (150, 150))
    #screen.blit(text, (100, 300))
    
    # Render and blit each line of the points text
    y_offset = 200
    for line in points_lines:
        points = font.render(line, True, (255, 255, 255))
        screen.blit(points, (100, y_offset))
        y_offset += 40  # Adjust the vertical spacing as needed
    
    screen.blit(play_button, (350, 500))

    pygame.display.flip()
    
    
def menu():
    """Display the main menu and handle user inputs to set the game configuration."""
    global speed, num_cards
    draw_menu()
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                waiting_for_input = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Si el jugador presiona Enter
                    waiting_for_input = False
                    # Actualizar la pantalla
                    pygame.display.flip()
                    screen.fill(BLACK)  # Rellena toda la pantalla con un color blanco



# Generar todas las combinaciones posibles de cartas
baraja = [(ranking, suit) for ranking in rank for suit in suits]

# Barajar las cartas
random.shuffle(baraja)

# Crear una pila y colocar las cartas en ella
pila = []
for carta in baraja:
    pila.append(carta)

# Cargar imágenes de cartas (deberían estar en una carpeta 'images/cards/')
card_images = {}
for ranking in rank:
    for suit in suits:
        card_file = f'images/cards/{ranking}_of_{suit}.png'
        image = pygame.image.load(card_file)
        image = pygame.transform.scale(image, (100, 140))  # Redimensionar las cartas
        card_images[(ranking, suit)] = image
        
        
# Crear una cola
cola = deque()

# Crear la cola "quemadas"
quemadas = deque()

# Función para verificar si es escalera
def es_escalera(ranking_mano):
    # Crear un diccionario para mapear rank a índices
    indices = {rank[i]: i for i in range(len(rank))}
    indices_mano = sorted(indices[ranking] for ranking in ranking_mano)

    # Verificar si los índices son consecutivos
    escalera_normal = all(indices_mano[i] + 1 == indices_mano[i + 1] for i in range(len(indices_mano) - 1))

    # Verificar la escalera especial A 2 3 4 5
    escalera_especial = indices_mano == [0, 1, 2, 3, 12]  # Índices correspondientes a A, 2, 3, 4, 5

    return escalera_normal or escalera_especial


# Función para analizar la cola y calcular puntos
def analizar_cola(cola):
    if len(cola) < 5:
        return 0  # No hay suficientes cartas para formar una tupla de 5

    # Obtener las últimas 5 cartas
    ultima_mano = list(cola)[-5:]
    ranking_mano = [carta[0] for carta in ultima_mano]
    suits_mano = [carta[1] for carta in ultima_mano]

    # Contar las ocurrencias de cada ranking y suit
    conteo_ranking = Counter(ranking_mano)
    conteo_palos = Counter(suits_mano)
    puntos = 0

    # Verificar combinaciones
    if 5 in conteo_ranking.values():
        puntos += 10  # Quintilla
    elif sorted(ranking_mano) == ['10', 'ace', 'jack', 'king', 'queen'] and len(set(suits_mano)) == 1:
        puntos += 9  # Flor Imperial
    elif len(set(suits_mano)) == 1 and es_escalera(ranking_mano):
        puntos += 8  # Escalera de Color
    elif 4 in conteo_ranking.values():
        puntos += 7  # Poker
    elif 3 in conteo_ranking.values() and 2 in conteo_ranking.values():
        puntos += 6  # Full House
    elif len(set(suits_mano)) == 1:
        puntos += 5  # Color
    elif es_escalera(ranking_mano):
        puntos += 4  # Escalera
    elif 3 in conteo_ranking.values():
        puntos += 3  # Tercia
    elif list(conteo_ranking.values()).count(2) == 2:
        puntos += 2  # Doble Par
    elif 2 in conteo_ranking.values():
        puntos += 1  # Par

    return puntos

def obtener_nombre_combinacion(puntos):
    if puntos == 10:
        return "Quintilla"
    elif puntos == 9:
        return "Flor Imperial"
    elif puntos == 8:
        return "Escalera de Color"
    elif puntos == 7:
        return "Poker"
    elif puntos == 6:
        return "Full House"
    elif puntos == 5:
        return "Color"
    elif puntos == 4:
        return "Escalera"
    elif puntos == 3:
        return "Tercia"
    elif puntos == 2:
        return "Doble Par"
    elif puntos == 1:
        return "Par"
    else:
        return "Nadota mi bro..."

# Función para dibujar las cartas en la pantalla
def draw_cards(mano):
    x_offset = 50
    y_offset = 100
    for idx, card in enumerate(mano):
        screen.blit(card_images[card], (x_offset + idx * 120, y_offset))

# Función para mostrar texto en pantalla
def draw_text(text, x, y, color=WHITE):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

#-----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    menu()


# Ciclo principal del juego con Pygame
screen.fill(BLACK)
for _ in range(5):
    if pila:
        carta = pila.pop()
        cola.append(carta)

# Contador de puntos
total_puntos = analizar_cola(cola)
puntos_acumulados = [total_puntos]  # Lista para almacenar los puntos acumulados
turno = 0

# Dibujar las cartas
draw_cards(cola)

# Mostrar la información en pantalla
draw_text(f"Turno: {turno}", 50, 300)
draw_text(f"Combinación: {obtener_nombre_combinacion(puntos_acumulados[turno])}", 50, 350)
draw_text(f"Puntos en este turno: {puntos_acumulados[turno]}", 50, 400)
draw_text(f"Puntos totales: {total_puntos}", 50, 450)

pygame.display.flip()

# Esperar a que el jugador presione Enter para continuar
waiting_for_input = True
while waiting_for_input:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            waiting_for_input = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Si el jugador presiona Enter
                waiting_for_input = False
                turno += 1  # Incrementar el turno
                # Actualizar la pantalla
                screen.fill(BLACK)  # Rellena toda la pantalla con un color blanco
                
    
while pila:
    # Hacer dequeue a un elemento de la cola y moverlo a la cola "quemadas"
    if cola:
        carta = cola.popleft()
        quemadas.append(carta)

    # Hacer un nuevo pop del stack y añadirlo a la primera cola
    if pila:
        carta = pila.pop()
        cola.append(carta)
        total_puntos += analizar_cola(cola)
        puntos_acumulados.append(total_puntos)  # Almacenar los puntos acumulados


    # Dibujar las cartas
    draw_cards(cola)

    # Mostrar la información en pantalla
    draw_text(f"Turno: {turno}", 50, 300)
    draw_text(f"Combinación: {obtener_nombre_combinacion(puntos_acumulados[turno]-puntos_acumulados[turno-1])}", 50, 350)
    draw_text(f"Puntos en este turno: {puntos_acumulados[turno]-puntos_acumulados[turno-1]}", 50, 400)
    draw_text(f"Puntos totales: {total_puntos}", 50, 450)

    # Actualizar la pantalla
    pygame.display.flip()

    # Esperar a que el jugador presione Enter para continuar
    waiting_for_input = True
    while waiting_for_input:
        if turno == 47:
            # Mostrar el resultado final cuando ya no se pueda hacer un pop del stack
            pygame.display.flip()
            screen.fill(BLACK)
            draw_text("¡Juego terminado!", 50, 50)
            draw_text(f"Turno: {turno}", 50, 300)
            draw_text(f"Puntos totales: {total_puntos}", 50, 450)
            draw_text(f"Presiona Espacio para salir", 50, 500)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting_for_input = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Si el jugador presiona Enter
                        waiting_for_input = False
                        screen.fill(BLACK)
                        break
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting_for_input = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Si el jugador presiona Enter
                        waiting_for_input = False
                        turno += 1  # Incrementar el turno
                        screen.fill(BLACK)  # Rellena toda la pantalla con un color blanco
    
# Cerrar Pygame
pygame.quit()