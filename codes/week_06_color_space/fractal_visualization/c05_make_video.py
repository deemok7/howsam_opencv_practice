# Specify the folder containing images and the output video file name
import os
import cv2

p = r"codes\week_06_color_space\fractal_visualization\out_frac_julia"
p = os.path.abspath(p)
assert os.path.exists(p)
image_folder = p
video_name = f"{p}/_out_video.mp4"

# Get the list of images in the folder
images = [
    img
    for img in os.listdir(image_folder)
    if img.endswith(".png") or img.endswith(".jpg")
]
images.sort(reverse=True)  # Sort images if needed

# Check if there are images
if not images:
    print("No images found in the specified folder.")
    exit()

# Read the first image to get the width and height
first_image = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = first_image.shape

# Define the codec and create VideoWriter object

fps = 15  # frame rate
fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # You can use 'MJPG' or 'XVID'
video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

# Loop through the images and write them to the video
for image in images:
    print(image)
    img_path = os.path.join(image_folder, image)
    frame = cv2.imread(img_path)
    if frame is None:
        print(f"Warning: {image} could not be read.")
        continue  # Skip this image if it cannot be read

    frame = cv2.resize(frame, (width, height))
    video.write(frame)  # Write the frame to the video
    print(f"Added {image} to video.")  # Debugging output

# Release the video writer object
video.release()
cv2.destroyAllWindows()
