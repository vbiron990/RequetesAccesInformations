import os
import requests
from io import BytesIO
from zipfile import ZipFile
import pandas as pd

# URL of the zipped CSV file
url = "https://s3.ca-central-1.amazonaws.com/cdn.bixi.com/wp-content/uploads/2023/11/DonneesOuvertes2023_10.zip"
local_zip_filename = "DonneesOuvertes2023_10.zip"
local_csv_filename = "bixi_data.csv"
output_directory = "bixi_trips_by_date"  # Adjust the output directory as needed

# Function to download and cache the zip file
def download_and_cache_zip_file(url, local_zip_filename):
    if not os.path.exists(local_zip_filename):
        response = requests.get(url)
        if response.status_code == 200:
            with open(local_zip_filename, 'wb') as zip_file:
                zip_file.write(response.content)
        else:
            print(f"Failed to download the file. Status code: {response.status_code}")

# Function to unzip and cache the CSV file
def unzip_and_cache_csv(local_zip_filename, local_csv_filename):
    # Check if the CSV file exists locally
    if not os.path.exists(local_csv_filename):
        # Check if the zip file exists locally
        if not os.path.exists(local_zip_filename):
            download_and_cache_zip_file(url, local_zip_filename)

        # Unzip the content
        with ZipFile(local_zip_filename) as zip_file:
            # Assume there is only one CSV file in the zip (you can modify this if there are multiple files)
            csv_filename = zip_file.namelist()[0]
            with zip_file.open(csv_filename) as csv_file:
                # Save the CSV file locally
                with open(local_csv_filename, 'wb') as local_csv_file:
                    local_csv_file.write(csv_file.read())

# Function to create the output directory if it doesn't exist
def create_output_directory(output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

# Function to check if the output CSV file already exists
def check_output_file_exists(output_csv_filename):
    return os.path.exists(output_csv_filename)

# Download and cache the zip file
download_and_cache_zip_file(url, local_zip_filename)

# Unzip and cache the CSV file
unzip_and_cache_csv(local_zip_filename, local_csv_filename)

# Create the output directory if it doesn't exist
create_output_directory(output_directory)

# Load the CSV file in chunks
chunk_size = 10000  # Adjust the chunk size based on your available memory
chunks = pd.read_csv(local_csv_filename, chunksize=chunk_size)

# Process each chunk and group by date
for chunk in chunks:
    # Convert STARTTIMEMS to datetime
    chunk['STARTTIME'] = pd.to_datetime(chunk['STARTTIMEMS'], unit='ms')

    # Group by date and process each group
    grouped_by_date = chunk.groupby(chunk['STARTTIME'].dt.date)

    for date, group in grouped_by_date:
        # Create a new CSV file for each date
        output_csv_filename = os.path.join(output_directory, f"bixi_trips_{date}.csv")

        # Check if the output file already exists
        if not check_output_file_exists(output_csv_filename):
            # Save the data to the new CSV file
            group.to_csv(output_csv_filename, index=False)
            print(f"Saved {len(group)} trips to {output_csv_filename}")
        else:
            # Append the data to the existing CSV file
            group.to_csv(output_csv_filename, mode='a', header=False, index=False)
            print(f"Appended {len(group)} trips to {output_csv_filename}")
