from GUI.SnakeGUI import *
from LogicOfGame.GeneticAlgorithm import *
from GUI.MatrixtableGUI import *


def choose_qui():
    print("Dobro dosli!")
    print("Izaberite koji prkaz zelite da vidite:")
    print("1. --> Realna simualacija")
    print("2. --> Brza simulacija")
    choice = input("Izbor >>> ")
    return choice


if __name__ == '__main__':

    new_population = get_init_population()
    best_fitness = - math.inf
    best_sum_fitness = 0
    best_population = new_population
    save_population(best_population)
    choice = choose_qui()
    for generation in range(num_generations):
        print("------------------------------Generacija: ", generation, " ------------------------------")
        if choice == "1":
            game_table = MatrixtableGUI()
            snake_gui = SnakeGUI(game_table)
            snake_gui.draw_first_food()
            fitness = get_fitness(new_population, snake_gui)
        else:
            fitness = get_fitness(new_population)
            game_table = None
            snake_gui = None


        if np.max(fitness) > best_fitness:
            best_fitness = np.max(fitness)
        if sum(fitness) > best_sum_fitness:
            best_sum_fitness = sum(fitness)
            best_population = new_population

        print("Najbolji fitness je: ", np.max(fitness))
        parents, children = GeneticAlgorithm(new_population, fitness).get_parents()
        new_population[0:parents.shape[0], :] = parents
        new_population[parents.shape[0]:, :] = children

    print("Najbolji fitness za 100 generacija je:  ", best_fitness)
    save_population(best_population)
    if choice == 1:
        game_table.window_table.mainloop()
