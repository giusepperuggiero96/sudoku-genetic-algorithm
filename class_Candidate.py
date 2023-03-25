import numpy
import random

Nd = 9 # Numero di celle (nel caso del sudoku standard sono 9)

class Candidate(object):
    """ Modella una soluzione candidato dello schema di sudoku """
    def __init__(self):
        self.values = numpy.zeros((Nd, Nd), dtype=int)
        self.fitness = 0
        return

    def update_fitness(self):
        """ La fitness di una soluzione candidata è determinata da quanto tale soluzione è "vicina" ad essere la vera soluzione dello schema. La vera soluzione è una griglia 9x9 di numeri appartenenti all'insieme [1, 9] nella quale ciascuna riga, ciascuna colonna e ciascun blocco 3x3 contengono tutte le cifre in [1, 9] senza alcun duplicato. Se il candidato contiene dei duplicati allora la sua fitness sarà <1 """
        row_count = numpy.zeros(Nd)
        column_count = numpy.zeros(Nd)
        block_count = numpy.zeros(Nd)
        row_sum = 0
        column_sum = 0
        block_sum = 0

        for i in range(0, Nd):  # Per ogni riga
            for j in range(0, Nd):  # Per ogni casella nella riga
                row_count[self.values[i][j]-1] += 1  # conta le occorrenze di quel particolare valore     

            row_sum += (1.0/len(set(row_count)))/Nd # row_sum aggiunge 1/9 ogni volta che una cifra è presente (non considera i duplicati, quindi se la riga contiene tutte le cifre row_sum è 1, altrimenti è <1 multipla di 1/9)
            row_count = numpy.zeros(Nd)

        for i in range(0, Nd):  # Per ogni colonna
            for j in range(0, Nd):  # per ogni casella nella colonna
                column_count[self.values[j][i]-1] += 1  # conta le occorrenze di quel particolare valore   

            column_sum += (1.0 / len(set(column_count)))/Nd # column_sum aggiunge 1/9 ogni volta che una cifra è presente
            column_count = numpy.zeros(Nd)


        # Per ciascun blocco
        for i in range(0, Nd, 3):
            for j in range(0, Nd, 3):
                block_count[self.values[i][j]-1] += 1
                block_count[self.values[i][j+1]-1] += 1
                block_count[self.values[i][j+2]-1] += 1
                
                block_count[self.values[i+1][j]-1] += 1
                block_count[self.values[i+1][j+1]-1] += 1
                block_count[self.values[i+1][j+2]-1] += 1
                
                block_count[self.values[i+2][j]-1] += 1
                block_count[self.values[i+2][j+1]-1] += 1
                block_count[self.values[i+2][j+2]-1] += 1

                block_sum += (1.0/len(set(block_count)))/Nd # block_sum aggiunge 1/9 ogni volta che una cifra è presente
                block_count = numpy.zeros(Nd)

        # Calcola la fitness come column_sum * block_sum (row_sum è 1 perchè è la condizione di generazione di un candidate nel seeding)
        if (int(row_sum) == 1 and int(column_sum) == 1 and int(block_sum) == 1):
            fitness = 1.0
        else:
            fitness = column_sum * block_sum
        
        self.fitness = fitness
        return
        
    def mutate(self, mutation_rate, given):
        """ Effettua una mutazione su una soluzione candidata scegliendo casualmente due caselle e ne scambia il valore """

        # Scelgo secondo una distribuzione uniforme un numero tra 0 e 1
        r = random.uniform(0, 1.1)
        while(r > 1): 
            r = random.uniform(0, 1.1)
    
        success = False
        if (r < mutation_rate):  # Se r è minore del tasso di mutazione allora effettuo la mutazione (maggiore è mutation_rate più frequentemente la mutazione avviene)
            while(not success):
                row1 = random.randint(0, 8)
                row2 = random.randint(0, 8)
                row2 = row1
                
                from_column = random.randint(0, 8)
                to_column = random.randint(0, 8)
                while(from_column == to_column):
                    from_column = random.randint(0, 8)
                    to_column = random.randint(0, 8)   

                # Controlla se le due caselle erano vuote nello schema di partenza
                if(given.values[row1][from_column] == 0 and given.values[row1][to_column] == 0):
                    # e che non stiamo generando uno schema invalido con la mutazione
                    if(not given.is_column_duplicate(to_column, self.values[row1][from_column])
                       and not given.is_column_duplicate(from_column, self.values[row2][to_column])
                       and not given.is_block_duplicate(row2, to_column, self.values[row1][from_column])
                       and not given.is_block_duplicate(row1, from_column, self.values[row2][to_column])):
                    
                        # Scambia i valori
                        temp = self.values[row2][to_column]
                        self.values[row2][to_column] = self.values[row1][from_column]
                        self.values[row1][from_column] = temp
                        success = True
    
        return success
