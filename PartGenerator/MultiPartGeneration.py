import matplotlib.pyplot as plt

from onshapeInterface import ProcessUrl, PartStudios, BlobElement
import json
from PartGenerator import Request
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
import Math3d as math3d
import numpy as np

import Send

def random_boolean_type():
    if np.random.randint(0, 2) == 0:
        return Request.BooleanType.UNION
    return Request.BooleanType.SUBTRACT

i = 0
def get_increasing_index():
    global i
    i += 1
    return str(i)

def generate_random_model_builder():
    # Generate the geometry & build into json
    builder = Request.RequestBuilder()
    master_dimensions = np.random.rand(3) * 1000 + 100
    master_length = np.linalg.norm(master_dimensions)

    builder.add_request(Request.Prism(get_increasing_index(),
                                      Request.BooleanType.UNION,
                                      origin=np.array([0,0,0]),
                                      dimensions=master_dimensions))

    num_extrudes = np.random.randint(1, 3)
    for i in range(num_extrudes):
        origin = np.random.rand(3) * master_dimensions
        dimensions = np.random.rand(3) * master_dimensions / 1.5 + 100
        builder.add_request(Request.Prism(get_increasing_index(),
                                          random_boolean_type(),
                                          origin=origin,
                                          dimensions=dimensions,
                                          origin_is_corner=False))

    # sphere1 = Request.Sphere("1", boolean_type=Request.BooleanType.SUBTRACT, diameter=100, origin=[100, 0, 0])
    # builder.add_request(sphere1)
    num_spheres = np.random.randint(1, 3)
    for i in range(num_spheres):
        origin = np.random.rand(3) * master_dimensions
        diameter = np.random.rand() * master_length / 5.0 + master_length / 10.0
        builder.add_request(Request.Sphere(get_increasing_index(),
                                           boolean_type=random_boolean_type(),
                                           diameter=diameter,
                                           origin=origin))

    num_cyl = np.random.randint(1, 3)
    for i in range(num_cyl):
        origin = np.random.rand(3) * master_dimensions
        depth = np.random.rand() * master_length / 1.5
        diameter = np.random.rand() * master_length / 5.0 + master_length / 10.0
        axis = np.random.rand(3) - 0.5
        builder.add_request(Request.Hole(get_increasing_index(),
                                         Request.BooleanType.UNION,
                                         origin=origin,
                                         axis=axis,
                                         depth=depth,
                                         diameter=diameter))

    num_holes = np.random.randint(2, 5)
    holes = []
    for i in range(num_holes):
        origin = np.random.rand(3) * master_dimensions / 2.0
        depth = master_length
        diameter = np.random.rand() * 100 + 25
        axis = np.random.rand(3) - 0.5
        hole = Request.Hole(get_increasing_index(),
                            Request.BooleanType.SUBTRACT,
                            origin=origin,
                            axis=axis,
                            depth=depth,
                            diameter=diameter)
        builder.add_request(hole)
        holes.append(hole)

    return builder, holes


if __name__ == "__main__":
    rows = 3
    cols = 3
    # Plot
    figure, axes = plt.subplots(rows, cols, subplot_kw=dict(projection="3d"))
    mngr = figure.canvas.manager.window.geometry("800x800+0+0")
    # mngr.window.setGeometry(50, 100, 640, 545)

    for r in range(rows):
        for c in range(cols):
            axes[r,c].set_axis_off()
    plt.ion()
    plt.show()

    json_url = ProcessUrl.OnshapeUrl("https://cad.onshape.com/documents/c3b4576ef97b70b3e09ba2f0/w/75bec76c270d0cb4899d9ce4/e/da7f3abe19b2d9b235ec0ffe")
    part_url = ProcessUrl.OnshapeUrl("https://cad.onshape.com/documents/c3b4576ef97b70b3e09ba2f0/w/75bec76c270d0cb4899d9ce4/e/fce32ac5b5d95c91f4cb12db")

    for r in range(rows):
        for c in range(cols):
            # axes = figure.add_subplot(projection='3d')
            # Generate the geometry & build into json
            builder, holes = generate_random_model_builder()
            your_mesh = Send.build_part(builder, part_url=part_url, json_url=json_url, name="v2")

            points = your_mesh.points
            x, y, z = (your_mesh.x, your_mesh.y, your_mesh.z)
            vectors = your_mesh.vectors

            hole_vectors = []
            other_vectors = []
            for triad in vectors:
                in_a_hole = False
                for hole in holes:
                    if math3d.check_triad_in_hole(triad, hole):
                        in_a_hole = True
                if in_a_hole:
                    hole_vectors.append(triad)
                else:
                    other_vectors.append(triad)
            hole_vectors = np.array(hole_vectors)
            other_vectors = np.array(other_vectors)

            poly_holes = mplot3d.art3d.Poly3DCollection(hole_vectors)
            poly_holes.set_facecolor((0, 0.5, 0.50, 0.95))
            axes[r, c].add_collection3d(poly_holes)

            poly_other = mplot3d.art3d.Poly3DCollection(other_vectors)
            poly_other.set_facecolor((0.5, 0.5, 0, 0.30))
            axes[r, c].add_collection3d(poly_other)

            scale = your_mesh.points.flatten()
            axes[r, c].auto_scale_xyz(x, y, z)
            axes[r,c].set_axis_off()
            figure.canvas.flush_events()
            figure.canvas.draw()

            # axes.autoscale(True)

    # plt.show(block=True)

    # Rotate the axes and update

    for angle in range(0, 360 * 4 + 1):
        for r in range(rows):
            for c in range(cols):
                # Normalize the angle to the range [-180, 180] for display
                angle_norm = (angle * 10 + 180) % 360 - 180

                azim = angle_norm
                roll = 0
                elev = 45

                # Update the axis view and title
                axes[r, c].view_init(elev, azim, roll)

        plt.draw()
        plt.pause(.0001)