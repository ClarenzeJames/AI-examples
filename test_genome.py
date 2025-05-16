import unittest
import genome
import numpy as np

class GenomeTest(unittest.TestCase):
    def testClassExists(self):
        self.assertIsNotNone(genome.Genome)

unittest.main()