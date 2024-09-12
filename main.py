import turtle
from turtle import *
import multiprocessing as mp
import math

from Camera import Camera
from Vector3 import Vector3
from Object import Object


distanceToCamera = 200

ScreenSize = 800
resolution = 200
resolutionRatio = int(ScreenSize/resolution)

offset = Vector3(0, 30, 0)


def minDistance(p, offset, obj):
    return obj.minDistance(p, offset)

def smoothMin(objects, k):
    h = max(k-abs(objects[1] - objects[0]), 0) / k
    return min(objects[1], objects[0]) - h*h*h*k/6


#rayMarch Algorithm
MaxIteration = 100
Epsilon = 0.001


def normal(p, offset):
    eps = Vector3(Epsilon, 0, 0)
    n = Vector3(
        minDistance(Vector3(p.x + eps.x, p.y, p.z), offset, objects[0]) - minDistance(Vector3(p.x - eps.x, p.y, p.z), offset, objects[0]),
        minDistance(Vector3(p.x, p.y + eps.x, p.z), offset, objects[0]) - minDistance(Vector3(p.x, p.y - eps.x, p.z), offset, objects[0]),
        minDistance(Vector3(p.x, p.y, p.z + eps.x), offset, objects[0]) - minDistance(Vector3(p.x, p.y, p.z - eps.x), offset, objects[0])
    )
    return n.unit()

def rayMarch(work_queue, final_queue, camera, offset):
    while work_queue.empty() == False:
        try:
            x1, y1, x2, y2  = work_queue.get_nowait()
            for x in range(x1, x2, resolutionRatio):
                for y in range(y1, y2, resolutionRatio):

                    directionVector = Vector3.add(
                        Vector3.add(
                            Vector3.scalerMultiply(distanceToCamera, camera.normal.unit()), 
                            Vector3.scalerMultiply(-x, camera.right.unit())), 
                            Vector3.scalerMultiply(y, Vector3.crossProduct(camera.normal, camera.right).unit())).unit()

                    currPosition = camera.pos
                    for i in range(0, MaxIteration):
                        stepDistance = smoothMin(list(map(lambda obj: minDistance(currPosition, offset, obj), objects)), 100)
                        #stepDistance = min(map(lambda obj: minDistance(currPosition, offset, obj), objects))

                        currPosition = Vector3.add(currPosition, Vector3.scalerMultiply(stepDistance, directionVector))
                        if stepDistance < Epsilon:
                            eps = Vector3(Epsilon, 0, 0)
                            
                            final_queue.put((x, y, normal(currPosition, offset)))
                            break
            
        except:
            break
                    
                              

def shadeScreen(final_queue, t, lightSources, camera):
    t.clear()
    while final_queue.empty() == False:
        shade = Vector3(0, 0, 0)
        x, y, normal = final_queue.get()
        for lightSource in lightSources:
            lightSourceUnit = lightSource[0].unit()
            
            diffuseStrength = max(0, Vector3.dotProduct(lightSourceUnit, normal))
            diffuse = Vector3.scalerMultiply(diffuseStrength, lightSource[1])

            reflection = Vector3.add(Vector3.scalerMultiply(-1, lightSourceUnit), Vector3.scalerMultiply(-2 * Vector3.dotProduct(lightSourceUnit, normal), normal))
            specularStrength = max(0, Vector3.dotProduct(camera.unit(), reflection))
            specular = Vector3.scalerMultiply(specularStrength, lightSource[1])

            shade = Vector3.add(shade, Vector3.add(Vector3.scalerMultiply(0.75, diffuse), Vector3.scalerMultiply(0.25, specular)))
    
        t.penup()
        t.goto(x, y)
        t.fillcolor((min(1, shade.x), min(1, shade.y), min(1, shade.z)))
        t.begin_fill()
        for i in range(0, 4):
            t.forward(ScreenSize/resolution)
            t.right(90)
        t.end_fill()
    t.screen.update()



def boxSDF(p, pt):
    size = 80
    q = Vector3(abs(p.x) - size, abs(p.y) - size, abs(p.z) - size)
    return Vector3.magnitude(Vector3(max(q.x, 0), max(q.y, 0), max(q.z, 0))) + min(max(q.x, max(q.y, q.z)), 0)

def sphereSDF(p, pt):
    return Vector3.magnitude(Vector3.add(p, pt)) - 80

def planeSDF(p):
    return Vector3.dotProduct(p, Vector3(0, 0, 1)) +25



objects = [
    Object(boxSDF),
    Object(sphereSDF)
]



def render(sc, t, factor, movementType, camera, offset):

    match movementType:
        case "vertical":
            camera.rotateVertical(factor)
        case "horizontal":
            camera.rotateHorizontal(factor)
        case "distance":
            camera.distanceToOrigin(factor)



    processes = []
    cores = mp.cpu_count()
    manager = mp.Manager()
    work_queue = manager.Queue()
    final_queue = manager.Queue()

    chunks = []
    for x in range(-int(math.sqrt(cores)/2), int(math.sqrt(cores)/2)): 
        for y in range(-int(math.sqrt(cores)/2), int(math.sqrt(cores)/2)): 
            chunks.append((
                x * int(ScreenSize/(math.sqrt(cores))), 
                y * int(ScreenSize/(math.sqrt(cores))),
                (x + 1) * int(ScreenSize/(math.sqrt(cores))), 
                (y + 1) * int(ScreenSize/(math.sqrt(cores)))))

    for chunk in chunks:
        work_queue.put(chunk)

    for i in range(0, cores):
        proc = mp.Process(target = rayMarch, args = (work_queue, final_queue, camera, offset))
        processes.append(proc)
        proc.start()

    for proc in processes:
        proc.join()

    lightSources = [(Vector3(-800, -800, 800), Vector3(0.8, 0, 0)),
                    (Vector3(-800, 800, 800), Vector3(0, 0.8, 0))]
    shadeScreen(final_queue, t, lightSources, camera.pos)
    
    sc.update()


def setOffset(sc, t, camera, offsetFactor):
    global offset
    offset = Vector3.add(offset, offsetFactor)
    return render(sc, t, 0, "distance", camera, offset)
    

def main():
    camera = Camera()
    sc = turtle.Screen()
    sc.setup(ScreenSize, ScreenSize)
    sc.bgcolor("black")
    sc.tracer(0)
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    

    render(sc, t, 0, "horizontal", camera, offset)


    
    turtle.onkey(lambda: render(sc, t, 20, "horizontal", camera, offset), 'Right')
    turtle.onkey(lambda: render(sc, t, -20, "horizontal", camera, offset), 'Left')
    turtle.onkey(lambda: render(sc, t, 20, "vertical", camera, offset), 'Up')
    turtle.onkey(lambda: render(sc, t, -20, "vertical", camera, offset), 'Down')
    turtle.onkey(lambda: render(sc, t, 20, "distance", camera, offset), 'j')
    turtle.onkey(lambda: render(sc, t, -20, "distance", camera, offset), 'k')
    turtle.onkey(lambda: setOffset(sc, t, camera, Vector3(0, 20, 0)), 'a')
    turtle.onkey(lambda: setOffset(sc, t, camera, Vector3(0, -20, 0)), 'd')
    turtle.onkey(lambda: setOffset(sc, t, camera, Vector3(0, 0, -20)), 'w')
    turtle.onkey(lambda: setOffset(sc, t, camera, Vector3(0, 0, 20)), 's')
    turtle.listen()
    sc.mainloop()
        

if __name__ == '__main__':
    main()