import unittest
import population as poplib
import simulation as simlib
import creature as crlib
import genome as genlib
import numpy as np

# The Genetic algorithm

class TestGA(unittest.TestCase):

    def testGA(self):
        # Generate random population
        pop = poplib.Population(pop_size=10,gene_count=3)
        sim = simlib.Simulation()

        # iterating through how ever many generations
        for generation in range(20):
            # Evaluate
            sim.eval_population(pop,2400)

            # Get fitness and fitness map data structures
            fits = [cr.get_distance_travelled() for cr in pop.creatures]
            fitmap = poplib.Population.get_fitness_map(fits)

            print(generation, np.max(fits), np.mean(fits))

            # Keeping the fittest
            fmax = np.max(fits)
            for cr in pop.creatures:
                if cr.get_distance_travelled() == fmax:
                    elite = cr
                    break

            # Making new generations
            new_gen = []
            
            # for each new creature
            for cid in range(len(pop.creatures)):
                # Select parents
                p1_ind = poplib.Population.select_parent(fitmap)
                p2_ind = poplib.Population.select_parent(fitmap)

                # Make new DNA via crossover
                dna = genlib.Genome.crossover(pop.creatures[p1_ind].dna, 
                                            pop.creatures[p2_ind].dna)
                
                # Mutate
                dna = genlib.Genome.point_mutate(dna, 0.1, 0.25)
                dna = genlib.Genome.grow_mutate(dna, 0.25)
                dna = genlib.Genome.shrink_mutate(dna, 0.25)

                # make new creature with DNA
                cr = crlib.Creature(1)
                cr.set_dna(dna)
                new_gen.append(cr)
            
            new_gen[0] = elite
            pop.creatures = new_gen
            
unittest.main()