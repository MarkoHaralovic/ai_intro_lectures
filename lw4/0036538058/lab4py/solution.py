import argparse
from NeuralNetwork import NeuralNetwork,sigmoid
from GeneticAlgorithm import GeneticAlgorithm
from Dataset import TrainDataset,TestDataset

def parse_command_line():
   parser = argparse.ArgumentParser()
   parser.add_argument('path_to_train_set',type=str,help="Path to the file with the training set.")
   parser.add_argument('path_to_test_set',type=str,help="Path to the file with the testing set.")
   parser.add_argument('neural_net_configuration',type=str,help="Example 5s5s, which would create FCN with 2 hidden layers with 5 neurons in each layer.")
   parser.add_argument('popsize',type=int,help="The size of population used in genetic algorithm.")
   parser.add_argument('elitism',type=int,help="Number of best individuals to keep from the previous generation.")
   parser.add_argument('p',type=float,help="Probability of mutation.")
   parser.add_argument('K',type=float,help="Mutation scale, standard deviation of Gaussian noise.")
   parser.add_argument('iter',type=int,help="Number of iterations of genetic algorithm.")
   
   args = parser.parse_args()
   return args

def create_nn_config(input_size, output_size, neural_net_configuration):
    nn_arch = []

    neural_net_configuration = list(map(int, neural_net_configuration))
    
    for i in range(len(neural_net_configuration)):
        if i == 0:
            layer_arch = {
                "input_dim": input_size,
                "output_dim": neural_net_configuration[i],
                "activation": sigmoid
            }
        else:
            layer_arch = {
                "input_dim": neural_net_configuration[i - 1],
                "output_dim": neural_net_configuration[i],
                "activation": sigmoid
            }
        nn_arch.append(layer_arch)
    
    layer_arch = {
        "input_dim": neural_net_configuration[-1], 
        "output_dim": output_size,
        "activation": None  
    }
    nn_arch.append(layer_arch)

    return nn_arch


def main():
   args = parse_command_line()

   neural_net_configuration = args.neural_net_configuration.split("s")[:-1]
   train_seth_path, test_seth_path = args.path_to_train_set,args.path_to_test_set
   popsize,elitism,p,K,iter = args.popsize,args.elitism,args.p,args.K,args.iter
   
   train_dataset = TrainDataset(data_path=train_seth_path)
   test_dataset = TestDataset(data_path=test_seth_path)
   
   nn_architecture = create_nn_config(input_size=len(train_dataset.get_feature_names()),
                                     output_size=len(test_dataset.get_target()),
                                     neural_net_configuration=neural_net_configuration
                                     )
   geneticAlgorithm = GeneticAlgorithm(population_size=popsize,
                                    elitism=elitism,
                                    mutation_rate=p,
                                    mutation_scale=K,
                                    iterations=iter,
                                    neural_net_architecture=nn_architecture,
                                    train_dataset=train_dataset,
                                    test_dataset=test_dataset
                                    )
   geneticAlgorithm.evolve()

if __name__ == '__main__':
   main()