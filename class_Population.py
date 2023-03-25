from class_Candidate import *

import numpy
import random
from functools import cmp_to_key

Nd = 9 # Numero di celle (nel caso del sudoku standard sono 9)

class Population(object):
    """ Un insieme di soluzioni candidate per il sudoku. Queste soluzioni candidtato sono anche dette i "cromosomi" della popolazione """

    def __init__(self):
        self.candidates = []
        return

    def seed(self, Nc, given):
        self.candidates = []
        
        # Determina i valori legali che ciascuna casella vuota dello schema di partenza può contenere
        helper = Candidate()
        helper.values = [[[] for j in range(0, Nd)] for i in range(0, Nd)]
        for row in range(0, Nd):
            for column in range(0, Nd):
                for value in range(1, 10):
                    if((given.values[row][column] == 0) and not (given.is_column_duplicate(column, value) or given.is_block_duplicate(row, column, value) or given.is_row_duplicate(row, value))):
                        # Se la casella è vuota e la cifra non è duplicato nè di colonna, nè di riga, nè di blocco, allora è la cifra è un valore legale
                        helper.values[row][column].append(value)
                    elif(given.values[row][column] != 0):
                        # Se la casella non è vuota 
                        helper.values[row][column].append(given.values[row][column])
                        break

        # Crea una nuova popolazione 
        for p in range(0, Nc):
            # Per ogni iterazione crea una soluzione candidata inizialmente vuota
            g = Candidate()
            for i in range(0, Nd): # Per ogni riga
                row = numpy.zeros(Nd)
                
                # Riempie la soluzione candidata
                for j in range(0, Nd): # per ogni colonna
                
                    # Se la casella della soluzione iniziale non è vuota la inserisco as-is
                    if(given.values[i][j] != 0):
                        row[j] = given.values[i][j]
                    # Altrimenti inserisco un valore casuale tra quelli legali che ho immagazzinato nella variabile helper
                    elif(given.values[i][j] == 0):
                        row[j] = helper.values[i][j][random.randint(0, len(helper.values[i][j])-1)]

                # Ritenta l'inserimento finchè la riga non è valida e quindi non contiene duplicati
                while(len(list(set(row))) != Nd):
                    for j in range(0, Nd):
                        if(given.values[i][j] == 0):
                            row[j] = helper.values[i][j][random.randint(0, len(helper.values[i][j])-1)]

                g.values[i] = row

            self.candidates.append(g)
        
        # Calcola la fitness di tutti i candidati nella popolazione
        self.update_fitness()
        
        print("Seeding complete.")
        
        return
        
    def update_fitness(self):
        """ Ricalcola la fitness di tutti i candidati nella popolazione """
        for candidate in self.candidates:
            candidate.update_fitness()
        return
        
    def sort(self):
        """ Ordina la popolazione sulla base della fitness """
        self.candidates = sorted(self.candidates, key=lambda x: x.fitness)
        return
