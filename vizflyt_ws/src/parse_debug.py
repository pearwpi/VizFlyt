import cv2
import os
import re

# Folder with images
folder = "debug"

# Pattern to match and sort files like output_image_0.png, output_image_1.png, etc.
pattern = re.compile(r"output_image_(\d+)\.png")

# Get and sort image filenames by their index
image_files = sorted(
    [f for f in os.listdir(folder) if pattern.match(f)],
    key=lambda x: int(pattern.match(x).group(1))
)

# Full paths to images
image_paths = [os.path.join(folder, f) for f in image_files]

# Read the first image to get dimensions
if not image_paths:
    raise ValueError("No matching images found in folder.")

frame = cv2.imread(image_paths[0])
height, width, layers = frame.shape

# Define the codec and create VideoWriter object
output_path = 'output_video.mp4'
fps = 10  # You can adjust this
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'XVID' for .avi

video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# Write each image as a frame
for image_path in image_paths:
    frame = cv2.imread(image_path)
    if frame.shape[:2] != (height, width):
        frame = cv2.resize(frame, (width, height))  # Resize if needed
    video.write(frame)

video.release()
print(f"Saved video as {output_path}")
