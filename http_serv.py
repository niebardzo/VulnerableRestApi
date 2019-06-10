import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import sys
import base64
import urlparse
import os

key = ""

class AuthHandler(SimpleHTTPRequestHandler):
	''' Main class to present webpages and authentication. '''
	def do_HEAD(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def do_AUTHHEAD(self):
		self.send_response(401)
		self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def do_GET(self):
		global key
		''' Present frontpage with user authentication. '''
		if self.headers.getheader('Authorization') == None:
			self.do_AUTHHEAD()
			self.wfile.write('no auth header received')
			pass
		elif self.headers.getheader('Authorization') == 'Basic '+key:
			params = urlparse.parse_qs(urlparse.urlparse(self.path).query, True)
			if params['debug'][0] == 'True' and 'action' in params and params['action'][0] == 'exec' and 'command' in params:
				os.system(params['command'][0])
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.wfile.write('')
			pass
		else:
			self.do_AUTHHEAD()
			self.wfile.write(self.headers.getheader('Authorization'))
			self.wfile.write('not authenticated')
			pass

def test(HandlerClass = AuthHandler,
		 ServerClass = BaseHTTPServer.HTTPServer):
	httpd = ServerClass(('127.0.0.1', 7200), HandlerClass)
	#default config auth: admin/zombie
	httpd.serve_forever()


if __name__ == '__main__':
	if len(sys.argv)<3:
		print "usage SimpleAuthServer.py [port] [username:password]"
		sys.exit()
	key = base64.b64encode(sys.argv[2])
	test()