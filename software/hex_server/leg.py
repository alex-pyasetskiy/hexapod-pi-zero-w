import numpy as np


class Leg:
    def __init__(self,
                 id,
                 junction_servos,
                 board,
                 correction=[0, 0, 0],
                 constraint=[[35, 145], [0, 165], [30, 150]]):
        self.id = id
        self.board=board
        self.junction_servos = junction_servos
        self.correction = correction
        self.constraint = constraint

    def set_angle(self, junction, angle):
        set_angle = np.min(
            [angle, self.constraint[junction][1], 180])
        #print(f"set_angle junction={junction} angle={set_angle}")
        set_angle = np.max(
            [set_angle, self.constraint[junction][0], 0])
        
        #print(f"set_angle junction={junction} angle={set_angle}")
        self.board.position(junction, degrees=set_angle)

    def set_raw_angle(self, junction, angle):
        #print(f"set_raw_angle junction={junction} angle={angle}")
        self.board.position(junction, degrees=angle)

    def move_junctions(self, angles):
        # print(f"move_junctions angles={angles}")
        self.board.position(self.junction_servos[0], degrees=angles[0])
        self.board.position(self.junction_servos[1], degrees=angles[1])
        self.board.position(self.junction_servos[2], degrees=angles[2])

    def reset(self):
        self.board.reset(self.junction_servos[0])
        self.board.reset(self.junction_servos[1])
        self.board.reset(self.junction_servos[2])
