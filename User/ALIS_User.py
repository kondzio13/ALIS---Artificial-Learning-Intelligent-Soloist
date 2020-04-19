'''
    Initiates the ALIS User system and UI
'''

# Import all relevant modules
import pygame
import os

from Modules.KeyFinder import KeyFinder
from Modules.UserFileHandler import Filer
from Modules.Generator import generateFromNet


class ALIS_Generator():


    def __init__(self):
        """

        Initializes an instance of the ALIS_Generator class.

        Attributes:
            __ALIS_on: Determines whether the program keeps running or closes
            __most_recent_key: Stores the most recent key used for writing solos

        """

        self.__ALIS_on = True
        self.__most_recent_key = ''

        print('')
        print('')
        print('####### ALIS, the Artificial Learning Intelligent Soloist #######')
        print('')
        print('ALIS is your innovative working tool for writing new, better')
        print('solos based on your preference and liking. Give me some info')
        print('about your solo and you\'ll be ready to rock in no time!')
        print('')

        while self.get_ALIS_on():
            self.displayMenu()
            choice = input('') # Stores user's choice
            self.branchToChoice(choice)
    

    def get_ALIS_on(self):
        '''Returns the value of __ALIS_on'''

        return self.__ALIS_on


    def turn_ALIS_off(self):
        '''Sets __ALIS_on to False'''

        self.__ALIS_on = False


    def get_most_recent_key(self):
        '''Returns the value of __most_recent_key'''

        return self.__most_recent_key
    

    def change_most_recent_key(self, newkey):
        '''Sets __most_recent_key to *newkey*'''

        self.__most_recent_key = newkey


    def displayContents(self, directory):
        '''Shows contents of *directory* directory'''

        print('')
        for direct in os.listdir(directory):
            print('-', direct)
        print('')


    def deleteFile(self, directory, filename):
        '''Removes the file *filename* from *directory* directory'''

        deleter = Filer(r'{}/{}'.format(directory, filename), 'x.txt')
        deleter.removeFile()


    def displayMenu(self):
        '''Displays the main menu to the user'''

        print('')
        print('######################## Main menu: ########################')
        print('')
        print('1: Generate a new guitar solo')
        print('2: Listen back to generated solos')
        print('3: Delete a solo')
        print('4: Delete a net')
        print('X: Quit program')
        print('')
        print('Enter value to proceed with task.')


    def branchToChoice(self, choice):
        '''Triggers relevant UI based on *choice*'''

        print('')
        if choice == '1':
            self.generateNewGuitarSolo()
        elif choice == '2':
            self.chooseAndPlaybackSolo()
        elif choice == '3':
            self.deleteSolo()
        elif choice == '4':
            self.deleteNet()
        elif choice == 'X':
            self.turn_ALIS_off()
        else:
            print('Invalid choice. Please try again...')


    def generateNewGuitarSolo(self):
        '''UI for generating new guitar solos'''

        directory1 = 'Nets' 
        directory2 = 'Generated_solos'
        if self.get_most_recent_key() == '':
            findkey = KeyFinder()
            new_key = findkey.get_pentakey()
            self.change_most_recent_key(new_key)
        else:
            print('Do you want to continue writing solos in the key of {}?'.format(self.get_most_recent_key()))
            valid_answer = False
            while not valid_answer:
                print('(y/n)')
                print('')
                keep_key = input('')
                if keep_key == 'n':
                    findkey = KeyFinder()
                    new_key = findkey.get_pentakey()
                    self.change_most_recent_key(new_key)
                    valid_answer = True
                elif keep_key == 'y':
                    valid_answer = True
                else:
                    print('Invalid answer') 
        
        print('What would you want to save this solo as?')
        solo_name = input('')

        solo_making = True

        while solo_making:
            print('')
            print('Which net would you like to use? (\'x\' to cancel)')
            self.displayContents(directory1)
            net_name = input('Net: ')
            print('')
            if net_name == 'x':
                    break
            else:
                try:
                    gen_text = generateFromNet(net_name)
                    converter = Filer('x.txt', '{}/{}.mid'.format(directory2, solo_name))
                    numed_list, last_note_end = converter.generatedToNums(gen_text)
                    scaled = findkey.fitToScale(numed_list)
                    converter.finishFinalMidi(scaled, last_note_end)
                    print('')
                    print('Midi writing successful. New solo saved as {}.mid'.format(solo_name))
                    solo_making = False
                    break
                except:
                    print('Net chosen was unable to produce a solo in the required format or is not in {}.'.format(directory1))
                    print('This could be because the net has not been trained enough.')
                    print('Try using a different model to generate your solo.')
                        
                
    def chooseAndPlaybackSolo(self):
        '''UI for playback songs'''

        directory = 'Generated_solos'
        print('Please enter the midi file name within {} which'.format(directory))
        print('you would like to playback: (\'x\' to cancel)')
        self.displayContents(directory)
        valid_midi_file = False
        while not valid_midi_file:
            try:
                midi_file = input('MIDI file: ')
                if midi_file =='x':
                    break
                self.playback(directory, midi_file)
                valid_midi_file = True
            except:
                print('MIDI file not found. Please enter valid file name from the {} directory.'.format(directory))


    def playback(self, directory, file):
        '''Play *file* from *directory*'''

        pygame.init() # Initialise pygame
        pygame.mixer.music.load('{}/{}'.format(directory, file)) # Load MIDI file
        pygame.mixer.music.play() # Play MIDI file


    def deleteSolo(self):
        '''UI for deleting a solo''' 

        directory = 'Generated_solos'
        print('Please enter the midi file name within {} which'.format(directory))
        print('you would like to delete: (\'x\' to cancel)')
        self.displayContents(directory)
        valid_midi_file = False
        while not valid_midi_file:
            try:
                midi_file = input('MIDI file: ')
                if midi_file =='x':
                    break
                self.deleteFile(directory, midi_file)
                valid_midi_file = True
            except:
                print('MIDI file not found. Please enter valid file name from the {} directory.'.format(directory))


    def deleteNet(self):
        '''UI for deleting a network model'''

        directory = 'Nets'
        print('Please enter the net name within {} which'.format(directory))
        print('you would like to delete: (\'x\' to cancel)')
        self.displayContents(directory)
        valid_net = False
        while not valid_net:
            
                net = input('Net: ')
                if net =='x':
                    break
                self.deleteFile(directory, net)
                valid_net = True
            
                print('Net not found. Please enter valid file name from the {} directory.'.format(directory))

        
    def quit_ALIS(self):
        '''UI for exiting the ALIS system'''

        print('################ Thank you for using ALIS  ################')
        endit = input('Enter to close program...')


# Only run if this is the main program running
if __name__ == '__main__':

    # Initiate an ALIS_Generator object
    alis = ALIS_Generator()
