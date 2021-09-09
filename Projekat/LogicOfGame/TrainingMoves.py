from LogicOfGame.NeuralNetwork import *
from LogicOfGame.Snake import *
from GUI.SnakeGUI import *

class RunGame(object):
    def __init__(self,individual_of_population, snake_gui=None):
        # snake gui je objekat klase SnakeGUI
        self.max_score = 0
        self.test_games = 1
        self.score_for_dying = 0  # skor ako udari u samu sebe ili u ivicu
        self.steps_per_game = 2500
        self.cruising_score = 0  # skor za kretanja u jednom pravcu duze vreme
        self.snake = Snake(450, 450)
        self.snake_head = None
        self.starting_snake_body = None
        self.individual_of_population = individual_of_population
        self.snake_gui = snake_gui  # treba da bude objekat klase SnakeGUI
        self.current_direction = None
        self.button_direction = None
        self.score = 0

    def play(self):
        for _ in range(self.test_games):
            self.snake.snake_head, self.snake.snake_body, self.snake.food_position, self.score = self.snake.start()
            if self.snake_gui != None: #ako je izabran realan nacin simulacije
                self.snake_gui.snake = self.snake
                self.snake_gui.draw_snake()

            same_direction_num = 0
            prev_direction = 0

            for _ in range(self.steps_per_game):

                predicted_direction = self._calculate_prediction_direction()

                if predicted_direction == prev_direction:
                    same_direction_num += 1
                else:
                    same_direction_num = 0
                    prev_direction = predicted_direction

                new_direction = self._calculate_new_direction(predicted_direction)
                self.button_direction = self.snake.select_button_direction(new_direction.tolist())

                next_step = self.snake.snake_body[0] + self.current_direction

                # ako je zmija udarila u ivicu ili u samu sebe
                if self.snake.is_blow_to_edge(self.snake.snake_body[0]) or self.snake.is_blow_with_self(next_step.tolist()):
                    self.score_for_dying -= 150
                    break

                if self.snake_gui != None:
                    self.snake.snake_body, self.snake.food_position, self.snake.score = self.snake.next_iteration(self.button_direction)
                    self.snake_gui.snake = self.snake
                    self.snake_gui.draw_iteration()
                else:
                    self.snake.snake_body, self.snake.food_position, self.snake.score = create_pygame_window(self.snake, self.button_direction)



                if self.snake.score > self.max_score:

                    self.max_score = self.snake.score


                if same_direction_num > 8 and predicted_direction != 0:
                    self.cruising_score -= 1
                else:
                    self.cruising_score += 2

        return self.score_for_dying + self.cruising_score + self.max_score * 5000

    def _calculate_prediction_direction(self):
        self.current_direction, is_left_blocked, is_front_blocked, is_right_blocked = self.snake.blocked_position_around()
        angle, snake_direction, apple_direction_normalized, snake_direction_normalized = self.snake.position_versus_food()

        """predvidjeni smer kretanja  koji ce se bodovati
        ->funkcija forward_propagation je iz fajla NeuralNetwork.py
        ->azni parameti za neuronsku mrezu:
         indeksi: 0. da li je levo polje blokirano (1 ako jeste, 0 ako nije)
         1. da li je polje ispred blokirano
         2. da li je polje desno blokirano
         3. smer jabuke od zmije (x)
         4. smer jabuke od zmije (y)
         5. trenutni pravac zmije (x)
         6. trenutni pravac zmije (y)

        """

        predicted_direction = np.argmax(np.array(forward_propagation(np.array(
            [is_left_blocked, is_front_blocked, is_right_blocked, apple_direction_normalized[0],
             snake_direction_normalized[0], apple_direction_normalized[1],
             snake_direction_normalized[1]]).reshape(-1, 7), self.individual_of_population))) - 1

        return predicted_direction

    def _calculate_new_direction(self, predicted_direction):
        new_direction = np.array(self.snake.snake_body[0]) - np.array(self.snake.snake_body[1])
        if predicted_direction == -1:
            new_direction = np.array([new_direction[1], -new_direction[0]])
        if predicted_direction == 1:
            new_direction = np.array([-new_direction[1], new_direction[0]])

        return new_direction

    def get_button_direction(self):
        return self.button_direction
