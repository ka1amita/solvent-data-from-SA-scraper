from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
import re

driver = webdriver.Chrome()

# scraping links on 45 pages of catalogue
def linkScraping(soup):
    link_tags = soup.find_all("a", href=re.compile("/product/"))
    for link_tag in link_tags:
        # to exclude the second link inside another <a> tag (that differs from the first by having siblings)
        if not link_tag.find_all():
            link = link_tag.get('href')
            print(link)
            links.append("https://www.sigmaaldrich.com"+link)
links = []
# up to 46
for pageNumber in range(1,5):
    webPage = "https://www.sigmaaldrich.com/CZ/en/products/analytical-chemistry/analytical-chromatography/solvents?country=CZ&language=en&cmsRoute=products&cmsRoute=analytical-chemistry&cmsRoute=analytical-chromatography&cmsRoute=solvents&page="+str(pageNumber)
    # webPage = "https://www.sigmaaldrich.com/CZ/en/products/analytical-chemistry/analytical-chromatography/solvents"
    # webPage = "https://www.sigmaaldrich.com/CZ/en/product/sigald/34851"
    driver.get(webPage)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    linkScraping(soup)

  
# driver.close()

# definition of empty lists for scraped values
names=[]
densities=[]

temperatures = []
failed = []
data = {}

#  scraping of the name
def nameScraping(soup):
    try:
        name_tag = soup.find(id="product-name")
        name = name_tag.get_text()
        print(name)
        names.append(name)
    except AttributeError:
        names.append("not found")
        print(link)
        failed.append(link)


#  scraping of the density
#  combine with temperature related to density!!!!!!!!!!!!
def densityScraping(soup):
    try:
        metadata = soup.find(string=re.compile("g/mL"))
        positionEnd = metadata.find("&nbsp;g/mL")
        positionBeginning = metadata.rfind('"',0,positionEnd)+1

        density = metadata[positionBeginning:positionEnd]
        print(density)
        densities.append(density)
        # return positionEnd
    except AttributeError:
        densities.append("not found")

# def temperatureScraping(soup,positionDensity):
#     # &nbsp;at 30&nbsp;°C (liquid)
#     try:
#         metadata = soup.find(string=re.compile("g/mL"))
#         positionEnd = metadata.find("&nbsp;°C",positionDensity,positionDensity+27)
#         positionBeginning = metadata.rfind('at ',positionEnd-7,positionEnd)+3

#         temperature = metadata[positionBeginning:positionEnd]
#         print(temperature)
#         temperatures.append(temperature)
#     except AttributeError:
#         temperatures.append("not found")
    

# driver = webdriver.Chrome()
for link in links:
    driver.get(link)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    nameScraping(soup)
    positionDensity = densityScraping(soup)
    temperatureScraping(soup,positionDensity)



# with open("soup.txt", "w") as my_file:
#     my_file.write(str(soup))

# with open("html.html", "w", encoding='utf-8') as my_file:
#     html = soup.prettify("utf-8")
#     my_file.write(str(html))


# same with selenium:
# name_tag = driver.find_element(By.ID, "product-name")
# name = name_tag.text



# output into dataframe
import pandas as pd

df=pd.DataFrame({"Title" :names, "Density" : densities})
print(df)

driver.close()
print("done!")


