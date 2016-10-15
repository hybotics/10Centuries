#!/usr/bin/env python3
import requests
import json
import datetime
import textwrap
import pprint

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

		print ("***** Global Stream *****")
		print ("")

		createdUNIX = 9999999999

		stream = tc.stream("Global", createdUNIX, 100)

		while (stream != False):
			if ((tc.status == 200) and (stream != False)):
				length = len(stream)
				post = stream[0]

				postThread = post["thread"]
				postChannels = post["channel"]
				postClient = post["client"]
				'''
				tc.displayFullPost(post)

				print ("")
				'''
				pp = pprint.PrettyPrinter(indent=2)
				pp.pprint(post)
				'''
				print ("Python10C: length = {0}, post = {1}".format(length, post))
				print ("")
				print ("Python10C: postThread = {0}".format(postThread))
				print ("")
				print ("Python10C: postChannels = {0}".format(postChannels))
				print ("")
				'''
				print ("Python10C: postClient = {0}".format(postClient))
				print ("")
				print ("----------------------------------------------------------------------------------------------")
				'''
				#print ("Python10C: Threaded Global Stream")
				#print ("")
				#createdUNIX = tc.displayThreadedStream(stream)
				createdUNIX = tc.displayFullTable(stream)
				print ("----------------------------------------------------------------------------------------------")

				stream = tc.stream("Global", createdUNIX, 100)
				'''	
			print ("Python10C: Mentions stream")
			stream = tc.stream("mentions", createdUNIX, 25)
			createdUNIX = tc.displayFullStream(stream)

			print ("----------------------------------------------------------------------------------------------")

			print ("Python10C: Global stream")
			stream = tc.stream("GloBAl", createdUNIX, 25)
			createdUNIX = tc.displayFullTable(stream)

			print ("----------------------------------------------------------------------------------------------")
			print ("")

			print ("Python10C: My Posts")
			createdUNIX = tc.displayMyPostStream()

			print ("----------------------------------------------------------------------------------------------")

			#print ("Python10C: tc.token = {0}".format(tc.token))
		else:
			print ("Python10C(3): Error {0}, Unable to get stream data!".format(tc.status))

		print ("")

		print ("Python10C: Logging out")
		tc.logout()
	else:
		print ("Python10C(2): Error {0}, Unable to get JSON data!".format(tc.status))
else:
	print ("Python10C(1): Error {0}, Unable to get JSON data!".format(tc.status))
