'''
    The KeyFinder class
'''

import random

class KeyFinder:


    def __init__(self):
        '''
            Initiates the KeyFinder object.

            Attributes:
                notes: array of valid notes
                chord_chart: used to determine key of the song
                progression: the chord progression of the song
                pentakey: stores the key of the song

        '''
        self.notes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
        self.chord_chart = self.genChordChart()
        self.progression = self.userChordProg()
        self.pentakey = self.findKey()


    def get_notes(self):
        '''Return notes'''

        return self.notes
    

    def get_chord_chart(self):
        '''Return chord_chart'''

        return self.chord_chart
    

    def get_progression(self):
        '''Return progression'''

        return self.progression


    def get_pentakey(self):
        '''Return pentakey'''

        return self.pentakey


    def genChordChart(self):
        '''
        Generates the Chord Chart to be used for identifying keys
        self.chordChart is a list of tuples including the KeyNote and a list with possible
        chords if that was the Key of the song.
        '''

        chord_chart = []
        for i in range(12):
            relChords = []
            ch0 = self.notes[i]
            ch1 = self.notes[(i + 2) % 12].lower()
            ch2 = self.notes[(i + 4) % 12].lower()
            ch7 = self.notes[(i + 3) % 12]
            ch3 = self.notes[(i + 5) % 12]
            ch4 = self.notes[(i + 7) % 12]
            ch5 = self.notes[(i + 9) % 12].lower()
            ch6 = self.notes[(i + 11) % 12]
            ch = [ch0, ch1, ch2, ch7, ch3, ch4, ch5, ch6]
            for chord in ch:
                relChords.append(chord)
            note = self.notes[i]
            chord_chart.append([note, relChords])
        return chord_chart


    def userChordProg(self):
        '''
        Retrieves the chord progression from user
        Returns progression as a list of tuples with the chord and number of bars 
        it is consecutively played for.
        '''
        invalid_nChords = True
        while invalid_nChords:
            try:
                nChords = int(input('How many chords in your chord progression? '))
                if nChords >= 0:
                    invalid_nChords = False
                else:
                    print('Number of chords must be greater than 0.')
            except:
                print('Invalid number of chords entered.')
        progression = []
        print('Use UPPERCASE letters to represent major keys and lowercase letter to represent minor. Use \'b\' after the chord base to represent \'black key\' chords:')
        for n in range(1, nChords + 1):
            invalidBase = True
            invalidSign = True
            while invalidBase or invalidSign:
                tempChord = input('Enter chord ' + str(n) + ': ')
                if ((ord(tempChord[0]) < 72) and (ord(tempChord[0]) > 64)) or ((ord(tempChord[0]) < 104) and (ord(tempChord[0]) > 96)):
                    invalidBase = False
                if len(tempChord) == 2:
                    if tempChord[1] == 'b':
                        if not (tempChord[0] == 'c' or tempChord[0] == 'f' or tempChord[0] == 'C' or tempChord[0] == 'F'):
                            invalidSign = False
                if len(tempChord) == 1:
                    invalidSign = False
                if invalidBase or invalidSign:
                    print('Invalid chord entered. Try again...')
                    invalidBase = True
                    invalidSign = True
            invalidBars = True
            while invalidBars:
                try:
                    tempBars = int(input('How long is this chord played for? *Max 4 bars* '))
                    if tempBars > 0 and tempBars < 5:
                        invalidBars = False
                    if invalidBars:
                        print('Invalid number of bars...')
                except:
                    print('Invalid number of bars. Must be integers...')
            progression.append([tempChord, tempBars])
        return progression


    def findKey(self):
        '''
        Note: solos generated on pentatonic scale bases. Notes in major pentatonic scales are the same as the relative minor pentatonic scale, hence only the major scales are considered
        Attempts to find a fitting pentatonic key to fit the progression for the solo and stores possible keys in possibleKeys
        '''

        possibleKeys = []
        progression = self.get_progression()
        pentakey = ''
        for key in self.get_chord_chart():
            isPossibleKey = True
            for chord in progression:
                if not chord[0] in key[1]:
                    isPossibleKey = False
            if isPossibleKey:
                possibleKeys.append(key[0])

        # Asks user for the key if finds more than one chord to which it fits
        if len(possibleKeys) > 1:
            print('If you know in which of the following keys the song/solo part is in, please enter below. If not, enter \'x\'.')
            print(*possibleKeys)
            invalidKey = True
            while invalidKey:
                key = input('')
                if key == 'x':
                    invalidKey = False
                if key in possibleKeys:
                    invalidKey = False
                if invalidKey:
                    print('Invalid key...')

            # If user doesn't know, asks about any more chords from other parts of the song and stores in moreChords
            if key == 'x':
                wantMoreChords = input('Do you use anymore chords throughout the song? (\'y\' or \'n\')')
                if wantMoreChords == 'y':
                    nChordsInvalid = True
                    while nChordsInvalid:
                        try:
                            nMoreChords = int(input('Enter number of extra chords: '))
                            if nMoreChords > 0:
                                nChordsInvalid = False
                        except:
                            print('Invalid number of chords...')
                    moreChords = []
                    for n in range(1, nMoreChords + 1):
                        invalidBase = True
                        invalidSign = True
                        while invalidBase or invalidSign:
                            tempChord = input('Enter chord ' + str(n) + ': ')
                            if ((ord(tempChord[0]) < 72) and (ord(tempChord[0]) > 64)) or ((ord(tempChord[0]) < 104) and (ord(tempChord[0]) > 96)):
                                invalidBase = False
                            if len(tempChord) == 2:
                                if tempChord[1] == 'b':
                                    if not (tempChord[0] == 'c' or tempChord[0] == 'f' or tempChord[0] == 'C' or tempChord[0] == 'F'):
                                        invalidSign = False
                            if len(tempChord) == 1:
                                invalidSign = False
                            if invalidBase or invalidSign:
                                print('Invalid chord entered. Try again...')
                                invalidBase = True
                                invalidSign = True
                        moreChords.append(tempChord)
                
                    # Checks the new chords against the chords that could work with the possible keys
                    for possibleKey in possibleKeys:
                        isStillPossibleKey = True
                        for i in range(12):
                            if self.get_chord_chart()[i][0] == possibleKey:
                                for xchord in moreChords:
                                    if not xchord in self.get_chord_chart()[i][1]:
                                        isStillPossibleKey = False
                        if not isStillPossibleKey:
                            possibleKeys.remove(possibleKey)
                
                # Chooses one of the possible keys to use
                if len(possibleKeys) > 1:
                    pentakey = random.choice(possibleKeys)
                else:
                    pentakey = possibleKeys[0]
            else:
                pentakey = key
        else:
            pentakey = possibleKeys[0]
        
        return pentakey


    def fitToScale(self, notes):
        '''Fits note values in *notes* to scale and returns 2d-array'''

        all_notes = notes
        for bundle in all_notes:
            note = bundle[1]
            bundle[1] = self.noteToKey(note)
        return all_notes
        

    def noteToKey(self, note):
        '''Adjusts *note* value to fit to the pentatonic scale and returns value'''

        note = int(note)
        shift = self.get_notes().index(self.get_pentakey())
        n_check = note - shift
        if self.get_pentakey()[0].isupper():
            values = [0, 2, 4, 7, 9]
        else:
            values = [0, 3, 5, 7, 10]
        zero_octave = n_check % 12
        if zero_octave in values:
            return str(note)
        elif zero_octave == 11:
            note += 1
            return str(note)
        else:
            note_not_in_key = True
            counter = 0
            change = 1
            if random.random() < 0.5:
                change = -1
            while note_not_in_key:
                zero_octave = (zero_octave + change) % 12
                counter = counter + change
                if zero_octave in values:
                    note = note + change
                    note_not_in_key = False
                    return str(note)
                else:
                    continue