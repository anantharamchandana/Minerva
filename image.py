import os
import requests
from bs4 import BeautifulSoup
from tkinter import simpledialog, Tk
from stem import Signal
from stem.control import Controller

# Function to set up a connection with Tor
def setup_tor():
    # This function assumes that the Tor service is already running
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()  # Authenticate with Tor
        controller.signal(Signal.NEWNYM)  # Request a new Tor circuit

# Function to search for images based on the keyword
def search_images(keyword):
    setup_tor()
    search_url = f"https://www.google.com/search?hl=en&tbm=isch&q={keyword}"
    
    session = requests.Session()
    session.proxies = {
        "http": "socks5h://127.0.0.1:9050",
        "https": "socks5h://127.0.0.1:9050",
    }
    
    try:
        response = session.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find image URLs
        image_tags = soup.find_all('img', limit=50)  # Limit to first 10 images
        image_urls = [img['src'] for img in image_tags if 'src' in img.attrs]
        return image_urls
    except Exception as e:
        print(f"Error fetching images: {e}")
        return []

# Function to download images
def download_images(image_urls):
    download_folder = "downloaded_images"
    os.makedirs(download_folder, exist_ok=True)  # Create folder if it doesn't exist

    for i, url in enumerate(image_urls):
        try:
            img_data = requests.get(url).content
            img_file_path = os.path.join(download_folder, f"image_{i + 1}.jpg")
            with open(img_file_path, 'wb') as img_file:
                img_file.write(img_data)
            print(f"Downloaded: {img_file_path}")
        except Exception as e:
            print(f"Error downloading image from {url}: {e}")

# Function to prompt for input and initiate the process
def main():
    root = Tk()
    root.withdraw()  # Hide the main window
    keyword = simpledialog.askstring("Image Search", "Enter the keyword to search for images:")
    
    if keyword:
        print(f"Searching for images of: {keyword}")
        image_urls = search_images(keyword)
        download_images(image_urls)

if __name__ == "__main__":
    main()
