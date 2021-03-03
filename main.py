from yahoo_finance_api import Yahoo_finance, Candle
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
import numpy as np

class resault:
	'''
	everytime we call findnext and confirm return the candle with the last index we checked
	'''
	def __init__(self,candle,pointer):
		self.candle = candle
		self.pointer = pointer


def confirm(candles,turn,index,CONFIG):
	print(f'----------in cinfirm------------- \n index = {index}')
	if turn:
		print(candles[index:index+CONFIG.get('confirm_steps')])
		try:
			min_candle = list(c for c in candles if c.close == min(c.close for c in candles[index:index+CONFIG.get('confirm_steps')]))[0]
		except IndexError:
			print('find min in except')
			min_candle = list(c for c in candles if c.close == min(c.close for c in candles[index:]))[0]
		if min_candle == candles[index]:
			return candles[index]
		return confirm(candles,turn,candles.index(min_candle),CONFIG)

	try:
		max_candle = list(c for c in candles if c.close == max(c.close for c in candles[index:index+CONFIG.get('confirm_steps')]))[0]
	except IndexError:
		max_candle = list(c for c in candles if c.close == max(c.close for c in candles[index:]))[0]
	if max_candle == candles[index]:
		return candles[index]
	return confirm(candles,turn,candles.index(max_candle),CONFIG)


def find_next(candles,turn,start,CONFIG):
	if turn:
		if start + 2*CONFIG.get('steps') >= len(candles):
			min_candle = list(c for c in candles if c.close == min(c.close for c in candles[start:]))[0]
			return min_candle
		
		min_candle = list(c for c in candles if c.close == min(c.close for c in candles[start:start + CONFIG.get('steps')]))[0]
		print(f'calling confrim func with index of {candles.index(min_candle)} >>> {min_candle}')
		return confirm(candles,turn,candles.index(min_candle),CONFIG)


	if start + 2*CONFIG.get('steps') >= len(candles):
		max_candle = list(c for c in candles if c.close == max(c.close for c in candles[start:]))[0]
		return max_candle
		
	max_candle = list(c for c in candles if c.close == max(c.close for c in candles[start:start + CONFIG.get('steps')]))[0]
	return confirm(candles,turn,candles.index(max_candle),CONFIG)
	

def get_peaks(candles,CONFIG):
	'''
	start from the beginning and check 1 step and then chech confirm steps to 
	'''
	max_candle = list((c for c in candles if c.close == max(c.close for c in candles)))[0]
	high_candles = [max_candle]
	find_low = True
	p = candles.index(max_candle)
	print(f'max candle = {max_candle}')
	can = find_next(candles,find_low,p,CONFIG)
	
	print(f'find next low : {can}')

	dates = []
	for c in candles:
		dates.append(datetime.fromtimestamp(c.date).date())
	print(len(dates))
	xaxis = dates
	plt.plot(xaxis,highs)
	plt.show()

if __name__ == '__main__':
	CONFIG = {'Data_range':'6mo','interval':'1d','steps':20,'confirm_steps':5}
	api = Yahoo_finance("fa93e6d304msh8a72bdb612353ddp17ece2jsnbf5ec10f005e","apidojo-yahoo-finance-v1.p.rapidapi.com")
	res = api.get_chart('AAPL',CONFIG.get('interval'),CONFIG.get('Data_range'))
	print('resonce resieved')
	dates = np.array(res['chart']['result'][0]['timestamp'])
	volumes = np.array(res['chart']['result'][0]['indicators']['quote'][0]['volume'])
	closes = np.array(res['chart']['result'][0]['indicators']['quote'][0]['close'])
	highs = np.array(res['chart']['result'][0]['indicators']['quote'][0]['high'])
	lows = np.array(res['chart']['result'][0]['indicators']['quote'][0]['low'])
	opens = np.array(res['chart']['result'][0]['indicators']['quote'][0]['open'])
	candles = []
	for i in range(0,len(closes)):
		candles.append(Candle(highs[i],lows[i],opens[i],closes[i],volumes[i],dates[i]))
	# print(candles)
	# print(len(candles))
	# print('---------')
	print([c.close for c in candles])
	print("----------------------------")
	get_peaks(candles,CONFIG)
