import dataio
import numpy as np


# This file is hardcoded with data from the Branca Recosntruction Experiment
# ----------------------------------------------
# Output matrices from Qt Calib for Branca model
matrix1 = [[0.227211, 0.973814, 0.007770, -30.251217],
[0.269131, -0.055122, -0.961525, 2.923447],
[-0.935918, 0.220561, -0.274608, 106.423331],
[0.0, 0.0, 0.0, 1.0]]

matrix2 = [[-0.526614, 0.850016, 0.012300, -8.769849],
[0.241173, 0.163258, -0.956652, -0.500820],
[-0.815177, -0.500820, -0.290975, 119.541449],
[0.0, 0.0, 0.0, 1.0]]

matrix3 = [[-0.966995, 0.253865, 0.021769, 15.072713],
[0.047646, 0.264090, -0.963320, 0.282367],
[-0.250303, -0.930488, -0.267469, 111.620220],
[0.0, 0.0, 0.0, 1.0]]

matrix5 = [[-0.879175, -0.475720, 0.027250, 30.393236],
[-0.162547, 0.245662, -0.955630, 5.987480],
[0.447918, -0.844595, -0.293306, 106.157313],
[0.0, 0.0, 0.0, 1.0]]

matrix6 = [[-0.037869, -0.999200, 0.012894, 22.224857],
[-0.274641, -0.001999, -0.961545, 14.117558],
[0.960801, -0.039954, -0.274346, 64.935072],
[0.0, 0.0, 0.0, 1.0]]

matrix7 = [[0.914689, -0.403788, 0.017322, -13.347893],
[-0.091854, -0.249430, -0.964027, 15.600609],
[0.393583, 0.880193, -0.265240, 56.615140],
[0.0, 0.0, 0.0, 1.0]]

matrix8 = [[0.975488, 0.219299, 0.018209, -28.997360],
[0.077644, -0.265590, -0.960954, 12.201045],
[-0.205900, 0.938813, -0.276107, 72.466453],
[0.0, 0.0, 0.0, 1.0]]

matrix10 = [[-0.000156, 0.999919, 0.012758, -25.367336],
[0.267385, 0.012335, -0.963511, 1.181789],
[-0.963590, 0.003261, -0.267365, 105.454207],
[0.0, 0.0, 0.0, 1.0]]
# ----------------------------------------------
def build_ref_planes():
    numbers = [1, 2, 3, 5, 6, 7, 8, 10]
    matrices = {1:matrix1, 2:matrix2, 3:matrix3, 5:matrix5, 6:matrix6, 7:matrix7, 8:matrix8, 10:matrix10}
    for n in numbers:
        transform_model("models/plane.off", np.matrix(matrices[n]), output="models/ref_plane{}.off".format(n))

def transform_model(filename, transformation, output=None):
    vertices, indices = dataio.read_OFF(filename)

    vertices = np.array([[v[0], v[1], v[2], 1] for v in vertices ])
    t_vertices = [np.array(transformation*np.transpose(np.matrix(v))) for v in vertices]
    for v in t_vertices:
        v.shape = 4

    if output is None:
        output = filename[:-4] + "_transformed.off"
    dataio.write_OFF(output, t_vertices, indices)


def apply_to_models():
    numbers = [1, 2, 3, 5, 6, 7, 8, 10]
    matrices = {1:matrix1, 2:matrix2, 3:matrix3, 5:matrix5, 6:matrix6, 7:matrix7, 8:matrix8, 10:matrix10}

    for n in numbers:
        transform_model("models/mybranca/mybranca{}m.off".format(n),
                    np.linalg.inv(np.matrix(matrices[n])), output="transformed/mybranca{}t.off".format(n))


if __name__ == '__main__':
    # build_ref_planes()
    apply_to_models()
