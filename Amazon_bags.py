import requests
from bs4 import BeautifulSoup
import csv


# Function to scrape product details from a single page
def scrape_page(url):
    payload = {'api_key': 'apikey', 'url': url}
    response = requests.get('http://api.scraperapi.com', params=payload)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    products = []
    
    for product in soup.select('.s-result-item'):
        product_url_element = product.select_one('.a-link-normal')
        product_name_element = product.select_one('.a-text-normal')
        product_price_element = product.select_one('.a-offscreen')
        product_rating_element = product.select_one('.a-icon-star-small')
        review_count_element = product.select_one('.a-size-small .a-link-normal')
        
        if product_url_element and product_name_element and product_price_element and product_rating_element and review_count_element:
            product_url = 'https://www.amazon.in' + product_url_element['href']
            product_name = product_name_element.text.strip()
            product_price = product_price_element.text.strip()
            product_rating = float(product_rating_element.text.split()[0])
            
            # Clean and convert review count to integer
            # review_count_text = review_count_element.text.replace(',', '').strip()
            # review_count = int(review_count_text) if review_count_text.isdigit() else 0
            
            products.append({
                'Product URL': product_url,
                'Product Name': product_name,
                'Product Price': product_price,
                'Rating': product_rating,
                # 'Number of Reviews': review_count
            })
    
    return products

# Main function to scrape multiple pages
def scrape_multiple_pages(base_url, num_pages):
    all_products = []
    
    for page in range(1, num_pages + 1):
        page_url = f'{base_url}&page={page}'
        page_products = scrape_page(page_url)
        all_products.extend(page_products)
    
    return all_products

# Base URL for the search results
base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'

# Number of pages to scrape
num_pages = 20

# Scrape the data from multiple pages
scraped_data = scrape_multiple_pages(base_url, num_pages)

# Save the data to a CSV file
csv_file = 'amazon_bag_data.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    csv_writer = csv.DictWriter(file, fieldnames=scraped_data[0].keys())
    csv_writer.writeheader()
    csv_writer.writerows(scraped_data)

print(f'Scraped data saved to {csv_file}')
