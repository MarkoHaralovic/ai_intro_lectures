import numpy as np
from NeuralNetwork import NeuralNetwork,mean_squared_error,FullyConnectedLayer,sigmoid
from Dataset import TrainDataset,TestDataset
class GeneticAlgorithm:
   
   def __init__(self,population_size:int,elitism:int,mutation_rate:float,mutation_scale:float,
                iterations:int,neural_net_architecture:list,train_dataset:TrainDataset,test_dataset:TestDataset
                ):
      self.population_size = population_size
      self._elitism = elitism
      self.mutation_rate = mutation_rate
      self.mutation_scale = mutation_scale
      self.iterations = iterations
      self.neural_net_architecture = neural_net_architecture
      self.train_dataset = train_dataset
      self.test_dataset = test_dataset
      self.population = self._init_population()
      
   def _init_population(self):
      return [NeuralNetwork(self.neural_net_architecture) for i in range(self.population_size)]
   
   def elitism(self):
      """One or more best individuals are transferred to the next generation."""
      fitnesses = {individual : self.fitness(individual) for individual in self.population}
      fitnesses = sorted(fitnesses,key=lambda x:fitnesses[x],reverse=True)
      top_individuals = fitnesses[:self._elitism]
      return top_individuals
   
   def fitness(self,individual):
      return 1/(mean_squared_error(self.train_dataset.get_labels(),individual.forward_pass(self.train_dataset.get_features())[0]))
      
   def selection(self):
      """Fitness proportional selection."""
      fitness_scores = [self.fitness(individual) for individual in self.population]
      total_fitness = sum(fitness_scores)
      
      selection_probabilities = [float(fitness.item()/ total_fitness) for fitness in fitness_scores]
      
      selected_indices = np.random.choice(len(self.population), size=self.population_size, p=selection_probabilities, replace=True)
      selected_individuals = [self.population[index] for index in selected_indices]
   
      return selected_individuals
   
   def crossover(self,parent_1,parent_2):
      """Arithmetic mean of selected individuals."""
      child = NeuralNetwork(parent_1.architecture)
      for i in range(len(child.layers)):
         layer = child.layers[i]
         for j in range(len(layer.weights)):
            layer.weights[j] = (parent_1.layers[i].weights[j] + parent_2.layers[i].weights[j])/2
         for k in range(len(layer.bias)):
            layer.bias[k] = (parent_1.layers[i].bias[k] + parent_2.layers[i].bias[k])/2
      return child
   
   def mutation(self,individual):
      """Crossover of selected individuals, implemented as Gaussian noise, so that tot the chromosome of weights is added vector
         from normal distribution with standard deviation K. Every chromosome weight is mutated with probability p.
      """
      if np.random.random() > self.mutation_rate:
         return individual
      for layer in individual.layers:
         for i in range(len(layer.weights)):
            layer.weights[i] += np.random.normal(0,self.mutation_scale)
      return individual
   
   def evolve(self):
      best, best_fitness = None, -float('inf')
      
      for generation in range(self.iterations):
         scores = [self.fitness(individual) for individual in self.population]
         
         elites = self.elitism()
         new_population = elites[:]

         while len(new_population) < self.population_size:
            parents =  self.selection()
            parent_1,parent_2 = parents[0],parents[1]
            child = self.crossover(parent_1,parent_2)
            child = self.mutation(child)
            new_population.append(child)
            
         self.population = new_population
         
         for individual in self.population:
            fitness = self.fitness(individual)
            if fitness > best_fitness:
               best, best_fitness = individual, fitness
         
         if generation % 200 == 0:
            mse_train = mean_squared_error(self.train_dataset.get_labels(), best.forward_pass(self.train_dataset.get_features())[0])
            mse_test = mean_squared_error(self.test_dataset.get_labels(), best.forward_pass(self.test_dataset.get_features())[0])
            print(f"Generation {generation}: Train MSE: {mse_train}, Test MSE: {mse_test}")
            
      final_mse_train = mean_squared_error(self.train_dataset.get_labels(), best.forward_pass(self.train_dataset.get_features())[0])
      final_mse_test = mean_squared_error(self.test_dataset.get_labels(), best.forward_pass(self.test_dataset.get_features())[0])
      print(f"Final Best: Train MSE: {final_mse_train}, Test MSE: {final_mse_test}")
      
