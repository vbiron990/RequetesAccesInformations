import subprocess

zip_urls = [
    "https://s3.ca-central-1.amazonaws.com/cdn.bixi.com/wp-content/uploads/2023/11/DonneesOuvertes2023_10.zip",
    "https://s3.ca-central-1.amazonaws.com/cdn.bixi.com/wp-content/uploads/2023/08/DonneesOuverte2022.zip",
    "https://s3.ca-central-1.amazonaws.com/cdn.bixi.com/wp-content/uploads/2023/06/Historique-BIXI-2021.zip",
    "https://s3.ca-central-1.amazonaws.com/cdn.bixi.com/wp-content/uploads/2023/06/Historique-BIXI-2020.zip",
    "https://s3.ca-central-1.amazonaws.com/cdn.bixi.com/wp-content/uploads/2023/06/Historique-BIXI-2019.zip",
    "https://s3.ca-central-1.amazonaws.com/cdn.bixi.com/wp-content/uploads/2023/06/Historique-BIXI-2018.zip",
    "https://s3.ca-central-1.amazonaws.com/cdn.bixi.com/wp-content/uploads/2023/06/Historique-BIXI-2018.zip",
    "https://s3.ca-central-1.amazonaws.com/cdn.bixi.com/wp-content/uploads/2023/06/Historique-BIXI-2017.zip",
    "https://s3.ca-central-1.amazonaws.com/cdn.bixi.com/wp-content/uploads/2023/06/Historique-BIXI-2016.zip",
    "https://s3.ca-central-1.amazonaws.com/cdn.bixi.com/wp-content/uploads/2023/06/Historique-BIXI-2015.zip",
    "https://s3.ca-central-1.amazonaws.com/cdn.bixi.com/wp-content/uploads/2023/06/Historique-BIXI-2014.zip",
]

# Adjust the output directory as needed
output_directory = "bixi_trips_by_date"

for url in zip_urls:
    # Construct the command to call the Bixi trips CSV script
    bixi_csv_command = [
        "python",
        "your_bixi_trips_csv_script.py",  # Replace with the actual name of your Bixi trips CSV script
        url,
        "--output-directory",
        output_directory,
    ]

    # Run the command
    subprocess.run(bixi_csv_command)

# After processing the Bixi trips CSV data, call generate_heatmaps.py
generate_heatmaps_command = [
    "python",
    "generate_heatmaps.py",  # Replace with the actual name of your generate_heatmaps script
    "--input-directory",
    output_directory,
]

subprocess.run(generate_heatmaps_command)

# After generating heatmaps, call generate_video.py
generate_video_command = [
    "python",
    "generate_video.py",  # Replace with the actual name of your generate_video script
    "--input-directory",
    output_directory,
    "--output-video",
    "bixi_trips_heatmap_video.mp4",  # Adjust the output video filename as needed
]

subprocess.run(generate_video_command)
