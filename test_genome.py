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

    # Gene spec things

    def testGeneSpecScale(self):
        spec = genome.Genome.get_gene_spec()
        gene = genome.Genome.get_random_gene(20)
        self.assertGreater(gene[spec["link-length"]["ind"]],0)

    # test for gene and genome to dict

    def testGeneToGeneDict(self):
        spec = genome.Genome.get_gene_spec()
        gene  = genome.Genome.get_random_gene(len(spec))
        gene_dict = genome.Genome.get_gene_dict(gene,spec)
        # print(gene_dict)
        self.assertIn("link-recurrence",gene_dict)

    def testGenomeToDict(self):
        spec = genome.Genome.get_gene_spec()
        dna  = genome.Genome.get_random_genome(len(spec),3)
        genome_dicts = genome.Genome.get_genome_dicts(dna,spec)
        # print(genome_dicts)
        self.assertEqual(len(genome_dicts),3)

    # test for the expanded links
    def testExpandLinks(self):
        links = [
            genome.URDFLink(name="A",parent_name="None",recur=1),
            genome.URDFLink(name="B",parent_name="A",recur=1),
            genome.URDFLink(name="C",parent_name="B",recur=2),
            genome.URDFLink(name="D",parent_name="C",recur=1)
        ]

        exp_links = [links[0]]

        genome.Genome.expandLinks(links[0], links[0].name,links, exp_links)
        names = [l.name+"-parent-is-"+l.parent_name for l in exp_links]
        print(names)
        self.assertEqual(len(exp_links), 6)


unittest.main()