import requests
from bs4 import BeautifulSoup
import csv


class ScrapeEngine:
    def __init__(self):
        self.element_name = "div"
        self.class_name = "test"
        self.id_name = "test"
        self.url = "test"
        self.filename = "scraped.csv"

    def request(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
        }
        req = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        self.find_elements(soup)

    def find_elements(self, soup):
        results = []
        elements = []

        if not self.element_name:
            print("Element name is required.")
            return

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
            result = {'text': element.text}
            results.append(result)

        self.write_to_csv(results, self.filename)

    @staticmethod
    def write_to_csv(results, name):
        file_name = name
        fieldnames = results[0].keys() if results else []

        with open(file_name, 'a', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerows(results)


if __name__ == "__main__":
    # Create an instance of the ScrapeEngine class and invoke the request method
    engine = ScrapeEngine()

    # Get user input for element name, class name, and id name
    engine.url = input("Enter the URL to scrape: ")
    engine.element_name = input("Enter the element name: ")
    engine.class_name = input("Enter the class name (optional): ")
    engine.id_name = input("Enter the id name (optional): ")

    engine.request()
