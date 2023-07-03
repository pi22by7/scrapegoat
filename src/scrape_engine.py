import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse, parse_qs
import csv


class ScrapeEngineException(Exception):
    pass


class ScrapeEngine:
    def __init__(self):
        self.element_name = "div"
        self.class_name = "caption"
        self.id_name = ""
        self.base_url = "https://webscraper.io/test-sites/e-commerce/static/phones/touch?page=2"
        self.file_name = "scraped.csv"
        self.user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                          "Chrome/47.0.2526.111 Safari/537.36"
        self.enable_pagination = True
        self.start_page = 1
        self.end_page = 1

    def request(self):
        try:
            headers = {
                "User-Agent": self.user_agent
            }
            page_number = None if self.enable_pagination is False else self.start_page
            self.clean_url()
            while True:
                url = self.construct_url(page_number)
                print(url)
                req = requests.get(url, headers=headers)
                req.raise_for_status()  # Raise an exception if the request was not successful
                soup = BeautifulSoup(req.content, 'html.parser')
                elements_found = self.find_elements(soup)
                if not elements_found or not self.enable_pagination:
                    break  # No more pages to scrape or pagination disabled
                if page_number >= self.end_page:
                    break
                page_number += 1

        except requests.RequestException as e:
            raise ScrapeEngineException(f"Error occurred during request: {e}")
        except Exception as e:
            raise ScrapeEngineException(f"An error occurred: {e}")

    def clean_url(self):
        parsed_url = urlparse(self.base_url)
        # query_params = parse_qs(parsed_url.query)
        sanitized_url = parsed_url._replace(query='').geturl()
        self.base_url = sanitized_url

    def construct_url(self, page_number=None):
        if page_number is None:
            return self.base_url
        else:
            return f"{self.base_url}?page={page_number}"

    def find_elements(self, soup):
        results = []
        elements = []

        if not self.element_name:
            raise ScrapeEngineException("Element name is required.")

        elements += soup.find_all(self.element_name)

        if self.class_name:
            elements = [
                element for element in elements
                if element.has_attr('class') and self.class_name in element.get('class')
            ]
        if self.id_name:
            elements = [
                element for element in elements
                if element.has_attr('id') and self.id_name == element.get('id')
            ]

        for element in elements:
            result = {'scraped data': element.text}
            results.append(result)

        self.write_to_csv(results, self.file_name)

        return len(elements) > 0

    @staticmethod
    def write_to_csv(results, name):
        try:
            file_name = name
            fieldnames = results[0].keys() if results else []

            with open(file_name, 'a', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames)
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerows(results)
        except IOError as e:
            raise ScrapeEngineException(f"Error occurred while writing to CSV: {e}")
        except Exception as e:
            raise ScrapeEngineException(f"An error occurred: {e}")


if __name__ == "__main__":
    # Create an instance of the ScrapeEngine class and invoke the request method
    engine = ScrapeEngine()

    # Get user input for element name, class name, and id name
    # engine.base_url = input("Enter the base URL to scrape: ")
    # engine.element_name = input("Enter the element name: ")
    # engine.class_name = input("Enter the class name (optional): ")
    # engine.id_name = input("Enter the id name (optional): ")
    # engine.user_agent = input("Enter a valid user-agent string (optional): ")
    # pagination_choice = input("Enable pagination? (y/n): ")
    # engine.enable_pagination = pagination_choice.lower() == 'y'

    engine.request()
