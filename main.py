import json
import random

input_file = open('input.json')
data = json.load(input_file)
input_file.close()

population_size = data['population_size']
mutation_probability = data['mutation_probability']
generations_size = data['generations_size']
graph_degree = data['graph_degree']
colors = data['colors']

graph = []
graph_edges = data['graph_nodes']

for i in range(graph_degree):
  vertex = []
  edges = graph_edges[i]["edge"]
  for j in range(graph_degree):
    vertex.append(0)
  for j in range(len(graph_edges[i]["edge"])):
    vertex[int(edges[j]) - 1] = 1
  graph.append(vertex)
for i in range(graph_degree):
  for j in range(0, i):
    graph[i][j] = graph[j][i]

for v in graph:
  print(v)

def createIndividual():
  individual = []
  for i in range(graph_degree):
    individual.append(colors[random.randint(0, 3)])
  return individual

def createPopulation():
  population = []
  for i in range(population_size):
    individual = createIndividual()
    population.append(individual)
  return population

def fitness(graph, individual):
  fitness = 0
  for i in range(graph_degree):
    for j in range(i, graph_degree):
      if (graph[i][j] == 1):
        if (individual[i] != individual[j]):
          fitness += 1
        else:
          return 0
  return fitness

def crossover(parent1, parent2):
  position = round(graph_degree / 2)
  child1 = []
  child2 = []
  for i in range(position + 1):
    child1.append(parent1[i])
    child2.append(parent2[i])
  for i in range(position + 1, graph_degree):
    child1.append(parent2[i])
    child2.append(parent1[i])
  return child1, child2

def mutation(individual):
  check = random.uniform(0, 1)
  if (check <= mutation_probability):
    position = random.randint(0, graph_degree - 1)
    individual[position] = colors[random.randint(0, 3)]
  return individual

def roulette_wheel_selection(population):
  total_fitness = 0
  for individual in population:
    total_fitness += 1/(1+fitness(graph, individual))
  cumulative_fitness = []
  cumulative_fitness_sum = 0
  for i in range(len(population)):
    cumulative_fitness_sum += 1/(1+fitness(graph, population[i]))/total_fitness
    cumulative_fitness.append(cumulative_fitness_sum)
  
  new_population = []
  for i in range(len(population)):
    roulette = random.uniform(0, 1)
    for j in range(len(population)):
      if (roulette <= cumulative_fitness[j]):
        new_population.append(population[j])
        break
  return new_population

population = createPopulation()
generation = 0
best_fitness = fitness(graph, population[0])
fittest_individual = population[0]
while (generation != generations_size):
  generation += 1
  population = roulette_wheel_selection(population)
  new_population = []
  random.shuffle(population)
  for i in range(0, population_size - 1, 2):
    child1, child2 = crossover(population[i], population[i+1])
    new_population.append(child1)
    new_population.append(child2)
  for individual in new_population:
    individual = mutation(individual)
  population = new_population
  for individual in population:
    fit = fitness(graph, individual)
    if (fit >= best_fitness):
      best_fitness = fit
      fittest_individual = individual

print("Generation: ", generation, " Best_Fitness: ", best_fitness, " Individual: ", fittest_individual)