# testing stuff
#  0    1     2    3    4    5  6     7    8     9   10   11
# 'C','C#','D','D#','E','F','F#','G','G#','A','A#','B'


import music21 as m21
from orow import orow2pcv


# 0 7 2 9 4 11 6 1 8 3 10 5  == circle of fifths
orow = "C,G,D,A,E,B,F#,C#,G#,D#,A#,F"

# orow = 'F, C#, A, A#, D, D#, E, C, G#, G, F#, B'


pcv = orow2pcv(orow)
row = m21.serial.ToneRow(pcv)

print(orow)
print(pcv)


for n in range(0,len(row)):
    print(n, row[n])

score = m21.stream.Score()
md = m21.metadata.Metadata()
md.title = orow
score.insert(0, md)
n1 = row[0]
n2 = row[3]
n3 = row[6]
n4 = row[9]
n1.octave = 2
n2.octave = 2
n3.octave = 2
n4.octave = 2
lo = m21.chord.Chord([n1,n2,n3,n4], type='whole')

n1 = row[11]
n2 = row[2]
n3 = row[5]
n4 = row[8]
n1.octave = 4
n2.octave = 4
n3.octave = 4
n4.octave = 4
mid = m21.chord.Chord([n1,n2,n3,n4], type='whole')

n1 = row[1]
n2 = row[4]
n3 = row[7]
n4 = row[10]
n1.octave = 6
n2.octave = 6
n3.octave = 6
n4.octave = 6
hi  = m21.chord.Chord([n1,n2,n3,n4], type='whole')

lo.lyric = 'lo'
mid.lyric = 'mid'
hi.lyric = 'hi'

print('lo: ', lo.fullName)
print('mid: ', mid.fullName)
print('hi: ', hi.fullName)

instr = m21.instrument.fromString('flute')
part = m21.stream.Part()
part.insert(0, instr)
part.insert(m21.tempo.MetronomeMark(number=60))
part.timeSignature = m21.meter.TimeSignature('4/4')
part.append(hi)
score.append(part)

instr = m21.instrument.fromString('piano')
part = m21.stream.Part()
part.insert(0, instr)
part.insert(m21.tempo.MetronomeMark(number=60))
part.timeSignature = m21.meter.TimeSignature('4/4')
part.append(mid)
score.append(part)

instr = m21.instrument.fromString('cello')
part = m21.stream.Part()
part.insert(0, instr)
part.insert(m21.tempo.MetronomeMark(number=60))
part.timeSignature = m21.meter.TimeSignature('4/4')
part.append(lo)
score.append(part)

score.write(fmt='xml', fp='testing.xml')


print("Finished\n\n")

