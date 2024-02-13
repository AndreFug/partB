import random as rd

# Define classes and their capacities
classCapacities  = {
    "Math": 54,
    "Physics": 42,
    "Chemistry": 36,
    "Biology": 37,
    "History": 22
}

# Define available rooms and their capacities
roomCapacities  = {
    "Room1": 65,
    "Room2": 36,
    "Room3": 25
}

# Genetic Algorithm parameters
pop_size = 100
maxGen = 1000
mutation_rate = 0.01

def initialize_population():
    population = []
    for _ in range(pop_size):
        chromosome = []
        remainingClasses = list(classCapacities.keys())
        remainingRooms = list(roomCapacities.keys())
        while remainingClasses:
            if not remainingRooms:
                remainingRooms = list(roomCapacities.keys())  # Reset remainingRooms if it becomes empty
            selectedRoom = rd.choice(remainingRooms)
            selectedClass = rd.choice(remainingClasses)
            remainingClasses.remove(selectedClass)
            chromosome.append(selectedRoom)
            remainingRooms.remove(selectedRoom)
        population.append(chromosome)
    return population


def fitness(chromosome):
    usedRooms = set(chromosome)
    numRooms = len(usedRooms)
    totalFit = numRooms
    for room in usedRooms:
        roomCap = roomCapacities[room]
        classesInRoom = [cls for cls, assignedRoom in zip(classCapacities.keys(), chromosome) if assignedRoom == room]
        totalCap = sum(classCapacities[cls] for cls in classesInRoom)
        fitnessValue = abs(totalCap - roomCap) / roomCap
        totalFit += fitnessValue
    return totalFit




def selection(population, k=2):
    # Calculate fitness values for all individuals in the population
    fitnessValues = [fitness(chromosome) for chromosome in population]
    
    # Adjust fitness values to ensure positive weights for selection
    minFit = min(fitnessValues)
    adjustedFitnessValues = [f - minFit + 1 for f in fitnessValues]

    # Perform selection with adjusted weights
    selectedInd = rd.choices(population, weights = adjustedFitnessValues, k=k)

    return selectedInd


def crossover(parent1, parent2):
    crossoverPoint = rd.randint(1, len(parent1) - 1)
    child1 = parent1[:crossoverPoint] + parent2[crossoverPoint:]
    child2 = parent2[:crossoverPoint] + parent1[crossoverPoint:]
    return child1, child2

def mutate(chromosome):
    mutatedChromosome = chromosome[:]
    for i in range(len(mutatedChromosome)):
        if rd.random() < mutation_rate:
            mutatedChromosome[i] = rd.choice(list(roomCapacities .keys()))
    return mutatedChromosome


def genetic_algorithm(elitism=True, elitism_ratio = 0.1, max_iterations = 20):
    bestSolution = None
    bestFit = float('inf')
    
    for iteration in range(max_iterations):
        population = initialize_population()
        generationsNoImprovement = 0
        
        for generation in range(1, maxGen + 1):
            newPop = []
            
            if elitism:
                numElites = max(1, int(elitism_ratio * pop_size))
                elites = sorted(population, key=fitness)[:numElites]
                newPop.extend(elites)
            
            for _ in range(pop_size // 2 - numElites if elitism else pop_size // 2):
                parent1, parent2 = selection(population)
                child1, child2 = crossover(parent1, parent2)
                child1 = mutate(child1)
                child2 = mutate(child2)
                newPop.extend([child1, child2])
            
            population = newPop
            currentBestSolution = min(population, key=fitness)
            currentBestFit = fitness(currentBestSolution)
            
            if currentBestFit < bestFit:
                bestSolution = currentBestSolution
                bestFit = currentBestFit
                generationsNoImprovement = 0
                
                # Print information about the best solution for the current generation
                print(f"Iteration {iteration + 1}, Generation {generation}:")
                print("Best solution:", bestSolution)
                print("Fitness:", bestFit)
            else:
                generationsNoImprovement += 1
            
            if generationsNoImprovement >= maxGen // 20:  
                break
        
        if bestFit == 0:  # Terminate if the best solution is found
            break
    
    return bestSolution

bestSolution = genetic_algorithm(elitism=True)
print("\nFinal Best Solution:")
print("Best solution:", bestSolution)
print("Fitness:", fitness(bestSolution))
