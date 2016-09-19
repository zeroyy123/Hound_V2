# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re


class pageDetail():
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
		[price,deal_cnt,ship_free] = self.get_items_row_1(elem)
		[title,ID]                 = self.get_items_row_2(elem)
		[shop_id,shop,location]    = self.get_items_row_3(elem)
		[icons,sametype]           = self.get_items_row_4(elem)
		
		item = pd.DataFrame({'title':[title],
							 'ID':[ID],
							 'price':[price],
							 'deal_cnt':[deal_cnt],
							 'ship_free':[ship_free],
							 'shop_id':[shop_id],
							 'shop':[shop],
							 'location':[location],
							 'icons':[icons],
							 'sametype':[sametype]
							})
		return item
	
	def get_items(self,get_other_en = 0):
		try:
			# elems = self.soup.find_all('div',class_='grid-left')
			# print 'li:',len(elems)
			# elems = elems[1].find_all('div',id='mainsrp-itemlist')
			elems = self.soup.find_all('div',id='mainsrp-itemlist')
			# print 'li:',len(elems)			
			# elems = elems[0].find_all('div',class_='items g-clearfix')
			elems = elems[0].find_all('div',class_='grid g-clearfix')
			
			
			elems = elems[0].find_all('div',class_='item J_MouserOnverReq  ')
			print 'li:',len(elems)
		except:
			print 'get items fail'
		
		if get_other_en == 1:
			try:
				other = self.soup.find_all('div',class_='m-widget-shopinfo')
			except:
				print 'get other information fail'
			
			return [elems,other]
		else:
			return elems
		
	def get_items_row_1(self,elem):
		row_1 = elem.find_all('div',class_='row row-1 g-clearfix')
		
		try:
			price = row_1[0].find_all('div',class_='price g_price g_price-highlight')
			price = price[0].find_all('strong')
			price = np.float64(price[0].text)
		except:
			print 'get price fail'
		
		try:
			deal_cnt = row_1[0].find_all('div',class_='deal-cnt')
			deal_cnt = deal_cnt[0].text
			# deal_cnt = deal_cnt.split('人')
			deal_cnt = deal_cnt.split(unicode('人','utf-8'))
			deal_cnt = int(deal_cnt[0])
		except:
			deal_cnt = 0
			print 'get deal cnt fail'
		
		ship_free = row_1[0].find_all('div',class_='ship icon-service-free')
		if len(ship_free) == 1:
			ship_free = 'yes'
		else:
			ship_free = 'no'
		return [price,deal_cnt,ship_free]
	
	def get_items_row_2(self,elem):
		row_2 = elem.find_all('div',class_='row row-2 title')
		try:
			title = row_2[0].find_all('a')
			title = title[0].text
			title = title.replace('\n','')
			title = title.replace(u'\xa0','')
			title = title.replace(u'\u2200','')
			title = title.replace(u'\xe4','')
			title = title.replace(' ','')
		except:
			print 'get title fail'
	
		
		try:
			ID = row_2[0].find_all('a')
			ID = int(ID[0].get('data-nid'))
		except: 
			ID = 0
			print 'get ID fail'
			
		return [title,ID]
	
	def get_items_row_3(self,elem):
		row_3 = elem.find_all('div',class_='row row-3 g-clearfix')
		
		try:
			shop = row_3[0].find_all('div',class_='shop')
			shop = shop[0].find_all('a')
			shop_id = float(shop[0].get('data-userid'))
			
			shop = shop[0].find_all('span')
			shop = shop[4].text
		except:
			shop_id = 0
			shop    = 0
			print 'get shop or shop id fail'
		
		try:
			location = row_3[0].find_all('div',class_='location')
			location = location[0].text
		except:
			print 'get location fail'
			
		return [shop_id,shop,location]
		
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
		