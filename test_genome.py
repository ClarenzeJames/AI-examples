import unittest
import genome
import numpy as np

class GenomeTest(unittest.TestCase):
    def testClassExists(self):
        self.assertIsNotNone(genome.Genome)

    ## Code to test the random genome
    def testRandomGene(self):
        self.assertIsNotNone(genome.Genome.get_random_gene)

    def testGeneNotNone(self):
        self.assertIsNotNone(genome.Genome.get_random_gene(5))

    def testRandomGeneHasValue(self):
        gene = genome.Genome.get_random_gene(5)
        self.assertIsNotNone(gene[0])
    
    def testRandomGeneLength(self):
        gene = genome.Genome.get_random_gene(20)
        self.assertEqual(len(gene), 20)
    
    def testRandomGeneIsNumpyArray(self):
        gene = genome.Genome.get_random_gene(20)
        self.assertEqual(type(gene),np.ndarray)

    def testRandomGenomeExists(self):
        data = genome.Genome.get_random_genome(20,5)
        self.assertIsNotNone(data)

unittest.main()