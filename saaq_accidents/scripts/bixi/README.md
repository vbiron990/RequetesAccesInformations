# Bixi Bike Data Processing

This project fetches open-source Bixi bike data, processes it, generates heatmaps, and creates a video.

## Installation

### 1. Clone the Repository

2. Create and Activate Anaconda Environment
bash
Copy code
conda create --name bixi_env python=3.8
conda activate bixi_env
3. Install Required Packages
conda install -c conda-forge pandas folium selenium imageio pillow
pip install webdriver_manager

Usage
1. Run the Main Script to Fetch Bixi Data and Generate Heatmaps
python main_script.py
This script will fetch open-source Bixi data, process it, generate heatmaps, and create a video. The resulting PNG files and video will be stored in the output_heatmaps folder.

2. Adjust Script Parameters (Optional)
You can adjust parameters in the main_script.py file, such as the Bixi data URLs, output directories, heatmap resolution, data point size, etc.

Notes
Make sure you have Chrome installed, as the script uses the Chrome browser to capture screenshots for the heatmaps.
Adjust the main_script.py file according to your requirements.
Feel free to explore and modify the scripts based on your needs!
