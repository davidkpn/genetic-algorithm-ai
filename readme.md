# Genetic un-supervised AI
General Genetic Algorithm, actually tested on two different games.

## Usage

- population - The amount of genome population that will live in each generation.  
- mutation rate - The chance of a mutation children's gene.  
- mutation step - the degree of impact  
- input size - The shape of the input, a few steps on some weights per step  
- n_elites - The number of elitist survivors to preserve for the next generation.
```python
from genetic_algorithm import Ai
ai = Ai(population=50, mutation_rate=.05, mutation_step=.2, input_size=(3,6), n_elites=1)
to_save = ai.run(eval_func, number_of_generations)
```

## Snake Game AI
![snake game illustration](https://media.giphy.com/media/gM5Jb8XwAw0vVlFdHQ/giphy.gif)

## Tetris Game AI
![tetris game illustration](https://media.giphy.com/media/ftkLX3MbK5nCz7KOkA/giphy.gif)




# Genetic Algorithm
the genetic algorithm is creating a population of genomes.

evaluate each genome according to *fitness function*

and evolve genomes generation by *cross-over* method.


## Fitness function
depends on the goal of the game, for instance, the well-known snake old mobile game -

the higher the score, the better, and the score raise by eating the apple.

to fine-tune the fit, I added more complex features like the distance from food.

if the snake gets closer, he's fitter.

possible features can be the number of moves takes the snake to get to the food, etc.


## Cross-Over method
takes the best 25% of the generation and breed them to reach the initial population size.

the breeding is taking two random genomes out of the 25% as parents of a child.

the child genome will absorb genes randomly from his parents with a mutation rate for the gene by the mutation step.


## Snake-game Input Graph Illustration

look in the snake-game-illustration.html
http://htmlpreview.github.io/?https://github.com/davidkpn/genetic-algorithm-ai/blob/master/snake-game-illustration.html

