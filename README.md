# Fish Pond

A complex Genetic Algorithm Simulation built from scratch using Python and Pygame. I did this project to simulate an ecosystem where fishes (preys) eolves survival strategies to escape the shark (predator) using flocking behaviours, vector physics, and Genetic Algorithm.

![Simulation GIF](/Documentation/fishpond.gif)

## How it works ?

- **Fish** : use flocking rules (such as alignments, separation, cohesion) to move together in group (nature)
- **Shark** : hunts fishes using a vision cone and chases them if they get too close.
- **Evolution** : fishes that survives longer pass their genes (speed, vision, etc.) to the next generation

Read more : [Fishpond Main Documentation (PDF)](/Documentation/FishPond.pdf)
## How to run ?

1. Install the dependancies :
```bash
pip install pygame numpy
```

2. Run 
```bash
python main.py ( for windows)

python3 main.py ( for linux)
```

## files
- `main.py`: main simulation loop and graphing (run this)
- `agents.py` : contains FISH and SHARK logic
- `genetic_algorithm.py` : Handles Evolution (crossover, mutation, etc.)
- `variables.py` : settings and configuration (such as screen size, population count , etc.)

## Reults image 

![Result of More iterations](/Documentation/fishpond.png)

## Author 
Vitthal Humbe (Kuron)