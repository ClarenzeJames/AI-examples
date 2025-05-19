import genome
from xml.dom.minidom import getDOMImplementation

class Creature:
    def __init__(self,gene_count):
        self.spec = genome.Genome.get_gene_spec()
        self.dna = genome.Genome.get_random_genome(len(self.spec),gene_count)

    def get_flat_links(self):
        genome_dicts = genome.Genome.get_genome_dicts(self.dna,self.spec)
        self.flat_links = genome.Genome.genome_to_links(genome_dicts)
        return self.flat_links

    def get_expanded_links(self):
        self.get_flat_links()
        # print(len(self.get_flat_links()))
        exp_links = []
        genome.Genome.expandLinks(self.flat_links[0], 
                                  self.flat_links[0].name,
                                  self.flat_links, 
                                  exp_links)
        self.exp_links = exp_links
        # print(len(self.exp_links))
        return self.exp_links
    
    # to XML function
    def to_xml(self):
        self.get_expanded_links()
        domimpl = getDOMImplementation()
        adom = domimpl.createDocument(None, "start", None)
        robot_tag = adom.createElement("robot")
        for link in self.exp_links:
            print(link)
            robot_tag.appendChild(link.to_link_ele(adom))
        first = True
        for lin in self.exp_links:
            if first:
                first = False
                continue
            robot_tag.appendChild(lin.to_joint_ele(adom))
        robot_tag.setAttribute("name","pepe")

        comp_xml = '<?xml version="1.0"?>' + "\n" + robot_tag.toprettyxml()
        return comp_xml
