import requests
import datetime

class Yahoo_finance:

	def __init__(self,token,host):
		self.base_url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2"
		self.headers = {'x-rapidapi-key': token, 'x-rapidapi-host':host}


	def get_chart(self,symbol,interval,data_range,region="US"):
		url = self.base_url + '/get-chart'
		print(f'url = {url}')
		querystring = {'symbol':symbol,'interval':interval,'range':data_range,'region':region}
		return requests.request('GET',url,params=querystring,headers=self.headers).json()


class Candle:

	def __init__(self,high,low,opens,close,vol,date):
		self.high = high
		self.low = low
		self.open = opens
		self.close = close
		self.vol = vol
		#save date as timestamp
		self.date = date

	def __eq__(self,other):
		if isinstance(other,Candle):
			return (self.high==other.high and self.low==other.low  and self.open==other.open and self.close==other.close and self.date==other.date and self.vol==other.vol)
		return False

	def __repr__(self):
		return f"this is candle of {datetime.datetime.fromtimestamp(self.date)} with close price of {self.close}"