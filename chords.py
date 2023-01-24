"""
Chordal development and processing. TTC operates the chordal mode on an entire tonerow at a time.
All chords share the the property that the interval
between adjacent pitches is either a perfect consonant (the perfect 4th = 5i) or an imperfect
consonant (major and minor thirds, i.e., 4i or 3i).
Chordal modes (Group) from the config file are 1, 2, 3 as described in the 12ToneChords.pdf
The other two options are 'R' to randomly choose one of the three groups or 'N' for none in which case this function will not be called.
"""
import random

import music21 as m21

def makeChords(row, group, sf, octaves=(2,4,6)):
    """
    Return a tuple of three, music21 chords. One for each register lo, mid, hi as described in 12ToneChords.pdf.
    'group' is the chordal group from the config file and 'sf' is the status file to write info into.

    Chord Qualities with intervals:
        dim: 3i + 3i + 3i = diminished 7th chord
        hdim: 3i + 3i + 4i = half-diminished 7th chord
        m7: 3i + 4i + 3i = minor 7th chord
        dom: 4i + 3i + 3i = dominant 7th chord
        mM7: 3i + 4i + 4i = minor chord with major 7th
        M7: 4i + 3i + 4i = major 7th chord
        M7a5: 4i + 4i + 3i = major 7th chord with augmented 5th
        ltDim: 5i + 3i + 3i = leading tone diminished triad above root
        Ma9: 3i + 5i + 3i = major triad with augmented 9th
        domA9: 3i + 3i + 5i = dominant 7th chord with augmented 9th C ◦7

    octaves are a tuple for the lo, mid and hi octave ranges.
    """
    # convert the row into a list of the note names and create new notes because m21 behaves strangely otherwise when using the notes from the row.
    row = row.noteNames()
    chordDur = m21.duration.Duration(random.choice(['whole', 'half', 'quarter', 'eighth', '16th']))

    # chord qualities with interval data
    cq = {'dim':(3,3,3), 'hdim':(3,3,4), 'm7':(3,4,3), 'dom':(4,3,3), 'mM7':(3,4,4), 'M7':(4,3,4), 'M7a5':(4,4,3), 'ltDim':(5,3,3), 'Ma9':(3,5,3), 'domA9':(3,3,5)}

    if group == 'R':  # random mode
        group = random.choice('1','2','3')

    if group == '1':
        qual = cq['dim']  # the only option in this group

        noteSet1 = []
        idx = 0
        note = m21.note.Note(row[idx])
        note.octave = octaves[0]
        noteSet1.append(note)  # get the Root 1
        for q in qual:  # get each of the other three notes
            idx += q
            note =  m21.note.Note(row[idx % 12])
            note.octave = octaves[0]
            noteSet1.append(note)

        noteSet2 = []
        idx = 11
        note =  m21.note.Note(row[idx])
        note.octave = octaves[1]
        noteSet2.append(note)  # get the Root 2
        for q in qual:  # get each of the other three notes
            idx += q
            note =  m21.note.Note(row[idx % 12])
            note.name = note.pitch.name
            note.octave = octaves[1]
            noteSet2.append(note)

        noteSet3 = []
        idx = 2
        note =  m21.note.Note(row[idx])
        note.octave = octaves[2]
        noteSet3.append(note)  # get the Root 3
        for q in qual:  # get each of the other three notes
            idx += q
            note =  m21.note.Note(row[idx % 12])
            note.octave = octaves[2]
            noteSet3.append(note)

        # chord registers
        lo = m21.chord.Chord(noteSet1)
        mid = m21.chord.Chord(noteSet2)
        hi = m21.chord.Chord(noteSet3)
        lo.duration = chordDur
        mid.duration = chordDur
        hi.duration = chordDur

    elif group == '2':
        pass
    elif group == '3':
        pass
    else:
        raise ValueError('Chordal Group should be one of 1, 2, 3, R or N. ' + repr(group))

    rest = m21.note.Rest()
    rest.duration = m21.duration.Duration(random.choice(['whole', 'half', 'quarter', 'eighth', '16th']))

    chordSet = [hi,mid,lo,rest]

    return(chordSet)

