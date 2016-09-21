# -*- coding:utf-8 -*-
import driverCtrl_tb as dc_tb
import pageDetail
import driverCtrl as dc
import MysqlDriver as MD 
import pandas as pd
import time 


class spiderTB():
	def __init__(self):
		# self.targets = ['女装','男装','内衣','鞋靴','箱包','帽子','配饰','童装','宠物服饰','玩具','奶食','数码','家电','手机','手机配件','美妆','洗护','保健品','珠宝','眼镜','手表','运动','户外','乐器','游戏','动漫','周边','宠物用品','孕产妇用品','保健用品','汽车用品','家饰','家纺','办公','DIY','五金','电子','百货','餐具','厨具','学习']
		
		self.cate = '配饰'
		#'帽子','围巾','丝巾','披肩','腰带','假领','手套','项链','手链','毛衣链','锁骨链','DIY饰品','发饰','耳饰','耳钉','戒指','吊坠','手串','手镯','胸针','头饰','对戒','首饰收纳'
		self.targets = ['帽子','围巾','丝巾','披肩','腰带','假领','手套','项链','手链','毛衣链','锁骨链','DIY饰品','发饰','耳饰','耳钉','戒指','吊坠','手串','手镯','胸针','头饰','对戒','首饰收纳']
		# self.path = U'D:/Python27/py/Hound_V2/'
		self.path = U'F:/GitHub/Hound_V2/'
		self.Mysql = MD.MysqlDriver()
	
	def crawl(self,DC,target):
		print unicode(target,'utf-8')
		[response,url] = DC.search(unicode(target,'utf-8'))
		max_page = DC.max_page_num()
		print max_page
		for i in range(max_page):
			print 'page: ',i+1
			page = pageDetail.pageDetail(response)
			items = page.get_items_data()
			if i == 0:
				df = items
			else:
				df = df.append(items)
			if i != max_page-1:	
				[response,url] = DC.next_page()
			time.sleep(1)
			
		df['capture_time'] = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		df['income'] = df['deal_cnt']*df['price']
		df['cate_1'] = unicode(self.cate,'utf-8')
		df['cate_2'] = unicode(target,'utf-8')
		df['cate_3'] = 'Null'
		
		print df
		df.to_csv(self.path+'data/'+unicode(target,'utf-8')+'.csv',encoding='utf-8')
		df = pd.read_csv(self.path+'data/'+unicode(target,'utf-8')+'.csv',encoding='utf-8')
		del df['Unnamed: 0']
		self.Mysql.create_table(table_name=unicode(target,'utf-8'),df=df)
		self.Mysql.insert_data(table_name=unicode(target,'utf-8'),df=df)
	
	
	def run(self):
		for target in self.targets:
			# DC = dc_tb.driverCtrl_tb(webdrv='PhantomJS')
			try:
				df =  pd.read_csv(self.path+'data/'+unicode(target,'utf-8')+'.csv',encoding='utf-8')
			except:
				print unicode(target,'utf-8')
				DC = dc_tb.driverCtrl_tb()
				# self.crawl(DC=DC,target=target)
				try:
					self.crawl(DC=DC,target=target)
				except:
					print 'crawl fail: ',target
					try:
						df = pd.read(self.path+ 'fail_log.csv',encoding='utf-8')
						del df['Unnamed: 0']
						df = df.append(pd.DataFrame({'name':[target]}))
						df.to_csv(self.path+ 'fail_log.csv',encoding='utf-8')
					except:
						df = pd.DataFrame({'name':[target]})
						df.to_csv(self.path+ 'fail_log.csv',encoding='utf-8')
				DC.driver_quit()
			
			
	