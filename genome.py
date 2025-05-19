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
            "link-length":{"scale":1},
            "link-shape":{"scale":1},
            "link-radius":{"scale":1},
            "link-recurrence":{"scale":1},
            "link-mass":{"scale":4},
            "joint-type":{"scale":1},
            "joint-parent":{"scale":1},
            "joint-axis-xyz":{"scale":1},
            "joint-origin-rpy-1":{"scale":np.pi * 2},
            "joint-origin-rpy-2":{"scale":np.pi * 2},
            "joint-origin-rpy-3":{"scale":np.pi * 2},
            "joint-origin-xyz-1":{"scale":1},
            "joint-origin-xyz-2":{"scale":1},
            "joint-origin-xyz-3":{"scale":1},
            "control-waveform":{"scale":1},
            "control-amp":{"scale":0.25},
            "control-freq":{"scale":1}
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
            for r in range(child.recur):
                child_copy = copy.copy(child)
                child_copy.parent_name = unique_parent_name
                uniq_name = child_copy.name + str(len(exp_links))
                child_copy.name = uniq_name
                exp_links.append(child_copy)
                Genome.expandLinks(child, uniq_name, flat_links, exp_links)

class URDFLink:
    def __init__(self, name, parent_name, recur, link_length=0.1, link_radius=0.1, link_mass=0.1,
                 joint_type=0.1, joint_parent=0.1, joint_axis_xyz=0.1, joint_origin_rpy_1=0.1, joint_origin_rpy_2=0.1, joint_origin_rpy_3=0.1,
                 joint_origin_xyz_1=0.1, joint_origin_xyz_2=0.1, joint_origin_xyz_3=0.1,
                 control_waveform=0.1, control_amp=0.1, control_freq=0.1):
        self.name = name
        self.parent_name = parent_name
        self.recur = recur
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