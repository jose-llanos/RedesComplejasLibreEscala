import numpy as np, random, operator, pandas as pd

import networkx as nx

class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def distance(self, city):
        xDis = abs(self.x - city.x)
        yDis = abs(self.y - city.y)
        distance = np.sqrt((xDis ** 2) + (yDis ** 2))
        return distance
    
    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"
    
class Fitness:
    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fitness= 0.0
    
    def routeDistance(self):
        if self.distance ==0:
            pathDistance = 0
            for i in range(0, len(self.route)):
                fromCity = self.route[i]
                toCity = None
                if i + 1 < len(self.route):
                    toCity = self.route[i + 1]
                else:
                    toCity = self.route[0]
                pathDistance += fromCity.distance(toCity)
            self.distance = pathDistance
        return self.distance
    
    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance())
        return self.fitness
    
def createRoute(cityList):
    route = random.sample(cityList, len(cityList))
    return route

def initialPopulation(popSize, cityList):
    population = []

    for i in range(0, popSize):
        population.append(createRoute(cityList))
    return population

def rankRoutes(population):
    fitnessResults = {}
    for i in range(0,len(population)):
        fitnessResults[i] = Fitness(population[i]).routeFitness()
    return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)

def selection(popRanked, eliteSize):
    selectionResults = []
    df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    
    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])
    for i in range(0, len(popRanked) - eliteSize):
        pick = 100*random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i,3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults

def matingPool(population, selectionResults):
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool

def breed(parent1, parent2):
    child = []
    childP1 = []
    childP2 = []
    
    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))
    
    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(parent1[i])
        
    childP2 = [item for item in parent2 if item not in childP1]

    child = childP1 + childP2
    return child

def breedPopulation(matingpool, eliteSize):
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))

    for i in range(0,eliteSize):
        children.append(matingpool[i])
    
    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool)-i-1])
        children.append(child)
    return children

def mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        if(random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))
            
            city1 = individual[swapped]
            city2 = individual[swapWith]
            
            individual[swapped] = city2
            individual[swapWith] = city1
    return individual

def mutatePopulation(population, mutationRate):
    mutatedPop = []
    
    for ind in range(0, len(population)):
        mutatedInd = mutate(population[ind], mutationRate)
        mutatedPop.append(mutatedInd)
    return mutatedPop

def nextGeneration(currentGen, eliteSize, mutationRate):
    popRanked = rankRoutes(currentGen)
    selectionResults = selection(popRanked, eliteSize)
    matingpool = matingPool(currentGen, selectionResults)
    children = breedPopulation(matingpool, eliteSize)
    nextGeneration = mutatePopulation(children, mutationRate)
    return nextGeneration

def geneticAlgorithmPlot(population, popSize, eliteSize, mutationRate, generations,rewiring):
    pop = initialPopulation(popSize, population)
    G = nx.generators.random_graphs.watts_strogatz_graph(popSize,3,rewiring)
    
    scores = []    
    
    for l in range(0,generations):            
        gen_scores=[]    
        for j in range(0, popSize):        
            candidato = pop[j]            
            vecinos=[]
            for k in G[j]:                
                vecinos.append(k)
                
            if(len(vecinos)>0):            
                random_index = random.sample(vecinos, 1)                                        
                pareja = pop[random_index[0]]                                
                child = breed(candidato, pareja)
                child = mutate(child,mutationRate)
                
                score_individuo  = 1/Fitness(candidato).routeFitness()
                score_child = 1/Fitness(child).routeFitness()                                
                
                if(score_child < score_individuo):                    
                    pop[j] =  child                    
                    G.add_edge(j,random_index[0])
                    gen_scores.append(score_child)
                else:
                    gen_scores.append(score_individuo)
    
        for j in range(0, popSize):            
            aristas = G.adj[j]
            
            vecinos=[]
            for k in aristas:                
                vecinos.append(k)
            
            for i in range(0,len(vecinos)):
                if random.random() < rewiring:                    
                    random_index = int(random.random()*100)                    
                    G.remove_edge(j, vecinos[i])                    
                    G.add_edge(j,random_index)                    
        
        gen_best = min(gen_scores)        
        scores.append(gen_best)
        
    return scores


cityList = []
#25 cities
for i in range(0,25):
    cityList.append(City(x=int(random.random() * 200), y=int(random.random() * 200)))
    
iteraciones = []      
promedios = []
#Number of iterations per run
maxiter = 50
#Number of experiments, to then gained the average from them in each iteration
numero_iteraciones = 50

for i in range(0,numero_iteraciones):
    print(i)
    #popsize 100, elite search 20%, rewiring 30%, mutation rate 10%
    iteracionTemporal = geneticAlgorithmPlot(population=cityList, popSize=100, eliteSize=20, mutationRate=0.01, generations=maxiter,rewiring = 0.3)

    iteraciones.append(iteracionTemporal)
    
for i in range(0,maxiter):
    sumatoria_temporal = 0
    for j in range(0,numero_iteraciones):        
        sumatoria_temporal = sumatoria_temporal + iteraciones[j][i]
            
    promedio_temporal = sumatoria_temporal / numero_iteraciones
    promedios.append(promedio_temporal)
    
print("\n")
print("Print averages per iteration:")
for i in range(0,maxiter):    
    print("%.9f"%promedios[i])