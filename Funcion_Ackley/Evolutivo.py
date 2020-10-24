import random
import operator
import math

def fitness(x):
    c=2*math.pi    
    res1=math.sqrt(0.5*((x[0]**2)+(x[1]**2)))
    sum1 = -20*math.exp(-0.2*(res1))    
    res2=0.5*(math.cos(c*x[0])+math.cos(c*x[1]))
    sum2 = -math.exp(res2)    
    resultado =sum1 + sum2+ math.e + 20        
    return resultado

#genetic algorithm function
def generateInd (bounds):	
   indv = []        
   for j in range(len(bounds)):              
       indv.append(random.uniform(bounds[j][0],bounds[j][1]))
   return indv
    
def generateFirstPopulation(sizePopulation, bounds):
    population = []    
    i = 0
    while i < sizePopulation:
        population.append(generateInd(bounds))
        i+=1    
    return population

def computePerfPopulation(population):
    populationPerf = {}
    populationSorted = {}
    i = 0
    for individual in population:
        populationPerf[i] = fitness(individual)
        i+=1
    arraySorted = sorted(populationPerf.items(), key = operator.itemgetter(1), reverse=False)
    
    for j in range(len(populationPerf)):              
        populationSorted[j] = population[arraySorted[j][0]]
    
    return populationSorted

def selectFromPopulation(populationSorted, best_sample, lucky_few):
	nextGeneration = []
	for i in range(best_sample):
		nextGeneration.append(populationSorted[i])
	for i in range(lucky_few):
		nextGeneration.append(random.choice(populationSorted))
	random.shuffle(nextGeneration)
	return nextGeneration

def createChild(individual1, individual2):
    child = []
    
    for i in range(len(individual1)):
        if (int(100 * random.random()) < 50):
            child.append(individual1[i])
        else:
            child.append(individual2[i])
    
    return child

def createChildren(breeders, number_of_child):
    nextPopulation = []

    for i in range(len(breeders)/2):
        for j in range(number_of_child):
            nextPopulation.append(createChild(breeders[i], breeders[len(breeders) -1 -i]))
    return nextPopulation

def mutateWord(ind,bounds):
    index_modification = int(random.random() * len(ind))
    new_value = random.uniform(bounds[j][0],bounds[j][1])
    new_ind = ind
    new_ind[index_modification] = new_value
    return ind
	
def mutatePopulation(population, chance_of_mutation, bounds):
    
    for i in range(len(population)):
        for j in range(len(bounds)):
            if random.random() * 100 < chance_of_mutation:
                population[i][j] = random.uniform(bounds[j][0],bounds[j][1])
                
    return population

def nextGeneration (firstGeneration, bounds, best_sample, lucky_few, number_of_child, chance_of_mutation):
	 populationSorted = computePerfPopulation(firstGeneration)
	 nextBreeders = selectFromPopulation(populationSorted, best_sample, lucky_few)
     
	 nextPopulation = createChildren(nextBreeders, number_of_child)
	 nextGeneration = mutatePopulation(nextPopulation, chance_of_mutation, bounds)
	 return nextGeneration

def multipleGeneration(number_of_generation, bounds, size_population, best_sample, lucky_few, number_of_child, chance_of_mutation):
    historic = []
    historic.append(generateFirstPopulation(size_population, bounds))
    
    for i in range (number_of_generation):
        historic.append(nextGeneration(historic[i], bounds, best_sample, lucky_few, number_of_child, chance_of_mutation))
    return historic

def getBestIndividualFromPopulation (population):
	return computePerfPopulation(population)[0]

def getListBestIndividualFromHistorique (historic):
	bestIndividuals = []
	for population in historic:
		bestIndividuals.append(getBestIndividualFromPopulation(population))
	return bestIndividuals

def mejorSolucionPorIteracion(historic):        	
    evolutionFitness = []
    for population in historic:
        evolutionFitness.append(format(fitness(getBestIndividualFromPopulation(population)),'.10f' ))        
    return evolutionFitness

def evolutionAverageFitness(historic, size_population):
    
    evolutionFitness = []
    for population in historic:
        populationPerf = computePerfPopulation(population)
        averageFitness = 0
        
        for i in range (len(populationPerf)):
            averageFitness += fitness(populationPerf[i])
        evolutionFitness.append(averageFitness/size_population)
        
bounds = [(-5,5),(-5,5)]
size_population = 100
best_sample = 20
lucky_few = 20
number_of_child = 5
number_of_generation = 50
chance_of_mutation = 5

if ((best_sample + lucky_few) / 2 * number_of_child != size_population):
	print ("population size not stable")
else:    
    iteraciones = []
    promedios = []
    
    numero_iteraciones = 100
    
    for i in range(0,numero_iteraciones):
        historic = multipleGeneration(number_of_generation, bounds, size_population, best_sample, lucky_few, number_of_child, chance_of_mutation)
        
        iteracionTemporal = mejorSolucionPorIteracion(historic)
        iteraciones.append(iteracionTemporal)
        
    for i in range(0,number_of_generation):
        sumatoria_temporal = 0
        for j in range(0,numero_iteraciones):
            sumatoria_temporal = sumatoria_temporal + float(iteraciones[j][i])
            
        promedio_temporal = sumatoria_temporal / numero_iteraciones
        promedios.append(promedio_temporal)
        
    print "\n"
    print "Promedios de las iteraciones"
    for i in range(0,number_of_generation):
        print "%.9f"%promedios[i]
    