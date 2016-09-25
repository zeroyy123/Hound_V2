# -*- coding:utf-8 -*-
import pageDetail
import driverCtrl as dc
import spiderTB
import spider1688
import tc_mysql_ctrl
import pandas as pd
import time 


if __name__ == '__main__':
	# TB = spiderTB.spiderTB()
	# TB.run()
	
	TB = spider1688.spider1688()
	TB.run()
	
	# TC = tc_mysql_ctrl.ctrl()
	# TC.run()
