import numpy as np

from cadlib import visualize
import example_cad


class CADProgram:
    def __init__(self, input):
        # grab the commands

        # divide into extrude blocks

        #
        pass

    def decode_sketch_command(self, command, args):
        pass

    def decode_extrude_command(self, args):
        theta = args[0]
        phi = args[1]
        px = args[2]
        py = args[3]

    def single_extrude(self, sketch_program, extrude_program):
        # sketch is N x 17
        # extrude is 1 x 17

        # First create the sketch plane
        extrude_args = extrude_program[1:]
        sketch_plane, microversion = create_sketch_plane("sketch 1", url, yaw=30, pitch=30, roll=30, px=10, py=10, pz=10)

if __name__ == "__main__":
    commands, args = example_cad.cad_1["commands"], example_cad.cad_1["args"]
    combined = np.concatenate([commands[:, np.newaxis], args], axis=1)
    print()