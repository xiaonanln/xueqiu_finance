# coding: utf8

import sys
import time
import urllib
import re
import json
import web_utils


XUEQIU_COM = 'https://xueqiu.com'


_visitedXueqiuComOnce = False

def visitXueqiuComOnce():
	global _visitedXueqiuComOnce
	if _visitedXueqiuComOnce:
		return 

	web_utils.get(XUEQIU_COM)
	_visitedXueqiuComOnce = True


def getQuotes(symbol):
	visitXueqiuComOnce()
	symbol = symbol.upper()
	url = XUEQIU_COM + '/v4/stock/quote.json?code=%s&_=%d' % (symbol, int(time.time()*1000))

	print >>sys.stderr, 'REQUEST %s' % url
	data = web_utils.get(url)
	data = json.loads(data, encoding='utf8')
	return data [symbol]

def getStockList(symbol):
	visitXueqiuComOnce()
	symbol = symbol.upper()
	url = XUEQIU_COM + '/stock/forchartk/stocklist.json?symbol=SPY&period=1minute&type=before&begin=0&end=9999999999999'

	data = web_utils.get(url)
	data = json.loads(data, encoding='utf8')
	return data ['chartlist']


def parseVolume(v):
	return int(float(v) )

def getVolume(data):
	vk = 'volume'
	if vk not in data:
		return None

	return parseVolume(data[vk])

if __name__ == '__main__':
	quotes = getQuotes('SPY')
	for k, v in quotes.iteritems():
		print >>sys.stderr, '>>>', k, '=', v.encode('utf8')
	vol = quotes['volume']
	print >>sys.stderr, 'Volume', parseVolume(vol), getVolume(quotes)

	print 'QQQ', getQuotes('QQQ')

	stockList = getStockList('SPY')
	print len(stockList), stockList[0], stockList[-1]
