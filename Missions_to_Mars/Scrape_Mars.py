from bs4 import BeautifulSoup
import requests
import pymongo
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
import pandas as pd
import json
import time

# get table data, exports to html
def get_data_table():
    url = 'https://space-facts.com/mars/'
    dfs = pd.read_html(url) 

    dfs[0].to_html('Missions_to_Mars/templates/space-facts.html', index=False)    


#get_data_table() 
#Main Scraper function
def scrape():
    
    get_data_table() 

    #create browser session
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of nasa news page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(1)
    #scrape sight for article
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser') 
    articles = soup.find_all('li', class_='slide') 
    article = articles[0]
    
    # Getting: title, paragraph, image 
    #Assign the text to variables that you can reference later
    title = article.find('div', class_='content_title').find('a').text
    para = article.find('div', class_='article_teaser_body').text
    
    #Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    
    #scrape sight for article make soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    #parsed html, find article, parsed for image
    image = soup.find('article', class_='carousel_item')
    style = image['style']
    arr = style.split("'")
    featured_image_url = f'jpl.nasa.gov/' + arr[1]
    #featured_image_url 
    
    #dictionary for mongo
    dic_mars_news = {'Title': title, 'Paragraph': para, 'Feaured Image URL': featured_image_url}
    
   #hemisphears loop: gets our images and titles from all 4
    try:
        #open page
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        
        #browser loads html, make soup
        base_url = 'https://astrogeology.usgs.gov/'
        
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        result_items = soup.find('div', class_='results').find_all('div', class_='item')
        hemisphere_image_urls = []
        #loop to navigate mars sight
        for item in result_items:
            #extracting link
            link = item.find('a', class_='itemLink')
            url = base_url + link['href']
            browser.visit(url)
            
            #navigating to image page
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            downloads = soup.find('div', class_='downloads').find_all('a')
            
            #loop through downloads to find images 
            img_url = ''
            for dl in downloads: 
                if '.jpg' == dl['href'][-4:]: 
                    img_url=dl['href']
            #append to dic list   
            title = soup.find('h2', class_="title").text
            dic = {"title": title, "img_url": img_url}
            hemisphere_image_urls.append(dic)
    except:
        print('scrape failed')  
     
    browser.quit() #close browser session
   
    # Initialize PyMongo to work with MongoDBs
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    # Define database and collections, database inserts
    db = client.mars_db
    #collections:
    #article collection
    db.articles.drop()
    collection = db.articles
    #features collection
    db.features.drop()
    fcollection = db.features
    fcollection.insert_one(dic_mars_news) #insert dic to database
    #insert documents into collection
    for dic in hemisphere_image_urls:
        collection.insert_one(dic)
 
        
#scrape()