from Vector3 import Vector3
import math

class Camera:
    def __init__(self):
        self.pos = Vector3(200, 0, 0)
        self.normal = Vector3(-1, 0, 0).unit()
        self.right = Vector3(0, -1, 0)
        self.up = Vector3(0, 0, 1)

    def translate(self, u):
        self.pos = Vector3.add(self.pos, u)

    def distanceToOrigin(self, a):
        targetDistance = self.pos.magnitude() + a
        self.pos = Vector3.scalerMultiply(targetDistance, self.pos.unit())
    

    #using spherical coordinates:
    def rotateVertical(self, a):
        a = -math.pi * a / 180
        phi = self.pos.magnitude()
        theta = math.atan(self.pos.y/self.pos.x)
        rho = math.acos(self.pos.z/phi)

        self.pos = Vector3(phi * math.cos(theta) * math.sin(rho + a),
                           phi * math.sin(theta) * math.sin(rho + a),
                           phi * math.cos(rho + a))
        
        self.normal = Vector3.scalerMultiply(-1, self.pos).unit()
        self.up = Vector3.crossProduct(self.right, self.normal).unit()


    def rotateHorizontal(self, a):
        a = math.pi * a / 180
        phi = self.pos.magnitude()
        theta = math.atan(self.pos.y/self.pos.x)
        rho = math.acos(self.pos.z/phi)

        self.pos = Vector3(phi * math.cos(theta + a) * math.sin(rho),
                           phi * math.sin(theta + a) * math.sin(rho),
                           phi * math.cos(rho))
        
        theta_right = math.atan2(self.right.y, self.right.x)
        
        self.normal = Vector3.scalerMultiply(-1, self.pos).unit()
        self.right = Vector3(math.cos(theta_right + a), math.sin(theta_right + a), 0).unit()
        self.up = Vector3.crossProduct(self.right, self.normal).unit()



