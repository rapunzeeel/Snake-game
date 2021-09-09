from LogicOfGame.TrainingMoves import *

input_neural_network = 7
hidden_layer1_neural_network = 9
hidden_layer2_neural_network = 15
output_neural_network = 3

individual_score = input_neural_network * hidden_layer1_neural_network + \
                   hidden_layer1_neural_network * hidden_layer2_neural_network + \
                   hidden_layer2_neural_network * output_neural_network  # 243 number of gen in chromosomes

num_generations = 100
number_of_chromosomes = 48
population_size = (number_of_chromosomes, individual_score)


def get_init_population():
    population = np.random.choice(np.arange(-1, 1, step=0.01), size=population_size, replace=True)
    return population


class GeneticAlgorithm(object):
    def __init__(self, population, fitness):
        self.population = population
        self.fitness = fitness
        self.parents = []
        self.children = None
        self.number_of_parents = 24
        self._already_choose_parents = []

    def selection(self):
        self._best_parent_selection()
        # self._roulette_selection()
        return self.parents

    def _roulette_selection(self):
        num_of_needed_parents = int(self.number_of_parents / 2)

        fitness_for_roulette = []
        for i in range(len(self.population)):
            if i not in self._already_choose_parents:
                fitness_for_roulette.insert(i, random.randint(0, 1) * self.fitness[i])
            else:
                fitness_for_roulette.insert(i, -9999999999)

        fitness_for_roulette = np.array(fitness_for_roulette)
        for i in range(num_of_needed_parents):
            get_max_fitness_index = np.where(fitness_for_roulette == np.max(fitness_for_roulette))[0][0]
            self.parents[i + 12, :] = self.population[get_max_fitness_index, :]
            self._already_choose_parents.append(get_max_fitness_index)
            fitness_for_roulette[get_max_fitness_index] = -999999999

    def _best_parent_selection(self):
        self.parents = np.empty((self.number_of_parents, self.population.shape[1]))
        for i in range(int(self.number_of_parents)):
            get_max_fitness_index = np.where(self.fitness == np.max(self.fitness))[0][0]
            self.parents[i, :] = self.population[get_max_fitness_index, :]
            self._already_choose_parents.append(get_max_fitness_index)
            self.fitness[get_max_fitness_index] = -999999999

    def crossover(self, number_of_crossover):  # number_of_crossover = (24,243)
        number_of_chromosome = number_of_crossover[0]
        number_of_gen = number_of_crossover[1]
        self.children = np.empty(number_of_crossover)

        for individual in range(int(number_of_chromosome / 2)):
            parent_index_random1 = random.randint(0, self.number_of_parents - 1)
            parent_index_random2 = random.randint(0, self.number_of_parents - 1)

            if parent_index_random1 != parent_index_random2:
                for gen in range(number_of_gen):
                    if random.uniform(0, 1) < 0.5:
                        self.children[individual, gen] = self.parents[parent_index_random1, gen]
                    else:
                        self.children[individual, gen] = self.parents[parent_index_random2, gen]
                    if random.uniform(0, 1) < 0.5:
                        self.children[individual + 12, gen] = self.parents[parent_index_random1, gen]
                    else:
                        self.children[individual + 12, gen] = self.parents[parent_index_random2, gen]

    def mutation(self):
        number_of_children = len(self.children)
        number_of_gen = len(self.children[0])
        for individual in range(number_of_children):
            if random.uniform(0, 1) < 0.2:
                random_coeff_for_children_gen = random.randint(0, number_of_gen - 1)

                random_coeff = np.random.choice(np.arange(-1, 1, step=0.001), size=1, replace=False)
                self.children[individual, random_coeff_for_children_gen] = \
                    self.children[individual, random_coeff_for_children_gen] + random_coeff

    def get_parents(self):
        self.selection()
        self.crossover((24, 243))
        self.mutation()
        return self.parents, self.children


def get_fitness(population, snake_gui=None):
    fitness = []
    for i in range(population.shape[0]):
        fit = RunGame(population[i], snake_gui).play()
        print('fitness vrednost za jedinku ' + str(i) + ' :  ', fit)
        fitness.append(fit)
    return np.array(fitness)


def save_population(best_population):
    file = open("Fajlovi/bestSnake.txt", 'w')
    for i in range(best_population.shape[0]):
        chromosome = ""
        for j in range(best_population.shape[1]):
            chromosome += str(best_population[i, j]) + ", "
        chromosome = chromosome[0:-2]
        chromosome += "\n"
        file.write(chromosome)
    file.close()


def read_population():
    file = open("Fajlovi/bestSnake.txt", 'r')
    population = np.empty([number_of_chromosomes, individual_score])
    for i in range(number_of_chromosomes):
        chromosome = file.readline().split(", ")
        print(chromosome)
        for j in range(individual_score):
            population[i, j] = float(chromosome[i])
    file.close()
    return population
