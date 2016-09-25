# -*- coding:utf-8 -*-
import pandas as pd
import MySQLdb as mysql
import numpy as np
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ctrl():
	def __init__(self):
		# self.targets = ['女装','男装','内衣','鞋靴','箱包','帽子','配饰','童装','宠物服饰','玩具','奶食','数码','家电','手机','手机配件','美妆','洗护','保健品','珠宝','眼镜','手表','运动','户外','乐器','游戏','动漫','周边','宠物用品','孕产妇用品','保健用品','汽车用品','家饰','家纺','办公','DIY','五金','电子','百货','餐具','厨具','学习']
		self.cate = '美妆'
		self.targets = ['面膜','洁面','防晒','爽肤水','眼霜','乳液','面霜','精华','卸妆','男士护肤','眼线','粉底液','BB霜','隔离','睫毛膏','彩妆盘','唇膏','腮红','香水','精油','身体护理','丰胸','纤体','脱毛']
		self.db = mysql.connect(host="127.0.0.1", user="root", passwd="238159", db="taobao",charset="utf8")
		self.cursor = self.db.cursor()
		
	def run(self): 
		print len(self.targets)
		for target in self.targets:
			table_name = unicode(target,'utf-8')
			print table_name
			
			new_table_name = unicode(self.cate + '_' + target,'utf-8')
			print new_table_name
			
			SQL = 'alter table ' + table_name + ' rename ' + new_table_name;
			self.cursor.execute(SQL)
			
			# SQL = 'alter table '+table_name+' add column capture_time varchar(255)'
			# self.cursor.execute(SQL)
			# SQL = 'update '+table_name+' set capture_time = "2016-09-20"'
			# self.cursor.execute(SQL) 
			
			# SQL = 'alter table '+table_name+' add column income float'
			# self.cursor.execute(SQL)
			# SQL = 'update '+table_name+' set income = deal_cnt*price'
			# self.cursor.execute(SQL) 
			# SQL = 'alter table '+table_name+' add column cate_1 varchar(255)'
			# self.cursor.execute(SQL)
			# SQL = 'update '+table_name+' set cate_1 = "' + table_name + '"'
			# self.cursor.execute(SQL)
			# SQL = 'alter table '+table_name+' add column cate_2 varchar(255)'
			# self.cursor.execute(SQL)
			# SQL = 'alter table '+table_name+' add column cate_3 varchar(255)'
			# self.cursor.execute(SQL)