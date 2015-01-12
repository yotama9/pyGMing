from random import randint as rint
import numpy as np
import matplotlib.pyplot as plt


#This is a script that reads "fix_xp_pool.txt" and gives a possible
#combination of monsters based on the file. The aim of this script is to
#generate an ancouter with a fixed xp. The input file reads as follow:
#
#encounter xpg
#hostile1 xp1
#hostile2 xp2
#...
#
#and so on
#the xpg indicates the xp level the group is allowed
#reading the xp pool from the input file

def show_example():
    print 'This is an example input file'
    print 'The file name should be fix_xp_pool.txt'
    print 'There should be one line that looks like'
    print 'encoutner 50'
    print 'and at least one more line with a monster name and a number'
    print 
    print 'ecnouter 50'
    print 'orc 10'
    print 'goblin 5'
    print 'ogre 25'


def read_fixed_xp_table(fix_xp_pool_file):

    out = {}
    order = [] #This list holds the order of the keys.
    #I don't check if fix_xp_pool exist. I should add that
    ops = 1#ops is the numbe of valid combination
    for line in open (fix_xp_pool_file).readlines():
        name,xp = line.split()
        xp = int(xp)

        if name == 'encounter': #The enocutner total xp
            XP = xp
            continue
        #how many combarant of that type can I fit in an encoutner
        #with xp value equal or less than the total encouter xp
        #I add +1 for the case with 0 combatant of that type
        num = XP/xp + 1
        if name in out: #Two entries with the same name
            print 'Two entries with the same name \x1B[3m{name}\x1B[23m in input file'.format(name=name)
        out[name] = [xp,num]
        order.append(name)
        ops *= num
    num = out[order[-1]][1]
    #the last combtatant is constrained, so there are less option than we
    #calculated
    ops /= num
    out['encounter'] = [XP,ops] 
    out['_order_'] = order[:]

    return out

def generate(xp_table):
    ops = xp_table['encounter'][1]
    opnum = rint(0,ops)
    print opnum
    keys = xp_table['_order_']
    tot = 0
    for key in keys:
        comb = xp_table[key]
         
        n = opnum/comb[1]
        tot += n *comb[0]
        opnum/=comb[1]

    print tot


xp_table = read_fixed_xp_table('fix_xp_pool.txt')
if not 'encounter' in xp_table:
    print '*Missing encounter entry in fix_xp_pool.txt file*'

    show_example()
    exit()

if len (xp_table) == 1:
    print '*Missing entries in fix_xp_pool.txt file*'
    show_example()
    exit()

print xp_table['encounter']
ops = xp_table['encounter'][1]
generate(xp_table)


