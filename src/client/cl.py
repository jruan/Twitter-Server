#!/usr/bin/env python

import sys
import argparse

sys.path.append('gen-py')

from cse124 import Twitter
from cse124.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


server = ""
port = ""
parameters = []
method = ""

def invoke_method():
	try:
		transport = TSocket.TSocket(server, port)
		transport = TTransport.TBufferedTransport(transport)
		
		protocol = TBinaryProtocol.TBinaryProtocol(transport)
		client = Twitter.Client(protocol)

		transport.open()
		
		if method == "createUser":
			client.createUser(parameters[0])
			print 'None'

		elif method == "subscribe":
			client.subscribe(parameters[0], parameters[1])
			print 'None'

		elif method == "unsubscribe":
			client.unsubscribe(parameters[0], parameters[1])
			print 'None'

		elif method == "post":
			client.post(parameters[0], parameters[1])
			print 'None'

		elif method == "readTweetsByUser":
			l = client.readTweetsByUser(parameters[0], int(parameters[1]))
			print l

		elif method == "readTweetsBySubscription":
			l = client.readTweetsBySubscription(parameters[0], int(parameters[1]))
			print l

		elif method == "star":
			client.star(parameters[0], long(parameters[1]))
			print 'None'
	
		transport.close() 

	except AlreadyExistsException, userx:
		print 'AlreadyExistesException for user ' + parameters[0]
		return 'AlreadyExistsException'

	except NoSuchUserException:
		print 'NoSuchUserException'
		return 'NoSuchUserException'

	except TweetTooLongException:
		print 'TweetTooLongException'
		return 'TweetTooLongException'

	except NoSuchTweetException:
		print 'NoSuchTweetException'
		return 'NoSuchTweetException'

	except Thrift.TException, tx:
		return '%s' & (tx.message)

	except Exception, users:
		return 'ERROR: %s' %(userx)
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Twitter Client")
	parser.add_argument("host", action = "store", help = "server:port", default="localhost:9090")
	parser.add_argument("method", action = "store", help = "method to invoke")
	parser.add_argument("parameters", action = "store", help ="parameter for method", nargs = '+',
			    metavar = 'S')

	args = parser.parse_args()
	server,port = args.host.split(':')
	method = args.method
	parameters = args.parameters

	invoke_method()
#except Thrift.TException, tx:
 # print '%s' % (tx.message)
