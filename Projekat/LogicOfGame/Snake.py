import random
import numpy as np
import math


class Snake(object):
    def __init__(self, width_window, height_window):  # position su koordinate pocetne zmije od 1 kvadratica
        self.width_window = width_window
        self.height_window = height_window
        self.snake_body = [[0, 0]]  # lista [x1,y1] koordinata
        self.tail = self.snake_body[-1]
        self.snake_head = self.snake_body[0]
        self.size = 1
        self.score = 0
        self.food = Food(width_window, height_window, self)
        self.food_position = [0, 0]
        self.next_step = None
        self.button_direction = None
        self.signe_for_eat = 0  # ako je zmija pojela hranu trenutnim pomeranjem, ova vrednost ce biti 1

        self.x_head = self.snake_head[0]
        self.y_head = self.snake_head[1]
        self.x_tail = self.tail[0]
        self.y_tail = self.tail[1]
        self.xspeed = 1
        self.yspeed = 0

    def move_snake(self, position):  # position ce biti koordinate gde treba da bude glava zmije nakon pomeranja
        self.snake_head = position  # promeni se referenca na glavu
        self.x_head = position[0]
        self.y_head = position[1]
        self.snake_body.insert(0, position)  # doda se nova glava
        del self.snake_body[-1]  # zmija je duza za 1 pa treba obristi zaostali rep
        self.tail = self.snake_body[-1]  # promeni se referenca na rep
        self.x_tail = self.tail[0]
        self.y_tail = self.tail[1]

    def grow_up(self, position):  # kada zmijica pojede hranju poraste i u listu tail se dodaje jos jedan element
        self.snake_body.insert(0, position)
        self.x_head = position[0]
        self.y_head = position[1]
        self.snake_head = position
        self.size += 1
        self.score += 1
        # rep ostaje isti, samo se glava pomeri na mesto gde je bila hrana

    def next_iteration(self, button_direction):
        # funkcija koja izvrsava pomeranja zmije, postavlja novu jabuku ako treba
        if button_direction == 2:  # ako treba da ide desno
            new_head_position = [self.snake_body[0][0] + 15, self.snake_body[0][1]]
        elif button_direction == 1:  # ako treba da ide levo
            new_head_position = [self.snake_body[0][0] - 15, self.snake_body[0][1]]
        elif button_direction == 0:  # ako treba da ide gore
            new_head_position = [self.snake_body[0][0], self.snake_body[0][1] - 15]
        else:  # treba da ide dole
            new_head_position = [self.snake_body[0][0], self.snake_body[0][1] + 15]

        self.snake_head = new_head_position

        if new_head_position == self.food_position:
            self.grow_up(new_head_position)
            self.food_position = self.food.set_food(self)
            self.signe_for_eat = 1
        else:
            self.move_snake(new_head_position)
            self.signe_for_eat = 0

        return self.snake_body, self.food_position, self.score

    def start(self):  # startni izgled svake zmije koja ce se trenirati
        self.score = 0
        self.snake_head = [105, 105]
        self.snake_body = [[105, 105], [90, 105], [75, 105]]  # prve tri kockice kao pocetna zmija
        self.food_position = self.food.set_food(self)
        return self.snake_head, self.snake_body, self.food_position, self.score

    def blocked_position_around(self):
        # proveravamo da li su okolne pozicije u odnosu na glavu zmije bokirane
        snake_direction = np.array(self.snake_body[0]) - np.array(self.snake_body[1])  # trenutni smer kretanja zmije
        left_direction = np.array([snake_direction[1], -snake_direction[0]])
        right_direction = np.array([-snake_direction[1], snake_direction[0]])

        is_front_blocked = self.is_direction_blocked(snake_direction)
        is_left_blocked = self.is_direction_blocked(left_direction)
        is_right_blocked = self.is_direction_blocked(right_direction)

        # vraca trenutni vektor kretanja zmije
        # i vraca nule i jedinice(npr: 1,0,0 levo blokirano, desno i pravo nije)


        return snake_direction, is_left_blocked, is_front_blocked, is_right_blocked

    def is_direction_blocked(self, direction_vector):
        # direction vector je vektor potencijalnog smera kretanja zmije (to ukljucije i one koju si levo, desno i pravo od nje)
        next_step = self.snake_body[0] + direction_vector
        if self.is_blow_to_edge(next_step) or self.is_blow_with_self(next_step.tolist()):
            return 1
        else:
            return 0

    def is_blow_to_edge(self, next_step):
        # provera da li su koordinate narednog koraka udarac u ivicu
        if next_step[0] >= self.width_window or next_step[0] < 0 or next_step[1] >= self.width_window or next_step[1] < 0:
            return True
        else:
            return False

    def is_blow_with_self(self, direction_vector):
        if direction_vector in self.snake_body[1:]:
            return True
        return False

    # pozicija glave zmije u odnosu na hranu
    def position_versus_food(self):
        # funkcija vraca ugao zmije i hrane,
        apple_direction = np.array([self.food_position[0], self.food_position[1]]) - np.array(self.snake_body[0])
        snake_direction = np.array(self.snake_body[0]) - np.array(self.snake_body[1])

        norm_apple_direction = np.linalg.norm(apple_direction)
        norm_snake_direction = np.linalg.norm(snake_direction)

        if norm_apple_direction == 0:
            norm_apple_direction = 15
        if norm_snake_direction == 0:
            norm_snake_direction = 15

        apple_direction_normalized = apple_direction / norm_apple_direction
        snake_direction_normalized = snake_direction / norm_snake_direction

        angle = math.atan2(apple_direction_normalized[1] * snake_direction_normalized[0] -
                           apple_direction_normalized[0] * snake_direction_normalized[1],
                           apple_direction_normalized[1] * snake_direction_normalized[1] +
                           apple_direction_normalized[0] * snake_direction_normalized[0]) / math.pi

        return angle, snake_direction, apple_direction_normalized, snake_direction_normalized

    def select_button_direction(self, new_direction):
        if new_direction == [15, 0]:
            button_direction = 2  # right
        elif new_direction == [-15, 0]:
            button_direction = 1  # left
        elif new_direction == [0, 15]:
            button_direction = -1  # down
        else:
            button_direction = 0  # up

        return button_direction


class Food(object):
    def __init__(self, width_window, height_window, snake):
        self.width_window = width_window
        self.height_window = height_window
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.coordinate = [self.x1, self.y1]
        self.food_size = 1
        self._old_food = None

    def set_food(self, snake):
        while True:
            n1 = random.randint(0, 29)
            n2 = random.randint(0, 29)
            if ([str(n1 * 15), str(n2 * 15)]) not in snake.snake_body:
                self.x1 = n1 * 15
                self.y1 = n2 * 15
                self.coordinate = [self.x1, self.y1]
                break

        return [self.x1, self.y1]

    def set_first_food(self):
        n1 = random.randint(0, 29)
        n2 = random.randint(0, 29)
        self._old_food = [self.x1, self.y1, self.x2, self.y2]
        self.x1 = n1 * 15
        self.y1 = n2 * 15
        self.coordinate = [self.x1, self.y1]
        self.x2 = self.x1 + 15
        self.y2 = self.y1 + 15
        return [self.x1, self.y1]
