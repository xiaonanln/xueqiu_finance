# coding: utf8

import sys
import urllib
import re
import web_utils


XUEQIU_COM = 'https://xueqiu.com'


_visitedXueqiuComOnce = False

def visitXueqiuComOnce():
	global _visitedXueqiuComOnce
	if _visitedXueqiuComOnce:
		return 

	web_utils.get(XUEQIU_COM)
	_visitedXueqiuComOnce = True


QUOTES_PATTERN = re.compile('<td.*?>(.*?)<span.*?>(.*?)</span></td>')

def getQuotes(symbol):
	visitXueqiuComOnce()

	url = XUEQIU_COM + '/S/%s' % symbol.upper()
	print >>sys.stderr, 'REQUEST %s' % url
	data = web_utils.get(url)
	# <td>50日均线：<span>226.49</span></td>

	quotes = {}
	for m in QUOTES_PATTERN.findall(data):
		k, v = m[0], m[1]
		k = unicode(k, 'utf8')
		v = unicode(v, 'utf8')
		if k.endswith(u'：'):
			k = k[:-1]

		print >>sys.stderr, '>', k.encode('utf8'), '=', v.encode('utf8')
		quotes[k] = v

	return quotes

def parseVolume(v):
	if v.endswith(u'股'):
		v = v[:-1]

	factor = 1
	while v.endswith(u'万'):
		v = v[:-1]
		factor *= 10000

	return int(float(v) * factor)

def getVolume(data):
	vk = u'成交量'
	if vk not in data:
		return None

	return parseVolume(data[vk])

if __name__ == '__main__':
	quotes = getQuotes('SPY')
	vol = quotes[u'成交量']
	print 'Volume', parseVolume(vol), getVolume(quotes)
