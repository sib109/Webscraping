import requests
import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    nasa_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    jpl_mars_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    mars_tweet_url = 'https://twitter.com/marswxreport?lang=en'
    mars_facts_url = 'https://space-facts.com/mars/'
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(nasa_url)
    soup = BeautifulSoup(browser.html, 'html.parser')
    results = soup.find_all('div', class_="list_text")
    news_title_list = []
    news_p_list = []
    for result in results:
        news_title = result.find('div', class_ = "content_title").text
        news_title_list.append(news_title)
        news_p = result.find('div', class_ = "article_teaser_body").text
        news_p_list.append(news_p)
        latest_news_title = news_title_list[0]
        latest_paragraph_text = news_p_list[0]

    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(jpl_mars_url)
    soup = BeautifulSoup(browser.html, 'html.parser')
    results = soup.find_all('div', class_="carousel_items")
    for result in results:
        background_image_url = result.article['style']
    image_link_part_one = jpl_mars_url.split('?')[0]
    image_link_part_two = background_image_url.split('spaceimages/')[1]
    image_link_part_two = image_link_part_two.split('.jpg')[0]
    image_link = image_link_part_one+image_link_part_two+'.jpg'

    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(mars_tweet_url)
    soup = BeautifulSoup(browser.html, 'html.parser')
    tweets = soup.find_all('p', class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    tweet_list = []
    for tweet in tweets:
        tweet_list.append(tweet.text)
        latest_tweet_temp = tweet_list[0]
        latest_tweet = latest_tweet_temp.split('pic')[0]

    tables = pd.read_html(mars_facts_url)
    mars_facts_df = tables[1]
    mars_facts_df = mars_facts_df.rename(columns = {0:'Fact',1:'Measure'})

    hemisphere_image_urls = []
    browser.visit(hemisphere_url)
    soup = BeautifulSoup(browser.html, 'lxml')
    images = soup.find_all(class_='item')
    for image in images:
        browser.visit(hemisphere_url)
        browser.click_link_by_partial_text(item.h3.text)
        soup = BeautifulSoup(browser.html, 'lxml')
        title = image.h3.text.replace(' Enhanced', '')
        img_url = soup.find(target='_blank')['href']
        hemisphere_image_urls.append({'title':title, 'img_url':img_url})

    browser.quit()

    final_output = dict (news_title = latest_news_title,
                news_p = latest_paragraph_text,
                image_url = image_link,
                mars_weather = latest_tweet,
                mars_facts = mars_facts_df,
                mars_hemisphere_images = hemisphere_image_urls)

    return final_output
