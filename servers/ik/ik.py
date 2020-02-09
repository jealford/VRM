import ikpy
import numpy as np
import math

class ik:
    my_chain = ikpy.chain.Chain.from_urdf_file("C:/Users/kevin/Desktop/Hackathon/servers/ik/robots/reactor_description.URDF", base_elements=None, last_link_vector=None, base_element_type="link", active_links_mask=None, name='chain')

    def inv_kine(self, pos):
        angles = self.my_chain.inverse_kinematics([
        [1, 0, 0, pos[0]],
        [0, 1, 0, pos[1]],
        [0, 0, 1, pos[2]],
        [0, 0, 0, 1]
        ])
        angles = angles / (math.pi * 2) * 360
        return angles[1:]
