import os
import glob
import imageio

# Input and output directories
input_directory = "output_heatmaps"
video_output_path = "bixi_trips_heatmap_video.mp4"

# Create a video from the generated PNG files
image_files = sorted(glob.glob(os.path.join(input_directory, "*.png")))
fps = 10

# Check if there are any PNG files to create the video
if not image_files:
    print("No PNG files found. Exiting.")
else:
    with imageio.get_writer(video_output_path, fps=fps) as writer:
        for image_file in image_files:
            img = imageio.imread(image_file)
            writer.append_data(img)

    print(f"Video created at: {video_output_path}")
