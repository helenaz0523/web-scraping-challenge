
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import pandas as pd
import time


def init_browser():

	executable_path = {"executable_path":"webdriver/chromedriver"}
	return Browser("chrome", **executable_path, headless = False)

def scrap_data_mongo():

	browser = init_browser()

	mars_scrape_data_dict = {}


	# NASA Mars News

	title_list=[]
	txt_list=[]

	url = "https://redplanetscience.com/"
	browser.visit(url)
	html = browser.html 
	soup = bs(html,"html.parser")
	results = soup.find_all('div', class_="list_text")

	for result in results:
		try:
			title_list.append(result.find(class_="content_title").text)
			txt_list.append(result.find(class_="article_teaser_body").text)


		except AttributeError as e:
			print(e)

	mars_scrape_data_dict['news_title'] = title_list[0] 
	mars_scrape_data_dict['news_paragraph'] = txt_list[0]


	# JPL Mars Space Images

	imageurl = "https://spaceimages-mars.com/"
	browser.visit(imageurl) 
	html = browser.html 
	soup = bs(html,"html.parser")
	image = soup.find('div', class_='floating_text_area')
	link = image.find("a")['href']
    featured_image_url = imageurl+link
    
	# result to mongoDB dictionary
	mars_scrape_data_dict['featured_image_url'] = featured_image_url



	# Mars Facts

	url = "https://galaxyfacts-mars.com/"
    browser.visit(url)
	tables = pd.read_html(url) 
	plant_table_df = tables[0]
	plant_table_df.columns = ["Description", "Mars_Info","Earth_Info"] 
	plant_table_df.set_index('Description', inplace=True) 

	plant_html_table = plant_table_df.to_html() 
	plant_html_table = plant_html_table.replace("\n", "")

	# result to mongoDB dictionary
	mars_scrape_data_dict['facts'] = plant_html_table


	# Mars Hemispheres
	hemisphere_img_urls = []

	url = "https://marshemispheres.com/"
	browser.visit(url)
	html = browser.html 
	soup = bs(html,"html.parser")

	items = soup.find_all('div', class_='item')
	hemisphere_img_urls = []
    
	for item in items:
		hemisphere_img_urls.append(dictionary_entry_01)
		title = item.find('h3').text
		hemisphere_url = 'https://marshemispheres.com/' + item.find('a', class_='itemLink product-item')['href']

		browser.visit(hemisphere_url)
		html = browser.html
		soup = bs(html, 'html.parser')
		hemisphere_img_url = 'https://marshemispheres.com/' + soup.find('img', class_='wide-image')['src']
		hemisphere_img_urls.append({'title': title, 'img_url': hemisphere_img_url})
		


	# result to mongoDB dictionary
	mars_scrape_data_dict["hemisphere_img_url"] = hemisphere_img_urls


	return mars_scrape_data_dict 