import numpy as np
import cv2
import random
import math
import os


def julia(c, z, max_iter):
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z * z + c
        n += 1
    return n


def generate_julia(cnt=0, MAX_ITER=100, WIDTH=800, HEIGHT=800):
    print(f"Generating Julia Set... ({MAX_ITER})")

    p = r"codes\week_06_color_space\fractal_visualization\out_frac_julia"
    p = os.path.abspath(p)
    os.makedirs(p, exist_ok=True)
    img_name = f"{p}/{cnt:04d}.png"
    let_continue = False
    if os.path.exists(img_name):
        let_continue = True

    if not let_continue:
        c = complex(-0.7, 0.27)
        xmin, xmax = -1.5, 1.5
        ymin, ymax = -1.5, 1.5

        # img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        logo_path = os.path.abspath(
            r"codes\week_06_color_space\fractal_visualization\howsam.png"
        )
        img = cv2.imread(f"{logo_path}")
        img = cv2.resize(img, (WIDTH, HEIGHT), interpolation=cv2.INTER_CUBIC)

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
                if np.all(color == [0, 0, 0]):
                    continue
                img[y, x] = color

        img = cv2.resize(img, (WIDTH, HEIGHT), interpolation=cv2.INTER_CUBIC)

    repeat = max(1, 5 - MAX_ITER)  # 0,0,0,0,1,1,1,2,2,3,4,5,...
    for _ in range(repeat):
        if not let_continue:
            img_name = f"{p}/{cnt:04d}.png"
            b = cv2.imwrite(img_name, img)
            if not b:
                a = 0
        cnt += 1
    return cnt

    # cv2.imshow("Julia Set", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def main_3_julia():
    cnt = 0
    repeat_cnt = 0
    MAX_ITER = 1
    while MAX_ITER < 1500:
        cnt = generate_julia(cnt, MAX_ITER, WIDTH=1080, HEIGHT=1080)
        # if MAX_ITER < 4:
        #     repeat_cnt += 1
        #     if repeat_cnt >= 2:
        #         MAX_ITER += 1
        #         repeat_cnt = 0
        # else:
        #     MAX_ITER += 1

        # MAX_ITER += 1
        MAX_ITER = MAX_ITER + max(0, MAX_ITER // 10) + 1


if __name__ == "__main__":
    # main_1()
    # main_2()
    main_3_julia()
