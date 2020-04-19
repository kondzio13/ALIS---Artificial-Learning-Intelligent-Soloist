'''
    Extra functions to do with generating MIDI message representative text
'''

import torch
import numpy as np
from Modules.CharacterRNN import CharRNN


def generateFromNet(net_name):
    '''Loads the network model with name *net_name* and returns a sample produced by the model'''

    check = torch.load(r'Nets/{}'.format(net_name))
    net = CharRNN(check['tokens'], check['n_hidden'], check['n_layers'])
    net.load_state_dict(check['state_dict'])

    return sample(net, 1500)

def sample(net, size, prime='### '):
    '''Returns a sample of text generated by *net* of size *size* and starting with *prime*'''
    
    net.eval() # Sets dropout layer to 'eval' mode.
    
    chars = [ch for ch in prime] # Run through *prime* characters
    
    h = net.init_hidden(1)
    
    for ch in prime:
        char, h = net.predict(ch, h)
    
    chars.append(char)
    
    # Keep passing in previous character and getting predictions.
    for ii in range(size):
        
        char, h = net.predict(chars[-1], h)
        chars.append(char)
    
    return ''.join(chars)