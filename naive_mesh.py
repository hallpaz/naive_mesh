# Based on generate_pointcloud.py file which is copied in the same repository

import argparse
import sys
import os
from PIL import Image
from DataStructures import Vertex, Triangle, DepthMap, BoundingBox

focalLength = 525.0
centerX = 319.5
centerY = 239.5
scalingFactor = 1000.00

BIG = 9999999.99
#yeah, below follows a sort of a magic number...you may change this empirically
mean_coefficient = 16

def generateOFF(depth_file,off_file):
    """
    Generate a dense mesh in OFF format from a depth image.

    Input:
    depth_file -- filename of depth image
    off_file -- filename of off file (with extension .off)

    """
    depth = Image.open(depth_file)

    if depth.mode != "I":
        print(depth.mode, "depth")
        raise Exception("Depth image is not in intensity format")

    min_distance = BIG
    max_distance = 0.0
    mean_distance = 0.0

    minx, miny, minz = BIG, BIG, BIG
    maxx, maxy, maxz = -BIG, -BIG, -BIG

    points = []
    vertices = []
    last_depth = 0.0
    divide_factor = 0

    for v in range(depth.size[1]):
        for u in range(depth.size[0]):
            Z = -depth.getpixel((u,v)) / scalingFactor
            if Z==0:
                continue
            X = -(u - centerX) * Z / focalLength
            Y = (v - centerY) * Z / focalLength

            if X < minx:
                minx = X
            if X > maxx:
                maxx = X
            if Y < miny:
                miny = Y
            if Y > maxy:
                maxy = Y
            if Z < minz:
                minz = Z
            if Z > maxz:
                maxz = Z

            distance = abs(last_depth - Z)
            mean_distance += distance
            if distance < min_distance:
                min_distance = distance
            if distance > max_distance:
                max_distance = distance
            last_depth = Z
            divide_factor += 1
            vertex = Vertex(X,Y,Z)
            points.append(str(vertex))
            vertices.append(vertex)

    bounding_box = BoundingBox(minx, miny, minz, maxx, maxy, maxz)
    #print(bounding_box)
    mean_distance = mean_distance / divide_factor
    #print(mean_distance, min_distance, max_distance)
    width = depth.size[0]
    height = depth.size[1]
    indices = []
    faces = []
    distanceThreshold = mean_distance*mean_coefficient
    for v in range(height - 1):
        for u in range(width - 1):
            #superior triangle
            hdistance = abs(depth.getpixel((u, v)) - depth.getpixel((u+1, v))) / scalingFactor
            vdistance = abs(depth.getpixel((u, v)) - depth.getpixel((u, v+1))) / scalingFactor
            if hdistance < distanceThreshold and vdistance < distanceThreshold:
                triangle = Triangle(v*width + u + 1, v*width + u, (v+1)*width + u )
                faces.append(triangle)
                indices.append( str(triangle))
            #inferior triangle
            hdistance = abs(depth.getpixel((u, v+1)) - depth.getpixel((u+1, v+1))) / scalingFactor
            vdistance = abs(depth.getpixel((u+1, v)) - depth.getpixel((u+1, v+1))) /scalingFactor
            if hdistance < distanceThreshold and vdistance < distanceThreshold:
                triangle = Triangle( v*width + u + 1 , (v+1)*width + u, (v+1)*width + u + 1 )
                faces.append(triangle)
                indices.append(str(triangle))

    meshfile = open(off_file,"w")
    meshfile.write('''OFF
    %d %d 0
    %s%s
    '''%(len(points),len(indices), "".join(points), "".join(indices)))
    meshfile.close()

    points = bounding_box.points()
    indices = bounding_box.indices()
    boxfile = open(off_file[0:-4] + "_bbox.off", "w")
    boxfile.write('''OFF
    %d %d 0
    %s%s
    '''%(len(points),len(indices), "".join(points), "".join(indices)))
    boxfile.close()
    return vertices, faces, bounding_box


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
    This script reads a depth image and generates a 3D model in OFF format.
    The model has a dense mesh naively tessellated.
    ''')
    parser.add_argument('depth_file', help='input depth image (format: png)')
    parser.add_argument('off_file', help='output OFF file (format: off)')
    args = parser.parse_args()

    generateOFF(args.depth_file, args.off_file)
