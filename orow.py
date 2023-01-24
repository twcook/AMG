# test serial stuff

from music21 import *

#  The original row is passed as a string of comma separated values. It must have exactly 12 members and no duplicates
#  # = sharps, b = flats
#  Example: D, C#, A, A#, F, D#, E, C, G#, G, F#, B
#  Flats are converted to their enharmonic sharps.
from collections import deque

def has_duplicates(aList):
    # For each element, check all following elements for a duplicate. Quick & dirty but works on small lists.
    for i in range(0, len(aList)):
        for x in range(i + 1, len(aList)):
            if aList[i] == aList[x]:
                return True
    return False

def check_tones(olist):
    for x in olist:
        if x not in ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']:
            return(False)
    return(True)

def orow2pcv(orow='D,C#,A,A#,F,D#,E,C,G#,G,F#,B'):
    """
    Typically the orow is passed in from the configuration file.
    If not, then the default is used.
    """
    mtx = {}
    # make all characters uppercase and remove any spaces in orow
    orow = "".join([x.strip() for x in orow.split(' ')]).upper()
    # Replace flats after uppercasing everything.
    orow = orow.replace('DB','C#')
    orow = orow.replace('EB','D#')
    orow = orow.replace('GB','F#')
    orow = orow.replace('AB','G#')
    orow = orow.replace('BB','A#')
    olist = orow.split(',')

    # check for valid length and that the values are not duplicated or missing
    if len(olist) is not 12:
        raise ValueError('The Original Row length must be 12. See: Creating an Original Row.')
    if has_duplicates(olist):
        raise ValueError('The Original Row must not contain duplicates. See: Creating an Original Row.')
    if not check_tones(olist):
        raise ValueError('The Original Row must contain all 12 tones. See: Creating an Original Row.')

    # Establish the Base Pitch Class for TTC
    base_pcv = {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}

    pcv = []
    for n in olist:
        pcv.append(base_pcv[n])

    return pcv
