import requests
from bs4 import BeautifulSoup

def scrape_title(url):
    """Scrape the title from a given URL."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string.strip() if soup.title else 'No Title Found'
        return title
    except Exception as e:
        return f"Error: {str(e)}"
    
# print(scrape_title('https://www.therestaurantstore.com/items/569395'))