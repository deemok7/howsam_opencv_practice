import numpy as np
import cv2
import random
import math
import time

# Common parameters
WIDTH, HEIGHT = 800, 800
MAX_ITER = 100

def mandelbrot(c, max_iter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z * z + c
        n += 1
    return n

def generate_mandelbrot(animate=False):
    print("Generating Mandelbrot Set...")
    xmin, xmax = -2.0, 1.0
    ymin, ymax = -1.5, 1.5
    
    img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    
    if animate:
        cv2.namedWindow("Mandelbrot Set", cv2.WINDOW_NORMAL)
    
    for x in range(WIDTH):
        for y in range(HEIGHT):
            cx = xmin + (xmax - xmin) * x / WIDTH
            cy = ymin + (ymax - ymin) * y / HEIGHT
            c = complex(cx, cy)
            m = mandelbrot(c, MAX_ITER)
            
            hue = int(255 * m / MAX_ITER)
            saturation = 255
            value = 255 if m < MAX_ITER else 0
            
            color = cv2.cvtColor(np.uint8([[[hue, saturation, value]]]), cv2.COLOR_HSV2BGR)[0][0]
            img[y, x] = color
            
            if animate and x % 10 == 0 and y % 10 == 0:  # Update every 10 pixels for performance
                display_img = cv2.resize(img, (WIDTH, HEIGHT), interpolation=cv2.INTER_LINEAR)
                cv2.imshow("Mandelbrot Set", display_img)
                if cv2.waitKey(1) == 27:  # ESC to exit early
                    cv2.destroyAllWindows()
                    return
    
    img = cv2.resize(img, (WIDTH, HEIGHT), interpolation=cv2.INTER_LINEAR)
    cv2.imshow("Mandelbrot Set", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def julia(c, z, max_iter):
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z * z + c
        n += 1
    return n

def generate_julia(animate=False):
    print("Generating Julia Set...")
    c = complex(-0.7, 0.27)
    xmin, xmax = -1.5, 1.5
    ymin, ymax = -1.5, 1.5
    
    img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    
    if animate:
        cv2.namedWindow("Julia Set", cv2.WINDOW_NORMAL)
    
    for x in range(WIDTH):
        for y in range(HEIGHT):
            zx = xmin + (xmax - xmin) * x / WIDTH
            zy = ymin + (ymax - ymin) * y / HEIGHT
            z = complex(zx, zy)
            m = julia(c, z, MAX_ITER)
            
            hue = int(255 * m / MAX_ITER)
            saturation = 255
            value = 255 if m < MAX_ITER else 0
            
            color = cv2.cvtColor(np.uint8([[[hue, saturation, value]]]), cv2.COLOR_HSV2BGR)[0][0]
            img[y, x] = color
            
            if animate and x % 10 == 0 and y % 10 == 0:
                display_img = cv2.resize(img, (WIDTH, HEIGHT), interpolation=cv2.INTER_LINEAR)
                cv2.imshow("Julia Set", display_img)
                if cv2.waitKey(1) == 27:
                    cv2.destroyAllWindows()
                    return
    
    img = cv2.resize(img, (WIDTH, HEIGHT), interpolation=cv2.INTER_LINEAR)
    cv2.imshow("Julia Set", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def generate_sierpinski(animate=False):
    print("Generating Sierpinski Triangle...")
    img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    
    vertices = [
        (WIDTH // 2, 50),
        (50, HEIGHT - 50),
        (WIDTH - 50, HEIGHT - 50),
    ]
    
    point = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
    
    if animate:
        cv2.namedWindow("Sierpinski Triangle", cv2.WINDOW_NORMAL)
    
    for i in range(50000):
        vertex = random.choice(vertices)
        point = ((point[0] + vertex[0]) // 2, (point[1] + vertex[1]) // 2)
        cv2.circle(img, point, 1, (0, 255, 0), -1)
        
        if animate and i % 100 == 0:  # Update every 100 iterations
            cv2.imshow("Sierpinski Triangle", img)
            if cv2.waitKey(1) == 27:
                cv2.destroyAllWindows()
                return
    
    cv2.imshow("Sierpinski Triangle", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def generate_koch_snowflake(animate=False):
    print("Generating Koch Snowflake...")
    img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    
    if animate:
        cv2.namedWindow("Koch Snowflake", cv2.WINDOW_NORMAL)
    
    def koch_curve(p1, p2, depth, animate_step=None):
        p1 = (int(p1[0]), int(p1[1]))
        p2 = (int(p2[0]), int(p2[1]))
        if depth == 0:
            cv2.line(img, p1, p2, (255, 255, 255), 1)
            if animate and animate_step and animate_step[0] % 10 == 0:
                cv2.imshow("Koch Snowflake", img)
                cv2.waitKey(1)
            animate_step[0] += 1
        else:
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]

            pA = (p1[0] + dx / 3, p1[1] + dy / 3)
            pC = (p1[0] + 2 * dx / 3, p1[1] + 2 * dy / 3)

            angle = math.atan2(dy, dx)
            length = math.sqrt(dx**2 + dy**2) / 3
            pBx = p1[0] + dx / 2 - length * math.sin(angle - math.pi / 3)
            pBy = p1[1] + dy / 2 + length * math.cos(angle - math.pi / 3)
            pB = (int(pBx), int(pBy))

            koch_curve(p1, pA, depth - 1, animate_step)
            koch_curve(pA, pB, depth - 1, animate_step)
            koch_curve(pB, pC, depth - 1, animate_step)
            koch_curve(pC, p2, depth - 1, animate_step)

    center_x, center_y = WIDTH // 2, HEIGHT // 2
    size = 300

    p1 = (center_x, center_y - size)
    p2 = (center_x - int(size * math.sqrt(3) / 2), center_y + size // 2)
    p3 = (center_x + int(size * math.sqrt(3) / 2), center_y + size // 2)

    depth = 4
    if animate:
        animate_step = [0]
        koch_curve(p1, p2, depth, animate_step)
        koch_curve(p2, p3, depth, animate_step)
        koch_curve(p3, p1, depth, animate_step)
    else:
        koch_curve(p1, p2, depth)
        koch_curve(p2, p3, depth)
        koch_curve(p3, p1, depth)

    cv2.imshow("Koch Snowflake", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def generate_barnsley_fern(animate=False):
    print("Generating Barnsley Fern...")
    img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    
    if animate:
        cv2.namedWindow("Barnsley Fern", cv2.WINDOW_NORMAL)
    
    x, y = 0, 0
    
    for i in range(100000):
        r = random.random()
        if r < 0.01:
            xn = 0
            yn = 0.16 * y
        elif r < 0.86:
            xn = 0.85 * x + 0.04 * y
            yn = -0.04 * x + 0.85 * y + 1.6
        elif r < 0.93:
            xn = 0.2 * x - 0.26 * y
            yn = 0.23 * x + 0.22 * y + 1.6
        else:
            xn = -0.15 * x + 0.28 * y
            yn = 0.26 * x + 0.24 * y + 0.44

        px = int(WIDTH * (xn + 3) / 6)
        py = int(HEIGHT - HEIGHT * (yn + 2) / 10)

        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
            img[py, px] = (0, 255, 0)
            
            if animate and i % 100 == 0:  # Update every 100 points
                cv2.imshow("Barnsley Fern", img)
                if cv2.waitKey(1) == 27:
                    cv2.destroyAllWindows()
                    return

        x, y = xn, yn

    cv2.imshow("Barnsley Fern", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    while True:
        print("\nFractal Generator Menu (using OpenCV):")
        print("1. Mandelbrot Set (Animated)")
        print("2. Julia Set (Animated)")
        print("3. Sierpinski Triangle (Animated)")
        print("4. Koch Snowflake (Animated)")
        print("5. Barnsley Fern (Animated)")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            generate_mandelbrot(animate=True)
        elif choice == "2":
            generate_julia(animate=True)
        elif choice == "3":
            generate_sierpinski(animate=True)
        elif choice == "4":
            generate_koch_snowflake(animate=True)
        elif choice == "5":
            generate_barnsley_fern(animate=True)
        elif choice == "6":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()