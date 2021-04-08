import numpy as np
import random
#to improve:
#1. recovery rate b is now treated to be a set amount of days, need to change to SIR model which is 1-e^(-bt)
#when we did random number, the chances of getting infected by more than one strain at the same time and mutating is really low (as it should be)


n_strain = 2       #starting off with 2 strains
max_strain = 10
a = np.random.rand(max_strain)     #infection rate of each strain, take a random probability from 0 to 1
b = np.random.rand(max_strain) * 14     #randomly generated average healing time
infected = np.zeros(max_strain)     #for each strain, record number of people currently infected to calculate potential infections

# print(str(a))
# print(str(b))
N = 20          #number of people in population
m = 0.5         #probability of mutation

med_rec = np.zeros((N, max_strain))   #for every person and every strain, record state of person with strain
death = np.zeros((N,), dtype=bool)



#initialize random people getting sick
for s in range(n_strain):       # randomly select one person to be infected with each strain
    med_rec[random.randint(0,N-1),s] = 1
    infected[s]+=1

t_range = 1000

for t in range(t_range-1):
    #print(str(t))
    #print(str(n_strain))
    print(str(med_rec))
    for p in range(N-1):  #for ever person
        if death[p]:        #this person no longer exist
            continue
        ill = 0     #keep track of whether the person is infected with more than one disease
        for s in range(n_strain-1):   #for every current existing strain
            if med_rec[p,s] == -1:      #this person is immune to this strain
                continue
            elif med_rec[p,s] == 0: #potentially be infected by exisiting virus
                #print(str(random.uniform(0,1)*infected[s])+" "+str(a[s]))
                if random.uniform(0,1)*infected[s]  > a[s]:      #gets sick for a probability, more people infected with the strain more likely it is for others to catch it
                    #TODO: handle the probability of infection better
                    med_rec[p,s] = 1
                    ill+=1
                    infected[s]+=1
            else:   #potentially heal or make a mutate strain if already ill
                if med_rec[p,s] > b[s]:       #healed
                    med_rec[p,s] = -1
                    infected[s] -= 1
                    continue    #move on to the next strain for this person
                else:
                    med_rec[p,s]+=1      #increment number of days being ill
                    ill+=1
                    #TODO: add chance of dying, perhaps related to how long the infection is
        if ill > 1:     #if infected with more than one strain
            #print(str(random.uniform(0,1))+" "+m)
            #PROBLEM: never gets into this situation
            if random.uniform(0,1) > m: #mutate
                print("new strain!")
                n_strain+=1
                med_rec[p] = 0  #reset entire row to 0 when we have multiple infections
                med_rec[n_strain-1] = 1 #-1 because we are using index


#TODO: need to go through array and tally up results (and pre-store them before plotting)