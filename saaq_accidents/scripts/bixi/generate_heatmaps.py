import os
import glob
import folium
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from folium.plugins import HeatMap
from PIL import Image, ImageDraw, ImageFont
import io

# Input and output directories
input_directory = "bixi_trips_by_date"
output_directory = "output_heatmaps"

# Function to create heatmap and save as PNG with specified resolution and data point size
def create_heatmap_and_save(input_csv_path, output_png_path, width=10000, height=8000, radius=150):
    # Load CSV data
    df = pd.read_csv(input_csv_path)

    # Drop rows with NaN values in latitude or longitude
    df = df.dropna(subset=['STARTSTATIONLATITUDE', 'STARTSTATIONLONGITUDE'])

    # Check if there are any rows left after dropping NaN values
    if df.empty:
        print(f"No valid data for {input_csv_path}")
        return

    # Create a folium map covering a broader area
    montreal_map = folium.Map(location=[45.5149, -73.5807], zoom_start=12)  # Adjust these coordinates and zoom level as needed

    # Create a HeatMap with trip start locations and custom radius
    heat_data = df[['STARTSTATIONLATITUDE', 'STARTSTATIONLONGITUDE']].values.tolist()
    HeatMap(heat_data, radius=radius).add_to(montreal_map)

    # Add date overlay to the map
    date_overlay = input_csv_path.split("_")[-1].split(".")[0]
    folium.Marker(location=[45.5149, -73.5807], icon=folium.DivIcon(html=f"<div style='font-size: 16pt;'>{date_overlay}</div>")).add_to(montreal_map)

    # Save the map as HTML
    html_path = "heatmap_temp.html"
    montreal_map.save(html_path)

    # Create a headless Chrome browser with the help of webdriver_manager
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument(f"--window-size={width},{height}")  # Set the window size for the browser
    
    # Use ChromeService to set the path to ChromeDriver
    chrome_service = ChromeService(ChromeDriverManager().install())

    try:
        # Open the HTML map and wait for a short time to ensure it is fully loaded
        browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
        browser.get(f'file://{os.path.abspath(html_path)}')
        browser.implicitly_wait(2)  # Adjust the wait time as needed

        # Capture a screenshot of the browser window
        screenshot = browser.get_screenshot_as_png()

        # Open the screenshot using PIL
        img = Image.open(io.BytesIO(screenshot))

        # Add text overlay with the date at the top center
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        text_width, text_height = draw.textsize(date_overlay, font=font)
        text_position = ((img.width - text_width) // 2, 10)
        draw.text(text_position, date_overlay, (255, 255, 255), font=font)

        # Save the modified image
        img.save(output_png_path)

    finally:
        # Close the browser
        browser.quit()

    # Remove the temporary HTML file
    os.remove(html_path)

# Ensure output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Process each CSV file in the input directory
for input_csv_path in glob.glob(os.path.join(input_directory, "*.csv")):
    # Extract the date from the CSV file name
    date = os.path.splitext(os.path.basename(input_csv_path))[0].split("_")[-1]

    # Create the output PNG file path
    output_png_path = os.path.join(output_directory, f"heatmap_{date}.png")

    # Create heatmap and save as PNG with specified resolution and data point size
    create_heatmap_and_save(input_csv_path, output_png_path, width=2000, height=1600, radius=20)

print("PNG files generated successfully.")
