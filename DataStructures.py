import math

class DepthMap:
    def __init__(self, points, width, height):
        self.points = points
        self.width = width
        self.height = height


class Vertex:
    def __init__(self, x, y, z, value = None):
        self.x = x
        self.y = y
        self.z = z
        if value is None:
            self.value = 1
        else:
            self.value = value

    def __add__(self, rhs):
        return Vertex(self.x + rhs.x, self.y + rhs.y, self.z + rhs.z)

    def invert(self):
        return Vertex(-self.x, -self.y, -self.z)

    def __sub__(self, rhs):
        return Vertex(self.x - rhs.x, self.y - rhs.y, self.z - rhs.z)

    def __mul__(self, rhs):
        return self.x * rhs.x + self.y * rhs.y + self.z * rhs.z

    def __truediv__(self, scalar):
        return Vertex(self.x/scalar, self.y/scalar, self.z/scalar)

    def scalar_mult(self, scalar):
        return Vertex(self.x*scalar, self.y*scalar, self.z*scalar)

    def normalize(self):
        norm = math.sqrt(self*self)
        if(norm < 0.000001):
            print("Trying to normalize 0 vector")
            return Vertex(0, 0, 0)
        return Vertex(self.x/norm, self.y/norm, self.z/norm)

    def distance(lhs, rhs):
        return math.sqrt((lhs.x - rhs.x)**2 + (lhs.y - rhs.y)**2 + (lhs.z - rhs.z)**2)

    def cross(lhs, rhs):
        x = (lhs.y*rhs.z - lhs.z*rhs.y)
        y = (lhs.z*rhs.x - lhs.x*rhs.z)
        z = (lhs.x*rhs.y - lhs.y*rhs.x)
        return Vertex(x, y, z)

    def __str__(self):
        return "%f %f %f\n"%(self.x,self.y,self.z)

    def repr(self):
        return str(self)

class Triangle:
    #triangle indices
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __str__(self):
        return "3 %d %d %d\n"%(self.a, self.b, self.c)

    def __repr__(self):
        return "{} {} {}".format(self.a, self.b, self.c)


class GridCell:
    def __init__(self, vertices):
        if(len(vertices) != 8):
            raise("Wrong number of vertices ({}) for cell".format(len(vertices)))
        self.vertices = vertices

    def __repr__(self):
        return "cell"


class BoundingBox:
    def __init__(self, minx, miny, minz, maxx, maxy, maxz):
        self.min_corner = (minx, miny, minz)
        self.max_corner = (maxx, maxy, maxz)
        self.vertices = [
            Vertex(minx, miny, minz),
            Vertex(maxx, miny, minz),
            Vertex(maxx, maxy, minz),
            Vertex(minx, maxy, minz),
            Vertex(minx, miny, maxz),
            Vertex(maxx, miny, maxz),
            Vertex(maxx, maxy, maxz),
            Vertex(minx, maxy, maxz)
        ]
        self.faces = [
            Triangle(2, 3, 0),
            Triangle(0, 1, 2),
            Triangle(6, 7, 4),
            Triangle(4, 5, 6)

            #Triangle(1, 5, 6),
            #Triangle(6, 2, 1),
            #Triangle(5, 4, 7),
            #Triangle(7, 6, 5),
            #Triangle(4, 1, 3),
            #Triangle(3, 7, 4)
        ]

    def points(self):
        return [str(i) for i in self.vertices]

    def indices(self):
        return [str(i) for i in self.faces]

    def __str__(self):
        return "Min Corner: " + str(self.min_corner) + " Max Corner: " + str(self.max_corner)
