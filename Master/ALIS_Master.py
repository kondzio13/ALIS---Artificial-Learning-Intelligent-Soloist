'''
    Initiates the ALIS  Master system and UI
'''

# Import all relevant modules
import os

from Modules.MasterFileHandler import FileHandler
from Modules.TrainNN import trainNSaveRNN


class ALIS_Trainer:


    def __init__(self):
        """

        Initializes an instance of the ALIS_Trainer class.

        Attributes:
            __ALIS_on: Determines whether the program keeps running or closes

        """

        self.__ALIS_on = True

        print('')
        print('')
        print('################ Welcome to ALIS\'s trainer ################')
        print('')
        print('Please make sure that all your midi files are cleaned and')
        print('inside a directory within \'Midi_training_data\'. Failure to')
        print('do so might return an error or miss out some solos when')
        print('creating the training set.')

        while self.get_ALIS_on():
            self.displayMenu()
            choice = input('') # Stores user's choice
            self.branchToChoice(choice)
        
        self.quit_ALIS()


    def get_ALIS_on(self):
        '''Returns the value of __ALIS_on'''

        return self.__ALIS_on


    def turn_ALIS_off(self):
        '''Sets __ALIS_on to False'''

        self.__ALIS_on = False


    def displayContents(self, directory):
        '''Shows contents of *directory* directory'''

        print('')
        for direct in os.listdir(directory):
            print('-', direct)
        print('')


    def createNSaveTrainingSet(self, midi_set):
        '''Creates and saves the training data set out of every midi file in *midi_set* directory'''

        training_set_text = ''
        directory = r'Midi_training_data/{}'.format(midi_set)
        for filename in os.listdir(directory):
            if filename.endswith(".mid"):
                filer = FileHandler(r'{}/{}'.format(directory, filename), 'x.txt')
                training_set_text = training_set_text + '### ' + filer.midiToText() # Note information for every solo seperated by '###'
            else:
                continue
        print('')
        training_set_text = training_set_text + '###'

        filer2 = FileHandler('x.txt', '{}.txt'.format(midi_set))
        filer2.writeTextToFile(training_set_text)


    def deleteFile(self, directory, filename):
        '''Removes the file *filename* from *directory* directory'''

        deleter = FileHandler(r'{}/{}'.format(directory, filename), 'x.txt')
        deleter.removeFile()


    def displayMenu(self):
        '''Displays the main menu to the user'''

        print('')
        print('######################## Main menu: ########################')
        print('')
        print('1: Create training set from MIDI files...')
        print('2: Train network on training set...')
        print('3: Delete training set...')
        print('4: Delete network...')
        print('X: Quit')
        print('')
        print('Enter value to proceed with task.')


    def branchToChoice(self, choice):
        '''Triggers relevant UI based on *choice*'''

        print('')
        if choice == '1':
            self.trainingSet()
        elif choice == '2':
            self.setUpTraining()
        elif choice == '3':
            self.deleteTrainingSet()
        elif choice == '4':
            self.deleteNet()
        elif choice == 'X':
            self.turn_ALIS_off()
        else:
            print('Invalid choice. Please try again...')


    def trainingSet(self):
        '''UI for creating and saving data set'''

        directory = 'Midi_training_data'
        print('Please enter directory name within {} which'.format(directory))
        print('you would like ALIS to use to create a text training set: (\'x\' to cancel)')
        self.displayContents(directory)
        valid_midi_training_set = False
        while not valid_midi_training_set:
            try:
                midi_training_set = input('Directory: ')
                if midi_training_set == 'x':
                    break
                self.createNSaveTrainingSet(midi_training_set)
                valid_midi_training_set = True
            except:   
                print('Directory not found. Please enter valid directory from the {} directory.'.format(directory))


    def setUpTraining(self):
        '''UI for training a network model'''

        directory = 'Training_sets'
        print('Choose training set to use for training: (\'x\' to cancel)')
        self.displayContents(directory)
        valid_training_set = False
        while not valid_training_set:
            try:
                training_set = input('Training set: ')
                if training_set == 'x':
                    break
                trainNSaveRNN(training_set)
                valid_training_set = True
            except:
                print('Training set not found. Please enter valid file name from the {} directory.'.format(directory))


    def deleteTrainingSet(self):
        '''UI for deleting a training set'''

        directory = 'Training_sets'
        print('Please enter the training set file name within {} which'.format(directory))
        print('you would like to delete: (\'x\' to cancel)')
        self.displayContents(directory)
        valid_training_set = False
        while not valid_training_set:
            try:
                training_set = input('Training Set: ')
                if training_set == 'x':
                    break
                self.deleteFile(directory, training_set)
                valid_training_set = True
            except:
                print('Training set not found. Please enter valid file name from the {} directory.'.format(directory))
    

    def deleteNet(self):
        '''UI for deleting network model'''

        directory = 'Nets'
        print('Please enter the net file name within {} which'.format(directory))
        print('you would like to delete: (\'x\' to cancel)')
        self.displayContents(directory)
        valid_net = False
        while not valid_net:
            try:
                net = input('Net: ')
                if net == 'x':
                    break
                self.deleteFile(directory, net)
                valid_net = True
            except:
                print('Net not found. Please enter valid net name from the {} directory.'.format(directory))


    def quit_ALIS(self):
        '''UI for exiting the ALIS system'''

        print('################ Thank you for using ALIS  ################')
        endit = input('Enter to close program...')

# Only run if this is the main program running
if __name__ == '__main__':

    # Initiates ALIS_Trainer object
    alis = ALIS_Trainer()
