from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    title_html = soup.find_all('div', class_="content_title")
    news_title = (title_html[1].text)
    p_html = soup.find_all('div', class_="article_teaser_body")
    news_p= (p_html[0].text)
    browser.quit()

    browser = init_browser()
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    relative_image_path = soup.find_all('a', class_='button fancybox')[0]["data-fancybox-href"]
    featured_image_url= url + relative_image_path
    browser.quit()

    browser = init_browser()
    url = "https://space-facts.com/mars/"
    browser.visit(url)
    time.sleep(1)
    df_list = pd.read_html(url)
    df = df_list[0]
    table_html = df.to_html(index = False, escape = True)
    mars_table = table_html.replace("\n", "")   
    browser.quit() 

   
    hemisphere_image_urls = []
    urls = ["https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced", 
        "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced",
        "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced",
        "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"]
    for url in urls:
        browser = init_browser()
        url = url
        browser.visit(url)
        time.sleep(1)
        html = browser.html
        soup = bs(html, "html.parser")
        dictionary = { "title" : [], "img_url" : []}
        title = soup.find('h2', class_='title').text
        img_url = soup.find_all('a', target="_blank")[3]["href"]
        dictionary["title"].append(title)
        dictionary["img_url"].append(img_url)
        hemisphere_image_urls.append(dictionary)
        browser.quit()
    mars_data = { "news_title" : news_title, "news_p" : news_p, "featured_image_url" : featured_image_url, "mars_table" : mars_table, "hemisphere_image_urls" : hemisphere_image_urls}
  
