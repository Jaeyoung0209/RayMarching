import math

class Vector3:
  
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def add(u, v):
        return Vector3(u.x + v.x, u.y + v.y, u.z + v.z)
    
    @staticmethod
    def scalerMultiply(a, u):
        return Vector3(a*u.x, a*u.y, a*u.z)
    
    @staticmethod
    def distance(u, v):
        return math.sqrt(math.pow(u.x - v.x, 2) + math.pow(u.y - v.y, 2) + math.pow(u.z - v.z, 2))
    
    @staticmethod
    def crossProduct(u, v):
        return Vector3(u.y * v.z - u.z * v.y, u.z * v.x - u.x * v.z, u.x * v.y - u.y * v.x)
    
    @staticmethod
    def dotProduct(u, v):
        return u.x * v.x + u.y * v.y + u.z * v.z

    
    def magnitude(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2) + math.pow(self.z, 2))

    def unit(self):
        factor = self.magnitude()
        return Vector3.scalerMultiply(1/factor, self)