import creature
import unittest
import numpy as np

class TestCreature(unittest.TestCase):
    def testCreatureExists(self):
        self.assertIsNotNone(creature.Creature)

unittest.main()