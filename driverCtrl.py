# -*- coding:utf-8 -*-
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import pandas as pd
import re

class driverCtrl():
	def __init__(self):
		self.driver = []
		self.results = pd.DataFrame({})


	def open_web_driver(self,proxy_ip='',webdrv=''):
		PROXY = proxy_ip # IP:PORT or HOST:PORT
		if proxy_ip == 'null':
			proxy_ip = ''
		if webdrv == 'PhantomJS':
			service_args = [
							'--proxy='+proxy_ip ,
							'--proxy-type=http',
							'--load-images=no',
							# '--disk-cache=yes',
						]
			self.driver = webdriver.PhantomJS(service_args=service_args)
		else:
			chrome_options = webdriver.ChromeOptions()
			# chrome_options.add_argument("user-data-dir="+ os.path.abspath(r"C:\Users\a16247\AppData\Local\Google\Chrome\User Data"))
			chrome_options.add_argument("user-data-dir="+ os.path.abspath(r"C:\Users\yy\AppData\Local\Google\Chrome\User Data"))
			if PROXY != '':
				chrome_options.add_argument('--proxy-server=http://'+PROXY)
			self.driver = webdriver.Chrome(chrome_options=chrome_options)
			# self.driver = webdriver.Chrome()
		self.driver.maximize_window()  #将浏览器最大化显示
		time.sleep(0.5)


	def driver_quit(self):
		self.driver.quit()

	def scrollCtrl(self):
		js="var q=document.body.scrollTop=100000"
		self.driver.execute_script(js)
		time.sleep(0.5)
		
	def save_xlsx(self,target):
		writer = pd.ExcelWriter('data/' + target+'.xlsx', engine='xlsxwriter')
		# Convert the dataframe to an XlsxWriter Excel object.
		self.results.to_excel(writer, sheet_name='Sheet1')
		# Close the Pandas Excel writer and output the Excel file.
		writer.save()




