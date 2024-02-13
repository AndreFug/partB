import random as rd
import string

# Paramaters
pop_size = 250
tournament_size = 4
crossover_rate = 2
mutation_rate = 0.1
eliteism_rate = 0.3

# Define the target string and gene set
target_string = "André_Fugledal*586780" # String length 21
geneset = "a","b","c","d","e","é","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","-","^","_","*","!","1","2","3","4","5","6","7","8","9","0",


def generate_random_string(length):
    return ''.join(rd.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def fitnesFunction(ind):
    numMatchingChars = sum(1 for i, j in zip(ind, target_string) if i == j)
    return numMatchingChars / len(target_string)

def genInitialPop(pop_size):
    return [generate_random_string(len(target_string)) for _ in range(pop_size)]

def tournament(pop, fitnessValue, tournament_size):
    selected = []
    for _ in range(len(pop)):
        tournamentt = rd.sample(list(zip(pop, fitnessValue)), tournament_size)
        winner = max(tournamentt, key = lambda x: x[1])[0]
        selected.append(winner)
    return selected

def singePointCrossover(parent1, parent2):
    crossover_point = rd.randint(1,len(target_string) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2




def mutate(individual, mutation_rate):
    mutated_ind = ""
    for char in individual:
        if rd.random() < mutation_rate:
            mutated_ind += rd.choice(geneset)
        else:
            mutated_ind += char
    return mutated_ind


def genAlgoElite(population_size, tournament_size, mutation_rate, elitism_rate):
    population = genInitialPop(population_size)
    generation = 1
    bestFit = 0.0
    bestFitInd = None
    while True:
            fitness_values = [fitnesFunction(individual) for individual in population]
            max_fitness = max(fitness_values)
            best_fit_index = fitness_values.index(max_fitness)
            current_best_fit_individual = population[best_fit_index]
            
            if max_fitness > bestFit:
                bestFit = max_fitness
                best_fit_individual = current_best_fit_individual
                
            if best_fit_individual == target_string:
                print("Best fit solution found:", best_fit_individual)
                break
                
            print("Generation:", generation, "Best Fit:", best_fit_individual, "Best Fitness:", bestFit)
            
            # Implement elitism
            elites_count = int(elitism_rate * population_size)
            elites_indices = sorted(range(len(fitness_values)), key=lambda i: fitness_values[i], reverse=True)[:elites_count]
            elites = [population[i] for i in elites_indices]
            
            selected = tournament(population, fitness_values, tournament_size)
            offspring = []
            
            # Keep elites in the offspring
            offspring.extend(elites)
            
            while len(offspring) < population_size:
                parent1 = rd.choice(selected)
                parent2 = rd.choice(selected)
                child1, child2 = singePointCrossover(parent1, parent2)
                child1 = mutate(child1, mutation_rate)
                child2 = mutate(child2, mutation_rate)
                offspring.append(child1)
                offspring.append(child2)
            
            population = offspring
            generation += 1

genAlgoElite(pop_size, tournament_size, mutation_rate, eliteism_rate)
