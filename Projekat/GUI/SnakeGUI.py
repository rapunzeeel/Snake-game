from LogicOfGame.Snake import Food
import random

import pygame

window_width = 500
window_height = 500

pygame.init()
display = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()


def draw_snake_pygame(snake_position):
    for position in snake_position:
        pygame.draw.rect(display, (0, 255, 0), pygame.Rect(position[0], position[1], 15, 15))


def draw_food_pygame(apple_position):
    pygame.draw.rect(display, (255, 0, 0), pygame.Rect(apple_position[0], apple_position[1], 15, 15))


def create_pygame_window(snake, button_direction):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        display.fill((255, 255, 255))

        draw_food_pygame(snake.food_position)
        draw_snake_pygame(snake.snake_body)

        snake_position, food_position, score = snake.next_iteration(button_direction)
        pygame.display.set_caption("SCORE: " + str(score))
        pygame.display.update()
        clock.tick(500)

        return snake_position, food_position, score


class SnakeGUI(object):
    def __init__(self, game_table):
        self.game_table = game_table  # objekat tipa MatrixTable
        self.rectangles = []
        self.rectangles_coordinates = []
        self.snake = None  # objekat tipa Snake

    def draw_first_food(self):
        self.game_table.food = Food(self.game_table.width, self.game_table.height, self.snake)
        [x1, y1] = self.game_table.food.set_first_food()
        self.game_table.food = self.game_table.canvas.create_rectangle(x1, y1, x1 + 15, y1 + 15, outline="#fb0",
                                                                       fill="#fb0")
        self.game_table.canvas.update()

    def draw_iteration(self):
        self.game_table.canvas.delete("all")
        self.game_table.draw_table(self.snake.score)
        # jedno iscrtavanje pomeranja zmije i jabuke na tabli
        self.draw_snake()
        if self.snake.signe_for_eat == 1:  # ako je pojela hranu
            [x1, y1] = self.set_food()
            self.game_table.canvas.create_rectangle(x1, y1, x1 + 15, y1 + 15, outline="#fb0", fill="#fb0")
            self.snake.food_position = [x1, y1]
            self.game_table.canvas.update()
        else:
            [x1, y1] = self.snake.food_position
            x2 = x1 + 15
            y2 = y1 + 15
            self.game_table.canvas.create_rectangle(x1, y1, x2, y2, outline="#fb0", fill="#fb0")
            self.game_table.canvas.update()

    def set_food(self):
        while True:
            n1 = random.randint(0, 29)
            n2 = random.randint(0, 29)
            if (str(n1 * 15) + ":" + str(n2 * 15)) not in self.snake.snake_body:
                x1 = n1 * 15
                y1 = n2 * 15
                break

        return [x1, y1]

    def _remove_square(self):
        # f-ja delete brise objekte sa cavasa
        self.game_table.canvas.delete(self.game_table.rectangles[
                                          -1])  # kada se zmija pomeri, njen rep se pomerio i stari rep mora da se obezboji na ekranu
        del self.game_table.rectangles[-1]
        # moraju se brisati i koordinate iz self.rectagles_coordinates
        # f-ja update menja stanje kako bi se stalno prikazivalo novo
        self.game_table.canvas.update()

    def draw_snake(self):
        for coordinate in self.snake.snake_body:
            x1 = coordinate[0]
            y1 = coordinate[1]
            self.game_table.canvas.create_rectangle(x1, y1, x1 + 15, y1 + 15, outline="#51CC00", fill="#51CC00")

            self.game_table.canvas.update()

    def if_not_in_rectangle(self, coordinate):
        x1 = coordinate[0]
        y1 = coordinate[1]
        if coordinate not in self.game_table.rectangles_coordinates:
            one_square = self.game_table.canvas.create_rectangle(x1, y1, x1 + 15, y1 + 15, outline="#51CC00",
                                                                 fill="#51CC00")
            self.game_table.rectangles_coordinates.append(coordinate)
            self.game_table.rectangles.insert(0, one_square)
