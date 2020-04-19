'''
    The Filer class
'''

import py_midicsv
import pickle
import os

class Filer():

    def __init__(self, fromFile, toFile):
        '''
            Initiates the Filer class.

            Attributes:
                fromFile: file to be deleted
                toFile: file to which MIDI should be saved

        '''

        self.fromFile = fromFile
        self.toFile = toFile
    

    def get_fromFile(self):
        '''Returns fromFile'''

        return self.fromFile
    

    def get_toFile(self):
        '''Returns toFile'''

        return self.toFile


    def generatedToNums(self, genText):
        '''Converts generated text to 2d-array of notes with note information. Returns the 2d-array'''

        tagless = self.cutTags(genText)
        splitted = self.splitNotes(tagless)
        num_notes, last_note_end= self.reprToNum(splitted)
        return num_notes, last_note_end
    

    def finishFinalMidi(self, num_notes_in_key, last_note_end):
        '''Takes 2d-array with adjusted note values and saves as MIDI file'''

        messages = self.doubleNoteMessages(num_notes_in_key)
        sorted_messages = self.mergeSortOnMessages(messages)
        on_off_messages = self.convToMidiMessages(sorted_messages)
        CSV_midi = self.addNecessaryMessages(on_off_messages, last_note_end)
        parsed_midi = self.createMidiFromCSV(CSV_midi)
        self.saveMidiAsFile(parsed_midi)


    def cutTags(self, generated):
        '''Removes tags and identifies returns a full solo'''

        gen_no_start_tags = generated[4:]
        end_of_solo = gen_no_start_tags.find(' ###')
        tagless = gen_no_start_tags[:end_of_solo]
        return tagless


    def splitNotes(self, generated):
        '''Splits text into 2d-array of notes with relevant data and returns it'''

        splitted_partly = generated.split()
        fully_split = []
        for note in splitted_partly:
            fully_split.append(note.split('!'))
        return fully_split
    

    def reprToNum(self, generated):
        '''Converts representative compressed values to integer values and return 2d-array'''

        num_notes = []
        for note in generated:
            try:
                new_note = []
                new_note.append(self.HextridecToDec(note[0]) * 6)
                new_note.append(str(ord(note[1])-26))
                new_note.append(self.HextridecToDec(note[2]) * 6)
                num_notes.append(new_note)
            except:
                continue
        end_track_on = num_notes[-1][-1] * 6
        return num_notes, end_track_on


    def HextridecToDec(self, hexatridecimal):
        '''Converts hexatridecimal value to integer value'''

        hexatridecimal = '0' + hexatridecimal
        i = int(hexatridecimal, 36)
        return i


    def doubleNoteMessages(self, num_notes):
        '''Splits note data into two lists - one for on-message and one for off-message. Returns the list.'''

        messages = []
        for bundle in num_notes:
            note = bundle[1]
            start = bundle[0]
            end = bundle[2]
            if start == end:
                continue
            message_start = [0, start, note]
            messages.append(message_start)
            message_end = [1, end, note]
            messages.append(message_end)
        return messages


    def mergeSortOnMessages(self, messages):
        '''Returns a sorted list of messages based on tick value'''

        if len(messages) >1: 
            middle = len(messages)//2 #Finding the mid of the messagesay 
            L = messages[:middle] # Dividing the messagesay elements  
            R = messages[middle:] # into 2 halves 
            self.mergeSortOnMessages(L) # Sorting the first half 
            self.mergeSortOnMessages(R) # Sorting the second half 
            i = 0
            j = 0
            k = 0
            # Copy data to temp messagesays L[] and R[] 
            while i < len(L) and j < len(R): 
                if L[i][1] < R[j][1]: 
                    messages[k] = L[i] 
                    i+=1
                else: 
                    messages[k] = R[j] 
                    j+=1
                k+=1
            # Checking if any element was left 
            while i < len(L): 
                messages[k] = L[i] 
                i+=1
                k+=1           
            while j < len(R): 
                messages[k] = R[j] 
                j+=1
                k+=1 
        return messages


    def convToMidiMessages(self, messages):
        '''Converts each list to a midi message'''

        on_off_messages = []
        for message in messages:
            if message[0] == 0:
                midi_message = ', Note_on_c, 0, '
                velocity = ', 95\n'
            else:
                midi_message = ', Note_off_c, 0, '
                velocity = ', 0\n'
            full_mess = '2, ' + str(message[1]) + midi_message + str(message[2]) + velocity
            on_off_messages.append(full_mess)
        return on_off_messages


    def addNecessaryMessages(self, messages, last_note_end):
        '''Returns list of messages with added header, settings information, end_of_track and end_of_file messages'''

        full_CSV_midi = []
        beginning = self.getBeginning()
        for message in beginning:
            full_CSV_midi.append(message)
        for message in messages:
            full_CSV_midi.append(message)
        end_track = self.findNextFullBar(last_note_end)
        end_track_message = '2, {}, End_track\n'.format(end_track)
        full_CSV_midi.append(end_track_message)
        full_CSV_midi.append('0, 0, End_of_file\n')
        return full_CSV_midi
        

    def findNextFullBar(self, last_note_end):
        '''Returns the next full bar on which the track and file will end'''

        end = last_note_end
        if end % 3840 == 0:
            return end
        else:
            neg_error = end % 3840
            error = 3840 - neg_error
            nextFullBar = end + error
            return nextFullBar    
    
    def getBeginning(self):
        '''Returns header and file settings information messages'''

        with open('BeginningGenMidi.txt', 'r') as the_file:
            beginning = the_file.readlines()
        return beginning


    def createMidiFromCSV(self, new_csv_List):
        '''Returns the converted parsed MIDI from list messages'''

        midi_object = py_midicsv.csv_to_midi(new_csv_List)
        print('Midi object created from text')
        return midi_object


    def saveMidiAsFile(self, midi_object):
        '''Save parsed MIDI to disk'''

        with open(self.get_toFile(), "wb") as midi_file:
            midi_writer = py_midicsv.FileWriter(midi_file)
            midi_writer.write(midi_object)
            print('Midi file saved')


    def removeFile(self):
        '''Removes file'''
        os.remove(self.get_fromFile())
        print('File deleted')
