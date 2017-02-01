import urllib2
import cookielib

cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
urllib2.install_opener(opener)

class MyOpener(object):
	def __init__(self, inner):
		self.inner = inner

	def request(self, url, method, **params):
		print '>>> %s' % url
		headers = {
		    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
		}
		req = urllib2.Request(
		    url = url,
		    # data = postdata,
		    headers = headers
		)
		resp = self.inner.open(req)
		try:
			data = resp.read()
		finally:
			resp.close()

		return data

	def get(self, url):
		return self.request(url, 'GET')

def new_opener():
	cookie = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
	return MyOpener(opener)

def request(url, method, **params):
	print '>>> %s' % url
	headers = {
	    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
	}
	req = urllib2.Request(
	    url = url,
	    # data = postdata,
	    headers = headers
	)
	resp = urllib2.urlopen(req)
	try:
		data = resp.read()
	finally:
		resp.close()

	return data

def get(url):
	return request(url, 'GET')

if __name__ == '__main__':
	print get('http://xueqiu.com')
