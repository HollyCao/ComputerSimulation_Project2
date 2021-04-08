import numpy as np
import random

n_strain = 2       #starting off with 2 strains
max_strain = 10

#ASSUMPTION: we are assuming a disease with mutation that happens when more than one strain is in the same person's body at the same time (which is totally not necessarily the case)


a = np.random.rand(max_strain)     #infection rate of each strain, take a random probability from 0 to 1
b = np.random.rand(max_strain) * 14     #randomly generated average healing time
print(str(a)+"\n"+str(b))
#NOTE: two lines below are random numbers we set, change to the two lines above for random instead of deterministic model (there are other random function used in the program because they were necessary for simulation)

# a = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]      #infection rate
# b = [7, 7, 5, 7, 9, 4, 5, 6, 3, 8]         #mean date it takes to recover5

infected = np.zeros(max_strain)     #an 1D array to record how many people are currently infected, basically the I variable but for each strain for each strain, we use this to ramp up new infection rate based on how many people are currently infected

N = 20          #number of people in population
m = 0.1         #1-probability of mutation, in this case probability of mutation is 0.05

med_rec = np.zeros((N, max_strain))   #A 2D array listing the state of each person (column) in pretains to each strain (row), where -1 is immune, 0 is susceptible, and 1 and above is infected and recording the number of days of infection

#########INITIALIZING ARRAYS WE WANT TO PLOT###############

P_mutation = np.zeros(max_strain)            #when does each mutation happen


#########END OF INITIALIZING ARRAYS WE WANT TO PLOT########


#ASSUMPTION: we are not taking death into consideration
#ASSUMPTION: randomly select one person to be infected with each strain that we start with (leftmost n_strain strains on the med_rec array)
for s in range(n_strain):
    med_rec[random.randint(0,N-1),s] = 1
    infected[s] = 1     #record first infection for the strain
    P_mutation[s] = 0   #we have it from time 0 without mutation

t_range = 100          #change this to simulate time period

I_mean = 0.2        #neutral in terms of infected or not infected, can change this, used in gaussian distribution of infection
for t in range(t_range-1):
    print(str(med_rec))
    #print("infection arr: "+str(infected))
    print("t = " + str(t))

    for p in range(N):  #for ever person
        ill = 0     #keep track of whether the person is infected with more than one disease, if so they are eligible for mutation (ASSUMPTION: not counting for infection this iteration)
        #print("person "+str(p))
        #ASSUMPTION: no one dies from the disease (so far)
        for s in range(n_strain):   #for every current existing strain
            if med_rec[p,s] == -1:      #this person is immune to this strain
                continue
            elif med_rec[p,s] == 0: #potentially be infected by exisiting virus
                if random.gauss(I_mean-infected[s]/N,1)  < a[s]:      #gets sick for a probability, more people infected with the strain more likely it is for others to catch it

                    #ASSUMPTION: we are using a gaussian distribution with mean around the middle (0.5) and standard deviation of infected/population of that desease to simulate encounterance
                    #instead of pre-calculating new infections which is I_new = I_old * e^(-bt) in notes, we are simulting the chances of infection
                    #ASSUMPTION: everyone have the same chance of encountering each other in the community
                    med_rec[p,s] = 1
                    infected[s]+=1
            else:   #potentially heal or make a mutate strain if already ill
                if med_rec[p,s] > random.gauss(b[s],1):       #healed
                    #ASSUMPTION: we are using gaussian function to simulate normal distribution of recovery around b[s] which is the mean rate we decided, and we're using 1 as standard deviation
                    med_rec[p,s] = -1
                    infected[s]-=1
                    continue    #move on to the next strain for this person
                else:
                    med_rec[p,s]+=1      #increment number of days being ill
                    ill+=1

        if n_strain >= max_strain:          #we can't mutate because our data structures only support so many strains
            continue

        if ill > 1:     #if infected with more than one strain
            if random.uniform(0,1) > 1-m: #mutate
                print("mutation @ time "+str(t)+" on strain "+str(n_strain)+" person "+str(p))
                P_mutation[n_strain] = t
                n_strain+=1
                med_rec[p] = 0  #reset entire row to 0 when we have multiple infections
                med_rec[p,n_strain-1] = 1 #-1 because we are using index


print("Mutation times: "+str(P_mutation))
#TODO: need to go through array and tally up results (and pre-store them before plotting)