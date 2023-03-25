
import numpy
import random

class Tournament(object):
    """ Modella un torneo che estrae dalla popolazione due candidati a caso, ne valuta la fitness e ritorna quello con fitness più elevata l'85% delle volte, quello con la fitness più bassa il 15% delle volte. """

    def __init__(self):
        return
        
    def compete(self, candidates):
        """ Sceglie a caso due candidati dalla popolazione """
        c1 = candidates[random.randint(0, len(candidates)-1)]
        c2 = candidates[random.randint(0, len(candidates)-1)]
        f1 = c1.fitness
        f2 = c2.fitness

        # Valuta chi dei due è il fittest e chi il weakest
        if(f1 > f2):
            fittest = c1
            weakest = c2
        else:
            fittest = c2
            weakest = c1

        selection_rate = 0.85
        r = random.uniform(0, 1.1)
        while(r > 1): 
            r = random.uniform(0, 1.1)
        if(r < selection_rate):
            return fittest
        else:
            return weakest
