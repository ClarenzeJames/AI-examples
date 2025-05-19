import creature
import unittest
import numpy as np

class TestCreature(unittest.TestCase):
    def testCreatureExists(self):
        self.assertIsNotNone(creature.Creature)

    def testCreateGetFlatLinks(self):
        c = creature.Creature(gene_count=3)
        links = c.get_flat_links()
        self.assertEqual(len(links),3)
    
    def testExpLinks(self):
        c = creature.Creature(gene_count=4)
        links = c.get_flat_links()
        exp_links = c.get_expanded_links()
        self.assertGreaterEqual(len(exp_links),len(links))

     # to XML
    def testLoadXML(self):
        c = creature.Creature(gene_count=4)
        xml_str = c.to_xml()
        with open("test.urdf","w") as f:
            f.write('<?xml version="1.0"?>' + "\n" + xml_str)
        self.assertIsNotNone(xml_str)

unittest.main()