from math import sqrt, acos, degrees, pi
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'

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


# v = Vector([-7.579, -7.88])
# w = Vector([22.737, 23.64])
# v = Vector([-2.029, 9.97, 4.172])
# w = Vector([-9.231, -6.639, -7.245])
# v = Vector([-2.328, -7.284, -1.214])
# w = Vector([-1.821, 1.072, -2.94])
v = Vector([2.118, 4.827])
w = Vector([0, 0])
# print(v.plus(w))
# print(v.minus(w))
# print(v.times_scalar(3))
# print(v.inner_product(w))
# print(v.angle(w))
# print(v.angle_in_degree(w))
# print(v.angle_with(w))
# print(v.angle_with(w, True))
print(v.is_parallel(w))
print(v.is_orthogonal(w))