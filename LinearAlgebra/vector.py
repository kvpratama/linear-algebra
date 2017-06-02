from math import sqrt, acos, degrees, pi
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'
    ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG = 'Only defined in two three dims msg'

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(self.coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def plus(self, v):
        new_coordinates = [x+y for x, y in zip(self.coordinates, v.coordinates)]
        # above line is similar to this:
        # new_coordinates = []
        # n = len(self.coordinates)
        # for i in range(n)
        #     new_coordinates.append(self.coordinates[i] + v.coordinates[i])
        return Vector(new_coordinates)

    def minus(self, v):
        new_coordinates = [x-y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def times_scalar(self, c):
        new_coordinates = [Decimal(c)*x for x in self.coordinates]
        return Vector(new_coordinates)

    def magnitude(self):
        # my code
        # new_coordinate = [(x ** 2) for x in self.coordinates]
        #
        # n = len(new_coordinate)
        # tot = 0
        # for i in range(n):
        #     tot += new_coordinate[i]
        #
        # tot **= 0.5
        # return tot
        coordinate_squared = [x**2 for x in self.coordinates]
        return Decimal(sqrt(sum(coordinate_squared)))

    def normalization(self):
        # my code
        # mag = self.magnitude()
        # new_coordinate = [(1/mag) * x for x in self.coordinates]
        # return new_coordinate
        try:
            magnitude = self.magnitude()
            return self.times_scalar(1./magnitude)
        except ZeroDivisionError:
            raise Exception('Cannot normalize the zero vector')

    def normalized(self):
        try:
            magnitude = self.magnitude()
            return self.times_scalar(Decimal('1.0')/magnitude)
        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)

    def inner_product(self, w):
        new_coordinate = [x*y for x,y in zip(self.coordinates, w.coordinates)]
        return sum(new_coordinate)

    def angle(self, w):
        inner_prod = self.inner_product(w)
        v_mag = self.magnitude()
        w_mag = w.magnitude()
        return acos(inner_prod / (v_mag * w_mag))

    def angle_in_degree(self, w):
        return degrees(self.angle(w))

    def angle_with(self, v, in_degrees=False):
        try:
            u1 = self.normalized()
            u2 = v.normalized()
            angle_in_radians = acos(round(u1.inner_product(u2), 3))

            if in_degrees:
                degrees_per_radian = 180. / pi
                return angle_in_radians * degrees_per_radian
            else:
                return angle_in_radians

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle with the zero vector')
            else:
                raise e

    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance

    def is_parallel(self, v):
        return (self.is_zero() or v.is_zero()
                    or self.angle_with(v) == 0
                    or self.angle_with(v) == pi)
        # parallel = True
        # n = len(self.coordinates)
        # for i in range(n):
        #
        #     if self.coordinates[i] > v.coordinates[i]:
        #         new_coordinate = self.coordinates[i] % v.coordinates[i]
        #     else:
        #         new_coordinate = v.coordinates[i] % self.coordinates[i]
        #
        #     print(new_coordinate)
        #     if new_coordinate != 0:
        #         parallel = False
        #         # break
        # return parallel

    def is_orthogonal(self, v, tolerance=13-10):
        return abs(self.inner_product(v)) < tolerance
        # orthogonal = True
        # new_coordinate = [x * y for x, y in zip(self.coordinates, v.coordinates)]
        # n = len(new_coordinate)
        # for i in range(n):
        #     if new_coordinate[i] != 0.0:
        #         orthogonal = False
        #         break
        # return orthogonal

    def component_orthogonal_to(self, basis):
        try:
            projection = self.component_parallel_to(basis);
            return self.minus(projection)
        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e

    def component_parallel_to(self, basis):
        try:
            u = basis.normalized()
            weight = self.inner_product(u)
            return u.times_scalar(weight)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def cross_product(self, w):
        try:
            new_coordinate = []
            new_coordinate.append(self.coordinates[1] * w.coordinates[2] - w.coordinates[1] * self.coordinates[2])
            new_coordinate.append(-(self.coordinates[0] * w.coordinates[2] - w.coordinates[0] * self.coordinates[2]))
            new_coordinate.append(self.coordinates[0] * w.coordinates[1] - w.coordinates[0] * self.coordinates[1])
            return Vector(new_coordinate)
        except ValueError as e:
            msg = str(e)
            if msg == 'need more than 2 values to unpack':
                self_embedded_in_R3 = Vector(self.coordinates + ('0',))
                v_embedded_in_R3 = Vector(v.coordinates + ('0',))
                return self_embedded_in_R3.cross(v_embedded_in_R3)
            elif (msg == 'too many values to unpack' or msg == 'need  more than 1 value to unpack'):
                raise Exception(self.ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG)
            else:
                raise e

    def area_of_parallelogram(self, w):
        cross_product = self.cross_product(w)
        return cross_product.magnitude()
        #return sqrt(cross_product.coordinates[0]**2 + cross_product.coordinates[1]**2 + cross_product.coordinates[2]**2)

    def area_of_triangle(self, w):
        # cross_product = self.cross_product(w)
        # return Decimal(0.5) * cross_product.magnitude()
        return self.area_of_parallelogram(w) / Decimal('2.0')

# v = Vector([-7.579, -7.88])
# w = Vector([22.737, 23.64])
# v = Vector([-2.029, 9.97, 4.172])
# w = Vector([-9.231, -6.639, -7.245])
# v = Vector([-2.328, -7.284, -1.214])
# w = Vector([-1.821, 1.072, -2.94])
# v = Vector([2.118, 4.827])
# w = Vector([0, 0])
# v = Vector([3.039, 1.879])
# b = Vector([0.825, 2.036])
# v = Vector([-9.88, -3.264, -8.159])
# b = Vector([-2.155, -9.353, -9.473])
# v = Vector([3.009, -6.172, 3.692, -2.51])
# b = Vector([6.404, -9.144, 2.759, 8.718])
v = Vector([8.462, 7.893, -8.187])
w = Vector([6.984, -5.975, 4.778])
v = Vector([-8.987, -9.838, 5.031])
w = Vector([-4.268, -1.861, -8.866])
v = Vector([1.5, 9.547, 3.691])
w = Vector([-6.007, 0.124, 5.772])
# print(v.cross_product(w))
print(v.area_of_parallelogram(w))
print(v.area_of_triangle(w))
# print(v.plus(w))
# print(v.minus(w))
# print(v.times_scalar(3))
# print(v.inner_product(w))
# print(v.angle(w))
# print(v.angle_in_degree(w))
# print(v.angle_with(w))
# print(v.angle_with(w, True))
# print(v.is_parallel(w))
# print(v.is_orthogonal(w))
# print(v.component_parallel_to(b))
# print(v.component_orthogonal_to(b))