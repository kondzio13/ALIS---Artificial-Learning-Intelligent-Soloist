'''
    Master FileHandler class
'''

import py_midicsv
import os


class FileHandler():

    def __init__(self, fromFile, toFile):
        '''
        Inititiates the FileHandler object.

        Atrribute:
            __fromFile: load data from this file
            __toFile: save data to this file
        '''

        self.__fromFile = fromFile
        self.__toFile = toFile

    def get_fromFile(self):
        '''Returns __fromFile'''

        return self.__fromFile
    
    def get_toFile(self):
        '''returns __toFile'''

        return self.__toFile

    def midiToText(self):
        '''Returns relevant contents of midi file as coded text'''

        csv_list = self.midiToCSV()
        cleaned_list = self.convertMessages(self.cleanTracks(csv_list))
        compressed_list = self.compressText(cleaned_list)
        text_list = self.joinNotes(compressed_list)
        return text_list

    def joinNotes(self, lister):
        '''Returns list of strings representing a note'''

        stringer = ''
        for note in lister:
            text_note = (note[0] + '!' + note[1] + '!' + note[2] + ' ')
            stringer = stringer + text_note
        return stringer

    def compressText(self, solo):
        '''Returns 2d-list of compressed representations of values for each note'''

        item = 0
        cutting = True
        comp_solo = []
        while cutting:
            if len(solo) != 0:
                note = solo[0][1]
                start = self.toHexatridecimal(solo[0][0])[1:]
                if start == '':
                    start = '0'
                looking = True
                item1 = 1
                while looking:
                    if solo[item1][1] == note:
                        end = self.toHexatridecimal(solo[item1][0])[1:]
                        if end == '':
                            end = '0'
                        del solo[item1]
                        looking = False
                    else:
                        item1 += 1
                asc_note = chr(int(note) + 26) # Shifts ascii value to ensure ascii character is printable
                comp_solo.append([start, asc_note, end])
                del solo[0]
            else:
                cutting = False   
        return comp_solo  

    def toHexatridecimal(self, decimalstring):
        '''Returns argument as a hexatridecimal string'''

        dec = int(decimalstring)
        x = (dec % 36)
        digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        rest = dec / 36
        if (rest == 0):
            return digits[x]
        return self.toHexatridecimal(rest) + digits[x]

    def convertMessages(self, csv_list):
        '''Returns 2d-list of relevant event information for each event as integers'''

        required_messages = ['Note_on_c', 'Note_off_c']
        csv_list = [message.split(', ') for message in csv_list]
        del_list = []
        for i in range(len(csv_list)):
            if csv_list[i][2] not in required_messages:
                del_list.append(i)
        deleted_items = 0
        for index in del_list:
            del csv_list[index - deleted_items]
            deleted_items += 1
        for message in csv_list:
            # Gets rid of '\n' in final item
            del message[0]
            del message[1]
            del message[1]
            del message[-1]
        return csv_list

    def cleanTracks(self, csv_list):   
        '''Returns list of MIDI messages in track with solo'''

        del_list = [] # List of messages to be deleted
        for i in range(len(csv_list)):
            track = csv_list[i][0]
            if track != '2':
                del_list.append(i)
        deleted_items = 0 # Makes sure all items are iterated over as elements from csv_list are deleted
        for index in del_list:
            del csv_list[index - deleted_items]
            deleted_items +=1
        return csv_list

    def midiToCSV(self):
        '''Returns content of MIDI file as CSV list'''

        csv_list = py_midicsv.midi_to_csv(self.get_fromFile())
        return csv_list


    def writeTextToFile(self, text):
        with open(self.get_toFile(), 'w') as training_file:
            training_file.write(text)

    def removeFile(self):
        '''Removes file'''

        os.remove(self.get_fromFile())
        print('File deleted')
