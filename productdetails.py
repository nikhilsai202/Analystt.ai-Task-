import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape additional product information from the product page
def scrape_product_info(url):
    payload = {'api_key': 'apikey', 'url': url}
    response = requests.get('http://api.scraperapi.com', params=payload)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        description = ""
        product_description_ul = soup.find('ul', class_='a-unordered-list')
        if product_description_ul:
            product_description_items = product_description_ul.find_all('li')
            description = " ".join(item.find('span', class_='a-list-item').get_text(strip=True) for item in product_description_items)

        asin = ""
        manufacturer = ""
        ul_element = soup.find('ul', class_='detail-bullet-list')
        if ul_element:
            li_elements = ul_element.find_all('li')
            for li in li_elements:
                text = li.get_text(strip=True)
                if "ASIN" in text:
                    asin = text.split(':')[1].strip()
                elif "Manufacturer" in text:
                    manufacturer = text.split(':')[1].strip()

        return {
            'Product URL': url,
            'Description': description,
            'ASIN': asin,
            'Manufacturer': manufacturer
        }
    else:
        print(f"Failed to fetch data for URL: {url}")
        return None

# Main function to process product URLs and scrape information
def process_product_urls(input_csv, output_csv):
    with open(input_csv, 'r', newline='', encoding='utf-8') as input_file:
        reader = csv.DictReader(input_file)
        product_urls = [row['Product URL'] for row in reader]

    scraped_data = []
    for product_url in product_urls:
        product_info = scrape_product_info(product_url)
        if product_info:
            scraped_data.append(product_info)

    with open(output_csv, 'w', newline='', encoding='utf-8') as output_file:
        fieldnames = ['Product URL', 'Description', 'ASIN', 'Manufacturer']
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(scraped_data)

    print(f'Scraped data saved to {output_csv}')

input_csv_file = 'amazon_bag_data.csv'

output_csv_file = 'product_data.csv'

process_product_urls(input_csv_file, output_csv_file)
