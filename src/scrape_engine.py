import requests
from bs4 import BeautifulSoup
import csv


class ScrapeEngineException(Exception):
    pass


class ScrapeEngine:
    def __init__(self):
        self.element_name = "body"
        self.class_name = ""
        self.id_name = ""
        self.url = "https://example.com"
        self.filename = "scraped.csv"
        self.user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                          "Chrome/47.0.2526.111 Safari/537.36"

    def request(self):
        try:
            headers = {
                "User-Agent": self.user_agent
            }
            print(self.url, self.filename, self.user_agent, self.id_name, self.class_name, self.element_name)
            req = requests.get(self.url, headers=headers)
            req.raise_for_status()  # Raise an exception if the request was not successful
            soup = BeautifulSoup(req.content, 'html.parser')
            self.find_elements(soup)
        except requests.RequestException as e:
            raise ScrapeEngineException(f"Error occurred during request: {e}")
        except Exception as e:
            raise ScrapeEngineException(f"An error occurred: {e}")

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

        self.write_to_csv(results, self.filename)

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
    engine.url = input("Enter the URL to scrape: ")
    engine.element_name = input("Enter the element name: ")
    engine.class_name = input("Enter the class name (optional): ")
    engine.id_name = input("Enter the id name (optional): ")

    engine.request()
