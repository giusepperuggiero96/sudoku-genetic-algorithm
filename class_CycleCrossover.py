from class_Candidate import *
import numpy
import random

Nd = 9 # Numero di celle (nel caso del sudoku standard sono 9)

class CycleCrossover(object):
    """ Il crossover modella l'analogia del mixing dei geni tra i candidati genitori al fine di creare un candidato figlio a fitness più elevata. Qui usiamo il cyclecrossover ( A. E. Eiben, J. E. Smith. Introduction to Evolutionary Computing. Springer, 2007) """

    def __init__(self):
        return
    
    def crossover(self, parent1, parent2, crossover_rate):
        """ Crea due candidati figli a partire dai genitori """
        child1 = Candidate()
        child2 = Candidate()
        
        # Inizializza i figli con i geni dei genitori
        child1.values = numpy.copy(parent1.values)
        child2.values = numpy.copy(parent2.values)

        r = random.uniform(0, 1.1)
        while(r > 1):
            r = random.uniform(0, 1.1)
            
        # Effettua il crossover (il parametro crossover_rate è sempre 1 in questa implementazione)
        if (r < crossover_rate):
            # Sceglie casualmente due punti di crossover
            crossover_point1 = random.randint(0, 8)
            crossover_point2 = random.randint(1, 9)
            while(crossover_point1 == crossover_point2):
                crossover_point1 = random.randint(0, 8)
                crossover_point2 = random.randint(1, 9)
                
            if(crossover_point1 > crossover_point2):
                temp = crossover_point1
                crossover_point1 = crossover_point2
                crossover_point2 = temp
                
            # Effettua il crossover delle righe nel range tra i due punti
            for i in range(crossover_point1, crossover_point2):
                child1.values[i], child2.values[i] = self.crossover_rows(child1.values[i], child2.values[i])

        return child1, child2

    def crossover_rows(self, row1, row2): 
        child_row1 = numpy.zeros(Nd)
        child_row2 = numpy.zeros(Nd)

        remaining = list(range(1, Nd+1))
        cycle = 0
        
        while((0 in child_row1) and (0 in child_row2)):  # Fintantochè rimangono spazi vuoti nelle righe
            if(cycle % 2 == 0):  # Cicli pari
                # Assegna il valore vuoto successivo
                index = self.find_unused(row1, remaining)
                start = row1[index]
                remaining.remove(row1[index])
                child_row1[index] = row1[index]
                child_row2[index] = row2[index]
                next = row2[index]
                
                while(next != start):  # Fintantochè non termina
                    index = self.find_value(row1, next)
                    child_row1[index] = row1[index]
                    remaining.remove(row1[index])
                    child_row2[index] = row2[index]
                    next = row2[index]

                cycle += 1

            else:  # Ciclo dispari - scambia i valori
                index = self.find_unused(row1, remaining)
                start = row1[index]
                remaining.remove(row1[index])
                child_row1[index] = row2[index]
                child_row2[index] = row1[index]
                next = row2[index]
                
                while(next != start):  # Fintantochè non termina
                    index = self.find_value(row1, next)
                    child_row1[index] = row2[index]
                    remaining.remove(row1[index])
                    child_row2[index] = row1[index]
                    next = row2[index]
                    
                cycle += 1
            
        return child_row1, child_row2  
           
    def find_unused(self, parent_row, remaining):
        for i in range(0, len(parent_row)):
            if(parent_row[i] in remaining):
                return i

    def find_value(self, parent_row, value):
        for i in range(0, len(parent_row)):
            if(parent_row[i] == value):
                return i
