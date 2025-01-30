from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Set up WebDriver
driver_path = "/Users/shamdhage/Desktop/new-brave-chromedriver-mac-x64/chromedriver"  # Path to ChromeDriver
service = Service(driver_path)
options = webdriver.ChromeOptions()
options.add_argument("--headless") #will run without ui
options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"  # Path to Brave
driver = webdriver.Chrome(service=service, options=options)

# opening Amazon category page
url = "https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar"
driver.get(url)

# wait for elements to load
wait = WebDriverWait(driver, 10)

# extract product links for all items shown on the page
items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.a-link-normal.s-line-clamp-4.s-link-style.a-text-normal")))
hrefs = [item.get_attribute("href") for item in items if item.get_attribute("href")]

data = []
def get_element_text(xpath):
    #function to extract the text from a given xpath
    try:
        return wait.until(EC.presence_of_element_located((By.XPATH, xpath))).text.strip()
    except:
        return "Not Available"

# iterating over product links
for link in hrefs:
    try:
        driver.get(link)  # open link in same tab

        # Extracting details
        product_name = get_element_text('//*[@id="productTitle"]')

        price = get_element_text('//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[3]/span[2]/span[2]')

        rating = get_element_text('//*[@id="acrPopover"]/span[1]/a/span')

        seller_name = get_element_text('//*[@id="sellerProfileTriggerId"]')

        # Append extracted data
        values = {"Product Name": product_name, "Price": price, "Rating": rating, "Seller Name": seller_name}
        data.append(values)
        print(values)

    except Exception as e:
        print(f"Error scraping {link}: {e}")
        continue  # Move to next product

# Save data to CSV
df = pd.DataFrame(data)
df.to_csv("Amazon_Data.csv", index=False)

# Close driver
driver.quit()
#here i am scraping the first page, but if you want I can even scrape the next few pages
print("Scraping complete. Data saved to Amazon_data.csv.")
