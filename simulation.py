import pybullet as p
import creature
from multiprocessing import Pool

class Simulation():
    def __init__(self, sim_id=0):
        self.physicsClientId = p.connect(p.DIRECT)
        self.sim_id = sim_id

    def run_creature(self, cr, iteration=2400): # physics engine runs at 240fps, this is 10s
        pid = self.physicsClientId
        p.resetSimulation(physicsClientId = pid)
        p.setPhysicsEngineParameter(enableFileCaching=0,physicsClientId = pid)
        plane_shape = p.createCollisionShape(p.GEOM_PLANE, physicsClientId = pid)
        floor = p.createMultiBody(plane_shape,plane_shape, physicsClientId = pid)
        p.setGravity(0,0,-10,physicsClientId = pid)

        xml_file = 'temp' + str(self.sim_id) + '.urdf'
        xml_str = cr.to_xml()
        with open(xml_file,'w') as f:
            f.write(xml_str)

        cid = p.loadURDF(xml_file,physicsClientId = pid)

        p.resetBasePositionAndOrientation(cid, [0,0,3], [0,0,0,1],physicsClientId = pid)

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
                                    force = 5)
            
    def eval_population(self,pop,iterations):
        for cr in pop.creatures:
            self.run_creature(cr,2400)
            
class ThreadedSim():
    def __init__(self, pool_size):
        self.sims = [Simulation(i) for i in range(pool_size)]

    @staticmethod
    def static_run_creature(sim, cr, iterations):
        sim.run_creature(cr, iterations)
        return cr
    
    def eval_population(self, pop, iterations):
        pool_args = []
        start_ind = 0
        pool_size = len(self.sims)
        while start_ind < len(pop.creatures):
            this_pool_args = []
            for i in range(start_ind, start_ind + pool_size):
                if i == len(pop.creatures): #the end
                    break
                # work out the sim ind
                sim_ind = i % len(self.sims)
                this_pool_args.append([
                    self.sims[sim_ind],
                    pop.creatures[i],
                    iterations
                ])
            
            pool_args.append(this_pool_args)
            start_ind = start_ind + pool_size

            new_creatures = []
            for pool_argset in pool_args:
                with Pool(pool_size) as p:
                    #it works on a copy of the creatres, so receives them
                    creatures = p.starmap(ThreadedSim.static_run_creature,pool_argset)
                    # and now put those creatures back into the main
                    new_creatures.extend(creatures)
            pop.creatures = new_creatures