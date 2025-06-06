import genome
from xml.dom.minidom import getDOMImplementation
from enum import Enum
import numpy as np

class MotionType(Enum):
    PULSE = 1
    SINE = 2

class Motor:
    def __init__(self, control_waveform, control_amp, control_freq):
        if control_waveform <= 0.5:
            self.motor_type = MotionType.PULSE
        else:
            self.motor_type = MotionType.SINE

        self.control_amp = control_amp
        self.control_freq = control_freq
        self.phase = 0

    def get_output(self):
        self.phase = (self.phase + self.control_freq) % (2 * np.pi)
        if self.motor_type == MotionType.PULSE:
            if self.phase < np.pi:
                output = 1
            else:
                output = -1

        if self.motor_type == MotionType.SINE:
            output = np.sin(self.phase)

        return output


class Creature:
    def __init__(self,gene_count):
        self.spec = genome.Genome.get_gene_spec()
        self.dna = genome.Genome.get_random_genome(len(self.spec),gene_count)
        self.flat_links = None
        self.motors = None
        self.get_flat_links()
        self.get_expanded_links()
        self.start_position = None
        self.last_position = None
        self.dist = 0

    def set_dna(self, dna):
        self.dna = dna
        self.flat_links = None
        self.motors = None
        self.get_flat_links()
        self.get_expanded_links()
        self.start_position = None
        self.last_position = None
        self.dist = 0

    def get_flat_links(self):
        genome_dicts = genome.Genome.get_genome_dicts(self.dna,self.spec)
        self.flat_links = genome.Genome.genome_to_links(genome_dicts)
        return self.flat_links

    def get_expanded_links(self):
        self.get_flat_links()
        exp_links = [self.flat_links[0]]
        genome.Genome.expandLinks(self.flat_links[0], 
                                  self.flat_links[0].name,
                                  self.flat_links, 
                                  exp_links)
        self.exp_links = exp_links
        return self.exp_links
    
    # for motors
    def get_motors(self):

        if self.motors == None:

            motors = []
            for i in range(1, len(self.exp_links)):
                link = self.exp_links[i]
                m = Motor(link.control_waveform, link.control_amp, link.control_freq)
                motors.append(m)
            self.motors = motors
        return self.motors
    
    def update_position(self, pos):
        if self.last_position != None:
            p1 = np.array(self.last_position)
            p2 = np.array(pos)
            dist = np.linalg.norm(p1-p2)
            self.dist = self.dist + dist

        if self.start_position == None:
            self.start_position = pos
        else: 
            self.last_position = pos

    def get_distance_travelled(self):
        # if self.start_position is None or self.last_position is None:
        #     return 0
        # p1 = np.array(self.start_position)
        # p2 = np.array(self.last_position)
        # dist = np.linalg.norm(p1-p2)
        # return dist
        return self.dist
    
    # to XML function
    def to_xml(self):
        self.get_expanded_links()
        domimpl = getDOMImplementation()
        adom = domimpl.createDocument(None, "start", None)
        robot_tag = adom.createElement("robot")
        for link in self.exp_links:
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
    
