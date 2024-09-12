# RayMarching Algorithm in Turtle Graphics
This is a for-fun project I made to see what would happen if I tried to implement the ray marching algorithm to render 3D shapes on Python's turtle graphic library. It is extremely slow as I am controlling the turtle to repeatedly make tiny squre for each pixel on the canvas, but I tried my best to speed the process up by parallel processing. Since my CPU contains 16 cores, I split up the canvas into 4x4 grid and used Python's multiprocessing library to assign each core to the divided grid cell. The resulting code can render any 3D object as long as a proper distance function is given. In addition, I added very simple diffusion lighting on the shapes by calculating the surface normal at each pixel. Overall, this project was a good utilization of the knowledge I learned in my calculus 3 course I recently took about vector calculus and linear algebra.

This is a rendered image of a simple cube and a sphere.

![image](https://github.com/user-attachments/assets/08b2091f-a5fd-47c2-8d8f-77332da2914c)

If I was to simply calculate the minimum distance between the two distance functions, I would get this intersection:

![image](https://github.com/user-attachments/assets/0013e2ae-0470-4209-ae4b-102d5398e904)

The surfaces of these shapes are lighted based on light sources I have set up in the scene, and are coloured based on the angle of the surface. And since this scene is rendered using ray marching, I can apply various functions to change how these shapes behave when they intersect with each other. One example is the smoothMin function, which I can apply to smooth out the intersecting edges of the shapes.

![image](https://github.com/user-attachments/assets/9e34088d-5bce-4e01-bc51-e09a2ee3d524)

This is an image of the same cube and sphere in the above image, but with the smoothMin function applied and the sphere displaced closer to the cube. The intersection between the two shapes are rounded to make a smooth surface, as expected.
