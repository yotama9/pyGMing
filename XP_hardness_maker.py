
def xp_hardness_calc(PC_level):
    easy = 0
    medium = 0
    hard = 0
    deadly = 0
    for l in PC_level:
        n = PC_level[l]
        if l == 1:
            easy += 25*n
            medium += 50*n
            hard += 75*n
            deadly += 100*n
        elif l == 2:
            easy += 50*n
            medium += 100*n
            hard += 150*n
            deadly += 200*n
        elif l == 3:
            easy += 75*n
            medium += 150*n
            hard += 225*n
            deadly += 400*n
        elif l == 4:
            easy += 125*n
            medium += 250*n
            hard += 375*n
            deadly += 500*n
        elif l == 5:
            easy += 250*n
            medium += 500*n
            hard += 750*n
            deadly += 1100*n
        elif l == 6:
            easy += 300*n
            medium += 600*n
            hard += 900*n
            deadly += 1400*n
        elif l == 7:
            easy += 350*n
            medium += 750*n
            hard += 1100*n
            deadly += 1700*n
        elif l == 8:
            easy += 450*n
            medium += 900*n
            hard += 1400*n
            deadly += 2100*n
        elif l == 9:
            easy += 550*n
            medium += 1100*n
            hard += 1600*n
            deadly += 2400*n
        elif l == 10:
            easy += 600*n
            medium += 1200*n
            hard += 1900*n
            deadly += 1600*n
        elif l == 11:
            easy += 800*n
            medium += 1600*n
            hard += 2400*n
            deadly += 3600*n
        elif l == 12:
            easy += 1000*n
            medium += 2000*n
            hard += 3000*n
            deadly += 4500*n
        elif l == 13:
            easy += 1100*n
            medium += 2200*n
            hard += 3400*n
            deadly += 5100*n
        elif l == 14:
            easy += 1250*n
            medium += 2500*n
            hard += 3800*n
            deadly += 5700*n
        elif l == 15:
            easy += 1400*n
            medium += 2800*n
            hard += 4300*n
            deadly += 6400*n
        elif l == 16:
            easy += 1600*n
            medium += 3200*n
            hard += 4800*n
            deadly += 7200*n
        elif l == 17:
            easy += 2000*n
            medium += 3900*n
            hard += 5900*n
            deadly += 8800*n
        elif l == 18:
            easy += 2100*n
            medium += 4200*n
            hard += 6300*n
            deadly += 9500*n
        elif l == 19:
            easy += 2400*n
            medium += 4900*n
            hard += 7300*n
            deadly += 10900*n
        elif l == 20:
            easy += 2800*n
            medium += 5700*n
            hard += 8500*n
            deadly += 12700*n
        else:
            print 'invalid players list'
            easy = 0
            medium = 0
            hard = 0
            deadly = 0
    return {'easy':easy,
            'medum':medium,
            'hard':hard,
            'deadly':deadly}

