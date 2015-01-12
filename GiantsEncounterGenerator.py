#This program released for everybody to use and tweak. If you manage to break
#your computer with it, that's your problem, and you'll have to handle it. 
#Essentially, this is GPL licesnce 
#The program was run and tested for total of about 10(!) times on my mahcine,
#With opensuse as an OS. It should work on every Linux os, and break on Windows
#Machines. Mac machine, should probably work too. You can remove the plotting
#part for it to work on your machine. 
#You need numpy for the program, to run, and pyplot for the plot, but you can
#throw this part away


from random import random
from random import randint as rint
import numpy as np
import matplotlib.pyplot as plt
from XP_hardness_maker import *
from Make_treasure import *



class Amonster:
    # A small class to print the important stuff about the monster. A proper way
    # to do this is to throw all the data in a text file and find the
    # approperiate line at the file. I guess that eventually I'll do that
    def __init__(self,kind,loot):
        self.kind = kind
        print ('\033[1m') 
        print (kind + '\033[0m') # Print the name of the monster in bold face
        print ('page: '+self.page())
        print ('HP: ' + self.hp_roller())
        print ('Init: ' + self.init_roller())
        #print the loot
        print ('\x1B[3m*Loot\x1B[23m')
        for l in loot:
            n = loot[l]
            if n == 0: continue
            print ('{l}: {n}'.format(l=l,n=loot[l]))
    
    def page (self): #The page in the monster manual
        if self.kind == 'hill':
            return '155'
        elif self.kind == 'stone':
            return '156'
        elif self.kind == 'dragon':
            return '102'

        
    def init_roller(self): #initiative roller. The bonus is base on the MM

        if self.kind == 'hill':
            bonus = -1
        elif self.kind == 'stone':
            bonus = 2
        elif self.kind == 'dragon':
            bonus = 0
        return str(rint (1,20) + bonus)

    def hp_roller(self):
        #Rolling hit points
        # out - the number to return starts with the HP bonus the monster has
        # d the die type 
        # nd the number of dies to throw 
        if self.kind == 'hill':
            out =40 
            d = 12
            nd = 10
        elif self.kind == 'stone':
            out = 60
            d = 12
            nd = 12
        elif self.kind == 'dragon':
            out = 10
            d = 8
            nd = 5
        i = 0
        while i < nd:
            out += rint (1,d)
            i += 1
        return str(out)
    
def fprob (x): 
    #This is the comulative probability function. 
    #The higher the XP (X) you put it, the hight the value it produce. 
    #It is far from a proper probability function, but it is good enough for our
    #needs. The 0.7 and 0.2 are empirical values, and you can change them

    X = x-xptable['hard']*0.7
    X /=  xptable['hard']*0.2
    return 1.0/(1.0 + np.exp(-X))

def plot_diffculty(xptable):
    #Here I plot the probability function
    X= np.linspace(0,xptable['deadly'],1000)
    dx = X[2] - X[1]
    Y = fprob(X)
    dY = [Y[i+1]/dx - Y[i]/dx for i in range (len(Y)-1)]
    dY.append(0)
    dY = np.array(dY)/max(dY)

    fig = plt.figure()
    ax = fig.add_axes((0.1,0.2,0.8,0.7))
    ax.plot(X,fprob(X),label=r'$P$ (cumulative)')
    ax.plot(X,dY,label=r'$p$')

    #marking XP levels
    for hard in xptable:
        x = xptable[hard]
        y = fprob(x)
        ax.annotate(hard,xy=(x,y))#the name
        ax.scatter(x,y,color='black')#the value
    #tidy up
    ax.plot((min(X),max(X)),(0.5,0.5),ls='-.',color='black')
    ax.set_xlim(0,xptable['deadly'])
    ax.set_ylim(0,1)
    ax.set_xlabel('Total encounter XP Value')
    ax.set_ylabel('Probability of accepting the encoutner')
    ax.legend(loc=2)
    fig.text(0.2,0.05,r'''Probability ($p$) and cumulative probability ($P$) as a function of 
    encounter xp level''')
    fig.savefig('/tmp/play.png')# store the plot
    fig.savefig('/tmp/play.pdf')



def count(name):
    #Unlike the monster class above, here I do have everything in a file called
    #pool.txt. The first number is number of individuals remained in the pool
    #file. The second is the weight, and the third is the number of ''specials''
    #The DM responsability is to update the pool whenver a monster dies
    f = open('pool.txt').readlines()[:]
    for line in f:
        words = line.split('=')
        if name == words[0].lower().strip():
            words = words[1].split()
            # the first number is the number of monsters in the pool
            # the second of the number is the "weight of the monster" 
            # the higher that number is, the higher the probability of this
            # monster to be picked by the generator
            return [int(words[i]) for i in range (len(words))]


hill = count('hill')
dragon = count('dragon')
stone = count('stone')


#The XP and CR of each monster in the pool
xpcr = {'hill':[1800,5],'stone':[2900,6],'dragon':[450,2]} 
# the number and weigt of each number in the pool, a proper way to do this is in
# the counter function above. Probebly next time
P = {'hill':hill,'stone':stone,'dragon':dragon}

tres_pool = make_treasure(P) #Get the treasure list
#XP dificaulty values, based on the PCs level
character_levels = {5:4,6:1}
xptable = xp_hardness_calc(character_levels)

#The probability to pick a certain monster

def RP_Calc(Pin):
    out = {}
    pcom = 0
    #the total value of the number and the weights. Serves as a poor man partion
    #function
    tp = sum([Pin[p][0]*Pin[p][1] for p in Pin])
    if tp == 0:
        print ("All the monsters are dead now\n go home")
        exit()
        
    for name in P: #This is the actualy probabilities calculation
        pname = Pin[name][0]*Pin[name][1]*1.0/tp
        if pname == 0:
            continue
        pcom += pname 
            
        out[pcom] = name
    return out

RP = RP_Calc(P)

xpval = 0

for m in P:
    plot_treasure(tres_pool,m)
n_monsters = 0
loot = {}
while True: #Generate the encoutner
    p = random() # Create a random number between 0 and 1
    for pm in sorted(RP.keys()): 
        # go throw the monsters and pick the appropriate one
        if p < pm:#If the number is less than the monster porbability, take it
            monster = RP[pm]
            break
    
    if P[monster][0] == 0:
        #Exhusted the monsters of this kind from the pool. Restart the loop
        continue 

    #Create treasure, for convinience, this is in separate file
    ctres = roll_treasure(tres_pool,monster)

    xpval += xpcr[monster][0]#The xp value, without the multiplayer
    
    # determine the multipplier. See the DM basic rules, page 57
    n_monsters += 1 
    if n_monsters == 1:
        multi = 1
    elif n_monsters == 2:
        multi = 1.5
    elif n_monsters <= 6:
        multi = 2
    elif n_monsters <= 10:
        multi = 2.5
    elif n_monsters <= 14:
        multi = 3
    else:
        multi = 4

    
    #update the monster pool
    P[monster][0] -= 1 
    #update the treasure pool
    for t in ctres:
        tres_pool[t].potential_removed(monster)
        tres_pool[t].items_removed(ctres[t])
    #Note that this doesn't chage the pool.txt file
    RP = RP_Calc(P)# We have removed a monster from the pool, new probabilities! 
    Amonster(monster,ctres)# The class above. Essentially, a nice wrapper to print data
    

    p = random() # A new random number, determine if this is a "special" monster
    if P[monster][2]*1.0/P[monster][0] > p:
        print ('Unique') #Again, the DM is responsible on changing the pool file

    p = random()# Generate new ranomd number
    if p < fprob(xpval*multi): #Exit the loop
        print ('Encounter XP: ' + str(xpval))
        print ('Diffculty XP: ' + str(xpval*multi))
        break
