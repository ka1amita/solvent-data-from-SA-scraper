# ref: https://www.codecademy.com/article/caupolicandiaz/web-scrape-with-selenium-and-beautiful-soup
# ref: https://requests.readthedocs.io/en/latest/user/quickstart

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By

# driver = webdriver.Firefox()
# driver.get("http://www.python.org")
# assert "Python" in driver.title
# elem = driver.find_element(By.NAME, "q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

webPage = "https://www.sigmaaldrich.com/CZ/en/product/sigald/34851"

driver.get(webPage)

# # <h1 class="MuiTypography-root jss126 MuiTypography-h1"><span id="product-name">Acetonitrile</span></h1>

# elem = driver.find_element(By.ID, "product-name")
# # also: driver.find_element_by_id(:"product-name")

# print(elem)



from bs4 import BeautifulSoup
import re

soup = BeautifulSoup(driver.page_source, 'html.parser')

with open("soup.txt", "w") as my_file:
    my_file.write(str(soup))

# with open("html.html", "w", encoding='utf-8') as my_file:
#     html = soup.prettify("utf-8")
#     my_file.write(str(html))

names=[]
densities=[]

name_tag = soup.find(id="product-name")
name = name_tag.get_text()
names.append(name)

density_tag = soup.find(string=re.compile("g/mL"))
# density_tags = soup.find_all(string=re.compile("g/mL"), limit=1)

positionEnd = density_tag.find("&nbsp;g/mL")
positionBeginning = density_tag.rfind('"',0,positionEnd)+1

density = density_tag[positionBeginning:positionEnd]

densities.append(density)

# for a in atag:
#   for title,price in zip(a.find_all('div', class_=re.compile("-m")),a.find_all('div', class_=re.compile("-k"))):
#       itemtitle.append(title.text)
#       itemprice.append(price.find('div').text)

import pandas as pd

df=pd.DataFrame({"Title" :names, "Density" : densities})
print(df)


driver.close()
print("done!")


