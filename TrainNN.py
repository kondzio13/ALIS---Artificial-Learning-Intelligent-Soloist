'''
    Extra functions focusing on training the RNN
'''

import torch
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F
from Modules.CharacterRNN import CharRNN
from Modules.CharacterRNN import one_hot_encode
import numpy as np
import time

def get_batches(arr, n_seqs, n_steps):
    '''
    Create a generator that returns batches of size
    n_seqs x n_steps from arr.
    
    Arguments:
        arr: Array you want to make batches from
        n_seqs: Batch size, the number of sequences per batch
        n_steps: Number of sequence steps per batch
    '''
    
    batch_size = n_seqs * n_steps
    n_batches = len(arr)//batch_size
    arr = arr[:n_batches * batch_size] # Keep only enough characters to make full batches
    arr = arr.reshape((n_seqs, -1)) # Reshape into n_seqs rows
    for n in range(0, arr.shape[1], n_steps):
        x = arr[:, n:n+n_steps] # The features
        y = np.zeros_like(x) # The targets shifted by one
        try:
            y[:, :-1], y[:, -1] = x[:, 1:], arr[:, n+n_steps]
        except IndexError:
            y[:, :-1], y[:, -1] = x[:, 1:], arr[:, 0]
        yield x, y


def train(net, data, epochs=10, n_seqs=10, n_steps=50, lr=0.001, clip=5, val_frac=0.1, print_every=2):
        '''
        Training a network
        
        Arguments:
            net: CharRNN network
            data: text data to train the network
            epochs: Number of epochs to train
            n_seqs: Number of mini-sequences per mini-batch, or the batch size
            n_steps: Number of character steps per mini-batch
            lr: learning rate
            clip: gradient clipping
            val_frac: Fraction of data to hold out for validation
            print_every: Number of steps for printing training and validation loss
        '''
        
        net.train()
        opt = torch.optim.Adam(net.parameters(), lr=lr)
        criterion = nn.CrossEntropyLoss()
        
        # Seperate data into training and validation data
        val_idx = int(len(data)*(1-val_frac))
        data, val_data = data[:val_idx], data[val_idx:]
            
        counter = 0
        n_chars = len(net.chars)
        iterations = epochs - (epochs // print_every) # Required due to nature of code for printing training and validation loss
        
        for e in range(iterations):
            time.sleep(10) # Added for processing spread to stop overheating
            h = net.init_hidden(n_seqs)
            
            for x, y in get_batches(data, n_seqs, n_steps):
                counter += 1
                x = one_hot_encode(x, n_chars)
                inputs, targets = torch.from_numpy(x), torch.from_numpy(y) # Turn one-hot-encoded data into torch tensors
                
                h = tuple([each.data for each in h]) # New variables for the hidden state, else it would backpropagate through entire training history
                
                net.zero_grad() # Set gradients to zero
                
                output, h = net.forward(inputs, h) # Pass inputs through the CharRNN object
                
                loss = criterion(output, targets.view(n_seqs*n_steps).type(torch.LongTensor)) # Calculate the loss
                loss.backward() # Calculates gradients for each learnable parameter
                
                nn.utils.clip_grad_norm_(net.parameters(), clip) # Helps prevent the exploding gradient problem in RNNs /LSTMs.
                
                opt.step() # Updates learnable parameter based on gradient
                
                if counter % print_every == 0:
                    '''Get validation loss'''
                    val_h = net.init_hidden(n_seqs)
                    val_losses = []
                    for x, y in get_batches(val_data, n_seqs, n_steps):
                        x = one_hot_encode(x, n_chars)
                        x, y = torch.from_numpy(x), torch.from_numpy(y)
                        val_h = tuple([each.data for each in val_h])
                        inputs, targets = x, y
                        output, val_h = net.forward(inputs, val_h)
                        val_loss = criterion(output, targets.view(n_seqs*n_steps).type(torch.LongTensor))
                        val_losses.append(val_loss.item())
                    print('Epoch: {}/{}...'.format(e+1, epochs))
                    print('Step: {}...'.format(counter))
                    print('Loss: {:.4f}...'.format(loss.item()))
                    print('Val Loss: {:.4f}'.format(np.mean(val_losses)))


def trainNSaveRNN(dataset):
    '''Trains using *dataset* and saves trained network model'''

    # get text from file
    with open(r'Training_sets/{}'.format(dataset), "r") as importedtextfile:
        text = importedtextfile.read()

    '''
    encode text and map each character to an integer and vice versa
    create two dictionaries
    int2char, maps integers to characters
    char2int, maps characters to integers
    '''

    chars = tuple(set(text))
    int2char = dict(enumerate(chars))
    char2int = {ch: ii for ii, ch in int2char.items()}
    encoded = np.array([char2int[ch] for ch in text])


    # Delete existing network if one exists
    if 'net' in locals():
        del net

    # Get number of epochs
    invalid_epos = True
    while invalid_epos:
        try:
            print('Enter number of epochs:')
            epos = int(input(''))
            if epos >= 0:
                invalid_epos = False
            else:
                print('Number of epochs must be at least 0')
        except:
            print('Invalid number of epochs entered.')
            print('')
        
    model_name = 'ALIS_{}_{}.net'.format(dataset[:-4], epos) # Uses *dataset* and epochs chosen to form network model name 
    net = CharRNN(chars, n_hidden=512, n_layers=3) # Initialize the network
    n_seqs, n_steps = 128, 60 # Batchsize and character per mini-batch
    train(net, encoded, epochs=epos, n_seqs=n_seqs, n_steps=n_steps, lr=0.001, print_every=10)

    # Format in which network model is saved
    checkpoint = {'n_hidden': net.n_hidden,
                'n_layers': net.n_layers,
                'state_dict':net.state_dict(),
                'tokens': net.chars}

    # Saves the network
    with open(r'Nets/{}'.format(model_name), 'wb') as f:
        torch.save(checkpoint, f)

    print('{} saved in the \'Nets\' directory.'.format(model_name))