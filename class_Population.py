from class_Candidate import *

import numpy
import random
from functools import cmp_to_key

Nd = 9 # Number of digits (in the case of standard Sudoku puzzles, this is 9).

class Population(object):
    """ A set of candidate solutions to the Sudoku puzzle. These candidates are also known as the chromosomes in the population. """

    def __init__(self):
        self.candidates = []
        return

    def seed(self, Nc, given):
        self.candidates = []
        
        # Determine the legal values that each square can take.
        helper = Candidate()
        helper.values = [[[] for j in range(0, Nd)] for i in range(0, Nd)]
        for row in range(0, Nd):
            for column in range(0, Nd):
                for value in range(1, 10):
                    if((given.values[row][column] == 0) and not (given.is_column_duplicate(column, value) or given.is_block_duplicate(row, column, value) or given.is_row_duplicate(row, value))):
                        # Value is available.
                        helper.values[row][column].append(value)
                    elif(given.values[row][column] != 0):
                        # Given/known value from file.
                        helper.values[row][column].append(given.values[row][column])
                        break

        # Seed a new population.       
        for p in range(0, Nc):
            g = Candidate()
            for i in range(0, Nd): # New row in candidate.
                row = numpy.zeros(Nd)
                
                # Fill in the givens.
                for j in range(0, Nd): # New column j value in row i.
                
                    # If value is already given, don't change it.
                    if(given.values[i][j] != 0):
                        row[j] = given.values[i][j]
                    # Fill in the gaps using the helper board.
                    elif(given.values[i][j] == 0):
                        row[j] = helper.values[i][j][random.randint(0, len(helper.values[i][j])-1)]

                # If we don't have a valid board, then try again. There must be no duplicates in the row.
                while(len(list(set(row))) != Nd):
                    for j in range(0, Nd):
                        if(given.values[i][j] == 0):
                            row[j] = helper.values[i][j][random.randint(0, len(helper.values[i][j])-1)]

                g.values[i] = row

            self.candidates.append(g)
        
        # Compute the fitness of all candidates in the population.
        self.update_fitness()
        
        print("Seeding complete.")
        
        return
        
    def update_fitness(self):
        """ Update fitness of every candidate/chromosome. """
        for candidate in self.candidates:
            candidate.update_fitness()
        return
        
    def sort(self):
        """ Sort the population based on fitness. """
        self.candidates = sorted(self.candidates, key=lambda x: x.fitness)
        return

    # Obsoleta
    def sort_fitness(self, x, y):
        """ The sorting function. """
        if(x.fitness < y.fitness):
            return 1
        elif(x.fitness == y.fitness):
            return 0
        else:
            return -1
