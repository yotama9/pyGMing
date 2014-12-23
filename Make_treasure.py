from random import random
from random import randint as rint
from scipy.stats import binom
import matplotlib.pyplot as plt

class Treausre:
    #A class that store information and function related to treasure. 
    #Created using the parameters
    #potentials: the creature type that may carry this treasure
    #number: the number of items of this treasure, and integer
    #inv_prov: the inver of the probability of this item appearance
    #for now, it is simply the total number of creautre that may 
    #carry this item (not creature type, creatures)
    def __init__(self,potentials,number,inv_prob):
        self.potentials = potentials[:]
        self.number = number
        self.inv_prob = inv_prob
        self.prob = 1.0/self.inv_prob

    def potential_removed(self,pname):
        # a creature was taken out of the pool, if this creaure
        # is a potential carrier of this treasure type, update the prob
        if pname in self.potentials:
            self.inv_prob -= 1
            self.prob = 1.0/self.inv_prob
        return

    def items_removed(self,n):
        #simply update the number of items of this treasure type
        self.number -= n
        return


def make_treasure(pool):
    #This is a function to generate the probability of a certain treasure to be
    #each of the monsters. 
    #monster must be a part of the pool dictionoary pool
    #Pool is of the form 
    #
    #tressure name, number of items, targets with it, targets without it

    #Tressure name - the name, e.g. regeneration ring, magic scroll, etc.

    #number of items  - an integer.

    #targets with it - if not empty means that only this kind of creatures will
    #have it. Doesn't mean that every individual of these creatures will have
    # separated with ';'

    #targets with it - if not empty, and targets with it is empty, the only
    #creatures that won't have it. Separated by ';'
    tres_file = open ('loot.txt').readlines()[:]
    tres = {}
     
    for line in tres_file: #going every entry in the file
        #Note there is no check that the file is valid
        key,n,only,exclude = line.strip().split(',') #getting the values, 'here'
        potentials = []
        npot = 0
        only = only.strip().split(';')#Splitting the cretures by names
        exclude = exclude.strip().split(';')
        n = int(n)

        has_excl = not exclude == ['']#a flag to note there are creatures to exlude
        has_only = not only == ['']# a flag to note the item belongs to some types 
        put_all = not has_only and not has_excl # a flag saying all creature has this
        for ctype in pool: #Going throue all the creatures in the encoutner pool
            nc = pool[ctype][0]
            if put_all: #add the loot option to this monster
                potentials.append(ctype)
                npot += nc
            elif has_excl and ctype in exclude:
                continue #skip this creature
            elif has_only and not ctype in only:
                continue #skip this crearure
            potentials.append(ctype)
            npot += nc
        tres[key] = Treausre(potentials,n,npot)#Create new treasure
    return tres

        
def roll_treasure(tres_pool,cname):
    #A function to generate treasure usning a treasure pool (tres_pool)
    #uses the Treasure class above
    #cname is the creature type/name, it must be in the tres_pool.
    out = {}
    for t in tres_pool:
        
        if not cname in tres_pool[t].potentials:
            # the creature is not listed for this treasure
            continue
        #Generate probabilities tables
        nt = tres_pool[t].number
        p_loot = tres_pool[t].prob
        
        pmf = binom.pmf(range(nt+1),nt,p_loot)
        #the number at each place of the pmf is the probability of giving that 
        #number of items of this treasure type
        p = random()
        n_to_give = 0
        while p > pmf[n_to_give]:
            p -= pmf[n_to_give]
            n_to_give += 1
        out[t] = n_to_give
    return out


def plot_treasure(tres_pool,cname):
    #this function plots the treasure porbability under specified conditoin
    #It follows the roll_treasure path, but is placed separately so it will
    #be both more readable, and the script will run faster
    fig = plt.figure()
    ax = fig.add_axes([0.05,0.22,0.9,0.72])
    subax = fig.add_axes([0.6,0.3,0.25,0.25])
    colors = ('red','green','blue','black')
    ci = 0
    for t in tres_pool:
        if not cname in tres_pool[t].potentials:
            continue
        nt = tres_pool[t].number
        p_loot = tres_pool[t].prob
        pmf = binom.pmf(range(nt+1),nt,p_loot)
        x = range(len(pmf))
        PMF = [pmf[0]]
        for i in range (1,len(pmf)):
            PMF.append(PMF[i-1]+pmf[i])#cummulative dist function
        mean = sum([i*pmf[i] for i in range (len(pmf))])
        subax.plot(x,pmf,color=colors[ci],label=t)
        subax.plot((mean,mean),(0,1),ls=':',color=colors[ci])
        pmf /= max(pmf) #Normalize the pmf, for easy reading
        ax.plot(x,pmf,color=colors[ci],label=t)
        ax.plot(x,PMF,color=colors[ci],ls='-.')
        ax.plot((mean,mean),(0,1),ls=':',color=colors[ci])
        ci += 1
    ax.set_xlim(0,4*mean)
    subax.set_xlim(0,4*mean)
    ax.set_ylim(0,1.01)
    ax.legend(loc=1)
    if not cname.lower() == 'dragon':
        fig.text(0.1,0.05,r'''
Normalized by the max probability (solid line) and cumulative probability 
(dot dash line) as a function of number of items of treasure type. The mean 
is marked with a dotted line. Color coding specified by the legend. 
Inset: non narmalized probability''')
    else:
        fig.text(0.1,0.05,r'''
Probability (solid line) and cummulative probability (dot,dash line) as a
function of number of items of treasure type. The mean is marked with a dotted
line''')
        
    fig.savefig('/tmp/play{cname}.png'.format(cname=cname))


