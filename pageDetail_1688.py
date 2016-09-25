# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re


class pageDetail_1688():
	def __init__(self,response):
		self.response = response
		try:
			self.soup= BeautifulSoup(response, "html.parser")
		except Exception,e:
			print '###################################################################################'
			print Exception,":",e
	
	def get_items_data(self,get_other_en=0):
		# if get_other_en == 0:
		elems = self.get_items() 
		for i in range(len(elems)):
			item = self.get_item_data(elems[i])
			if i == 0:
				items = item
			else:
				items = items.append(item)
		return items
	
	def get_item_data(self,elem):
		[price,income]             = self.get_items_row_1(elem)
		[title]                    = self.get_items_row_2(elem)
		[shop_name,memberid,offerid]    = self.get_items_row_3(elem)

		
		item = pd.DataFrame({'title':[title],
							 'ID':[offerid],
							 'price':[price],
							 'shop_id':[memberid],
							 'shop':[shop_name],
							 'income':[income]
							})
		return item
	
	def get_items(self):
		try:
			elems = self.soup.find_all('ul',id='sm-offer-list')
			print 'ul:',len(elems)			
			# elems = elems[0].find_all('div',class_='items g-clearfix')
			elems_temp = elems[0].find_all('li')
			# print 'li:',len(elems_temp)
			elems = []
			for i in range(len(elems_temp)):
				rank = elems_temp[i].get('t-rank')
				try:
					rank = elems_temp[i].get('t-rank')
					if type(rank) == unicode:
						elems.append(elems_temp[i])
				except:
					print 'li: null'
		except:
			print 'get items fail'
		
		print 'totals len: ',len(elems)
		return elems
		
	def get_items_row_1(self,elem):
		row_1 = elem.find_all('div',class_='s-widget-offershopwindowprice sm-offer-price sw-dpl-offer-price')
		try:
			price = row_1[0].find_all('span',class_='sm-offer-priceNum sw-dpl-offer-priceNum')
			price = price[0].get('title')
			price = float(price.replace('¥',''))
		except:
			price = 1000000.0
			print 'get price fail'
		
		try:
			income = row_1[0].find_all('span',class_='sm-offer-trade sw-dpl-offer-trade sm-offer-tradeBt')
			income = income[0].get('title')
		except:
			income = ''
			print 'get income fail'
		
		return [price,income]
	
	def get_items_row_2(self,elem):
		row_2 = elem.find_all('div',class_='s-widget-offershopwindowtitle sm-offer-title sw-dpl-offer-title')
		try:
			title = row_2[0].find_all('a')
			for i in range(len(title)):
				if title[i].get('offer-stat') == 'title':
					title = title[i].get('title')
		except:
			print 'get title fail'
			
		return [title]
	
	def get_items_row_3(self,elem):
		row_3 = elem.find_all('div',class_='s-widget-offershopwindowcompanyinfo sm-offer-company sw-dpl-offer-company')

		try:
			shop = row_3[0].find_all('a')
			for i in range(len(shop)):
				if shop[i].get('offer-stat') == 'com':
					item = shop[i]
			shop_name = item.get('title')
			
			memberid = item.get('memberid')
			offerid  = float(item.get('offerid'))
		except:
			offerid = 0
			memberid = ''
			shop_name  = ''
			print 'get shop or shop id fail'
			
		return [shop_name,memberid,offerid]
		
	def get_items_row_4(self,elem):
		row_4 = elem.find_all('div',class_='row row-4 g-clearfix') 
		
		sametype = '1家店铺在售'
		try:
			li = row_4[0].find_all('ul',class_='icons')
			
			# sametype = li[0].find_all('li',class_='samestyle')
			# sametype = sametype[0].find_all('a')
			# sametype = sametype[0].text
			sametype = 'null'
			
			li = li[0].find_all('li',class_='icon ')
			# print 'icons cnt:',len(li)
		except:
			sametype = 'null'
			print 'get icons cnt fail'
		icons = ''
		
		if len(li) != 0:
			try:
				for i in range(len(li)):
					icon = li[i].find_all('span')
					icon = icon[0].get('class')
					icon = icon[0]
					icon = icon.split('-')
					icon = icon[2]
					icons = icons + ' ' + icon
			except:
				icons = ''
				# print 'get icons fail'
		return [icons,sametype]
		