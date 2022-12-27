from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
from bs4 import BeautifulSoup

# Headers for BeautifulSoup4 (just in case)
headers = {'user-agent': 'Chrome/108.0.5355.0'}

# Set options to run Selenium 'Headless'
options = Options()
#options.headless = True
#options.add_argument("--window-size=1920,1200")

# Set up driver path
DRIVER_PATH = '/usr/local/bin/chromedriver'
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

# List of Details
titles = []
links = []
SKU = []
debug = []

# Page number (104 in total)
page_num = 1

# Get title for Selenium
driver.get('https://www.bigbuy.eu/en/electronics.html?page=')
time.sleep(5)

while page_num != 2:
    # Get source code for beautiful soup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    time.sleep(2)

    # Find all product links
    prod_titles = soup.find_all('a', class_='productCard-link')

    # Odd title link, Remove & Ignore
    odd_title = '\n                                Options                                \n'

    # Iterate through list of links to pull title, SKU and link
    for i in range(len(prod_titles)):
        title_string = prod_titles[i].text

        # If the title is blank or odd_title, skip, else add
        if title_string != '\n\n' and title_string != odd_title:
            titles.append(title_string)
            links.append(prod_titles[i]['href'])
            split_title = title_string.split()

            # Extract SKU from title
            found_sku = False
            for word in split_title:
                if word.isalpha() == False and word.isnumeric() == False and word.isupper():
                    SKU.append(word)
                    debug.append(title_string)
                    found_sku = True
                    break
                else:
                    continue
            if found_sku == False:
                SKU.append("NO SKU WAS FOUND")
                debug.append(title_string)
        else:
            continue

    # Go to next page
    try:
        next_button = driver.find_elements(By.CLASS_NAME, "paginator-button")[3]
        driver.execute_script("arguments[0].click();", next_button)
        page_num = page_num + 1
    except:
        print("END: Page "+str(page_num))
        break

# Format data
print("# of titles =", len(titles))
print("# of links =", len(links))
scraped_data = pd.DataFrame([titles, links, SKU]).transpose()
scraped_data.columns = ["Product Title", "Link", "SKU"]
scraped_data = scraped_data[scraped_data["Product Title"] != ""]
print(scraped_data.head())

# Save data into csv
scraped_data.to_csv("big_buy_data2.csv", index=False)