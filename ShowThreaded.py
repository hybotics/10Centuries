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
		streamName = "Global"
		nrPosts = 200
		showHeaders = True

		print ("***** {0} Stream *****".format(streamName))
		print ("")

		fullStream = tc.stream(streamName, 9999999999, nrPosts)
		length = len(fullStream)
		createdUNIX = fullStream[length - 1]["created_unix"]
		#print ("ShowFullTable: length(fullStream) = {0}".format(length))

		for i in range(0, 9):
			stream = tc.stream(streamName, createdUNIX, nrPosts)
			fullStream = fullStream + stream
			length = len(fullStream)
			createdUNIX = fullStream[length - 1]["created_unix"]
			#print ("ShowFullTable: length(fullStream) = {0}".format(length))

		if ((tc.status == 200) and (fullStream != False)):
			createdUNIX = tc.displayThreadedStream(fullStream)

			if showHeaders:
				showHeaders = False

			#stream = tc.stream(streamName, createdUNIX, nrPosts)
		else:
			print ("ShowFullTable(3): Error {0}, Unable to get stream data!".format(tc.status))

		print ("")

		print ("ShowFullTable: Logging out")
		tc.logout()
	else:
		print ("ShowFullTable(2): Error {0}, Unable to get JSON data!".format(tc.status))
else:
	print ("ShowFullTable(1): Error {0}, Unable to get JSON data!".format(tc.status))
