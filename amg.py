# amg.py - Atonal Music Generator
# An application to create compositions based on a 12 Tone Original Row input or based on a group of Pitch Set Classes.
# All defined in a configuration file.  
import sys
import os
import random
import time
from uuid import uuid4
from collections import deque, OrderedDict

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import Text
import music21 as m21
import tkinter.font as tkFont

import config
from edm import  house

from orow import orow2pcv
from status import Status
from chords import makeChords
from compCycles import compCycles

class AMG(tk.Frame):
    def __init__(self, master, cfgData):
        tk.Frame.__init__(self, master, bg='#c9c7c6')
        self.master = master
        self.init_window(cfgData)

    def init_window(self, cfgData):
        self.master.title('Atonal Music Generator')
        self.pack(fill=tk.BOTH, expand=1)
        self.cfgData = cfgData

        menu_main = tk.Menu(self.master)
        self.master.config(menu=menu_main)
        menu_file = tk.Menu(menu_main)
        menu_file.add_command(label='Open', command = self.cfg_open)
        menu_file.add_command(label='Save', command = self.cfg_save)
        menu_file.add_command(label='Quit', command = self.app_exit)
        menu_main.add_cascade(label='File', menu=menu_file)

        menu_gen = tk.Menu(menu_main)
        menu_gen.add_command(label='12 Tone Serial', command = self.twelveTone)
        menu_gen.add_command(label='Pitch Set Class', command = self.psClass)
        menu_main.add_cascade(label='Generate', menu=menu_gen)

        menu_help = tk.Menu(menu_main)
        menu_main.add_cascade(label='Help', menu=menu_help)

        menu_about = tk.Menu(menu_main)
        menu_main.add_cascade(label='About', menu=menu_about)

        self.__setVars()
        self.__showForm()


    def __setVars(self):
        # setup data variables
        self.v_version = tk.StringVar(value=self.cfgData['amg_version'])

        self.v_outpath = tk.StringVar(value=self.cfgData['outpath'])
        self.v_outfile = tk.StringVar(value=self.cfgData['outfile'])
        self.v_mxml = tk.StringVar(value=self.cfgData['musicxmlPath'])

        self.v_copyright = tk.StringVar(value=self.cfgData['copyright'])
        self.v_date = tk.StringVar(value=self.cfgData['date'])
        self.v_composer = tk.StringVar(value=self.cfgData['composer'])
        self.v_title = tk.StringVar(value=self.cfgData['title'])

        self.v_mode = tk.StringVar(value=self.cfgData['mode'])
        self.v_chordal = tk.StringVar(value=self.cfgData['chordal'])
        self.v_orow = tk.StringVar(value=self.cfgData['orow'])
        self.v_duration = tk.StringVar(value=self.cfgData['duration'])
        self.v_pcs = tk.StringVar(value=self.cfgData['pcs'])
        self.v_tempo = tk.StringVar(value=self.cfgData['tempo'])
        self.v_timesig = tk.StringVar(value=self.cfgData['timesig'])
        self.v_pct_cluster = tk.StringVar(value=self.cfgData['pct_cluster'])
        self.v_pct_repeat = tk.StringVar(value=self.cfgData['pct_repeat'])

        self.v_max_cluster = tk.StringVar(value=self.cfgData['max_cluster'])
        self.v_max_repeat = tk.StringVar(value=self.cfgData['max_repeat'])

        self.v_rois = tk.StringVar(value=self.cfgData['rois'])
        self.v_same_series = tk.StringVar(value=self.cfgData['same_series'])

        temp = ''
        for t in self.cfgData['timechanges'].keys():
            temp += t + ': ' + self.cfgData['timechanges'][t]
        self.v_timechanges = Text(root, height=5, width=10, bg='#FFD8D1', padx=15, pady=5)
        self.v_timechanges.pack(side=tk.LEFT)
        self.v_timechanges.insert(1.0, temp)

        temp = ''
        for t in self.cfgData['tempochanges'].keys():
            temp += t + ': ' + self.cfgData['tempochanges'][t]
        self.v_tempochanges = tk.Text(root, height=5, width=10, bg='#FFE6D1', padx=15, pady=5)
        self.v_tempochanges.pack(side=tk.LEFT)
        self.v_tempochanges.insert(1.0, temp)

        temp = ''
        for t in self.cfgData['parts'].keys():
            temp += t + ': ' + self.cfgData['parts'][t] + '\n'
        self.v_parts = Text(root, height=5, width=30, bg='#D1D3FF', padx=15, pady=5)
        self.v_parts.pack(side=tk.LEFT)
        self.v_parts.insert(1.0, temp)

        return

    def __showForm(self):
        sysLabel = tk.Label(self, text='System Section', bg='#E2FFD1', relief='ridge').grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        versionLabel = tk.Label(self, text='Version: ' + self.cfgData['amg_version'], bg='#F8FFD1').grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

        mainLabel = tk.Label(self, text='Main Section', bg='#E2FFD1', relief='ridge').grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        outpathLabel = tk.Label(self, text='Output Path: ', bg='#F8FFD1').grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        outpathEntry = tk.Entry(self, textvariable=self.v_outpath).grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
        outfileLabel = tk.Label(self, text='Output File: ', bg='#F8FFD1').grid(row=2, column=3, padx=5, pady=5, sticky=tk.W)
        outfileEntry = tk.Entry(self, textvariable=self.v_outfile).grid(row=2, column=4, padx=5, pady=5, sticky=tk.W)
        mxmlLabel = tk.Label(self, text='Music XML Path: ', bg='#F8FFD1').grid(row=2, column=5, padx=5, pady=5, sticky=tk.W)
        mxmlEntry = tk.Entry(self, textvariable=self.v_mxml).grid(row=2, column=6, padx=5, pady=5, sticky=tk.W)

        mdLabel = tk.Label(self, text='Metadata Section', bg='#E2FFD1', relief='ridge').grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        copyrightLabel = tk.Label(self, text='Copyright: ', bg='#F8FFD1').grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        copyrightEntry = tk.Entry(self, textvariable=self.v_copyright).grid(row=4, column=2, padx=5, pady=5, sticky=tk.W)
        dateLabel = tk.Label(self, text='Date: ', bg='#F8FFD1').grid(row=4, column=3, padx=5, pady=5, sticky=tk.W)
        dateEntry = tk.Entry(self, textvariable=self.v_date).grid(row=4, column=4, padx=5, pady=5, sticky=tk.W)
        titleLabel = tk.Label(self, text='Title: ', bg='#F8FFD1').grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        titleEntry = tk.Entry(self, textvariable=self.v_title).grid(row=5, column=2, padx=5, pady=5, sticky=tk.W)
        composerLabel = tk.Label(self, text='Composer: ', bg='#F8FFD1').grid(row=5, column=3, padx=5, pady=5, sticky=tk.W)
        composerEntry = tk.Entry(self, textvariable=self.v_composer).grid(row=5, column=4, padx=5, pady=5, sticky=tk.W)
        compLabel = tk.Label(self, text='Composition Section', bg='#E2FFD1', relief='ridge').grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)
        orowLabel = tk.Label(self, text='Original Row: ', bg='#F8FFD1').grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)
        orowEntry = tk.Entry(self, textvariable=self.v_orow).grid(row=7, column=2, padx=5, pady=5, sticky=tk.W)
        numseriesLabel = tk.Label(self, text='Number of PCS: ', bg='#F8FFD1').grid(row=7, column=3, padx=5, pady=5, sticky=tk.W)
        numseriesEntry = tk.Entry(self, textvariable=self.v_pcs).grid(row=7, column=4, padx=5, pady=5, sticky=tk.W)
        tempoLabel = tk.Label(self, text='Tempo: ', bg='#F8FFD1').grid(row=8, column=1, padx=5, pady=5, sticky=tk.W)
        tempoEntry = tk.Entry(self, textvariable=self.v_tempo).grid(row=8, column=2, padx=5, pady=5, sticky=tk.W)
        timesigLabel = tk.Label(self, text='Time Signature: ', bg='#F8FFD1').grid(row=8, column=3, padx=5, pady=5, sticky=tk.W)
        timesigEntry = tk.Entry(self, textvariable=self.v_timesig).grid(row=8, column=4, padx=5, pady=5, sticky=tk.W)
        clusterLabel = tk.Label(self, text='Percentage of Clusters: ', bg='#F8FFD1').grid(row=9, column=1, padx=5, pady=5, sticky=tk.W)
        clusterEntry = tk.Entry(self, textvariable=self.v_pct_cluster).grid(row=9, column=2, padx=5, pady=5, sticky=tk.W)
        repeatLabel = tk.Label(self, text='Percentage of Repeats: ', bg='#F8FFD1').grid(row=9, column=3, padx=5, pady=5, sticky=tk.W)
        repeatEntry = tk.Entry(self, textvariable=self.v_pct_repeat).grid(row=9, column=4, padx=5, pady=5, sticky=tk.W)
        clustermaxLabel = tk.Label(self, text='Max Notes in Clusters: ', bg='#F8FFD1').grid(row=10, column=1, padx=5, pady=5, sticky=tk.W)
        clustermaxEntry = tk.Entry(self, textvariable=self.v_max_cluster).grid(row=10, column=2, padx=5, pady=5, sticky=tk.W)
        repeatmaxLabel = tk.Label(self, text='Max Number of Repeats: ', bg='#F8FFD1').grid(row=10, column=3, padx=5, pady=5, sticky=tk.W)
        repeatmaxEntry = tk.Entry(self, textvariable=self.v_max_repeat).grid(row=10, column=4, padx=5, pady=5, sticky=tk.W)
        modeLabel = tk.Label(self, text='Composition Mode: ', bg='#F8FFD1').grid(row=11, column=1, padx=5, pady=5, sticky=tk.W)
        modeEntry = tk.Entry(self, textvariable=self.v_mode).grid(row=11, column=2, padx=5, pady=5, sticky=tk.W)
        durationLabel = tk.Label(self, text='Duration Level: ', bg='#F8FFD1').grid(row=11, column=3, padx=5, pady=5, sticky=tk.W)
        durationEntry = tk.Entry(self, textvariable=self.v_duration).grid(row=11, column=4, padx=5, pady=5, sticky=tk.W)
        chordalLabel = tk.Label(self, text='Chordal Mode: ', bg='#F8FFD1').grid(row=12, column=1, padx=5, pady=5, sticky=tk.W)
        chordalEntry = tk.Entry(self, textvariable=self.v_chordal).grid(row=12, column=2, padx=5, pady=5, sticky=tk.W)

        return

    def app_exit(self):
        self.quit()
        #if messagebox.askokcancel(title="Exit AMG", message="Click Ok to quit."):
            #self.quit()
        #else:
            #return

    def cfg_open(self):
            fopen = filedialog.askopenfiles(mode='r')
            if not fopen:
                return
            try:
                self.cfgData = config.config(fopen[0].name)
                self.__setVars()
                self.__showForm()
            except:
                e = sys.exc_info()[0]
                m = sys.exc_info()[1]
                messagebox.showerror(message="Error: {0}: \nMessage: {1}".format(e, m))
            return

    def cfg_save(self):
        if not messagebox.askokcancel("Configuration", "Saving: " + os.path.join(self.v_outpath.get(), self.v_outfile.get()+'.amgd' )):
            return

        if not os.path.exists(self.v_outpath.get()):
            os.makedirs(self.v_outpath.get())
        try:
            with open(os.path.join(self.v_outpath.get(), self.v_outfile.get() + '.amgd'), 'w') as f:
                f.write('[MAIN]\n')
                f.write('outfile: ' + self.v_outfile.get().strip() + '\n')
                f.write('outpath: ' + self.v_outpath.get().strip() + '\n')
                f.write('musicxmlPath: ' + self.v_mxml.get().strip() + '\n')

                f.write('[METADATA]\n')
                f.write('composer: ' + self.v_composer.get().strip() + '\n')
                f.write('date: ' + self.v_date.get().strip() + '\n')
                f.write('title: ' + self.v_title.get().strip() + '\n')
                f.write('copyright: ' + self.v_copyright.get().strip() + '\n')

                f.write('[COMP]\n')
                f.write('Mode: ' + self.v_mode.get().strip() + '\n')
                f.write('Chordal: ' + self.v_chordal.get().strip() + '\n')
                f.write('ORow: ' + self.v_orow.get().strip() + '\n')
                f.write('PCS: ' + self.v_pcs.get().strip() + '\n')
                f.write('Duration: ' + self.v_duration.get().strip() + '\n')
                f.write('Tempo: ' + self.v_tempo.get().strip() + '\n')
                f.write('TimeSig: ' + self.v_timesig.get().strip() + '\n')
                f.write('Cluster: ' + self.v_pct_cluster.get().strip() + '\n')
                f.write('ClusterMax: ' + self.v_max_cluster.get().strip() + '\n')
                f.write('Repeat: ' + self.v_pct_repeat.get().strip() + '\n')
                f.write('RepeatMax: ' + self.v_max_repeat.get().strip() + '\n')
                f.write('ROIS: ' + self.v_rois.get().strip() + '\n')
                f.write('Same Series: ' + self.v_same_series.get().strip() + '\n')
                # TODO: time/tempo changes and tracks
                f.write('[TIMECHANGES]\n')
                f.write(self.v_timechanges.get(1.0,tk.END))
                f.write('[TEMPOCHANGES]\n')
                f.write(self.v_tempochanges.get(1.0,tk.END))
                f.write('[PARTS]\n')
                f.write(self.v_parts.get(1.0,tk.END))
                f.write('\n;DO NOT EDIT THIS SECTION. The SYS section must be in all .amgd files.\n')
                f.write('[SYS]\n')
                f.write('version: ' + self.cfgData['amg_version'] + '\n\n')
                f.close()

                # reload this file using the config loader and re-paint the form
                self.cfgData = config.config(os.path.join(self.v_outpath.get(), self.v_outfile.get() + '.amgd'))
                self.__showForm()
        except:
            e = sys.exc_info()[0]
            m = sys.exc_info()[1]
            print("Error: {0}: \nMessage: {1}".format(e, m))
            print(sys.exc_info()[2].print_last())
            messagebox.showerror(message="Error: {0}: \nMessage: {1}".format(e, m))

        return


    def _arrange(self, notes):
        """
        Create the arrangement of notes for a specific tonerow.
        This includes repeating notes and creating clusters (chords).
        For each new measure, randomly select a value, 0 - 1 to use for dynamics.
        """
        durationList = self.getDuration()
        nq = deque()  # note queue
        mq = deque()  # measure queue - clusters, repeats and single notes.

        for n in notes:
            anote = m21.note.Note(n)
            anote.duration = m21.duration.Duration(random.choice(durationList))
            nq.append(anote)

        if random.randint(0,100) <= self.cfgData['pct_cluster']:
            while len(nq) > 0:
                cluster = []
                cluster_size = random.randint(1,self.cfgData['max_cluster'])
                for x in range(0,min(cluster_size, len(nq))):
                    cluster.append(nq.popleft())
                mq.append(m21.chord.Chord(cluster))
                mq.append(m21.dynamics.Dynamic(m21.dynamics.dynamicStrFromDecimal(random.random())))  # add random dynamics
        else:
            for i in range(0,len(nq)):
                tnote = nq.popleft()
                if random.randint(0,100) <= self.cfgData['pct_repeat']:
                    n = random.randint(1,self.cfgData['max_repeat'])
                    for x in range(0, n):
                        mq.append(tnote)

        return mq


    def getDuration(self):
        if self.cfgData['duration'] == '0':
            return ['half', 'quarter', 'eighth']
        elif self.cfgData['duration'] == '1':
            return ['whole', 'half', 'quarter', 'eighth', '16th']
        elif self.cfgData['duration'] == '2':
            return ['breve', 'whole', 'half', 'quarter', 'eighth', '16th']
        else:
            return ['breve', 'whole', 'half', 'quarter', 'eighth', '16th', '32nd', '64th']

    def Linear(self, pcv, score, statusFile):
        # Linear composition mode is where each instrument is composed without regard to other instruments.
        trans_types = ['P', 'I', 'R', 'RI']
        durationList = self.getDuration()
        pcsDict = {}
        # Create a tonerow object for the original pitch class set
        tonerow = m21.serial.pcToToneRow(pcv)
        statusFile.write('Pitch Sets Used:\n')
        # use this many pitch class set for each part.
        for s in range(0, int(self.cfgData['pcs'])):
            # Select a tonerow transform
            trType = random.choice(trans_types)
            trIdx = random.randrange(0,11)
            row = tonerow.zeroCenteredTransformation(trType, trIdx)
            pcsDict[s] = (trType+':'+str(trIdx),row)
            statusFile.write(trType+':'+str(trIdx) + ' = ')
            rowStr = ''
            for pitch in row:
                rowStr += pitch.name + ', '
            statusFile.write(rowStr.rstrip(', ') +  '\n')
        # Create the Parts with Instruments and the music for that part, append to the score.   This is essentially the Linear mode.
        statusFile.write('\nParts: \n')
        for n in self.cfgData['parts']:
            time.sleep(.001)  # Avoid the id clashes in music21
            part = m21.stream.Part()
            try:
                instr = m21.instrument.fromString(self.cfgData['parts'][n])
            except:
                instr = m21.instrument.fromString('piano')
            part.insert(0, instr)
            statusFile.write(str(n) + ': ' + instr.instrumentName + '\n')
            loNote = instr.lowestNote
            hiNote = instr.highestNote
            statusFile.write('Range: ' + repr(loNote) + ' - ' + repr(hiNote) + '\n')
            # Add the initial tempo and time signature
            part.insert(m21.tempo.MetronomeMark(number=int(self.cfgData['tempo'])))
            part.timeSignature = m21.meter.TimeSignature(self.cfgData['timesig'])

            for s in range(0, int(self.cfgData['pcs'])):
                # Check for tempo and time signature changes and make them on the Part if required.
                if self.cfgData['tempochanges'].get(str(s)):
                    part.append(m21.tempo.MetronomeMark(number=int(self.cfgData['tempochanges'][str(s)])))
                if self.cfgData['timechanges'].get(str(s)):
                    part.append(m21.meter.TimeSignature(self.cfgData['timechanges'][str(s)]))
                pcsID, row = pcsDict[s]
                for p in row.pitches:
                    anote = m21.note.Note(p)
                    time.sleep(.001)  # Avoid the id clashes in music21
                    if pcsID:
                        anote.addLyric(pcsID)
                        pcsID = ''
                    anote.duration = m21.duration.Duration(random.choice(durationList))
                    part.append(anote)
            score.append(part)
        return score


    def Complimentary(self, pcv, score, statusFile):
        # Complimentary composition mode is where complimentary cycle sets are used to create a melody.
        durationList = self.getDuration()
        base_notes = {0:'C',1:'C#',2:'D',3:'D#',4:'E',5:'F',6:'F#',7:'G',8:'G#',9:'A',10:'A#',11:'B'}

        # Create a tonerow object for the original pitch class set
        tonerow = m21.serial.pcToToneRow(pcv)

        statusFile.write('Pitch Sets Used:\n')
        pcsDict = compCycles(pcv)
        if not pcsDict:
            pcv_str = str(pcv).strip('[]')
            statusFile.write("The matrix from row: " + pcv_str + " doesn't contain any P/I complimentary cycles.\n")
            messagebox.showerror(message="The matrix from row: {0} doesn't contain any P/I complimentary cycles.\n".format(pcv_str))
            return(score)

        print(pcsDict[1])
        statusFile.write(str(pcsDict[1]))
        pList = pcsDict[1][0][1]
        iList = pcsDict[1][1][1]
        voice0 = []  # the bass register voice.
        voice1 = []  # the piano register voice.
        durations = []
        velocities = []
        for x in range(0,12):
            voice0.append(base_notes[pList[x]])
            voice0.append(base_notes[iList[x]])
            # create a list of durations
            durations.append(m21.duration.Duration(random.choice(durationList)))
            durations.append(m21.duration.Duration(random.choice(durationList)))
            # create a list of velocities/volume
            velocities.append(random.randint(60,127))
            velocities.append(random.randint(60,127))

        # create voice1 based on the two voice0 neighbor notes
        for x in range(0,24):
            if x == 0:
                voice1.append([voice0[23],voice0[1]])
            elif x == 23:
                voice1.append([voice0[0],voice0[22]])
            else:
                voice1.append([voice0[x-1],voice0[x+1]])

        # Create the Bass Part with Instruments and the music for that part, append to the score.
        statusFile.write('\nParts: \n')
        part0 = m21.stream.Part()
        instr0 = m21.instrument.fromString('Contrabass')
        part0.insert(0, instr0)
        statusFile.write('0: ' + instr0.instrumentName + '\n')
        # Add the initial tempo and time signature
        part0.insert(m21.tempo.MetronomeMark(number=int(self.cfgData['tempo'])))
        part0.timeSignature = m21.meter.TimeSignature(self.cfgData['timesig'])
        for x in range(0,24):
            anote = m21.note.Note(voice0[x]+'3')
            time.sleep(.001)  # Avoid the id clashes in music21
            anote.duration = durations[x]
            anote.volume.velocity = velocities[x]
            anote.addLyric(anote.nameWithOctave)
            anote.addLyric(anote.pitch.pitchClassString)
            part0.append(anote)

        part1 = m21.stream.Part()
        instr1 = m21.instrument.fromString('Piano')
        part1.insert(0, instr1)
        statusFile.write('1: ' + instr0.instrumentName + '\n')
        # Add the initial tempo and time signature
        part1.insert(m21.tempo.MetronomeMark(number=int(self.cfgData['tempo'])))
        part1.timeSignature = m21.meter.TimeSignature(self.cfgData['timesig'])

        for x in range(0,24):
            achord = m21.chord.Chord(voice1[x])
            time.sleep(.001)  # Avoid the id clashes in music21
            achord.duration = durations[x]
            achord.volume.velocity = velocities[x]
            part1.append(achord)

        # add the parts to the score in the desired sequence
        score.append(part1)
        score.append(part0)

        return score

    def Sequential(self, pcv, score, statusFile):
        # Sequential composition mode is where each instrument is composed in connection with the other instruments.
        # They all use the same set of PCSs and the same set of Durations.
        trans_types = ['P', 'I', 'R', 'RI']
        durationList = self.getDuration()
        pcsDict = {}
        notesDict = {}

        # Create a tonerow object for the original pitch class set
        tonerow = m21.serial.pcToToneRow(pcv)

        statusFile.write('Pitch Sets Used:\n')
        # use this many pitch class set for each part.
        for s in range(0, int(self.cfgData['pcs'])):
            # Select a tonerow transform
            trType = random.choice(trans_types)
            trIdx = random.randrange(0,11)
            row = tonerow.zeroCenteredTransformation(trType, trIdx)
            pcsDict[s] = (trType+':'+str(trIdx),row)
            statusFile.write(trType+':'+str(trIdx) + ' = ')

            # Create the notes with durations
            rowStr = ''
            notesDict[s] = []
            for anote in row:
                if len(notesDict[s]) == 0:  # first note in set gets the ID as a lyric
                    anote.addLyric(trType+':'+str(trIdx))
                anote.duration = m21.duration.Duration(random.choice(durationList))
                notesDict[s].append(anote)

                rowStr += anote.name + ', '

            # write the details to the status file
            rowStr = rowStr.rstrip(', ')
            statusFile.write(rowStr +  '\n')

        # Create the Parts with Instruments and the music for that part, append to the score.   This is essentially the Linear mode.
        statusFile.write('\nParts: \n')
        for n in self.cfgData['parts']:
            time.sleep(.001)  # Avoid the id clashes in music21
            part = m21.stream.Part()
            try:
                instr = m21.instrument.fromString(self.cfgData['parts'][n])
            except:
                instr = m21.instrument.fromString('piano')
            part.insert(0, instr)
            statusFile.write(str(n) + ': ' + instr.instrumentName + '\n')
            loNote = instr.lowestNote
            hiNote = instr.highestNote

            statusFile.write('Range: ' + repr(loNote) + ' - ' + repr(hiNote) + '\n')

            # Add the initial tempo and time signature
            part.insert(m21.tempo.MetronomeMark(number=int(self.cfgData['tempo'])))
            part.timeSignature = m21.meter.TimeSignature(self.cfgData['timesig'])

            for s in range(0, len(notesDict)):
                for anote in notesDict[s]:
                    part.append(anote)
            score.append(part)

        return score

    def Orchestral(self, pcv, score, statusFile):
        # Orchestral composition mode is where each instrument plays a portion of the ToneRow simultaneously.
        trans_types = ['P', 'I', 'R', 'RI']
        durationList = self.getDuration()
        pcsDict = {}
        notesDict = {}

        # Create a tonerow object for the original pitch class set
        tonerow = m21.serial.pcToToneRow(pcv)

        statusFile.write('Pitch Sets Used:\n')
        # use this many pitch class sets for each part.
        for s in range(0, int(self.cfgData['pcs'])):
            # Select a tonerow transform
            trType = random.choice(trans_types)
            trIdx = random.randrange(0,11)
            row = tonerow.zeroCenteredTransformation(trType, trIdx)
            pcsDict[s] = (trType+':'+str(trIdx),row)
            statusFile.write(trType+':'+str(trIdx) + ' = ')
            rowStr = ''
            for pitch in row:
                rowStr += pitch.name + ', '
            statusFile.write(rowStr.rstrip(', ') +  '\n')

            chordSet = makeChords(row, '1', sf, (2,4,6))
            notesDict[s] = chordSet

        # Create the Parts with Instruments and the music for that part, append to the score.
        statusFile.write('\nParts: \n')
        for n in self.cfgData['parts']:
            time.sleep(.001)  # Avoid the id clashes in music21
            part = m21.stream.Part()
            try:
                instr = m21.instrument.fromString(self.cfgData['parts'][n])
            except:
                instr = m21.instrument.fromString('piano')
            part.insert(0, instr)
            statusFile.write(str(n) + ': ' + instr.instrumentName + '\n')
            loNote = instr.lowestNote
            hiNote = instr.highestNote

            statusFile.write('Range: ' + repr(loNote) + ' - ' + repr(hiNote) + '\n')

            # Add the initial tempo and time signature
            part.insert(m21.tempo.MetronomeMark(number=int(self.cfgData['tempo'])))
            part.timeSignature = m21.meter.TimeSignature(self.cfgData['timesig'])
            for s in range(0, len(notesDict)):
                part.append(notesDict[s][int(n) % 3 ])
                part.append(notesDict[s][3])

            score.append(part)

        return score


    def twelveTone(self):
        self.generate()


    def psClass(self):
        chords = OrderedDict()
        chordNum = 0
        durationList = self.getDuration()
        circle = {0:'C',1:'C#',2:'D',3:'D#',4:'E',5:'F',6:'F#',7:'G',8:'G#',9:'A',10:'A#',11:'B'}
        from PitchSetClasses import pitchSetClass
        psc = pitchSetClass()
        sets = self.cfgData['pc_sets']

        for n in sets:
            s = sets[n].split(':')[1]
            setName = sets[n].split(':')[0]
            for x in s.split(','):
                notes = []
                chordNum += 1
                for y in psc.getByName(setName)[0]:
                    anote = m21.note.Note(circle[ (int(y) + int(x)) % 12 ])
                    anote.duration = m21.duration.Duration(random.choice(durationList))
                    anote.volume.velocity = 127
                    notes.append(anote)
                    time.sleep(.001)  # Avoid the id clashes in music21                    
                chords[setName + ': '+ str(chordNum)] = m21.chord.Chord(notes)

        score = m21.stream.Score()
        # Setup Metadata
        md = m21.metadata.Metadata()
        md.title = self.cfgData['title']
        md.composer = self.cfgData['composer']
        md.date = m21.metadata.DateSingle(data=self.cfgData['date'])
        md.copyright = self.cfgData['copyright']
        md.alternativeTitle = 'Generated by AMG version: ' + self.cfgData['amg_version']
        score.insert(0, md)

        part = m21.stream.Part()
        instr = m21.instrument.fromString('piano')
        part.insert(0, instr)
        # Add the initial tempo and time signature
        part.insert(m21.tempo.MetronomeMark(number=int(self.cfgData['tempo'])))
        part.timeSignature = m21.meter.TimeSignature(self.cfgData['timesig'])

        for c in chords.keys():
            part.append(chords[c])
            arest = m21.note.Rest()
            arest.duration = m21.duration.Duration(random.choice(durationList))
            part.append(arest)
            time.sleep(.001)  # Avoid the id clashes in music21
            
        score.append(part)
        try:
            score.write(fmt='midi', fp=os.path.join(self.cfgData['outpath'], self.cfgData['outfile'] + '.mid'))
        except:
            e = sys.exc_info()[0]
            m = sys.exc_info()[1]
            messagebox.showerror(message="MIDI Error: {0}: \nMessage: {1}".format(e, m))
        try:
            score.write(fmt='xml', fp=os.path.join(self.cfgData['outpath'], self.cfgData['outfile'] + '.xml'))
        except:
            e = sys.exc_info()[0]
            m = sys.exc_info()[1]
            messagebox.showerror(message="XML Error: {0}: \nMessage: {1}".format(e, m))
        try:
            self.genAnimation(score)
        except:
            e = sys.exc_info()[0]
            m = sys.exc_info()[1]
            messagebox.showerror(message="Animation Error: {0}: \nMessage: {1}".format(e, m))

        messagebox.showinfo("Generator", "Generation is complete.\n Your files are located in " + self.cfgData['outpath'])


    def generate(self):
        statusFile = Status(os.path.join(self.cfgData['outpath'], self.cfgData['outfile'] + '.txt'))
        messagebox.showinfo("Composer", "This may take a few minutes depending on the size of the work.\n"+"Press Ok to start composing.")
        m21.environment.set('musicxmlPath', self.cfgData['musicxmlPath'])
        base_pcv =  {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}

        tr = m21.serial.ToneRow()
        score = m21.stream.Score()
        # Setup Metadata
        md = m21.metadata.Metadata()
        md.title = self.cfgData['title']
        md.composer = self.cfgData['composer']
        md.date = m21.metadata.DateSingle(data=self.cfgData['date'])
        md.copyright = self.cfgData['copyright']
        md.alternativeTitle = 'Generated by AMG version: ' + self.cfgData['amg_version']
        score.insert(0, md)

        # convert the original row into a list of pitch class values
        orow = self.cfgData['orow']
        pcv = orow2pcv(orow)

        statusFile.write("Original Row: " + orow + '\n')

        if self.cfgData['mode'] == 'Linear':
            score = self.Linear(pcv, score, statusFile)
        elif self.cfgData['mode'] == 'Complimentary':
            score = self.Complimentary(pcv, score, statusFile)
        elif self.cfgData['mode'] == 'Sequential':
            score = self.Sequential(pcv, score, statusFile)
        elif self.cfgData['mode'] == 'Orchestral':
            score = self.Orchestral(pcv, score, statusFile)
        else:
            messagebox.showinfo("Generator", "Fatal Error in Mode selection.\n")
            return


        messagebox.showinfo("Generator", "Composition is complete.\n"+"Press Ok to generate files.")

        try:
            score.write(fmt='midi', fp=os.path.join(self.cfgData['outpath'], self.cfgData['outfile'] + '.mid'))
        except:
            e = sys.exc_info()[0]
            m = sys.exc_info()[1]
            messagebox.showerror(message="MIDI Error: {0}: \nMessage: {1}".format(e, m))
        try:
            score.write(fmt='xml', fp=os.path.join(self.cfgData['outpath'], self.cfgData['outfile'] + '.xml'))
        except:
            e = sys.exc_info()[0]
            m = sys.exc_info()[1]
            messagebox.showerror(message="XML Error: {0}: \nMessage: {1}".format(e, m))
        try:
            self.genAnimation(score)
        except:
            e = sys.exc_info()[0]
            m = sys.exc_info()[1]
            messagebox.showerror(message="Animation Error: {0}: \nMessage: {1}".format(e, m))

        messagebox.showinfo("Generator", "Generation is complete.\n Your files are located in " + self.cfgData['outpath'])

        statusFile.close()

        return

    def genAnimation(self, score):
        """
        Generate a Xaos animation file from the score data.
        """
        formulaDict = {'Piano':'mandel6', 'Pan Flute':'newton', 'Acoustic Bass':'mandel4', 'Keyboard':'octo', 'Harpsichord':'newton4', 'Clavichord':'barnsley1', 'Electric Organ':'barnsley2', 'Harmonica':'barnsley3', 'Violin':'phoenix', 'Electric Guitar':'magnet', 'Acoustic Guitar':'magnet2', 'Flute':'catseye', 'Oboe':'lambda', 'Clarinet':'manowar', 'Saxophone':'spider'}
        aFile = open(os.path.join(self.cfgData['outpath'], self.cfgData['outfile'] + '.xaf'), 'w')
        aFile.write("; A Xaos animation file\n")
        aFile.write("; Generated by the Twelve Tone Composer\n")
        aFile.write("(initstate)\n")
        aFile.write("(letterspersec 5)\n")
        aFile.write("(maxiter 275)\n")
        aFile.write("(autorotate #t)\n")
        aFile.write("(rotationspeed -5)\n")
        aFile.write("(angle 270)\n")
        aFile.write("(filter 'palette #t)\n")
        aFile.write("(cycling #t)\n")
        aFile.write("(cyclingspeed 3)\n")
        aFile.write("(outcoloring 7)\n")
        aFile.write("(incoloring 3)\n")

        aFile.write("(clearscreen)\n")
        aFile.write("(display)\n")
        aFile.write("(defaultpalette 1000)\n")
        aFile.write("(plane 0)\n")
        aFile.write("(formula 'spider)\n")
        aFile.write("(view -0.01 -0.006 0.009 0.009)\n")
        aFile.write("(usleep 250000)\n")

        aFile.write("(textposition 'center 'bottom)\n")
        aFile.write('(text "Title: ' + score.metadata.title + ' by ' + score.metadata.composer + ' ")\n')
        aFile.write("(textsleep)\n")

        # position vars
        x = -0.012
        y = -0.106
        z = 0.169
        n = 0.069
        totDur = 0

        for part in score.parts:
            partDur = 0
            aFile.write('\n; Part: ' + str(part.id) + '\n')
            for m in part:
                partDur += m.seconds
                if isinstance(m, m21.stream.instrument.Instrument):
                    formula =  formulaDict.get(str(m), 'mandel')
                    aFile.write("(formula '" + formula + ')\n')
                if isinstance(m, m21.stream.Measure):
                    aFile.write('\n; Measure: ' + str(m.id) +'\n')
                    palNum = 0
                    move = 0.0
                    viewDur = m.seconds * 1000000
                    totDur += m.seconds

                    for note in m.notes:
                        move += note.duration.ordinal / 333
                        for p in note.pitches:
                            palNum += int(p.frequency)/10

                    aFile.write('(defaultpalette ' + str(int(palNum)) + ')\n')
                    aFile.write("(morphview " + str(x - move) + " " + str(y + move) + " " + str(z + move) + " " + str(n + move) + ")\n")
                    aFile.write("; Seconds in measure: " + str(m.seconds) + "\n")
                    aFile.write("(usleep " + str(int(viewDur)) + ")\n")

        aFile.write("(initstate)\n")
        aFile.close()
        return
    

if __name__ == "__main__":
    if len(sys.argv) == 2:
        cfgfile = sys.argv[1]
    else:
        cfgfile = 'default.amgd'

    cfg_data = config.config(cfgfile)

    root = tk.Tk()
    root.geometry('2048x1200')
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(size=18)
    #fixed_font = tkFont.nametofont("fixed")
    #fixed_font.configure(size=18)

    # imgPath = r'amg.jpg'
    # img = tk.PhotoImage(file=imgPath)
    # root.tk.call('wm', 'iconphoto', root._w, img)
    app = AMG(root, cfgData=cfg_data)
    root.mainloop()
