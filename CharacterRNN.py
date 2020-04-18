'''
    CharRNN class and one_hot_encode()
'''

import torch
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import time

def one_hot_encode(arr, n_labels):
    '''Returns the one-hot-encoded data'''
    one_hot = np.zeros((np.multiply(*arr.shape), n_labels), dtype=np.float32) # Initialize encoded array
    one_hot[np.arange(one_hot.shape[0]), arr.flatten()] = 1. # Fill appropriate elements with ones
    one_hot = one_hot.reshape((*arr.shape, n_labels)) # Reshape to get back to original array
    return one_hot

class CharRNN(nn.Module):
    
    def __init__(self, tokens, n_hidden, n_layers=3,
                drop_prob=0.5, lr=0.001):
        '''
        Initiates the CharRNN class
        
        Attributes:
            chars: Set of characters from training data
            n_hidden: number of hidden layers
            n_layers: number of stacked LSTM layers
            drop_prob: probability of zeroing out some input tensor elements
            lr: learning rate
            int2char: dictionary mapping integers to characters
            char2int: dictionary mapping characters to integers
            lstm: nn.LSTM object containing the LSTM layers
            dropout: dropout layer used for regularization and preventing the co-adaptation of neurons
            fc: final output layer

        '''
        super().__init__() # Initiates __init__() of nn.Module
        self.drop_prob = drop_prob
        self.n_layers = n_layers
        self.n_hidden = n_hidden
        self.lr = lr
        
        # Creating character dictionaries
        self.chars = tokens
        self.int2char = dict(enumerate(self.chars))
        self.char2int = {ch: ii for ii, ch in self.int2char.items()}
        

        # Initialise layers
        self.lstm = nn.LSTM(len(self.chars), n_hidden, n_layers,
                           dropout=drop_prob, batch_first=True)
        self.dropout = nn.Dropout(drop_prob) 
        self.fc = nn.Linear(n_hidden, len(self.chars))
        
        # Initialize the weights
        self.init_weights()
        
    def forward(self, x, hc):
        '''
        Forward pass through the network. x are the input, and the hidden/cell state is 'hc'.
        '''

        # Get x, and the new hidden state (h, c) from the lstm
        x, (h, c) = self.lstm(x, hc)
        
        # Pass x through dropout layer
        x = self.dropout(x)
        
        # Stack up LSTM outputs using view
        x = x.view(x.size()[0]*x.size()[1], self.n_hidden)
        
        # Put x through the fully connected layer
        x = self.fc(x)
        
        # Return x and the hidden state (h, c)
        return x, (h, c)
    
    def predict(self, char, h=None):
        '''
        Given a character, predict the next character. Returns the predicted character and the hidden state.
        '''

        if h is None:
            h = self.init_hidden(1)
        
        x = np.array([[self.char2int[char]]])
        x = one_hot_encode(x, len(self.chars))
        
        inputs = torch.from_numpy(x)
        
        h = tuple([each.data for each in h])
        out, h = self.forward(inputs, h)
        p = F.softmax(out, dim=1).data # Apply softmax to output tensor
        
        top_ch = np.arrange(len(self.chars))
        p = p.numpy().squeeze()
        char = np.random.choice(top_ch, p=p/p.sum()) # Choose prediction (implements a factor of randomness)
        
        return self.int2char[char], h
    
    def init_weights(self):
        '''initialise weights for fully connected layer'''
        initrange = 0.1
        
        # Set bias tensor to all zeros
        self.fc.bias.data.fill_(0)
        # FC weights as random uniform
        self.fc.weight.data.uniform_(-1, 1)
        
    def init_hidden(self, n_seqs):
        '''initialise hidden state'''
        # Create two new tensors with sizes n_layers x n_seqs x n_hidden,
        # initialised to zero, for hidden state and cell state of LSTM
        weight = next(self.parameters()).data
        return (weight.new(self.n_layers, n_seqs, self.n_hidden).zero_(),
                weight.new(self.n_layers, n_seqs, self.n_hidden).zero_())