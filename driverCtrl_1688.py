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

class driverCtrl_1688(dc.driverCtrl):
	def __init__(self,proxy_ip='',webdrv=''):
		self.open_web_driver(proxy_ip=proxy_ip,webdrv=webdrv)
		self.open_web()
		
	def open_web(self):
		url = "http://www.1688.com"
		self.driver.get(url)

	def search(self,string):
		search_key = string
		elems = self.driver.find_elements_by_xpath('//input[@id="alisearch-keywords"]')
		##print len(elems)
		elems[0].send_keys(Keys.BACKSPACE + search_key + Keys.RETURN)
		time.sleep(1)
		
		elems = self.driver.find_elements_by_xpath('//button[@id="alisearch-submit"]')
		try:
			elems[0].click()
			time.sleep(1)
		except:
			print 'no total link'
			
		self.sort_row(rule = 2)
		time.sleep(1)

		
		js="var q=document.body.scrollTop=100000"
		self.driver.execute_script(js)
		time.sleep(2)
		content = self.driver.page_source.encode('utf-8')
		url     = self.driver.current_url.encode('utf-8')
		return [content,url]
	
	def max_page_num(self):
		elems = self.driver.find_elements_by_xpath('//em[@class="fui-paging-num"]')
		string = elems[0].text
		return int(string)
	
	def next_page(self):
		elems = self.driver.find_elements_by_xpath('//a[@class="fui-next"]')
		print "next page:",len(elems)
		retry_cnt = 0
		while retry_cnt != 3:
			try:
				ActionChains(self.driver).move_to_element(elems[0]).perform()
				time.sleep(0.5)
				elems[0].click()
				time.sleep(0.5)
				retry_cnt = 3
			except:
				retry_cnt = retry_cnt + 1
				print 'next_page retry ',retry_cnt
		try:		
			time.sleep(1)	
			elems = self.driver.find_elements_by_xpath('//a[@class="fui-next"]')
			ActionChains(self.driver).move_to_element(elems[0]).perform()
			# js="var q=document.body.scrollTop=100000"
			# self.driver.execute_script(js)
		except:
			print 'none next page'
		time.sleep(1)
		content = self.driver.page_source.encode('utf-8')
		url     = self.driver.current_url.encode('utf-8')
		return [content,url]
	
	# 0:综合 1：人气 2：销量 3：信用 4：价格
	def sort_row(self,rule = 0):				
		elems = self.driver.find_elements_by_xpath('//div[@id="sm-filtbar"]\
													/div[@class="sm-widget-bar"]\
													/div\
													/div[@class="filtItems"]\
													/ul/li\
													/a\
													')
		
		print 'sort cnt:',len(elems)
		elems[1].click()
		time.sleep(1)
	
												
	def item_inner_scan(self,max_page = 0):
		if max_page == 0:
			max_page = self.max_page_num()
		
		for i in range(max_page):
			self.next_page()
			time.sleep(1)