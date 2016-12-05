
import sys, numpy as np, os, random


class Evolver(object) :
    def __init__(self, population, parents, mrate, length, value_range, int_type=True):
        # population size
        self.population = population
        # number of parents in every generation
        self.parents = parents
        # mutation rate
        self.mrate = mrate
        # tournament pool
        self.tourn = int(parents / 2)
        # dimention of a creature
        self.length = length
        # value range (min,max)
        self.value_range = value_range
        # data type
        self.int_type = True
        # current population pool - randoms
        self.startPool()
        # previous population pool
        self.prevpool = np.zeros((population, self.length)) 
        # current population fitness
        self.curfit = np.zeros(self.population)
        # previous population fitness
        self.prevfit = np.zeros(self.population)
        # fittest overall (creature, error)
        self.fittest = []
        # fittest current gen (creature, error)
        self.fitest_curgen = []
        # array of errors in (%,real value)
        self.errors = []
        
    def startPool(self):
        self.curpool = np.random.choice(np.arange(self.value_range[0],self.value_range[1]),size=(self.population,self.length),replace=True)
        if self.int_type:
            self.curpool = self.curpool.astype(int)
    
    def mate(mom, dad):
        cutoff = np.random.randint(0,self.length)  
        return np.concatenate(mom[:cutoff],dad[cutoff:])
        
    def evolve(self, fitfunc):
        print('starting evolution cycle...')
        # fitfunc takes vector and returns its fitness
        self.prevpool = np.copy(self.curpool)
        self.prevfit = np.copy(self.curfit)
        # dummy next population array
        self.curpool = np.zeros((self.population, self.length))
        # dummy winners array - to use as parents
        self.winners = np.zeros((self.parents,self.length))
        # dummy children array
        self.children = np.zeros((self.population-self.parents,self.length))
        # Each element of curfit is an array consisting of the index of the 
        # creature's fitness, e.g. nth element [2.54] means that the nth  
        # element in prevpool (nth individual) has a fintess of 2.54
        self.curfit = np.apply_along_axis(fitfunc,1,self.prevpool)
        # select winners based on a tournament system
        print('got fitness estimation')
        for n in xrange(self.parents):
            print('selecting parents...')
            # select random solutions - indexes of fitVec
            # tournament size is half
            selected = np.random.choice(range(len(self.curfit)), self.tourn, replace=False)
            print('toutrament:')
            print(selected)
            # find min from those selected - index in selected
            wnr = np.argmin(self.curfit[selected])
            # store the winner
            print('winner index:')
            print(wnr)
            self.winners[n] = self.prevpool[wnr]
            print('winner:')
            print(self.winners[n])
        # create children
        print('mating in progress...')
        for n in xrange(0,self.population - self.parents,2):
            # get random elite parent
            mom = self.winners[np.random.randint(0, self.parents)]
            # get random any parent
            dad = self.prevpool[np.random.randint(0, self.population)]
            # generate cutoff for crossover
            cutoff = np.random.randint(0,self.length)  
            # join two parents
            self.children[n] = np.concatenate((mom[:cutoff],dad[cutoff:]))
            if n+1 < len(self.children):
                self.children[n+1] = np.concatenate((dad[:cutoff],mom[cutoff:]))
        # introduce mutation
        # [1] matrix with some deviations multiplied with nextPop
        print('creating xmen...')
        mutants = np.matrix([np.float(np.random.normal(1,0.3,1)) if random.random() < self.mrate else 1 for x in range(self.children.size)]).reshape(self.children.shape)
        self.children = np.multiply(self.children, mutants)
        print('creating new generation...')
        # create new current population
        self.curpool = np.concatenate((self.winners,self.children))
        if self.int_type:
            self.curpool = self.curpool.astype(int)
        # find the fittest and save
        fittestInd = np.argmin(self.curfit)
        self.fittest_curgen = (self.prevpool[fittestInd], self.curfit[fittestInd])
        print('current fittest index is')
        print(self.fittest_curgen)
        # save errors
        if not self.fittest:
            self.errors.append((100, self.fittest_curgen[1]))
            # save as best result
            self.fittest = self.fittest_curgen
        else:
            self.errors.append((((self.fittest_curgen[1]/self.errors[0][1])*100), self.fittest_curgen[1]))
            #check if best result and save
            if self.fittest_curgen[1] < self.fittest[1]:
                self.fittest = self.fittest_curgen
        


def shuffle2d(arr):
    oned = arr.flatten()
    np.random.shuffle(oned)
    twod = np.reshape(oned, arr.shape)
    return twod

"""
# number of photo
value_range = [0,8]
# resolution , should be square
length = 4 # 20x20
population = 10
parents = 4
mrate = 0.1


ev = Evolver(population, parents, mrate, length, value_range)

print(ev.curpool)

def func(x):
    return sum(x)

ev.evolve(func)
print('ev.curfit:')
print(ev.curfit)
print('ev.winners')
print(ev.winners)
print('ev.children')
print(ev.children)
print('ev.curpool')
print(ev.curpool)
print('fittest')
print(ev.fittest)
"""
