#!/usr/bin/env python

import sys
import unittest

sys.path.append('gen-py')

from cse124 import Twitter
from cse124.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

class tester(unittest.TestCase):
	def setUp(self):
		self.transport = TSocket.TSocket('169.228.66.135', '6508')
		self.transport = TTransport.TBufferedTransport(self.transport)
		protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
		self.client = Twitter.Client(protocol)
		self.transport.open()
		
	def tearDown(self):
		self.transport.close()

	def test_create_users(self):
		self.client.createUser("sharon")
		self.client.createUser("scott");
		self.client.createUser("andrew")

		try:
			self.client.subscribe("tyler", "sharon")
			self.fail("exception not caught")

		except NoSuchUserException:
			pass

		
	def test_create_existing_users(self):
		self.client.createUser("darren")
		self.client.createUser("ralphie")
		self.client.createUser("jason")
		
		try:	
			self.client.createUser("jason");
			self.fail("exption not thrown")
		
		except AlreadyExistsException:
			pass

	def test_subscribe(self):
		self.client.subscribe("jason", "darren")
		self.client.post("darren", "Tweet 1");
		self.client.post("darren", "Tweet 2");

		l = self.client.readTweetsBySubscription("jason", 2)
		self.assertTrue(len(l) == 2)
		
		l = self.client.readTweetsBySubscription("jason", 5)
		self.assertTrue(len(l) == 2)

		t1 = l[0];
		t2 = l[1];

		self.assertEqual(t1.tweetString, "Tweet 2")
		self.assertEqual(t2.tweetString, "Tweet 1")
		
	def test_subscribe_exception(self):
		self.client.createUser("A")
		try:
			self.client.subscribe("A", "victor")
			self.fail("First Exception not thrown")
		
		except NoSuchUserException:
			pass
		
		try:
			self.client.subscribe("victor", "A")
			self.fail("Second Exception not thrown")
			
		except NoSuchUserException:
			pass
			
	def test_subscribe_to_self(self):
		self.client.subscribe("scott", "scott")
		self.client.post("scott", "tweet 1");
		self.client.post("scott", "tweet 2");

		l = self.client.readTweetsBySubscription("scott", 2)
		self.assertEqual(len(l), 2)

		l = self.client.readTweetsBySubscription("scott", 5)
		self.assertEqual(len(l), 2)
		
		t1 = l[0]
		t2 = l[1]
		
		self.assertEqual(t1.tweetString, "tweet 2")
		self.assertEqual(t2.tweetString, "tweet 1")

	def test_unsubscribe(self):
		self.client.unsubscribe("scott", "scott")
		l = self.client.readTweetsBySubscription("scott", 2)

		self.assertEqual(len(l), 0)
		
		self.client.unsubscribe("jason", "darren")
		l2 = self.client.readTweetsBySubscription("jason", 2)
		self.assertEqual(len(l2), 0)

	def test_unsubscribe_exception(self):
		try:
			self.client.unsubscribe("victor", "jason")
			self.fail("First exception not thrown")

		except:
			pass
		
		try:
			self.client.unsubscribe("jason", "victor")
			self.fail("Second exception not thrown")

		except:
			pass

	def test_unsubscribe_nop(self):
		self.client.createUser("B")
		self.client.createUser("C")

		self.client.post("B", "tweet 1")
		self.client.post("C", "tweet 2")

		self.client.subscribe("B", "B")
		self.client.subscribe("C", "C")

		l = self.client.readTweetsBySubscription("B", 2)
		l2 = self.client.readTweetsBySubscription("C", 2)

		self.assertEqual(len(l), 1)
		self.assertEqual(len(l), 1)

		self.client.unsubscribe("B", "C")
		l = self.client.readTweetsBySubscription("B", 2)
		self.assertEqual(len(l), 1)
		self.client.unsubscribe("C", "B")
		l = self.client.readTweetsBySubscription("C", 2)
		self.assertEqual(len(l), 1)
			
	def test_post(self):
		self.client.post("jason", "Tweet 1")
		self.client.post("jason", "Tweet 2")
		
		l = self.client.readTweetsByUser("jason", 5)
		self.assertEqual(len(l), 2)
		
		self.assertEqual(l[0].tweetString, "Tweet 2")
		self.assertEqual(l[1].tweetString, "Tweet 1")

	def test_post_exception(self):
		try:
			self.client.post("victor", "Tweet 1")
			self.fail("First exception not thrown")

		except NoSuchUserException:
			pass
		
		try:
			self.client.post("thomas", "Tweet")
			self.fail("Second Excpetion not thrown")

		except NoSuchUserException:
			pass
	
		try:
			self.client.post("ralphie", "aijaosjdoasndoandonasodnsoandisadosandosandoisandoisandoisandoisandiosandooinasoidnoiasndoiasndosandoisandoasndoisandoisandoisandoisandoisand aoidnsaoidn iasidon oiasnd asodasod nasd oainsdosa nasdaodnas aaosndonsaodnaodnasodn")
			self.fail("Third Exception not thrown")

		except TweetTooLongException:
			pass

			
	def test_read_tweets_by_users(self):
		self.client.createUser("user1")
		self.client.post("user1", "Tweet 1")
		self.client.post("user1", "Tweet 2")
		self.client.post("user1", "Tweet 3")
		self.client.post("user1", "Tweet 4")

		self.client.post("jason", "Tweet 3")
		self.client.post("jason", "Tweet 4")

		l = self.client.readTweetsByUser("user1", 2)
		self.assertEqual(len(l), 2)
		
		self.assertEqual(l[0].tweetString, "Tweet 4")
		self.assertEqual(l[1].tweetString, "Tweet 3")
		
		l = self.client.readTweetsByUser("jason", 2)
		self.assertEqual(len(l), 2)

		self.assertEqual(l[0].tweetString, "Tweet 4")
		self.assertEqual(l[1].tweetString, "Tweet 3")

		l = self.client.readTweetsByUser("user1", 5)
		self.assertEqual(len(l), 4)

		self.assertEqual(l[0].tweetString, "Tweet 4")
		self.assertEqual(l[1].tweetString, "Tweet 3")
		self.assertEqual(l[2].tweetString, "Tweet 2")
		self.assertEqual(l[3].tweetString, "Tweet 1")

		l = self.client.readTweetsByUser("jason", 5)
		self.assertEqual(len(l), 4)

		self.assertEqual(l[0].tweetString, "Tweet 4")
                self.assertEqual(l[1].tweetString, "Tweet 3")
                self.assertEqual(l[2].tweetString, "Tweet 2")
                self.assertEqual(l[3].tweetString, "Tweet 1")
		
		l = self.client.readTweetsByUser("user1", 0)
		self.assertEqual(len(l), 0)

		l = self.client.readTweetsByUser("user1", -3)
		self.assertEqual(len(l), 0)

			
	def test_read_tweets_by_users_exception(self):
		try:
			self.client.readTweetsByUser("thomas", 3)		
			self.fail("First Exception not thrown")

		except NoSuchUserException:
			pass
		
		try:
			self.client.readTweetsByUser("victor", 2)
			self.fail("Second exception not thrown")

		except NoSuchUserException:
			pass

	def test_read_tweets_by_subscription(self):
		self.client.createUser("newuser1")
		self.client.createUser("newuser2")

		self.client.post("newuser1", "tweet1")
		self.client.post("newuser2", "tweet2")
		self.client.post("newuser2", "tweet3")
		self.client.post("newuser1", "tweet4")

		
		self.client.subscribe("newuser1", "newuser1")
		self.client.subscribe("newuser2", "newuser2")

		l = self.client.readTweetsBySubscription("newuser1", 2)
		l2 = self.client.readTweetsBySubscription("newuser2", 2)

		self.assertEqual(len(l), 2)
		self.assertEqual(len(l2), 2)
		
		self.assertEqual(l[0].tweetString, "tweet4")
		self.assertEqual(l[1].tweetString, "tweet1")

		self.assertEqual(l2[0].tweetString, "tweet3")
		self.assertEqual(l2[1].tweetString, "tweet2")

		l = self.client.readTweetsBySubscription("newuser1", 3)
		l2 = self.client.readTweetsBySubscription("newuser2", 3)

		self.assertEqual(len(l), 2)
		self.assertEqual(len(l2), 2)
		
		self.assertEqual(l[0].tweetString, "tweet4")
		self.assertEqual(l[1].tweetString, "tweet1")

		self.assertEqual(l2[0].tweetString, "tweet3")
		self.assertEqual(l2[1].tweetString, "tweet2")

		self.client.subscribe("newuser1", "newuser2")
		self.client.subscribe("newuser2", "newuser1")

		l = self.client.readTweetsBySubscription("newuser1", 2)
		l2 = self.client.readTweetsBySubscription("newuser2", 2)

		self.assertEqual(len(l), 2)
		self.assertEqual(len(l2), 2)

		self.assertEqual(l[0].tweetString, "tweet4")
		self.assertEqual(l[1].tweetString, "tweet3")

		self.assertEqual(l2[0].tweetString, "tweet4")
		self.assertEqual(l2[1].tweetString, "tweet3")

		l = self.client.readTweetsBySubscription("newuser1", 5)
		l2 = self.client.readTweetsBySubscription("newuser2",5)

		self.assertEqual(len(l), 4)
		self.assertEqual(len(l2), 4)

		self.assertEqual(l[0].tweetString, "tweet4")
		self.assertEqual(l[1].tweetString, "tweet3")
		self.assertEqual(l[2].tweetString, "tweet2")
		self.assertEqual(l[3].tweetString, "tweet1")

		self.assertEqual(l2[0].tweetString, "tweet4")
		self.assertEqual(l2[1].tweetString, "tweet3")
		self.assertEqual(l2[2].tweetString, "tweet2")
		self.assertEqual(l2[3].tweetString, "tweet1")

		l = self.client.readTweetsBySubscription("newuser1", 0)
		l2 = self.client.readTweetsBySubscription("newuser2", 0)

		self.assertEqual(len(l), 0)
		self.assertEqual(len(l2), 0)

		l = self.client.readTweetsBySubscription("newuser1", -1)
		l2 = self.client.readTweetsBySubscription("newuser2", -2)

		self.assertEqual(len(l), 0)
		self.assertEqual(len(l2), 0)

	def test_read_tweets_by_sub_exception(self):
		try:
			self.client.readTweetsBySubscription("newuser4", 3)
			self.fail("Exception should have been thrown")

		except NoSuchUserException:
			pass	
			
		try:
			self.client.readTweetsBySubscription("newuser5", 3)
			self.fail("Exception should have been thrown")
			
		except NoSuchUserException:
			pass
			
	
	def test_rate_tweets(self):
		self.client.createUser("rater")
		self.client.post("rater", "tweet 1")
		self.client.post("rater", "tweet 2")
		self.client.post("rater", "tweet 3")

		l = self.client.readTweetsByUser("rater", 3)
		t1_id = l[0].tweetId
		t2_id = l[1].tweetId
		t3_id = l[2].tweetId

		self.client.star("jason", t1_id)
		self.client.star("scott", t1_id)
		self.client.star("andrew", t1_id)

		self.client.star("sharon", t2_id)
		self.client.star("ralphie", t2_id)

		self.client.star("darren", t3_id)

		l = self.client.readTweetsByUser("rater", 3)
		self.assertEqual(l[0].numStars, 3)
		self.assertEqual(l[1].numStars, 2)
		self.assertEqual(l[2].numStars, 1)

	def test_rate_tweets_exception(self):
		try:
			self.client.star("thomas", 0)
			self.fail("Exception 1 should have been thrown")

		except NoSuchUserException:
			pass

		try:
			self.client.star("victor", 0)
			self.fail("Exception 2 should have been thrown")

		except NoSuchUserException:
			pass

		try:
			self.client.star("jason", 1234567)
			self.fail("exception 3 should have been thrown")

		except NoSuchTweetException:
			pass

		try:
			self.client.star("jason", 6543211)
			self.fail("exception 4 should have been thrown")

		except NoSuchTweetException:
			pass
			
	def test_rate_only_once(self):
		self.client.createUser("rater2")
		self.client.post("rater2", "tweet 1")
		self.client.post("rater2", "tweet 2")
		self.client.post("rater2", "tweet 3")

		l = self.client.readTweetsByUser("rater2", 3)
		t1_id = l[0].tweetId
		t2_id = l[1].tweetId
		t3_id = l[2].tweetId

		self.client.star("jason", t1_id)
		self.client.star("jason", t1_id)
		self.client.star("scott", t1_id)
		self.client.star("andrew", t1_id)

		self.client.star("ralphie", t2_id)
		self.client.star("ralphie", t2_id)
		self.client.star("darren", t2_id)

		self.client.star("sharon", t3_id)
		self.client.star("sharon", t3_id)

		l = self.client.readTweetsByUser("rater2", 3)
		self.assertEqual(l[0].numStars, 3)
		self.assertEqual(l[1].numStars, 2)
		self.assertEqual(l[2].numStars, 1)


if __name__ == '__main__': 
	unittest.main()
