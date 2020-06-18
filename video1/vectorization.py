import numpy as np
import re
from struct import *
from binascii import crc32
from itertools import product

class vectorizeString(object):
    def __init__(self):
        self.dictionary = list('abcdefghijklmnopqrstuvwxyz')
        self.featuresspace = np.array([crc32(x) for x in ["".join(comb) for comb in product(self.dictionary, repeat=3)]])
        pass

    def generate_vector(self, element):
        element = self.preprocess(element)
        trigrams = self.get_trigrams(element)
        element_vector = self.vectorize_element(trigrams, self.featuresspace)
        return element_vector
    
    def vectorize_element(self, trigrams, featurespace):
        vec = np.zeros(featurespace.shape[0])
        i = 1
        for component in trigrams:
            vec[np.where(featurespace==component)]==i
            i+=1
        return vec
    
    def get_trigrams(self, element):
        nlength = len(element)
        return np.array([crc32(element[i: (i+3)]) for i in xrange(nlength-3+1)])
    
    
    def preprocess(self, element):
        return re.sub('[a-zA-Z]', '', elemeny.lower()).ljust(3)
