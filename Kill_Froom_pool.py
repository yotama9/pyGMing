import sys
import os

def pool_reader(poolname): # reading the existing pools
    out = []
    lines = open(poolname).readlines()[:] #Reading the current condition
    backup = open('.pool.bk','w') #A backup file
    for line in lines:
        words  = line.split()
        name = words[0] #The name of the monster
        n = int(words[2]) #Howmany of that monster are there
        toput = [name,n] + words[3:] #Don't tuch the rest
        out.append(toput)
        backup.write(line)

    backup.flush()
    backup.close()

    return out

def asker(poolname): #This is the class 
    pool = pool_reader(poolname)
    while True: #Printg the use option
        for i in range (len(pool)):
            index = i + 1
            name  = pool[i][0]
            n = pool[i][1]
            line = '{index}){name} ({n})'.format(index = index,
                                               name=name,
                                               n=n)
                                                
            print line 
        print '0)Done'
        inp = raw_input('pick one> ') #Waiting for user input
        try:
            inp = int(inp) #Getting the index
        except ValueError: #The user gave a non nubmber input
            print 'Use integer in the range 0, {r}'.format(r=len(pool))
            continue
        if inp <0 or inp > len(pool): #The user gave an out of range input
            print 'Use integer in the range 0, {r}'.format(r=len(pool))
            continue
        if inp == 0: #End the loop, return the new pool
            return pool
        else: #kill one monster
            pool[inp-1][1] -= 1
            pool[inp-1][1] = max(pool[inp-1][1],0)


def store_pool(pool,poolname):
    out = open (poolname,'w')
    for p in pool:
        name = p[0]
        n = p[1]
        line = '{name} = {n}'.format(name=name,n=n)
        for w in p[2:]:
            line += ' {w}'.format(w=w)
        line += '\n'
        out.write(line)
    out.flush()
    out.close()
    #We have written the new pool file, done
    return



def ask_store_pool(pool,poolname):
    oldpool = pool_reader(poolname)
    lines = []
    for i in range (len(oldpool)):
        name = oldpool[i][0]
        old_num = oldpool[i][1]
        new_num = pool[i][1]
        if old_num == new_num: #I wish to pring only the new lines
            continue
        line = '{name}: {old} -> {new}'.format(name=name,
                                               old = old_num,
                                               new = new_num)
        lines.append(line)
        
    if len(lines) == 0:
        print 
        print '\033[1mNothing has changed, leaving\033[0m'
        print 
        exit()
    print 
    print ('\033[1m') 
    print ('Changes:')
    print ('\033[0m') 
    for line in lines:
        print line

    while True:
        inp = raw_input('1)Save\n2)Cancel')
        if not inp in ['1','2']:
            print 'Please pick 1 or 2\n'
            continue
        if inp == '1':
            return True
        else:
            return False



if __name__ == '__main__':
    print sys.argv, len(sys.argv)
    if len (sys.argv) == 1:
        poolname ='pool.txt'
    else:
        poolname = '{}.txt'.format(sys.argv[1])
    if not os.path.isfile(poolname):
        poolname = str(sys.argv[1])
        if not os.path.isfile(poolname):
            print 'couldn\'t find pool file named {}'.format(poolname)
            exit()

    pool = asker(poolname)
    store = ask_store_pool(pool,poolname)
    if store:
        store_pool(pool,poolname)
    
