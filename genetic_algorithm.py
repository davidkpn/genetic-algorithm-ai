'''
Owner: David K.
An evolutionary genetic algorithm AI.
This unsupervised learning will generate weights according to input,
and improve them based on action results.
the only requierments are numpy package to handle math tasks.

to improve:
1. add made in generation field to the Genome object
2. Error handling, wrong input and so on..
'''
import numpy as np

####################
# HELPERS
####################
def get_fitness_key(item):
    return item.fitness

def random_choice(a, b):
    return a if round(np.random.rand()) else b
####################

class Ai:
    '''
    input_size => (moves, weights)
    population => number of genomes for each generation
    mutation_rate => learning rate, default is .05
    mutation_step => how much to manipulate the weight, default is .2
    n_elites => number of best genomes to keep for the next generation, default 1
    '''
    def __init__(self, population=50, mutation_rate=.05, mutation_step=.2, input_size=(3,6), n_elites=1):
        self.population_size = population
        self.mutation_rate = mutation_rate
        self.mutation_step = mutation_step
        self.input_size = input_size
        self.current_genome = 0
        self.generation = 0
        self.genomes = []
        self.elites = []
        self.n_elites = n_elites
        self.winners = []
        self.create_initial_population()

    def create_initial_population(self):
        for i in range(self.population_size):
            genome = Genome(self.input_size,self.mutation_rate, self.mutation_step)
            self.genomes.append(genome)
        print(f"Initialized AI with {self.population_size} Starting Genomes")

    '''
        function => user function gets a genome and calculate his fitness based on genome's results.
                    for each genome apply the activate function to get results.
        generations => once the function done, evolve the generation
                       until the generation will reach the max user picked.

        return => the ai net, ai.elites[0] is the best calculate during the run.
    '''
    # def run(self, function, generations):
    #     print(f"AI is evaluating for {generations} generations")
    #     while self.generation < generations:
    #         for genome in self.genomes:
    #
    #         function(self.genomes[self.current_genome])
    #         self.current_genome += 1
    #         if self.current_genome >= self.population_size:
    #             self.evolve()
    #     return self
    #
    # def evolve(self):
    #     print(f"generation {self.generation} evolved.")
    #     self.current_genome = 0
    #     self.generation += 1
    #     self.genomes = sorted(self.genomes, key=get_fitness_key, reverse=True) # decending sort => first is highest
    #     self.elites = self.genomes[:self.n_elites]
    #     self.winners.append(self.elites[0].copy())
    #     print(f"Elite's fitness: {self.elites[0].fitness}")
    #     print(f"elite's weights are: {self.elites[0].weights}")
    #     # remove the lower 75% population by fitness
    #     self.genomes = self.genomes[:round(len(self.genomes)/4)]
    #     # reset the fitness values of the top genomes
    #     # so the genome of the next generation will start equally
    #     for genome in self.genomes:
    #         genome.fitness = -1
    #     children = []
    #     for elite in self.elites:
    #         children.append(elite)
    #     while len(children) < self.population_size:
    #         random_father = self.genomes[np.random.randint(len(self.genomes))]
    #         random_mother = self.genomes[np.random.randint(len(self.genomes))]
    #         # crossover between two random genomes to make a child
    #         children.append( Genome.make_child(random_father, random_mother) )
    #     # the new genomes are the evolved children of the best 25% of last generation
    #     self.genomes = children

    def run(self, function, generations):
        print(f"AI is evaluating for {generations} generations")
        while self.generation < generations:
            for genome in self.genomes:
                function(genome) # analayze genome
            self.evolve()
        return self

    def evolve(self):
        print(f"generation {self.generation} evolved.")
        self.generation += 1
        self.genomes = sorted(self.genomes, key=get_fitness_key, reverse=True) # decending sort => first is highest
        self.elites = self.genomes[:self.n_elites]
        self.winners.append(self.elites[0].copy())
        print(f"Elite's fitness: {self.elites[0].fitness}")
        print(f"elite's weights are: {self.elites[0].weights}")
        # remove the lower 75% population by fitness
        self.genomes = self.genomes[:round(len(self.genomes)/4)]
        # reset the fitness values of the top genomes
        # so the genome of the next generation will start equally
        for genome in self.genomes:
            genome.fitness = -1 # -1 to quauioton snake ability

        children = self.elites.copy()
        while len(children) < self.population_size:
            random_father, random_mother = np.random.choice(self.genomes, 2)
            # crossover between two random genomes to make a child
            children.append(Genome.make_child(random_father, random_mother))
        # the new genomes are the evolved children of the best 25% of last generation
        self.genomes = children

class Genome:
    '''
    input_size => (moves, weights)
    mutation_rate => learning rate, default is .05
    mutation_step => how much to manipulate the weight, default is .2
    '''
    def __init__(self, input_size, mutation_rate, mutation_step):
        self.input_size = input_size
        self.mutation_rate = mutation_rate
        self.mutation_step = mutation_step
        self.id = np.random.rand()
        self.fitness = -1
        self.weights = np.random.uniform(-1,1,input_size[1])

        # for input in range(self.input_size[1]):
        #     self.weights.append(np.random.randint(-10,10) * np.random.rand())
    '''
    given set of action with weights, return the best action based on the
    genome's weight rating
    actions must be the shape of the given input.
    '''
    def activate(self, actions):
        if len(actions[0]) != self.input_size[1]:
            print(f'Error: wrong input, expected input shape:{self.input_size}')
            return actions[0]
        best_action_rating = float('-inf')
        best_action_index = 0
        for i, action in enumerate(actions):
            rating = 0
            for index, value in enumerate(action):
                rating += value * self.weights[index]
            if rating > best_action_rating:
                best_action_rating = rating
                best_action_index = i
        return best_action_index

    def copy(self):
        copied_genome = Genome(self.input_size, self.mutation_rate, self.mutation_step)
        copied_genome.id = self.id
        copied_genome.fitness = self.fitness
        copied_genome.weights = self.weights
        return copied_genome

    @classmethod
    def make_child(cls, father_genome, mother_genome):
        child = Genome(father_genome.input_size, father_genome.mutation_rate, father_genome.mutation_step)
        child.weights = []
        for input in range(father_genome.input_size[1]):
            weight = random_choice(father_genome.weights[input], mother_genome.weights[input])#np.random.choice([a,b], 1, p=[.5,.5])[0]
            if np.random.rand() < child.mutation_rate: # np.random.choice(2, p=[.98, .02])#[1-child.mutation_rate, child.mutation_rate]
                weight += (np.random.rand() - .5) * child.mutation_step#np.random.rand() * child.mutation_step * 2 - child.mutation_step
            child.weights.append(weight)

        return child
