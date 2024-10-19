import tkinter as tk
from tkinter import simpledialog
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import csv

# Function to open dialog box and return search keyword
def get_search_keyword():
    # Create the root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open a dialog box to take input from the user
    search_query = simpledialog.askstring("Input", "Enter the search keyword:")

    root.destroy()  # Destroy the root window after getting input
    
    return search_query

# Selenium automation for DuckDuckGo search
def duckduckgo_search_and_scrape(keyword):
    # Initialize WebDriver (e.g., for Chrome, Firefox, or Edge)
    driver = webdriver.Chrome()  # Use webdriver.Firefox() if using Firefox

    # Open DuckDuckGo
    driver.get("https://duckduckgo.com/")

    # Find the search box and enter the keyword
    search_box = driver.find_element("name", "q")
    search_box.send_keys(keyword)

    # Simulate pressing the Enter key
    search_box.send_keys(Keys.RETURN)

    # Wait for results to load
    time.sleep(3)

    # Parse the page source using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Scrape all search results
    results = soup.find_all('a', class_='result__a')

    # List to store search results
    search_results = []

    # Loop through the results and collect titles and links
    for idx, result in enumerate(results):
        title = result.get_text()  # Extract the title of the result
        link = result.get('href')  # Extract the link
        search_results.append([title, link])

    # Close the browser
    driver.quit()

    return search_results

# Save results to a CSV file
def save_results_to_csv(results, filename='search_results.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Link'])  # Write the header row
        writer.writerows(results)  # Write all search results

    print(f"Results saved to {filename}")

# Main program execution
if __name__ == "__main__":
    keyword = get_search_keyword()
    if keyword:
        search_results = duckduckgo_search_and_scrape(keyword)
        save_results_to_csv(search_results)  # Save results to CSV
    else:
        print("No keyword entered.")