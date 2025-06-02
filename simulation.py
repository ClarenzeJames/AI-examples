import pybullet as p
import creature

class Simulation():
    def __init__(self):
        self.physicsClientId = p.connect(p.DIRECT)

    def run_creature(self, cr, iteration=2400): # physics engine runs at 240fps, this is 10s
        pid = self.physicsClientId
        p.resetSimulation(physicsClientId = pid)
        p.setGravity(0,0,-10,physicsClientId = pid)
        xml_file = 'temp.urdf'
        xml_str = cr.to_xml()
        with open(xml_file,'w') as f:
            f.write(xml_str)

        cid = p.loadURDF(xml_file,physicsClientId = pid)
        for step in range(iteration):
            p.stepSimulation(physicsClientId = pid)
            # make it run every 1/10 of a second
            if step % 24 == 0:
                self.update_motors(cid=cid, cr=cr)
                
            pos, orn = p.getBasePositionAndOrientation(cid, physicsClientId = pid)
            cr.update_position(pos)

    def update_motors(self, cid, cr):
        """
        cid is physics engine
        cr is creature object
        """
        for jid in range(p.getNumJoints(cid, 
                                        physicsClientId = self.physicsClientId)):
            m = cr.get_motors()[jid]
            p.setJointMotorControl2(cid, jid, 
                                    physicsClientId = self.physicsClientId,
                                    controlMode=p.VELOCITY_CONTROL,
                                    targetVelocity=m.get_output(),
                                    force = 5,
                                    
                                    )
