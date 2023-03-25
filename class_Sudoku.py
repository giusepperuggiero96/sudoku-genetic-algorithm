from class_Given import *
from class_Tournament import *
from class_Population import *
from class_CycleCrossover import *
import numpy
import random

Nd = 9 # Numero di celle (nel caso del sudoku standard sono 9)

class Sudoku(object):
    """ Solves a given Sudoku puzzle using a genetic algorithm. """

    def __init__(self):
        self.given = None
        return
    
    def load(self, path):
        # Carica uno schema da risolvere
        with open(path, "r") as f:
            values = numpy.loadtxt(f).reshape((Nd, Nd)).astype(int)
            self.given = Given(values)
        return

    def save(self, path, solution):
        # Salva uno schema su file
        with open(path, "w") as f:
            numpy.savetxt(f, solution.values.reshape(Nd*Nd), fmt='%d')
        return
        
    def solve(self):
        Nc = 1000  # Numero di soluzioni candidate (quindi dimensione della popolazione)
        Ne = int(0.05*Nc)  # Dimensione della popolazione d'elite (5%)
        Ng = 1000  # Numero di generazioni massimo
        Nm = 0  # Numero di mutazioni
        
        # Parametri di mutazione
        phi = 0
        sigma = 1   # Deviazione standard
        mutation_rate = 0.06   # Tasso di mutazione
    
        # Crea una popolazione iniziale a partire dallo schema parziale fornito
        self.population = Population()
        self.population.seed(Nc, self.given)
    
        stale = 0   # Parametro che ci permette di capire se siamo in una situazione di stallo

        # Itera fino a Ng volte (generazioni)
        for generation in range(0, Ng):
        
            print("Generazione %d" % generation)
            
            # Controlla se nella popolazione attuale abbiamo una soluzione
            best_fitness = 0.0
            for c in range(0, Nc):
                fitness = self.population.candidates[c].fitness
                if(fitness == 1):
                    print("\nSoluzione trovata alla generazione %d!\n" % generation)
                    for i in range(0, 9):
                        print(str(self.population.candidates[c].values[i][0:3]) + "  " + str(self.population.candidates[c].values[i][3:6]) + "  " + str(self.population.candidates[c].values[i][6:9]))
                        if not((i+1)%3):
                           print("")
                    return self.population.candidates[c]

                # Contestualmente tiene traccia della migliore fitness
                if(fitness > best_fitness):
                    best_fitness = fitness

            print("Best fitness: %f" % best_fitness)

            # Inizia il processo di creazione di una nuova popolazione
            next_population = []

            # Ordina la popolazione in base alla fitness e seleziona le Ne elites che verranno mantenute intatte nella prossima generazione
            self.population.sort()
            elites = []
            for e in range(0, Ne):
                elite = Candidate()
                elite.values = numpy.copy(self.population.candidates[e].values)
                elites.append(elite)

            # Crea il resto della popolazione
            # Per (Nc-Ne)/2 volte
            for count in range(Ne, Nc, 2):
                # Seleziona due genitori a partire da due tornei
                t = Tournament()
                parent1 = t.compete(self.population.candidates)
                parent2 = t.compete(self.population.candidates)
                # Effettua il crossover e ottiene le due soluzioni figlie
                cc = CycleCrossover()
                child1, child2 = cc.crossover(parent1, parent2, crossover_rate=1.0)
                # Effettua (o non effettua) la mutazione sul figlio 1
                old_fitness = child1.fitness
                success = child1.mutate(mutation_rate, self.given)
                child1.update_fitness()
                if(success):
                    Nm += 1
                    if(child1.fitness > old_fitness):  # Se c'è stata una mutazione e tale mutazione ha aumentato la fitness dell'individuo aumento il valore di phi
                        phi = phi + 1
                
                # Effettua (o non effettua) la mutazione sul figlio 1
                old_fitness = child2.fitness
                success = child2.mutate(mutation_rate, self.given)
                child2.update_fitness()
                if(success):
                    Nm += 1
                    if(child2.fitness > old_fitness):  # Se c'è stata una mutazione e tale mutazione ha aumentato la fitness dell'individuo aumento il valore di phi
                        phi = phi + 1
                
                # Aggiungo i due figli alla popolazione
                next_population.append(child1)
                next_population.append(child2)

            # Aggiungo infine le elite alla nuova popolazione
            for e in range(0, Ne):
                next_population.append(elites[e])
                
            # La nuova popolazione sostituisce la vecchia e ne calcola la nuova fitness
            self.population.candidates = next_population
            self.population.update_fitness()
            
            # Calcola il nuovo tasso di mutazione adattativo (si basa sulla regola del 20% di successi di Rechenberg). Questo avviene al fine di evitare troppe mutazioni man mano che la fitness sale verso l'unità
            if(Nm == 0):
                phi = 0  # Se non ci sono state mutazioni qui evita una divisione per zero
            else:
                phi = phi / Nm
            
            # Se le mutazioni hanno portato benefici più del 20% delle volte aumento il valore di sigma dello 0.2%
            if(phi > 0.2):
                sigma = sigma/0.998
            # altrimenti lo abbasso dello stesso valore
            elif(phi < 0.2):
                sigma = sigma*0.998

            # Calcolo il nuovo tasso di mutazione
            # Se sigma è aumentata la campana si allarga e posso ottenere con più probabilità valori più lontani da zero, quindi in sostanza aumento la probabilità di tassi di mutazione più elevati
            mutation_rate = abs(numpy.random.normal(loc=0.0, scale=sigma, size=None))
            Nm = 0
            phi = 0

            # Controlla se la popolazione è in stallo
            self.population.sort()
            if(self.population.candidates[0].fitness != self.population.candidates[1].fitness):
                stale = 0
            else:
                stale += 1

            # Se la popolazione è in stallo da più di 100 generazioni faccio un nuovo seed della popolazione
            if(stale >= 100):
                print("La popolazione e' in fase di stallo. Provo a ricreare...\n")
                self.population.seed(Nc, self.given)
                stale = 0
                sigma = 1
                phi = 0
                Nm = 0
                mutation_rate = 0.06
        
        print("Attenzione : non e' stata trovata soluzione.\n")
        return None
