# -*- coding:utf-8 -*-
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import driverCtrl as dc
import numpy as np

class driverCtrl_tb(dc.driverCtrl):
	def __init__(self,proxy_ip='',webdrv=''):
		self.open_web_driver(proxy_ip=proxy_ip,webdrv=webdrv)
		self.open_web()
		
	def open_web(self):
		url = "http://www.taobao.com"
		self.driver.get(url)

	def search(self,string):
		search_key = string
		elems = self.driver.find_elements_by_xpath('//div[@class="search-combobox-input-wrap"]/input')
		##print len(elems)
		elems[0].send_keys(Keys.BACKSPACE + search_key + Keys.RETURN)
		time.sleep(1)
		
		elems = self.driver.find_elements_by_xpath('//div[@class="crumb g-clearfix"]/a[@class="total link"]')
		try:
			elems[0].click()
			time.sleep(1)
		except:
			print 'no total link'
			
		self.sort_row(rule = 2)
		time.sleep(1)
		self.price_row(rule = -2)
		time.sleep(2)
		
		# filter the same goods
		# self.filter_row()
		# time.sleep(1)
		
		js="var q=document.body.scrollTop=100000"
		self.driver.execute_script(js)
		time.sleep(2)
		content = self.driver.page_source.encode('utf-8')
		url     = self.driver.current_url.encode('utf-8')
		return [content,url]
	
	def max_page_num(self):
		elems = self.driver.find_elements_by_xpath('//div[@class="m-page g-clearfix"]/div[@class="wraper"]/div[@class="inner clearfix"]/div[@class="total"]')
		string = elems[0].text
		string = string.split(' ')
		string = string[1]
		return int(string)
	
	def next_page(self):
		elems = self.driver.find_elements_by_xpath('//div[@class="wraper"]/div[@class="inner clearfix"]/ul/li[@class="item next"]/a')
		
		retry_cnt = 0
		while retry_cnt != 3:
			try:
				elems[0].click()
				time.sleep(0.5)
				retry_cnt = 3
			except:
				retry_cnt = retry_cnt + 1
				print 'next_page retry ',retry_cnt
				
		
		js="var q=document.body.scrollTop=100000"
		self.driver.execute_script(js)
		content = self.driver.page_source.encode('utf-8')
		url     = self.driver.current_url.encode('utf-8')
		return [content,url]
	
	# 0:综合 1：人气 2：销量 3：信用 4：价格
	def sort_row(self,rule = 0):				
		elems = self.driver.find_elements_by_xpath('//div[@id="mainsrp-sortbar"]\
													/div[@class="m-sortbar"]\
													/div[@class="sort-row"]\
													/div[@class="sort-inner"]\
													/ul/li\
													')
		
		print 'sort cnt:',len(elems)
		elems[rule].click()
		time.sleep(1)
	
	def price_row(self,rule = -1):
		elems = self.driver.find_elements_by_xpath('//div[@id="mainsrp-sortbar"] \
		                                            /div[@class="m-sortbar"]\
													/div[@class="sort-row"]\
													/div[@class="sort-inner"]\
													/div[@class="prices"]\
													/div[@class="ranks"]\
													/div[@class="items J_SortbarPriceRanks"]\
													/a\
													')

		if rule == -1:
			max_statistics = 0
			max_count      = 0
			for i in range(len(elems)):
				temp = elems[i].get_attribute('data-percent')
				temp = int(temp)
				if temp > max_statistics:
					max_statistics = temp
					max_count      = i
			
			elems[max_count].click()
		elif rule == -2:
			try:
				start = elems[1].get_attribute('data-start')
				print 'start: ',start
			except:
				start = '100'
				print 'none price distribution: ',start
			# end   = elems[3].get_attribute('data-end')			
			# print 'end: ',end
			
			elems = self.driver.find_elements_by_xpath('//div[@id="mainsrp-sortbar"] \
												/div[@class="m-sortbar"]\
												/div[@class="sort-row"]\
												/div[@class="sort-inner"]\
												/div[@class="prices"]\
												/div[@class="inputs J_LaterHover"]\
												/div[@class="inner"]\
												/ul[@class="items g-clearfix"]\
												/li\
												/input\
												') 
			print len(elems)
			elems[0].send_keys(Keys.BACKSPACE + start)
			
			ActionChains(self.driver).move_to_element(elems[0]).perform()
			elems = self.driver.find_elements_by_xpath('//div[@id="mainsrp-sortbar"] \
												/div[@class="m-sortbar"]\
												/div[@class="sort-row"]\
												/div[@class="sort-inner"]\
												/div[@class="prices"]\
												/div[@class="inputs J_LaterHover"]\
												/div[@class="inner"]\
												/ul[@class="items g-clearfix"]\
												/li/button\
												')
			print len(elems)	
			# ActionChains(self.driver).move_to_element(elems[0]).perform()
			
			print elems[0].get_attribute('type')
			try:                       #mouse shall not move to the driver window
				elems[0].click()
			except:
				elems[0].click()
		else:
			elems[rule].click()
		time.sleep(1)
													
	
	def filter_row(self):
		elems = self.driver.find_elements_by_xpath('//div[@id="mainsrp-sortbar"] \
		                                            /div[@class="m-sortbar"]\
													/div[@class="filter-row"]\
													/div[@class="extra"]\
													/a\
													')
		elems[0].click()
	
	def item_inner_scan(self,max_page = 0):
		if max_page == 0:
			max_page = self.max_page_num()
		
		for i in range(max_page):
			self.next_page()
			time.sleep(1)