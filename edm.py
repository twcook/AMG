import random
import os
import time

import music21 as m21
from tkinter import messagebox
from orow import orow2pcv

import config
from chords import makeChords
from status import Status

def house(cfgData):
    """
    Design notes:
    Create several instruments and let the producer shape the sound in the DAW.
    When adding notes to the voices, I need to create three instruments for the three chords and create another for the melody. The should be different for each style.
    Chords:
    Hi: Piccolo
    Mid: Viola
    Low: Contrabass

    Melody: Elec. Piano
    Counter-Melody: Trombone
    Percussion: GM2 Drumkit
    """
    sf = Status(os.path.join(cfgData['outpath'], cfgData['outfile'] + '.txt'))
    messagebox.showinfo("Composer", "This may take a few minutes depending on the size of the work.\n"+"Press Ok to start composing.")
    m21.environment.set('musicxmlPath', cfgData['musicxmlPath'])
    base_pcv =  {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}
    trans_types = ['P', 'I', 'R', 'RI']

    tr = m21.serial.ToneRow()
    score = m21.stream.Score()
    # Setup Metadata
    md = m21.metadata.Metadata()
    md.title = cfgData['title']
    md.composer = cfgData['composer']
    md.date = m21.metadata.DateSingle(data=cfgData['date'])
    md.copyright = cfgData['copyright']
    md.alternativeTitle = 'Generated by TTC version: ' + cfgData['ttc_version']
    score.insert(0, md)
    # Add the initial tempo and time signature
    score.insert(m21.tempo.MetronomeMark(number=140))
    ts = m21.meter.TimeSignature('12/8')
    score.timeSignature = ts

    # convert the original row into a list of pitch class values
    orow = cfgData['orow']
    pcv = orow2pcv(orow)

    sf.write("Original Row: " + orow + '\n')

    part01 = m21.stream.Part()
    instr = m21.instrument.fromString('Piccolo')
    part01.insert(0, ts)
    part01.insert(0, instr)
    sf.write(instr.instrumentName + '\n')

    part02 = m21.stream.Part()
    instr = m21.instrument.fromString('Viola')
    part02.insert(0, ts)
    part02.insert(0, instr)
    sf.write(instr.instrumentName + '\n')

    part03 = m21.stream.Part()
    instr = m21.instrument.fromString('Contrabass')
    part03.insert(0, ts)
    part03.insert(0, instr)
    sf.write(instr.instrumentName + '\n')

    part04 = m21.stream.Part()
    instr = m21.instrument.fromString('Piano')
    part04.insert(0, ts)
    part04.insert(0, instr)
    sf.write(instr.instrumentName + '\n')

    part05 = m21.stream.Part()
    instr = m21.instrument.fromString('Trombone')
    part05.insert(0, ts)
    part05.insert(0, instr)
    sf.write(instr.instrumentName + '\n')

    #part06 = m21.stream.Part()
    #instr = m21.instrument.fromString('Percussion')
    #part06.insert(0, ts)
    #part06.insert(0, instr)
    #sf.write(instr.instrumentName + '\n')

    newIntro = True
    # 16 bars
    for x in range(1,17):
        tonerow = m21.serial.pcToToneRow(pcv)
        trType = random.choice(trans_types)
        trIdx = random.randrange(0,11)
        row = tonerow.zeroCenteredTransformation(trType, trIdx)
        chordSet = makeChords(row, '1', sf, (1,3,5))

        m = m21.stream.Measure()
        m.insert(0, ts)
        m.append(chordSet[0])
        m.append(chordSet[3])
        part01.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        m.append(chordSet[1])
        m.append(chordSet[3])
        part02.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        m.append(chordSet[2])
        m.append(chordSet[3])
        part03.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        trType = random.choice(trans_types)
        trIdx = random.randrange(0,11)
        row = tonerow.zeroCenteredTransformation(trType, trIdx)
        for note in row:
            note.duration = m21.duration.Duration(random.choice(['eighth', '16th', '32nd', '64th']))
            if x == 1  and newIntro:
                note.addLyric("Intro")
                newIntro = False
            m.append(note)
        part04.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        trType = random.choice(trans_types)
        trIdx = random.randrange(0,11)
        row = tonerow.zeroCenteredTransformation(trType, trIdx)
        for note in row:
            note.duration = m21.duration.Duration(random.choice(['eighth', '16th', '32nd', '64th']))
            m.append(note)
        part05.append(m)

    newBreakdown1 = True
    # 32 bars
    for x in range(1,33):
        tonerow = m21.serial.pcToToneRow(pcv)
        trType = random.choice(trans_types)
        trIdx = random.randrange(0,11)
        row = tonerow.zeroCenteredTransformation(trType, trIdx)
        chordSet = makeChords(row, '1', sf, (1,3,5))

        m = m21.stream.Measure()
        m.insert(0, ts)
        m.append(chordSet[0])
        m.append(chordSet[3])
        part01.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        m.append(chordSet[1])
        m.append(chordSet[3])
        part02.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        m.append(chordSet[2])
        m.append(chordSet[3])
        part03.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        trType = random.choice(trans_types)
        trIdx = random.randrange(0,11)
        row = tonerow.zeroCenteredTransformation(trType, trIdx)
        for note in row:
            note.duration = m21.duration.Duration(random.choice(['eighth', '16th', '32nd', '64th']))
            if x == 1  and newBreakdown1:
                note.addLyric("Breakdown #1")
                newBreakdown1 = False
            m.append(note)
        part04.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        trType = random.choice(trans_types)
        trIdx = random.randrange(0,11)
        row = tonerow.zeroCenteredTransformation(trType, trIdx)
        for note in row:
            note.duration = m21.duration.Duration(random.choice(['eighth', '16th', '32nd', '64th']))
            m.append(note)
        part05.append(m)

    newBuildup1 = True
    # 32 bars
    for x in range(1,33):
        tonerow = m21.serial.pcToToneRow(pcv)
        trType = random.choice(trans_types)
        trIdx = random.randrange(0,11)
        row = tonerow.zeroCenteredTransformation(trType, trIdx)
        chordSet = makeChords(row, '1', sf, (1,3,5))

        m = m21.stream.Measure()
        m.insert(0, ts)
        m.append(chordSet[0])
        m.append(chordSet[3])
        part01.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        m.append(chordSet[1])
        m.append(chordSet[3])
        part02.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        m.append(chordSet[2])
        m.append(chordSet[3])
        part03.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        trType = random.choice(trans_types)
        trIdx = random.randrange(0,11)
        row = tonerow.zeroCenteredTransformation(trType, trIdx)
        for note in row:
            note.duration = m21.duration.Duration(random.choice(['eighth', '16th', '32nd', '64th']))
            if x == 1  and newBuildup1:
                note.addLyric("Buildup #1")
                newBuildup1 = False
            m.append(note)
        part04.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        trType = random.choice(trans_types)
        trIdx = random.randrange(0,11)
        row = tonerow.zeroCenteredTransformation(trType, trIdx)
        for note in row:
            note.duration = m21.duration.Duration(random.choice(['eighth', '16th', '32nd', '64th']))
            m.append(note)
        part05.append(m)

    newDrop1 = True
    # 32 bars
    for x in range(1,33):
        tonerow = m21.serial.pcToToneRow(pcv)
        trType = random.choice(trans_types)
        trIdx = random.randrange(0,11)
        row = tonerow.zeroCenteredTransformation(trType, trIdx)
        chordSet = makeChords(row, '1', sf, (1,3,5))

        m = m21.stream.Measure()
        m.insert(0, ts)
        m.append(chordSet[0])
        m.append(chordSet[3])
        part01.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        m.append(chordSet[1])
        m.append(chordSet[3])
        part02.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        m.append(chordSet[2])
        m.append(chordSet[3])
        part03.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        trType = random.choice(trans_types)
        trIdx = random.randrange(0,11)
        row = tonerow.zeroCenteredTransformation(trType, trIdx)
        for note in row:
            note.duration = m21.duration.Duration(random.choice(['eighth', '16th', '32nd', '64th']))
            if x == 1  and newDrop1:
                note.addLyric("Drop #1")
                newDrop1 = False
            m.append(note)
        part04.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        trType = random.choice(trans_types)
        trIdx = random.randrange(0,11)
        row = tonerow.zeroCenteredTransformation(trType, trIdx)
        for note in row:
            note.duration = m21.duration.Duration(random.choice(['eighth', '16th', '32nd', '64th']))
            m.append(note)
        part05.append(m)


    newBreakdown2 = True
    # 32 bars
    for x in range(1,33):
        tonerow = m21.serial.pcToToneRow(pcv)
        trType = random.choice(trans_types)
        trIdx = random.randrange(0,11)
        row = tonerow.zeroCenteredTransformation(trType, trIdx)
        chordSet = makeChords(row, '1', sf, (1,3,5))

        m = m21.stream.Measure()
        m.insert(0, ts)
        m.append(chordSet[0])
        m.append(chordSet[3])
        part01.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        m.append(chordSet[1])
        m.append(chordSet[3])
        part02.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        m.append(chordSet[2])
        m.append(chordSet[3])
        part03.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        trType = random.choice(trans_types)
        trIdx = random.randrange(0,11)
        row = tonerow.zeroCenteredTransformation(trType, trIdx)
        for note in row:
            note.duration = m21.duration.Duration(random.choice(['eighth', '16th', '32nd', '64th']))
            if x == 1  and newBreakdown2:
                note.addLyric("Breakdown #2")
                newBreakdown2 = False
            m.append(note)
        part04.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        trType = random.choice(trans_types)
        trIdx = random.randrange(0,11)
        row = tonerow.zeroCenteredTransformation(trType, trIdx)
        for note in row:
            note.duration = m21.duration.Duration(random.choice(['eighth', '16th', '32nd', '64th']))
            m.append(note)
        part05.append(m)

    newBuildup2 = True
    # 32 bars
    for x in range(1,33):
        tonerow = m21.serial.pcToToneRow(pcv)
        trType = random.choice(trans_types)
        trIdx = random.randrange(0,11)
        row = tonerow.zeroCenteredTransformation(trType, trIdx)
        chordSet = makeChords(row, '1', sf, (1,3,5))

        m = m21.stream.Measure()
        m.insert(0, ts)
        m.append(chordSet[0])
        m.append(chordSet[3])
        part01.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        m.append(chordSet[1])
        m.append(chordSet[3])
        part02.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        m.append(chordSet[2])
        m.append(chordSet[3])
        part03.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        trType = random.choice(trans_types)
        trIdx = random.randrange(0,11)
        row = tonerow.zeroCenteredTransformation(trType, trIdx)
        for note in row:
            note.duration = m21.duration.Duration(random.choice(['eighth', '16th', '32nd', '64th']))
            if x == 1  and newBuildup2:
                note.addLyric("Buildup #2")
                newBuildup2 = False
            m.append(note)
        part04.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        trType = random.choice(trans_types)
        trIdx = random.randrange(0,11)
        row = tonerow.zeroCenteredTransformation(trType, trIdx)
        for note in row:
            note.duration = m21.duration.Duration(random.choice(['eighth', '16th', '32nd', '64th']))
            m.append(note)
        part05.append(m)

    newDrop2 = True
    # 32 bars
    for x in range(1,33):
        tonerow = m21.serial.pcToToneRow(pcv)
        trType = random.choice(trans_types)
        trIdx = random.randrange(0,11)
        row = tonerow.zeroCenteredTransformation(trType, trIdx)
        chordSet = makeChords(row, '1', sf, (1,3,5))

        m = m21.stream.Measure()
        m.insert(0, ts)
        m.append(chordSet[0])
        m.append(chordSet[3])
        part01.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        m.append(chordSet[1])
        m.append(chordSet[3])
        part02.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        m.append(chordSet[2])
        m.append(chordSet[3])
        part03.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        trType = random.choice(trans_types)
        trIdx = random.randrange(0,11)
        row = tonerow.zeroCenteredTransformation(trType, trIdx)
        for note in row:
            note.duration = m21.duration.Duration(random.choice(['eighth', '16th', '32nd', '64th']))
            if x == 1  and newDrop2:
                note.addLyric("Drop #2")
                newDrop2 = False
            m.append(note)
        part04.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        trType = random.choice(trans_types)
        trIdx = random.randrange(0,11)
        row = tonerow.zeroCenteredTransformation(trType, trIdx)
        for note in row:
            note.duration = m21.duration.Duration(random.choice(['eighth', '16th', '32nd', '64th']))
            m.append(note)
        part05.append(m)

    newOutro = True
    # 16 bars
    for x in range(1,17):
        tonerow = m21.serial.pcToToneRow(pcv)
        trType = random.choice(trans_types)
        trIdx = random.randrange(0,11)
        row = tonerow.zeroCenteredTransformation(trType, trIdx)
        chordSet = makeChords(row, '1', sf, (1,3,5))

        m = m21.stream.Measure()
        m.insert(0, ts)
        m.append(chordSet[0])
        m.append(chordSet[3])
        part01.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        m.append(chordSet[1])
        m.append(chordSet[3])
        part02.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        m.append(chordSet[2])
        m.append(chordSet[3])
        part03.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        trType = random.choice(trans_types)
        trIdx = random.randrange(0,11)
        row = tonerow.zeroCenteredTransformation(trType, trIdx)
        for note in row:
            note.duration = m21.duration.Duration(random.choice(['eighth', '16th', '32nd', '64th']))
            if x == 1  and newOutro:
                note.addLyric("Outro")
                newOutro = False
            m.append(note)
        part04.append(m)

        m = m21.stream.Measure()
        m.insert(0, ts)
        trType = random.choice(trans_types)
        trIdx = random.randrange(0,11)
        row = tonerow.zeroCenteredTransformation(trType, trIdx)
        for note in row:
            note.duration = m21.duration.Duration(random.choice(['eighth', '16th', '32nd', '64th']))
            m.append(note)
        part05.append(m)


    score.append(part01)
    score.append(part02)
    score.append(part03)
    score.append(part04)
    score.append(part05)

    score.write(fmt='xml', fp=os.path.join(cfgData['outpath'], cfgData['outfile'] + '.xml'))
    score.write(fmt='midi', fp=os.path.join(cfgData['outpath'], cfgData['outfile'] + '.mid'))

    return