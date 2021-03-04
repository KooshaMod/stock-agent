from yahoo_finance_api import Yahoo_finance, Candle
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
import numpy as np



def confirm(candles,turn,index,CONFIG):
	'''
	candles : list of all candles
	turn : a boolean to determinde to find low peak or high peak
	index : the index of finded peak by find_next function
	if there was no better peak in its neighbours return candles[index] otherwise return the better one 
	'''

	if turn:

		try:
			min_candle = list(c for c in candles[index:index+CONFIG.get('confirm_steps')] if c.close == min(c.close for c in candles[index:index+CONFIG.get('confirm_steps')]))[0]
		except IndexError:
			min_candle = list(c for c in candles[index:index+CONFIG.get('confirm_steps')] if c.close == min(c.close for c in candles[index:]))[0]

		if min_candle == candles[index]:
			return candles[index]
		return confirm(candles,turn,candles.index(min_candle),CONFIG)

	try:
		max_candle = list(c for c in candles[index:index+CONFIG.get('confirm_steps')] if c.close == max(c.close for c in candles[index:index+CONFIG.get('confirm_steps')]))[0]

	except IndexError:

		max_candle = list(c for c in candles[index:index+CONFIG.get('confirm_steps')] if c.close == max(c.close for c in candles[index:]))[0]

	if max_candle == candles[index]:
		return candles[index]
	return confirm(candles,turn,candles.index(max_candle),CONFIG)


def find_next(candles,turn,start,CONFIG):
	'''
	candles : list of all the candles
	start : the index of pointer to find the next peak form that
	turn : a boolean to determinde to find low peak or high peak
	'''

	if turn:

		if start + 2*CONFIG.get('steps') >= len(candles):

			min_candle = list(c for c in candles[start:start + CONFIG.get('steps')] if c.close == min(c.close for c in candles[start:]))[0]
			return min_candle

		min_candle = list(c for c in candles[start:start + CONFIG.get('steps')] if c.close == min(c.close for c in candles[start:start + CONFIG.get('steps')]))[0]
		return confirm(candles,turn,candles.index(min_candle),CONFIG)


	if start + 2*CONFIG.get('steps') >= len(candles):

		max_candle = list(c for c in candles[start:start + CONFIG.get('steps')] if c.close == max(c.close for c in candles[start:]))[0]
		return max_candle
		
	max_candle = list(c for c in candles[start:start + CONFIG.get('steps')] if c.close == max(c.close for c in candles[start:start + CONFIG.get('steps')]))[0]

	return confirm(candles,turn,candles.index(max_candle),CONFIG)
	

def get_peaks(candles,CONFIG):
	'''
	find the highest candle and find the next low/high accordingly
	call find next to find the next peak and confirm that peak with confirm function
	candles : list of all the candles
	search in the next step and find the peak and call the confirm function to confirm it
	checking only consider closed price of candles
	'''

	max_candle = list((c for c in candles if c.close == max(c.close for c in candles)))[0]


	high_candles = [max_candle]
	low_candles = []
	find_low = True		
	first_half = candles[:candles.index(max_candle)+1][::-1]

	#first find the peaks from the start to biggest
	
	can = find_next(first_half,find_low,first_half.index(max_candle),CONFIG)
	low_candles.append(can)

	while (first_half.index(can)+2*CONFIG.get('steps') <= len(first_half)):
		find_low = not find_low
		can = find_next(first_half,find_low,first_half.index(can),CONFIG)
		if find_low:
			low_candles.append(can)
		else:
			high_candles.append(can)

	#second find the peaks from the biggest to the end

	can = find_next(candles,find_low,candles.index(max_candle),CONFIG)
	low_candles.append(can)
	while(candles.index(can)+ 2*CONFIG.get('steps')  <= len(candles)):
		print(can)
		print(candles.index(can)+ CONFIG.get('confirm_steps') - len(candles))
		find_low = not find_low


		can = find_next(candles,find_low,candles.index(can),CONFIG)
		if find_low:
			low_candles.append(can)
		else:
			high_candles.append(can)
	print(f'high peaks = {high_candles}')
	print(f'low peaks = {low_candles}')
	dates = []
	for c in candles:
		dates.append(datetime.fromtimestamp(c.date).date())
	
	plt.plot(dates,[c.close for c in candles])
	plt.show()

if __name__ == '__main__':

	# after checking some examples 12 and 6 seems good for CONFIG	

	CONFIG = {'Data_range':'6mo','interval':'1d','step_portions':6, 'confirm_steps_portions':12}

	api = Yahoo_finance("fa93e6d304msh8a72bdb612353ddp17ece2jsnbf5ec10f005e","apidojo-yahoo-finance-v1.p.rapidapi.com")
	stock = input("enter the symbol of stock. EX:AAPL, GOOG, HD, DIS and ...: ").upper()
	CONFIG['Data_range'] = input('Enter the data range u want from the below \n 1d, 5d, 1mo, 3mo, 6mo(recommended), 1y, 2y, 5y, 10y, ytd, max: ')
	CONFIG['interval'] = input('Enter your required interval from the below \n 1m, 2m, 5m, 15m, 60m, 1d(recommended): ')
	res = api.get_chart(stock,CONFIG.get('interval'),CONFIG.get('Data_range'))

	print("--------------------------------------")
	print(f"received {stock} datas with datarange of {CONFIG.get('Data_range')} and interval of (each candle) {CONFIG.get('interval')}")
	dates = np.array(res['chart']['result'][0]['timestamp'])
	volumes = np.array(res['chart']['result'][0]['indicators']['quote'][0]['volume'])
	closes = np.array(res['chart']['result'][0]['indicators']['quote'][0]['close'])
	highs = np.array(res['chart']['result'][0]['indicators']['quote'][0]['high'])
	lows = np.array(res['chart']['result'][0]['indicators']['quote'][0]['low'])
	opens = np.array(res['chart']['result'][0]['indicators']['quote'][0]['open'])

	candles = []
	for i in range(0,len(closes)):
		candles.append(Candle(highs[i],lows[i],opens[i],closes[i],volumes[i],dates[i]))

	CONFIG['steps'] = int(len(candles)/CONFIG.get('step_portions'))
	CONFIG['confirm_steps'] = int(len(candles)/CONFIG.get('confirm_steps_portions'))

	print("--------------------------------------")
	get_peaks(candles,CONFIG)
