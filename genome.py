import numpy as np
import copy

class Genome():
    def __init__(self):
        pass

    @staticmethod
    def get_random_gene(length):
        gene = np.array([np.random.random() for i in range(length)])
        return gene
    
    @staticmethod
    def get_random_genome(gene_length, gene_count):
        genome = [Genome.get_random_gene(gene_length) for i in range(gene_count)]
        return genome
    
    @staticmethod
    def get_gene_spec():
        gene_spec ={
            "link_length":{"scale":1},
            "link_shape":{"scale":1},
            "link_radius":{"scale":1},
            "link_recurrence":{"scale":1},
            "link_mass":{"scale":4},
            "joint_type":{"scale":1},
            "joint_parent":{"scale":1},
            "joint_axis_xyz":{"scale":1},
            "joint_origin_rpy_1":{"scale":np.pi * 2},
            "joint_origin_rpy_2":{"scale":np.pi * 2},
            "joint_origin_rpy_3":{"scale":np.pi * 2},
            "joint_origin_xyz_1":{"scale":1},
            "joint_origin_xyz_2":{"scale":1},
            "joint_origin_xyz_3":{"scale":1},
            "control_waveform":{"scale":1},
            "control_amp":{"scale":0.25},
            "control_freq":{"scale":1}
        }
        ind = 0
        for key in gene_spec.keys():
            gene_spec[key]["ind"] = ind
            ind = ind + 1
        return gene_spec
    
    # To dictionary

    @staticmethod
    def get_gene_dict(gene,spec):
        gdicts = {}
        for key in spec:
            ind = spec[key]['ind']
            scale = spec[key]['scale']
            gdicts[key] = gene[ind] * scale
        return gdicts
    
    @staticmethod
    def get_genome_dicts(genome,spec):
        gdicts = []
        for gene in genome:
            gdicts.append(Genome.get_gene_dict(gene,spec))
        return gdicts
    
    # expand the links into graph
    @staticmethod
    def expandLinks(parent_link, unique_parent_name, flat_links, exp_links):
        children = [l for l in flat_links if l.parent_name == parent_link.name]
        
        for child in children:
            for r in range(child.link_recurrence):
                child_copy = copy.copy(child)
                child_copy.parent_name = unique_parent_name
                uniq_name = child_copy.name + str(len(exp_links))
                child_copy.name = uniq_name
                exp_links.append(child_copy)
                Genome.expandLinks(child, uniq_name, flat_links, exp_links)

    # Genome to links
    @staticmethod
    def genome_to_links(genome_dicts):
        links = []
        link_ind = 0
        parent_names = [str(link_ind)]
        for gdict in genome_dicts:
            link_name = str(link_ind)
            parent_ind = gdict["joint_parent"] * len(parent_names)
            parent_name = parent_names[int(parent_ind)]
            recur = gdict["link_recurrence"]
            link = URDFLink(name=link_name,
                            parent_name = parent_name,
                            link_recurrence = recur + 1,
                            link_length = gdict["link_length"],
                            link_radius = gdict["link_radius"],
                            link_mass = gdict["link_mass"],
                            joint_type = gdict["joint_type"],
                            joint_parent = gdict["joint_parent"],
                            joint_axis_xyz = gdict["joint_axis_xyz"],
                            joint_origin_rpy_1 = gdict["joint_origin_rpy_1"],
                            joint_origin_rpy_2 = gdict["joint_origin_rpy_2"],
                            joint_origin_rpy_3 = gdict["joint_origin_rpy_3"],
                            joint_origin_xyz_1 = gdict["joint_origin_xyz_1"],
                            joint_origin_xyz_2 = gdict["joint_origin_xyz_2"],
                            joint_origin_xyz_3 = gdict["joint_origin_xyz_3"],
                            control_waveform = gdict["control_waveform"],
                            control_amp = gdict["control_amp"],
                            control_freq = gdict["control_freq"]
            )
            links.append(link)
            if link_ind != 0: # don't re-add the first link
                parent_names.append(link_name)
            link_ind = link_ind + 1
        
        links[0].parent_name = "None"
        return links

class URDFLink:
    def __init__(self, name, parent_name, link_recurrence, link_length=0.1, link_radius=0.1, link_mass=0.1,
                 joint_type=0.1, joint_parent=0.1, joint_axis_xyz=0.1, joint_origin_rpy_1=0.1, joint_origin_rpy_2=0.1, joint_origin_rpy_3=0.1,
                 joint_origin_xyz_1=0.1, joint_origin_xyz_2=0.1, joint_origin_xyz_3=0.1,
                 control_waveform=0.1, control_amp=0.1, control_freq=0.1):
        self.name = name
        self.parent_name = parent_name
        self.link_recurrence = link_recurrence
        self.link_length = link_length
        self.link_radius = link_radius
        self.link_mass = link_mass
        self.joint_type = joint_type
        self.joint_parent = joint_parent
        self.joint_axis_xyz = joint_axis_xyz
        self.joint_origin_rpy_1 = joint_origin_rpy_1
        self.joint_origin_rpy_2 = joint_origin_rpy_2
        self.joint_origin_rpy_3 = joint_origin_rpy_3
        self.joint_origin_xyz_1 = joint_origin_xyz_1
        self.joint_origin_xyz_2 = joint_origin_xyz_2
        self.joint_origin_xyz_3 = joint_origin_xyz_3
        self.control_waveform = control_waveform
        self.control_amp = control_amp
        self.control_freq = control_freq