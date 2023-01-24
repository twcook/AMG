"""
Generate a Xaos animation file from a MIDI.
"""
import os
import sys
from mido import MidiFile

def animate(inFile):
    print('Using: ', inFile)
    mf = MidiFile(inFile)
    trackData = {}

    for i, track in enumerate(mf.tracks):
        trackTime = 0
        for message in track:
            if message.type in ('note_on','note_off'):
                trackTime += message.time
        trackData[i] = [trackTime,' nada ']

    print(mf.ticks_per_beat)
    print(mf.length)
    print(trackData)
    outFile = os.path.splitext(inFile)[0] + '.xaf'
    af = open(outFile, 'w')
    af.write("; A Xaos animation file\n")
    af.write("; Generated by midi2xaos.py\n")
    af.write("(initstate)\n")
    af.write("(letterspersec 5)\n")
    af.write("(maxiter 275)\n")
    af.write("(autorotate #t)\n")
    af.write("(rotationspeed -5)\n")
    af.write("(angle 270)\n")
    af.write("(filter 'palette #t)\n")
    af.write("(cycling #t)\n")
    af.write("(cyclingspeed 3)\n")
    af.write("(outcoloring 7)\n")
    af.write("(incoloring 3)\n")

    af.write("(clearscreen)\n")
    af.write("(display)\n")
    af.write("(defaultpalette 1000)\n")
    af.write("(plane 0)\n")
    af.write("(formula 'spider)\n")
    af.write("(view -0.01 -0.006 0.009 0.009)\n")
    af.write("(usleep 250000)\n")

    af.write("(textposition 'center 'bottom)\n")
    af.write('(text "Title: ' +  ' ")\n')
    af.write("(textsleep)\n")



    print('Created: ', outFile)
    af.close()
    return

if __name__ == "__main__":
    if len(sys.argv) == 2:
        midiFile = sys.argv[1]
        animate(midiFile)
    else:
        print("\n\nA midi file is required.\n\n")
        exit()

    print("\n\nDone.\n\n")