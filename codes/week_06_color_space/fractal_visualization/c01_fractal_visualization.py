import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.path import Path
import matplotlib.patches as patches


def mandelbrot(c, max_iter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z * z + c
        n += 1
    return n


def plot_mandelbrot():
    print("\nGenerating Mandelbrot Set...")
    xmin, xmax = -2.0, 1.0
    ymin, ymax = -1.5, 1.5
    width, height = 800, 800
    max_iter = 100

    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    img = np.zeros((height, width))

    for i in range(height):
        for j in range(width):
            img[i, j] = mandelbrot(x[j] + 1j * y[i], max_iter)

    plt.figure(figsize=(10, 10))
    plt.imshow(img.T, cmap="hot", extent=[xmin, xmax, ymin, ymax])
    plt.title("Mandelbrot Set")
    plt.xlabel("Real")
    plt.ylabel("Imaginary")
    plt.colorbar()
    plt.show()


def julia(c, z, max_iter):
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z * z + c
        n += 1
    return n


def plot_julia():
    print("\nGenerating Julia Set...")
    c = -0.7 + 0.27j
    xmin, xmax = -1.5, 1.5
    ymin, ymax = -1.5, 1.5
    width, height = 800, 800
    max_iter = 100

    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    img = np.zeros((height, width))

    for i in range(height):
        for j in range(width):
            img[i, j] = julia(c, x[j] + 1j * y[i], max_iter)

    plt.figure(figsize=(10, 10))
    plt.imshow(img.T, cmap="magma", extent=[xmin, xmax, ymin, ymax])
    plt.title(f"Julia Set for c = {c}")
    plt.xlabel("Real")
    plt.ylabel("Imaginary")
    plt.colorbar()
    plt.show()


def plot_sierpinski():
    print("\nGenerating Sierpinski Triangle...")

    def sierpinski(points, degree, ax):
        colormap = plt.cm.get_cmap("viridis")
        colors = [colormap(i) for i in np.linspace(0, 1, degree)]

        def draw_triangle(points, color):
            triangle = plt.Polygon(points, fill=True, color=color)
            ax.add_patch(triangle)

        def get_mid(p1, p2):
            return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

        def sierpinski_recursive(points, degree):
            draw_triangle(points, colors[degree - 1])
            if degree > 1:
                sierpinski_recursive(
                    [
                        points[0],
                        get_mid(points[0], points[1]),
                        get_mid(points[0], points[2]),
                    ],
                    degree - 1,
                )
                sierpinski_recursive(
                    [
                        points[1],
                        get_mid(points[0], points[1]),
                        get_mid(points[1], points[2]),
                    ],
                    degree - 1,
                )
                sierpinski_recursive(
                    [
                        points[2],
                        get_mid(points[2], points[1]),
                        get_mid(points[0], points[2]),
                    ],
                    degree - 1,
                )

        sierpinski_recursive(points, degree)

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect("equal")
    ax.axis("off")

    points = [(0, 0), (1, 0), (0.5, np.sqrt(3) / 2)]
    sierpinski(points, 6, ax)
    plt.title("Sierpinski Triangle")
    plt.show()


def plot_koch_snowflake():
    print("\nGenerating Koch Snowflake...")

    def koch_snowflake(order, scale=10):
        def _koch_snowflake_complex(order):
            if order == 0:
                angles = np.array([0, 120, 240]) + 90
                return scale * np.exp(np.deg2rad(angles) * 1j)
            else:
                ZR = 0.5 - 0.5j * np.sqrt(3) / 3
                p1 = _koch_snowflake_complex(order - 1)
                p2 = np.roll(p1, shift=-1)
                dp = p2 - p1
                new_points = np.empty(len(p1) * 4, dtype=np.complex128)
                new_points[::4] = p1
                new_points[1::4] = p1 + dp / 3
                new_points[2::4] = p1 + dp * ZR
                new_points[3::4] = p1 + dp / 3 * 2
                return new_points

        points = _koch_snowflake_complex(order)
        x, y = points.real, points.imag
        return x, y

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect("equal")
    ax.axis("off")

    x, y = koch_snowflake(order=4)
    ax.fill(x, y, facecolor="lightblue", edgecolor="navy")
    plt.title("Koch Snowflake")
    plt.show()


def plot_barnsley_fern():
    print("\nGenerating Barnsley Fern...")

    def barnsley_fern(n_points):
        x, y = [0], [0]

        for _ in range(n_points):
            r = random.random()
            if r < 0.01:
                xn = 0
                yn = 0.16 * y[-1]
            elif r < 0.86:
                xn = 0.85 * x[-1] + 0.04 * y[-1]
                yn = -0.04 * x[-1] + 0.85 * y[-1] + 1.6
            elif r < 0.93:
                xn = 0.2 * x[-1] - 0.26 * y[-1]
                yn = 0.23 * x[-1] + 0.22 * y[-1] + 1.6
            else:
                xn = -0.15 * x[-1] + 0.28 * y[-1]
                yn = 0.26 * x[-1] + 0.24 * y[-1] + 0.44

            x.append(xn)
            y.append(yn)

        return x, y

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect("equal")
    ax.axis("off")

    x, y = barnsley_fern(100000)
    ax.scatter(x, y, s=0.1, color="green", marker=".")
    plt.title("Barnsley Fern")
    plt.show()


def main_1():
    while True:
        print("\nFractal Generator Menu:")
        print("1. Mandelbrot Set")
        print("2. Julia Set")
        print("3. Sierpinski Triangle")
        print("4. Koch Snowflake")
        print("5. Barnsley Fern")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            plot_mandelbrot()
        elif choice == "2":
            plot_julia()
        elif choice == "3":
            plot_sierpinski()
        elif choice == "4":
            plot_koch_snowflake()
        elif choice == "5":
            plot_barnsley_fern()
        elif choice == "6":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


def main_2():
    for i in range(1, 7):
        choice = f"{i}"
        if choice == "1":
            plot_mandelbrot()
        elif choice == "2":
            plot_julia()
        elif choice == "3":
            plot_sierpinski()
        elif choice == "4":
            plot_koch_snowflake()
        elif choice == "5":
            plot_barnsley_fern()


if __name__ == "__main__":
    # main_1()
    main_2()
