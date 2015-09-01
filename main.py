from __future__ import division
import random

def converter(input, numberOfOrganisms, numberOfChroms):
	mathExpressionGene = []
	mathExpressionChroms = []
	for i in range(0, numberOfOrganisms):
		for x in range(0, numberOfChroms):
			term = 0
			if (''.join(map(str, input[i][x])) == '1010'):
				term = '+'
			elif(''.join(map(str, input[i][x])) == '1011'):
				term = '-'
			elif(''.join(map(str, input[i][x])) == '1100'):
				term = '*'
			elif(''.join(map(str, input[i][x])) == '1101'):
				term = '/'
			elif(''.join(map(str, input[i][x])) == '1110'):
				term = 'inv'
			elif(''.join(map(str, input[i][x])) == '1111'):
				term = 'inv'
			else:
				term = int(''.join(map(str, input[i][x])), 2)
			mathExpressionGene.append(term)
		mathExpressionChroms.append(mathExpressionGene)
		mathExpressionGene = []
	return mathExpressionChroms

def clean(input, numberOfOrganisms, numberOfChroms, numberOfGenes):
	evaluated = []
	evaluatedOrganismLevel = []
	for y in range(0, numberOfOrganisms):
		alternator = 0
		for i in range(0, numberOfChroms):
			if alternator == 0:
				if isinstance(input[y][i],(int, long)):
					evaluated.append(input[y][i])
					alternator = 1
			elif alternator == 1:
				if not isinstance(input[y][i],(int, long)) and not input[y][i] == 'inv':
					evaluated.append(input[y][i])
					alternator = 0
		if len(evaluated) > 0:
			if not isinstance(evaluated[len(evaluated)-1],(int, long)):
					evaluated.pop()

		evaluatedOrganismLevel.append(evaluated)
		evaluated = []

	return evaluatedOrganismLevel
	
def evaluate(population, numberOfOrganisms):
	evaluated = []
	for i in range(0, numberOfOrganisms):
		try:
			evaluated.append(eval(''.join(map(str, population[i]))))
		except:
			evaluated.append(0)
	return evaluated

def mutate(input, chromosones, genes, mutationRate): # can only be fed a single organism at a time
	for i in range(0, chromosones):
		for x in range(0, genes):
			rand = random.uniform(0,1)
			if (rand <= mutationRate):
				if input[i][x] == 0:
					input[i][x] = 1
				else:
					input[i][x] = 0
	return input

def calcFitness(evaluatedPopulation, wantedValue, numberOfOrganisms):
	organismFitness = []
	for i in range(0, numberOfOrganisms):
		if abs(wantedValue) == abs(evaluatedPopulation[i]):
			organismFitness.append(2)
		elif abs(wantedValue) > abs(evaluatedPopulation[i]):
			organismFitness.append(abs(-1+abs(wantedValue-evaluatedPopulation[i])/abs(wantedValue)))
			if organismFitness[len(organismFitness)-1] == 0:
				organismFitness[len(organismFitness)-1] = 0.0001
		else:
			organismFitness.append(abs(-1+abs(evaluatedPopulation[i]-wantedValue)/abs(evaluatedPopulation[i])))
			if organismFitness[len(organismFitness)-1] == 0:
				organismFitness[len(organismFitness)-1] = 0.0001

	return organismFitness

def createRandPop(numberOfOrganisms, chromosones, genes):
	# creating a population
	individualGenes = []
	individualChromosone = []
	organisms = []
	population = []
	for x in range(0,numberOfOrganisms):
		for y in range(0,chromosones):
			for i in range(0,genes):
				individualGenes.append(random.randint(0,1))

			individualChromosone.append(individualGenes) # population,organisms's,chroms,genes
			individualGenes = []
		organisms.append(individualChromosone)
		individualChromosone = []
	return organisms

def newPopGen(rouletteSelection, numberOfChroms, numberOfGenes, population, sizeOfWantedPopulation, mutationRate, crossoverProb):
	pop = []
	while(len(pop) < sizeOfWantedPopulation):
		tempChromPop = []
		tempGenePop = []
		crossoverProb = crossoverProb*100
		crostest = random.randint(0, 100)
		if crostest >= crossoverProb:
			pop.append(population[rouletteSelection[0]])
			pop.append(population[rouletteSelection[1]])
			continue
		randGeneNum = random.randint(0, numberOfGenes-1)
		randChromNum = random.randint(0, numberOfChroms-1)
		for i in range(0, numberOfChroms):
			for x in range(0, numberOfGenes):
				if randChromNum <= i and randGeneNum <= x:
					tempGenePop.append(population[rouletteSelection[1]][i][x])
				else:
					tempGenePop.append(population[rouletteSelection[0]][i][x])

			tempChromPop.append(tempGenePop)
			tempGenePop = []

		tempChromPop = mutate(tempChromPop, numberOfChroms, numberOfGenes, mutationRate)
		pop.append(tempChromPop)
		tempChromPop = []

	return pop


def printEquations(fitnessOfPopulation, cleanedPopulation, evaluatedPopulation, numberOfOrganisms):
	for i in range(0, numberOfOrganisms):
		if fitnessOfPopulation[i] == 2:
			print ''.join(map(str, cleanedPopulation[i]))
			print "Value of :"+str(evaluatedPopulation[i])
			found += 1
	print "We found: " + str(found) + " equations!!!"


def roulette(numberOfOrganisms, numberOfValuesWanted, populationFitness):
	rouletteSelection = []
	total = float(sum(populationFitness))
	while len(rouletteSelection)<numberOfValuesWanted:
		current = 0
		pick = random.uniform(0, total)
		for i in range(0, len(populationFitness)):
			current += populationFitness[i]
			if (current > pick) and not(i in rouletteSelection):
				rouletteSelection.append(i)
				break

	return rouletteSelection

def averageFitness(fitnessOfPopulation, cleanedPopulation, bestAws, bestScore):
	total = 0
	for x in range(0, len(fitnessOfPopulation)):
		if bestScore < fitnessOfPopulation[x]:
			bestScore = fitnessOfPopulation[x]
			bestAws = cleanedPopulation[x]
		total += fitnessOfPopulation[x]

	print (total/len(fitnessOfPopulation))
	return bestAws, bestScore

def algorithm():
	bestScore = 0
	bestAws = []
	population = createRandPop(numberOfOrganisms, numberOfChroms, numberOfGenes)
	for x in range(0, generations):
		convertedPopulation = converter(population, numberOfOrganisms,numberOfChroms)
		cleanedPopulation = clean(convertedPopulation, numberOfOrganisms, numberOfChroms, numberOfGenes)
		evaluatedPopulation = evaluate(cleanedPopulation, numberOfOrganisms)
		fitnessOfPopulation = calcFitness(evaluatedPopulation, wantedValue, numberOfOrganisms)
		rouletteSelection = roulette(numberOfOrganisms, 2, fitnessOfPopulation)
		population = newPopGen(rouletteSelection,numberOfChroms, numberOfGenes, population, numberOfOrganisms, mutationRate, crossoverProb)
		bestAws, bestScore = averageFitness(fitnessOfPopulation, cleanedPopulation, bestAws, bestScore)
		print x+1, "out of", generations
	print ("The Best Score was", bestScore, 'with the awnswer of', ''.join(map(str, bestAws)))


wantedValue = 987654321
numberOfOrganisms = 10
numberOfGenes = 4 # number of bits
numberOfChroms = 100 # number of genes
crossoverProb = 0.7
mutationRate = 0.05
generations = 5000

algorithm()