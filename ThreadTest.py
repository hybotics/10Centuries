#!/usr/bin/env python3
import requests
import json
import datetime
import textwrap

from TenCenturies import TenCenturies

u_name = "YOUR EMAIL ADDRESS"
u_pass = "YOUR PASSWORD"

'''
	Login
'''
tc = TenCenturies(u_name, u_pass)

if (tc.status == 200):
	userData = tc.user()

	if (tc.status ==200):
		'''
		print ("Python10C: userData = '{0}'".format(userData))
		print {""}
		print ("Python10C: tc.name = '{0}'".format(tc.name))
		print ("")

		print ("Python10C: tc.desc = '{0}'".format(tc.desc))
		print ("")

		print ("Python10C: tc.counts = '{0}'".format(tc.counts))
		print ("")

		print ("Python10C: tc.verified = '{0}'".format(tc.verified))
		print ("")

		lastName = tc.name["last_name"]
		uid = userData["id"]
		userName= userData["username"]

		if (lastName == ""):
			print ("@{0} ({1}) [{2}] ".format(userName, firstName, uid))
		elif ((lastName == "") and (firstName == "")):
			print ("@{0} [{1}] ".format(userName, uid))
		else:
			print ("@{0} ({1} {2}) [{3}] ".format(userName, posterFirst, posterLast, uid))

		print ("")
		'''

		createdUNIX = 9999999999
		streamName = "Global"
		reverse = True

		length = 0
		first = True
		fullStream = []

		'''
			These two variables control how many posts are retrieved
				nrPosts		= How many posts to get per call to the API
				maxNrPosts	= The size of the stream to retrieve
		'''
		nrPosts = 200
		maxNrPosts = nrPosts * 2

		print ("***** {0} Stream *****".format(streamName))
		print ("\nThreadTest (A): Collecting {0} posts\n".format(maxNrPosts))

		fullStream = tc.makeStream(streamName, nrPosts, maxNrPosts)
		'''
		#	Collect posts - this could go into the library
		while (length < maxNrPosts):
			print ("ThreadTest (B): createdUNIX = {0}".format(createdUNIX))

			stream = tc.stream(streamName, createdUNIX, nrPosts)

			if (first):
				fullStream = stream
				first = False
			else:
				fullStream = fullStream + stream

			length = len(fullStream)
			lastPost = fullStream[length - 1]
			createdUNIX = lastPost["created_unix"]

		print ("ThreadTest (C): fullStream has {0} posts".format(length))
		'''
		print ("")


		#	Start processing the stream of posts
		threadList = []
		length = len(fullStream)

		#print ("\nThreadTest (A): len(fullStream) = {0}".format(length))

		for postNr in range(0, length):
			post = fullStream[postNr]

			#	Print the current post in an easy to read format
			#tc.prettyJSON(post)

			postID = post["id"]
			postThread = post["thread"]

			#print ("\nThreadTest (B): postNr = {0}, postID = {1},\n    postThread = {2}".format(postNr, postID, postThread))
			#print ("")

			if (postThread):
				threadID = postThread["thread_id"]
				replyTo = postThread["reply_to"]

				if ((threadID not in threadList) and (postID not in threadList)):
					print ("ThreadTest (A): [{0}] Getting thread {1} for post {2}".format(postNr, threadID, postID))

					threadStream = tc.thread(threadID, reverse)

					if (tc.status == 200):
						length = len(threadStream)

						print ("ThreadTest (B): [{0}] {1} posts in thread {2}".format(postNr, length, threadID))

						if (length > 0):
							print ("ThreadTest (C): [{0}] threadList = {1}\n".format(postNr, threadList))
							tc.displayFullTable(threadStream, False)
							print ("")

						threadList.insert(0, threadID)
					else:
						print ("ThreadTest (D): [{0}] Error {1}, Unable to get posts for thread {2}".format(postNr, tc.status, threadID))
			elif (postID not in threadList):
					print ("ThreadTest (E): [{0}] threadList = {1}\n".format(postNr, threadList))
					print ("ThreadTest (F): [{0}] Post {1} is not part of a thread".format(postNr, postID))
					tc.displayTablePost(post)
					print ("")

		#threadList = []
		#tc.prettyJSON(thread)

		print ("\nThreadTest: Logging out")
		tc.logout()
	else:
		print ("ThreadTest: Error {0}, Unable to get JSON data!".format(tc.status))
else:
	print ("ThreadTest (I): Error {0}, Unable to get JSON data!".format(tc.status))
