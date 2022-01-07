import requests
from bs4 import BeautifulSoup
import csv


class ScrapeEngine:
    # URL = ""

    def request(self):
        url = input()
        req = requests.get(url)

        soup = BeautifulSoup(req.content, 'html5lib')
        self.find_ele(soup)

    def find_ele(self, soup1):
        selected_classes = ""
        selected_id = ""
        results = []
        # result = {}

        table = soup1.find('div', attrs={'id': selected_id})

        for row in table.findAll('div', attrs={'class': selected_classes}):
            result = {'text': row.text}
            results.append(result)

        self.write(results)

    @staticmethod
    def write(res):
        sel_file = "test.csv"
        # writer = res[0].keys
        writer = []
        for i in range(len(res)):
            writer.append(res[i].keys)
        filename = sel_file
        with open(filename, 'w', newline='') as f:
            w = csv.DictWriter(f, writer)
            w.writeheader()
            for result in res:
                w.writerow(result)
