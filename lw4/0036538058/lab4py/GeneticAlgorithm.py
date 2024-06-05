import numpy as np
from NeuralNetwork import NeuralNetwork,FullyConnectedLayer,mean_squared_error,sigmoid
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
   
   def elitism(self,fitnesses):
      """One or more best individuals are transferred to the next generation."""
      sorted_by_fitness = sorted(fitnesses, key=lambda x: x[1], reverse=True)
      top_individuals = [individual[0] for individual in sorted_by_fitness[:self._elitism]]
      return top_individuals
   
   def fitness(self,individual):
      return 1/(1e6 + mean_squared_error(self.train_dataset.get_labels(),individual.forward_pass(self.train_dataset.get_features())[0]))
      
   def get_population_fitnesses(self):
      fitnesses = [(individual, self.fitness(individual)) for individual in self.population]
      return fitnesses
   
   def selection(self,fitness_scores):
      """Fitness proportional selection."""
      sorted_by_fitness = sorted(fitness_scores, key=lambda x: x[1], reverse=True)
      
      total_fitness = sum(fitness[1] for fitness in sorted_by_fitness)
      
      parents = []
      for _ in range(2):  
         random_number = np.random.uniform(0, total_fitness)
         cumulative_fitness = 0
         for individual, fitness in sorted_by_fitness:
               cumulative_fitness += fitness
               if cumulative_fitness >= random_number:
                  parents.append(individual)
                  break 
      return parents[0], parents[1]
   
   def crossover(self,parent_1,parent_2):
      """Arithmetic mean of selected individuals."""
      child_1 = NeuralNetwork(parent_1.architecture)
      child_2 = NeuralNetwork(parent_2.architecture)
    
      for i in range(len(child_1.layers)):
        layer_1 = child_1.layers[i]
        layer_2 = child_2.layers[i]
        parent_1_layer = parent_1.layers[i]
        parent_2_layer = parent_2.layers[i]
        
        ratio_1 = np.random.uniform(0,1)
        ratio_2 = 1- ratio_1 

        layer_1.weights = ratio_1 * parent_1_layer.weights + ratio_2 * parent_2_layer.weights
        layer_1.bias = ratio_1 * parent_1_layer.bias + ratio_2 * parent_2_layer.bias
        
        ratio_1 = np.random.uniform(0,1)
        ratio_2 = 1- ratio_1 
        
        layer_2.weights = ratio_1 * parent_1_layer.weights + ratio_2 * parent_2_layer.weights
        layer_2.bias = ratio_1 * parent_1_layer.bias + ratio_2 * parent_2_layer.bias
      return child_1,child_2
   
   def mutation(self,individual):
      """Crossover of selected individuals, implemented as Gaussian noise, so that the chromosome of weights is added vector
         from normal distribution with standard deviation K. Every chromosome weight is mutated with probability p.
      """
      for layer in individual.layers:
        for i in range(len(layer.weights)):
            if np.random.random() < self.mutation_rate:
                layer.weights[i] += np.random.normal(0, self.mutation_scale)
      return individual
   
   def evolve(self):
      best, best_fitness = None, -float('inf')
      
      for generation in range(self.iterations):
         fitnesses = self.get_population_fitnesses()
         elites = self.elitism(fitnesses)
         new_population = elites[:]

         while len(new_population) < self.population_size:
            parent_1,parent_2 = self.selection(fitnesses)
            child1,child2 = self.crossover(parent_1,parent_2)
            child1 = self.mutation(child1)
            child2 = self.mutation(child2)
            new_population.append(child1)
            new_population.append(child2)
            
         self.population = new_population
         
         for individual in self.population:
            fitness = self.fitness(individual)
            if fitness > best_fitness:
               best, best_fitness = individual, fitness
         
         if generation % 2000 == 0:
            mse_train = mean_squared_error(self.train_dataset.get_labels(), best.forward_pass(self.train_dataset.get_features())[0])
            mse_test = mean_squared_error(self.test_dataset.get_labels(), best.forward_pass(self.test_dataset.get_features())[0])
            print(f"[Train error @{generation+2000}]: {mse_train:.6f}")
            # print(f"Generation {generation}: Train MSE: {mse_train:.6f}}, Test MSE: {mse_test:.6f}}")
            
      final_mse_train = mean_squared_error(self.train_dataset.get_labels(), best.forward_pass(self.train_dataset.get_features())[0])
      final_mse_test = mean_squared_error(self.test_dataset.get_labels(), best.forward_pass(self.test_dataset.get_features())[0])
      print(f"[Test error]: {final_mse_test:.6f}")
      # print(f"Final Best: Train MSE: {final_mse_train:.6f}}, Test MSE: {final_mse_test:.6f}}")
      