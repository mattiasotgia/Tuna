
import glob
import sys

import numpy as np
from tuna.utils.helpers import create_logger

from tqdm import tqdm

class DatasetLoader:

    def __init__(self,
                 training_features: np.ndarray,
                 training_labels: np.ndarray,
                 shuffle = True,
                 split = 0.8, 
                 ):
        self.features = training_features
        self.labels = training_labels
        self.shuffle = shuffle
        self.split = split

    @classmethod
    def load_csv(cls, path: str, skip_first: int = 1, equalize_populations = False, split = 1, shuffle = True) -> 'DatasetLoader':

        length_of_csv = 0

        __files = glob.glob(path)
        
        if not __files:
            create_logger(__name__).error('Empty list? Check import...')
            sys.exit(2)
        
        try:
            with open(__files[0], 'r') as __f0:
                length_of_csv = len(__f0.readlines()[0].split(','))
        except FileNotFoundError:
            create_logger(__name__).error('File path not found\n%s', __files[0])
            sys.exit(2)
        except Exception as e:
            create_logger(__name__).error(e)
            sys.exit(2)
        
        __tmp = []
        
        print('Loading dataset...')
        for __f in tqdm(__files):
            try:
                __tmp_loadtxt = np.loadtxt(__f, delimiter=',', usecols=range(skip_first, length_of_csv))
                __tmp.append(__tmp_loadtxt)
            except Exception as e:
                create_logger(__name__).error('Having some problems with a file...\n%s\n%s', __f, e) 

        __tmp = np.concatenate(__tmp)

        ## Randomize the loaded order
        if shuffle: 
            order = np.random.permutation(__tmp[:,-1].size)
            __tmp = __tmp[order]

        training_features = __tmp[:,0:-1]
        training_labels = __tmp[:,-1]
        
        ## TODO:
        ##  - Missing equalization
        
        if equalize_populations:
            pass


        return cls(training_features=training_features,
                   training_labels=training_labels,
                   shuffle=shuffle,
                   split=split)
