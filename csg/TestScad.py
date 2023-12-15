from solid import *

if __name__ == "__main__":
    scadfile = import_scad('cube.scad')
    print()
    # b = scadfile.box(2,4,6)
    # scad_render_to_file(b, 'out_file.scad')