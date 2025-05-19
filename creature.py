import genome

class Creature:
    def __init__(self,gene_count):
        self.spec = genome.Genome.get_gene_spec()
        self.dna = genome.Genome.get_random_genome(len(self.spec),gene_count)
        self.flat_links = None
        