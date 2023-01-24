import sys
import os
import datetime

class Status(object):

    def __init__(self, outfile):
        self.statusFile = open(outfile, 'w')
        self.statusFile.write('Created: ' +  datetime.datetime.now().strftime("%H:%M  %Y-%m-%d") + '\n')

    def write(self, text):
        self.statusFile.write(text)

    def close(self):
        self.statusFile.close()

