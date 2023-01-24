"""
return the complimentary cycles from a matrix based on an original row
In Complimentary mode, the number of PCSs in the config is use to define the maximum number of sets to use.
If there are fewer sets then they will be reused in sequence to match that number.
"""
import music21 as m21

def compCycles(pcv):
    # get rows from a matrix based on the orow
    primes = {}
    matrix_str = m21.serial.rowToMatrix(pcv)
    n = 0
    # convert the string to a dict of prime rows.
    for s in matrix_str.splitlines():
        primes['P'+str(n)] = s.split()
        n += 1

    # convert the string values to integers
    p_keys = primes.keys()
    for k in p_keys:
        r = primes[k]
        r = [int(i) for i in r]
        primes[k] = r

    # create the inversions
    inversions = {}
    for k in p_keys:
        p = primes[k]
        inversions[k.replace('P','I')] = list(reversed(p))

    # find P/I add9 (seven semitones) dyads - see: https://youtu.be/WFeKVhDTWbs?t=14m10s
    i_keys = inversions.keys()
    comp_cycles = set()
    for k in p_keys:
        for i in i_keys:
            for z in range(0, 12):
                n = (primes[k][z] + inversions[i][z]) %12
                if n != 9:
                    comp_cycles.discard((k, i ))
                    break
                else:
                    comp_cycles.add((k, i ))

    if len(comp_cycles) > 0:
        x = 0
        pcsDict = {}
        for s in comp_cycles:
            x += 1
            pcsDict[x] = [(s[0], primes[s[0]]),(s[1], inversions[s[1]])]
    else:
        print('The Row: ', pcv, " doesn't contain any complimentary cycles.")
        pcsDict = None

    return(pcsDict)
