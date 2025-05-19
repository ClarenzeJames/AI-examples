import numpy as np
import copy

class Genome:
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
            "link_recurrence":{"scale":4},
            "link_mass":{"scale":1},
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
        sibling_ind = 1
        
        for c in children:
            for r in range(int(c.link_recurrence)):
                sibling_ind = sibling_ind + 1
                c_copy = copy.copy(c)
                c_copy.parent_name = unique_parent_name
                uniq_name = c_copy.name + str(len(exp_links))
                c_copy.name = uniq_name
                exp_links.append(c_copy)
                c_copy.sibling_ind = sibling_ind
                Genome.expandLinks(c, uniq_name, flat_links, exp_links)

    # Genome to links
    @staticmethod
    def genome_to_links(genome_dicts):
        links = []
        link_ind = 0
        parent_names = [str(link_ind)]

        # add all of the links
        for gdict in genome_dicts:
            link_name = str(link_ind)
            parent_ind = gdict["joint_parent"] * len(parent_names)
            parent_name = parent_names[int(parent_ind)]
            recur = gdict["link_recurrence"]

            link_ind = link_ind + 1
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
        self.sibling_ind = 1

    def to_link_ele(self,adom):
        link_tag = adom.createElement("link")
        link_tag.setAttribute("name", self.name)

        # Visual Tag
        vis_tag = adom.createElement("visual")
        geom_tag = adom.createElement("geometry")
        cyl_tag = adom.createElement("cylinder")
        cyl_tag.setAttribute("length", str(self.link_length))
        cyl_tag.setAttribute("radius", str(self.link_radius))

        geom_tag.appendChild(cyl_tag)
        vis_tag.appendChild(geom_tag)

        # collision tag
        coll_tag = adom.createElement("collision")
        coll_geom_tag = adom.createElement("geometry")
        coll_cyl_tag = adom.createElement("cylinder")
        coll_cyl_tag.setAttribute("length", str(self.link_length))
        coll_cyl_tag.setAttribute("radius", str(self.link_radius))

        coll_geom_tag.appendChild(coll_cyl_tag)
        coll_tag.appendChild(coll_geom_tag)

        # inertial tag
        inertial_tag = adom.createElement("inertial")
        mass_tag = adom.createElement("mass")
        mass = np.pi * (self.link_radius ** 2) * self.link_length
        mass_tag.setAttribute("value", str(mass))
        inertia_tag = adom.createElement("inertia")
        inertia_tag.setAttribute("ixx","0.03")
        inertia_tag.setAttribute("iyy","0.03")
        inertia_tag.setAttribute("izz","0.03")
        inertia_tag.setAttribute("ixy","0")
        inertia_tag.setAttribute("ixz","0")
        inertia_tag.setAttribute("iyx","0")

        inertial_tag.appendChild(mass_tag)
        inertial_tag.appendChild(inertia_tag)

        link_tag.appendChild(vis_tag)   
        link_tag.appendChild(coll_tag)
        link_tag.appendChild(inertial_tag)

        return link_tag
    
    def to_joint_ele(self,adom):
        joint_tag = adom.createElement("joint")
        joint_tag.setAttribute("name", self.name + "_to_" + self.parent_name)
        if self.joint_type >= 0.5:
            joint_tag.setAttribute("type", "revolute")
        else:
            joint_tag.setAttribute("type", "fixed")

        parent_tag = adom.createElement("parent")
        parent_tag.setAttribute("link", self.parent_name)
        child_tag = adom.createElement("child")
        child_tag.setAttribute("link", self.name)
        axis_tag = adom.createElement("axis")
        if self.joint_axis_xyz <= 0.33:
            axis_tag.setAttribute("xyz", "1 0 0")
        elif self.joint_axis_xyz > 0.33 and self.joint_axis_xyz <= 0.66:
            axis_tag.setAttribute("xyz", "0 1 0")
        else:
            axis_tag.setAttribute("xyz", "0 0 1")
        limit_tag = adom.createElement("limit")
        limit_tag.setAttribute("effort", "1")
        limit_tag.setAttribute("lower", "1")
        limit_tag.setAttribute("upper", "0")
        limit_tag.setAttribute("velocity", "1")
        origin_tag = adom.createElement("origin")
        
        rpy_1 = self.joint_origin_rpy_1 * self.sibling_ind
        rpy = str(rpy_1) + " " + str(self.joint_origin_rpy_2) + " " + str(self.joint_origin_rpy_3)
        origin_tag.setAttribute("rpy", rpy)
        xyz = str(self.joint_origin_xyz_1) + " " + str(self.joint_origin_xyz_2) + " " + str(self.joint_origin_xyz_3)
        origin_tag.setAttribute("xyz", xyz)

        joint_tag.appendChild(parent_tag)
        joint_tag.appendChild(child_tag)
        joint_tag.appendChild(axis_tag)
        joint_tag.appendChild(limit_tag)
        joint_tag.appendChild(origin_tag)

        return joint_tag
    

    def to_link_xml(self,adom):
        ele = self.to_link_ele(adom)
        return ele.toprettyxml()

    def to_joint_xml(self,adom):
        ele = self.to_joint_ele(adom)
        return ele.toprettyxml()