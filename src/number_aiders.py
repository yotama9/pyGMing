def number_confirmer(val=None,minv=None,maxv=None):
    #an aider class to confirm that that an integer value is valid
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

