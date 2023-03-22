# sudoku_genetic

Ci proponiamo di creare un programma che generi schemi di sudoku a varie difficoltà e, in seguito, riesca a risolvere tali schemi attraverso un algoritmo genetico. Il programma sarà in grado di generare e risolvere schemi di dimensione variabile.

Un algoritmo genetico è un tipo di euristica utilizzata solitamente per la risoluzione di problemi di tipo NP-Hard, che prende ispirazione dai processi biologici di selezione naturale e di evoluzione della specie. Infatti gli algoritmi genetici attuano dei meccanismi analoghi a quelli presenti in natura.

Il funzionamento di questo tipo di algoritmi è in sintesi il seguente: si parte da delle soluzioni casuali o pseudo-casuali (i primi individui della popolazione), questi vengono combinati (in analogia alla riproduzione sessuata) ed inoltre viene aggiunta, con una particolare probabilità, un elemento di disordine casuale (a rappresentare le mutazioni genetiche).

E' bene tenere presente che, nonostante l'applicazione di questi algoritmi a problemi di ottimizzazione combinatoria, la natura intrinsecamente casuale degli algoritmi genetici non permette di stabilire a priori se e in quanto tempo l'algoritmo troverà una soluzione accettabile.

Andiamo ora ad evidenziare delle specificità del problema del sudoku rispetto a questo tipo di approccio risolutivo. Innanzitutto và notato che uno schema di sudoku presenza una singola soluzione, e pertanto tutte le altre sono da considerarsi inaccettabili, e dunque uno dei primi problemi è quello di creare una funzione di fitness adeguata. In questa implementazione è stata utilizzata una metrica che utilizza il numero di errori presenti nella soluzione di tentativo, man mano che gli errori diminuiscono la fitness function si avvicina al valore 1, ottenibile solamente con la soluzione corretta e che quindi farà terminare l'esecuzione.

## Esecuzione

Per eseguire questo programma bisogna eseguire il comando `python3 sudoku_generator.py`
E' consigliato eseguirlo in un python venv come di seguito
```
python3 -m venv .
source ./bin/activate
pip install numpy
python3 sudoku_generator.py
```

## Requisiti

python 3.7+</br>
numpy
