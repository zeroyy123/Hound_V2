# -*- coding:utf-8 -*-
import driverCtrl_tb as dc_tb
import pageDetail
import driverCtrl as dc
import spiderTB
import tc_mysql_ctrl
import pandas as pd
import time 


if __name__ == '__main__':
	# TB = spiderTB.spiderTB()
	# TB.run()
	
	TC = tc_mysql_ctrl.ctrl()
	TC.run()
