# Naive Mesh from Depth Image
A python 3 script to build a dense and naively tessellated 3D mesh from a depth
image and some functions that might be useful to transform the mesh and read and
right off files.

Additionally, it also builds the model's axis aligned bounding box.

**Requirements:**

- PIL (for naive_mesh.py)
- numpy (for the I/O functions in dataio.py)

Sample image inside "images" directory is from the dataset of the following work:

*Sungjoon Choi and Qian-Yi Zhou and Vladlen Koltun. Robust Reconstruction of Indoor Scenes. IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2015.*


**usage:**

python naive_mesh.py *depthimage_filename* *output_filename*
