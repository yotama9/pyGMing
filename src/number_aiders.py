

def roll_die(val):
    from numpy.random import randint as rint
    out = 0
    plus_parts = val.split('+')
    for pp in plus_parts:
        minus_parts = pp.split('-')
        for mp in minus_parts[1:]:
            try: 
                if 'd' in mp:
                    n,d = mp.split('d')
                else:
                    d =1 #We have a constant bonus, the die rolls will be 1
                    n = mp
                if n.strip() == '':
                    n = 1
                n = int(n)
                d = int(d)
                out -= sum(rint(1,d+1,n)) #rolling the die
            except ValueError:
                return None
        
        try:
            if 'd' in minus_parts[0]:
                n,d = minus_parts[0].split('d')
            else:
                d = 1#We have a constant bonus, the die rolls will be 1
                n = minus_parts[0]
            if n.strip() == '':
                n = 1
            n = int(n)
            d = int(d)
            out += sum(rint(1,d+1,n))
        except ValueError:
            return None
    print out

    return out

            




def number_confirmer(val=None,minv=None,maxv=None,mayDie=False):
    #an aider class to confirm that that an integer value is valid
    
    val = str(val)
    if 'd' in val:
        val = roll_die(val)
    

    try: #Make sure that the input string is integer
        val = int(val) 
    except ValueError:
        return None
    except TypeError:
        return None
    if minv and val < minv: #Make sure the value is inbounds
        return None
    if maxv and val > maxv:
        return None

    return val

