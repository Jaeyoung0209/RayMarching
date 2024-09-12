from Vector3 import Vector3

class Object:
    def __init__(self, distanceFunction):
        self.distanceFunction = distanceFunction

    def minDistance(self, p, pt):
        return self.distanceFunction(p, pt)