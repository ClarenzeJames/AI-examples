import pybullet as p
import pybullet_data as pd
import creature
import time

p.connect(p.GUI)
p.setPhysicsEngineParameter(enableFileCaching=0)
p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
plane_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(plane_shape,plane_shape)
p.setGravity(0,0,-10)

# creating the creature
c = creature.Creature(gene_count=5)

with open('test.urdf','w') as f:
    c.get_expanded_links()
    f.write(c.to_xml())

cid = p.load(URDF='test.urdf')

p.setRealTimeSimulation(1)

while True:
    for i in range(p.getNumJoints(cid)):
        m = c.get_motors()[i]
        p.setJointMotorControl2(cid, i, controlMode=p.VELOCITY_CONTROL,
                                targetVelocity=m.get_output(), force=5)
        
    time.sleep(0.1)
