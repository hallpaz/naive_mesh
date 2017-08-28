import numpy as np


def read_OFF(off_file):
    '''Returns a list of vertices and a list of triangles (both represented as
        numpy arrays)'''

    vertexBuffer = []
    indexBuffer = []
    with open(off_file, "r") as modelfile:
        first = modelfile.readline().strip()
        if first != "OFF":
            raise(Exception("not a valid OFF file ({})".format(first)))

        parameters = modelfile.readline().strip().split()

        if len(parameters) < 2:
            raise(Exception("OFF file has invalid number of parameters"))

        for i in range(int(parameters[0])):
            coordinates = modelfile.readline().split()
            vertexBuffer.append([float(coordinates[0]), float(coordinates[1]), float(coordinates[2])])

        for i in range(int(parameters[1])):
            indices = modelfile.readline().split()
            indexBuffer.append([int(indices[1]), int(indices[2]), int(indices[3])])

    return np.array(vertexBuffer), np.array(indexBuffer)


def write_OFF(output_file, vertices, indices):
    '''Receives a list of vertices and a list of indices (both as numpy arrays)
       and writes them to an off file'''

    # converts indices and vertices to a string representation
    str_vertices = ["{} {} {}\n".format(v[0], v[1], v[2]) for v in vertices]
    str_indices = ["3 {} {} {}\n".format(i[0], i[1], i[2]) for i in indices]
    with open(output_file, 'w') as meshfile:
        meshfile.write(
        '''OFF
        %d %d 0
        %s%s
        '''%(len(str_vertices),len(str_indices), "".join(str_vertices), "".join(str_indices)))

def write_uv_PLY(output_file, vertices, indices, uv):

    str_vertices = ["{} {} {}\n".format(v[0], v[1], v[2]) for v in vertices]
    str_indices = ["3 {} {} {} 6 {} {} {} {} {} {}\n".format(i[0], i[1], i[2],
    uv[i[0]][0], uv[i[0]][1], uv[i[1]][0], uv[i[1]][1], uv[i[2]][0], uv[i[2]][1]) for i in indices]
    # str_uv = ["{} {} {}".format(n[0], n[1], n[2]) for n in normals]
    # str_vertices = [ "{} {}\n".format(str_vertices[i], str_normals[i]) for i in range(len(vertices)) ]

    with open(output_file,"w") as meshfile:
        meshfile.write('''ply
    format ascii 1.0
    comment VCGLIB generated
    element vertex {0}
    property float x
    property float y
    property float z
    element face {1}
    property list uchar int vertex_indices
    property list uchar float texcoord
    end_header
{2}
{3}
'''.format(len(str_vertices), len(str_indices), ''.join(str_vertices), ''.join(str_indices)))

def write_PLY(output_file, vertices, indices, normals):

    str_vertices = ["{} {} {}".format(v[0], v[1], v[2]) for v in vertices]
    str_indices = ["3 {} {} {}\n".format(i[0], i[1], i[2]) for i in indices]
    str_normals = ["{} {} {}".format(n[0], n[1], n[2]) for n in normals]

    str_vertices = [ "{} {}\n".format(str_vertices[i], str_normals[i]) for i in range(len(vertices)) ]

    with open(output_file,"w") as meshfile:
        meshfile.write('''ply
    format ascii 1.0
    comment VCGLIB generated
    element vertex {0}
    property float x
    property float y
    property float z
    property float nx
    property float ny
    property float nz
    element face {1}
    property list uchar int vertex_indices
    end_header
{2}
{3}
'''.format(len(str_vertices), len(str_indices), ''.join(str_vertices), ''.join(str_indices)))


def write_PLY(output_file, vertices, indices, normals, colors):

    str_vertices = ["{} {} {}".format(v[0], v[1], v[2]) for v in vertices]
    str_indices = ["3 {} {} {}\n".format(i[0], i[1], i[2]) for i in indices]
    str_normals = ["{} {} {}".format(n[0], n[1], n[2]) for n in normals]
    # no transparency, alpha = 255
    str_colors = ["{} {} {}".format(c[0], c[1], c[2]) for c in colors]

    str_vertices = [ "{} {} {}\n".format(str_vertices[i], str_normals[i], str_colors[i]) for i in range(len(vertices)) ]

    with open(output_file,"w") as meshfile:
        meshfile.write('''ply
format ascii 1.0
comment VCGLIB generated
element vertex {0}
property float x
property float y
property float z
property float nx
property float ny
property float nz
property uchar red
property uchar green
property uchar blue
element face {1}
property list uchar int vertex_indices
end_header
{2}
{3}
'''.format(len(str_vertices), len(str_indices), ''.join(str_vertices), ''.join(str_indices)))


def read_points(filename: str):
    '''Reads a file with points coordinates per line and returns a list of
        numpy arrays'''
    points = []
    with open(filename) as myfile:
        file_lines = myfile.readlines()
        for line in file_lines:
            content = line.split()
            content = [float(n) for n in content]
            # each element is a numpy array
            points.append(content)
    return np.array(points)


def write_points(points:list, filename:str):
    '''Receives a list of numpy arrays and writes it to a file, one point per line'''

    if len(points) == 0:
        return None
    with open(filename, "w") as myfile:
        for point in points:
            if len(point) == 2:
                myfile.write("{} {}\n".format(point[0], point[1]))
            elif len(point) == 3:
                myfile.write("{} {} {}\n".format(point[0], point[1], point[3]))
            else:
                raise Exception("Points should have dimension 2 or 3")
