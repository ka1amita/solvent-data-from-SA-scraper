from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re

driver = webdriver.Chrome()

def linkScraping(soup):
    # function for extracting links from scraped tags with bs4 and saved as a list
    # only links inside <a> tags with href containing "/product/" and having no children are saved; links are modified before saving
    link_tags = soup.find_all("a", href=re.compile("/product/"))
    for link_tag in link_tags:
        if not link_tag.find_all():
            link = link_tag.get('href')
            links.append("https://www.sigmaaldrich.com"+link)

# scraping tags on 45 pages of catalogue with selenium
links = []
for pageNumber in range(1,46):
    webPage = "https://www.sigmaaldrich.com/CZ/en/products/analytical-chemistry/analytical-chromatography/solvents?country=CZ&language=en&cmsRoute=products&cmsRoute=analytical-chemistry&cmsRoute=analytical-chromatography&cmsRoute=solvents&page="+str(pageNumber)
    driver.get(webPage)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    linkScraping(soup)

driver.close()

# saving links inside a file

with open("solvent_links_from_sigma-aldrich.txt", "w") as file:
    for link in links:
        file.write(link + "\n")

