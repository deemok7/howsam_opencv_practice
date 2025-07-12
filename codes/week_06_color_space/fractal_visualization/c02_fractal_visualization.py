import numpy as np
import cv2
import random
import math

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


def generate_mandelbrot():
    print("Generating Mandelbrot Set...")
    xmin, xmax = -2.0, 1.0
    ymin, ymax = -1.5, 1.5

    img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    for x in range(WIDTH):
        for y in range(HEIGHT):
            cx = xmin + (xmax - xmin) * x / WIDTH
            cy = ymin + (ymax - ymin) * y / HEIGHT
            c = complex(cx, cy)
            m = mandelbrot(c, MAX_ITER)

            # Color mapping
            hue = int(255 * m / MAX_ITER)
            saturation = 255
            value = 255 if m < MAX_ITER else 0

            # Convert HSV to BGR
            color = cv2.cvtColor(
                np.uint8([[[hue, saturation, value]]]), cv2.COLOR_HSV2BGR
            )[0][0]
            img[y, x] = color

    # Scale up for better viewing
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


def generate_julia():
    print("Generating Julia Set...")
    c = complex(-0.7, 0.27)
    xmin, xmax = -1.5, 1.5
    ymin, ymax = -1.5, 1.5

    img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    for x in range(WIDTH):
        for y in range(HEIGHT):
            zx = xmin + (xmax - xmin) * x / WIDTH
            zy = ymin + (ymax - ymin) * y / HEIGHT
            z = complex(zx, zy)
            m = julia(c, z, MAX_ITER)

            # Color mapping
            hue = int(255 * m / MAX_ITER)
            saturation = 255
            value = 255 if m < MAX_ITER else 0

            color = cv2.cvtColor(
                np.uint8([[[hue, saturation, value]]]), cv2.COLOR_HSV2BGR
            )[0][0]
            img[y, x] = color

    img = cv2.resize(img, (WIDTH, HEIGHT), interpolation=cv2.INTER_LINEAR)
    cv2.imshow("Julia Set", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def generate_sierpinski():
    print("Generating Sierpinski Triangle...")
    img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    # Define the three vertices of the triangle
    vertices = [
        (WIDTH // 2, 50),  # Top vertex
        (50, HEIGHT - 50),  # Bottom left
        (WIDTH - 50, HEIGHT - 50),  # Bottom right
    ]

    # Start from a random point
    point = (random.randint(0, WIDTH), random.randint(0, HEIGHT))

    for _ in range(50000):
        # Choose a random vertex
        vertex = random.choice(vertices)

        # Move halfway from current point to vertex
        point = ((point[0] + vertex[0]) // 2, (point[1] + vertex[1]) // 2)

        # Draw the point
        cv2.circle(img, point, 1, (0, 255, 0), -1)

    cv2.imshow("Sierpinski Triangle", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def generate_koch_snowflake():
    print("Generating Koch Snowflake...")
    img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    def koch_curve(p1, p2, depth):
        p1 = (int(p1[0]), int(p1[1]))
        p2 = (int(p2[0]), int(p2[1]))
        if depth == 0:
            cv2.line(img, p1, p2, (255, 255, 255), 1)
        else:
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]

            # Calculate the 3 intermediate points
            pA = (p1[0] + dx / 3, p1[1] + dy / 3)
            pC = (p1[0] + 2 * dx / 3, p1[1] + 2 * dy / 3)

            # Calculate the peak point (pB)
            angle = math.atan2(dy, dx)
            length = math.sqrt(dx**2 + dy**2) / 3
            pBx = p1[0] + dx / 2 - length * math.sin(angle - math.pi / 3)
            pBy = p1[1] + dy / 2 + length * math.cos(angle - math.pi / 3)
            pB = (int(pBx), int(pBy))

            # Recursively draw the 4 segments
            koch_curve(p1, pA, depth - 1)
            koch_curve(pA, pB, depth - 1)
            koch_curve(pB, pC, depth - 1)
            koch_curve(pC, p2, depth - 1)

    # Define the initial triangle
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    size = 300

    p1 = (center_x, center_y - size)
    p2 = (center_x - int(size * math.sqrt(3) / 2), center_y + size // 2)
    p3 = (center_x + int(size * math.sqrt(3) / 2), center_y + size // 2)

    # Draw the snowflake
    depth = 4  # Recursion depth
    koch_curve(p1, p2, depth)
    koch_curve(p2, p3, depth)
    koch_curve(p3, p1, depth)

    cv2.imshow("Koch Snowflake", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def generate_barnsley_fern():
    print("Generating Barnsley Fern...")
    img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    x, y = 0, 0

    for _ in range(100000):
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

        # Scale and position the point
        px = int(WIDTH * (xn + 3) / 6)
        py = int(HEIGHT - HEIGHT * (yn + 2) / 10)

        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
            img[py, px] = (0, 255, 0)  # Green color

        x, y = xn, yn

    cv2.imshow("Barnsley Fern", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main_1():
    while True:
        print("\nFractal Generator Menu (using OpenCV):")
        print("1. Mandelbrot Set")
        print("2. Julia Set")
        print("3. Sierpinski Triangle")
        print("4. Koch Snowflake")
        print("5. Barnsley Fern")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            generate_mandelbrot()
        elif choice == "2":
            generate_julia()
        elif choice == "3":
            generate_sierpinski()
        elif choice == "4":
            generate_koch_snowflake()
        elif choice == "5":
            generate_barnsley_fern()
        elif choice == "6":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


def main_2():
    for i in range(1, 7):
        if i!=2:
            continue
        choice = f"{i}"

        if choice == "1":
            generate_mandelbrot()
        elif choice == "2":
            generate_julia()
        elif choice == "3":
            generate_sierpinski()
        elif choice == "4":
            generate_koch_snowflake()
        elif choice == "5":
            generate_barnsley_fern()
        elif choice == "6":
            print("Exiting program...")
            break


if __name__ == "__main__":
    # main_1()
    main_2()
