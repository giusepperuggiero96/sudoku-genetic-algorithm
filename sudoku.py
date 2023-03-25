from class_Candidate import *
from class_Population import *
from class_Given import *
from class_Tournament import *
from class_CycleCrossover import *
from class_Sudoku import *
import sudoku_generator


sudoku_generator.createGrid()
print("\nRisolvo la griglia appena creata..\n")
import numpy
import random
random.seed()
     
s = Sudoku()
s.load("puzzle_mild.txt")
solution = s.solve()
if(solution):
    s.save("solution.txt", solution)


