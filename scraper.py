import time
from selenium import webdriver
import pandas as pd
import csv

driver = webdriver.Firefox()
URL = ""
driver.get(URL)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(15)    #sleep timer so that the program doesn't execute before the website loads

results = driver.find_elements_by_xpath("//div[contains(@class,'div-class')]")
# change div and div-class to relevant tag-name and class-name

totalResults = len(results)             # just displays total 
print(totalResults)                   # scraped values for dev reference

labelres = []                         # the result list that will be converted to a .csv file
for i in range(len(results)):
    labelres.append(results[i].text)

data = pd.DataFrame(labelres)
data.to_csv('labels.csv', index=False)
data

driver.close()
