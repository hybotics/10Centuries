#!/usr/bin env python3
import requests
import json
import datetime
import pprint
import textwrap

class TenCenturies():
	authURL = "https://api.10centuries.org/auth/status"
	loginURL = "https://api.10centuries.org/auth/login"
	streamHomeURL = "https://api.10centuries.org/content/blurbs/home"
	streamGlobalURL = "https://api.10centuries.org/content/blurbs/global"
	streamMentionsURL = "https://api.10centuries.org/content/blurbs/mentions"
	threadURL = "https://api.10centuries.org/content/blurbs/thread/"
	contentURL = "https://api.10centuries.org/content/social/thread"

	logoutURL = "https://api.10centuries.org/auth/logout"

	appID = "YOUR APP ID HERE"

	libName = "TenCenturies"

	'''
		Initalize and log the user in
	'''
	def __init__ (self, userName, userPass):
		self.status = 0
		self.auth = ""

		self.token = ""
		self.result = ""
		self.udata = ""

		self.desc = ""
		self.counts = ""
		self.name = ""
		self.verified = ""

		self.displayedThreads = []

		acctData = {
			"client_guid" : self.appID,
			"acctname" : userName,
			"acctpass" : userPass
		}

		result = requests.post(self.loginURL, data=acctData)
		self.status = result.status_code

		#print ("{0}: result = '{1}'".format(self.libName, result))
		#print ("{0}: result.text = '{1}'".format(self.libName, result.text))

		if (self.status == 200):
			text = json.loads(result.text)
			data = text["data"]
			#print ("{0}: data = '{1}'".format(self.libName, data))

			self.token = data["token"]
			#print ("{0}: Login was successful: self.token = '{1}'".format(self.libName, self.token))

			self.auth = { "authorization" : self.token }

		return None

	'''
		***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
		Utility functions used by various other routines
		***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
	'''

	'''
		Return a UNIX time date, formatted in long form:
			dateText[0] = October 14, 2016
			dateText[1] = time as 12:04pm
	'''
	def longDate (self, unixTime):
		value = datetime.datetime.fromtimestamp(unixTime)
		dateText = [value.strftime('%d-%b-%Y'), value.strftime('%I:%M%p').lower()]

		return dateText

	'''
		Return a UNIX time date, formatted in short form:
			dateText[0] = 14-Oct-2016
			dateText[1] = time as 12:04pm
	'''
	def shortDate (self, unixTime):
		value = datetime.datetime.fromtimestamp(unixTime)
		dateText = [value.strftime('%d-%b-%Y'), value.strftime('%I:%M%p').lower()]

		return dateText

	'''
		Creates a stream of posts.
			streamName (string)		= the name of the stream (Global, Home, or Mentions)
			nrPosts (integer)		= the number of posts to get per call to the API
			maxNrPosts (integer)	= the maximum number of posts to get (multiple of nrPosts)
	'''
	def makeStream (self, streamName, nrPosts=100, maxNrPosts=100):
		print ("\n{0} (A) [makeStream]: Collecting {0} posts\n".format(maxNrPosts))

		length = 0
		createdUNIX = 9999999
		first = True
		fullStream = []
		while (length < maxNrPosts):
			print ("{0} (B) [makeStream]: createdUNIX = {1}".format(self.libName, createdUNIX))
			stream = self.stream(streamName, createdUNIX, nrPosts)

			if (first):
				fullStream = stream
				first = False
			else:
				fullStream = fullStream + stream

			length = len(fullStream)
			print ("{0} (C) [makeStream]: There are {1} posts in fullStream".format(self.libName, length))
			lastPost = fullStream[length - 1]
			createdUNIX = lastPost["created_unix"]

		length = len(fullStream)
		print ("{0} (D) [makeStream]: Returning {1} posts".format(self.libName, length))

		return fullStream

	'''
		Print some JSON encoded text in a more Human readable format
	'''
	def prettyJSON (self, jsonText, indent=2):
		#	Print the current post in an easy to read format
		pp = pprint.prettyJSONer(indent=indent)
		pp.pprint(jsonText)

	'''
		***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
		Main driver routines. If these do not work, nothing else will.
		***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
	'''

	'''
		Logout
	'''
	def logout (self):
		result = requests.post(self.logoutURL, data="")

	'''
		Get single or multiple single posts. The post list must be comma
			separated.
	'''
	def posts (self, postIDs):
		URL = "https://api.10centuries.org/content/"
		data = ""

		params = { "post_ids" : postIDs }

		result = requests.get(URL, headers=self.auth, params=params)

		self.status = result.status_code

		if (self.status == 200):
			text = json.loads(result.text)
			data = text["data"]
			length = len(data)

			for i in range(0, length):
				self.displayFullPost(data[i])
		else:
			print ("{0}: Invalid postIDs({1})!".format(self.libName, postIDs))

		print ("")

		return data

	'''
		Get up to 200 posts from a user's Global, Home, or Mentions stream
	'''
	def stream (self, streamName, beforeUNIX=9999999999, nrPosts=50):
		self.status = 2000
		data = ""
		name = ""
		streamURL = ""
		stream = False

		name = streamName.upper()
		#print ("{0}: name = '{1}'".format(self.libName, name))

		if (name == "GLOBAL"):
			streamURL = self.streamGlobalURL
		elif (name == "HOME"):
			streamURL = self.streamHomeURL
		elif (name == "MENTIONS"):
			streamURL = self.streamMentionsURL
		else:
			self.status = 2010

		if (streamURL != ""):
			params = {
				"before_unix" :  beforeUNIX,
				"count" : nrPosts
			 }

			result = requests.get(streamURL, headers=self.auth, params=params)
			self.status = result.status_code

			if (self.status == 200):
				text = json.loads(result.text)

				if "data" in text:
					stream = text["data"]
			else:
				self.status = 2020

		return stream

	'''
		Return the posts that are part of a thread.
		Optionally, reverse the list.
	'''
	def thread (self, threadID, reverseIt=False):
		thread = []
		params = { "thread_id" : threadID }

		result = requests.get(self.contentURL, headers=self.auth, params=params)
		self.status = result.status_code

		if (self.status == 200):
			text = json.loads(result.text)

			#self.prettyJSON(text)
			data = text["data"]["posts"]
			length = len(data)

			#print ("{0}: len(data) = {1}".format(self.libName, length))
			#self.prettyJSON(data)

			if (reverseIt and (length > 0)):
				#	Put the thread in reverse (post ID) order
				for i in range(length - 1, -1, -1):
					thread.append(data[i])
		else:
			self.status = 2020
			thread = False

		return thread

	'''
		Authenticate a user and return their information
	'''
	def user (self):
		self.status = 0

		#	Get account data
		result = requests.get(self.authURL, headers=self.auth)
		self.status = result.status_code

		if (self.status == 200):
			acctData = json.loads(result.text)

			data = acctData["data"]

			account = data["account"]

			if (account != False):
				#	We have the data for this account
				#print ("{0}: Authorization succeeded!".format(self.libName))
				self.userData = account[0]
				#print ("{0}: user = '{1}'".format(self.libName, user))
				self.name = self.userData["name"]
				#print ("{0}: self.name = '{1}'".format(self.libName, self.name))
				self.desc = self.userData["description"]
				#print ("TenCenturies self.desc = '{1}'".format(self.libName, self.desc))
				self.userID = self.userData["id"]
				#print ({0}: self.userID = {1}".format(self.libName, self.userID))
				self.counts = self.userData["counts"]
				#print ("{0}: self.counts = '{1}'".format(self.libName, self.counts))
				self.verified = self.userData["verified"]
				#print ("{0}: self.verified = '{1}'".format(self.libName, self.verified))
			else:
				#	Uh oh!
				print ("{0}: Authorization FAILED!")
				self.userData = ""
		else:
			print ("{0}: Error {1}, Unable to get JSON data!".format(self.libName, self.status))
			self.userData = ""

		return self.userData

	'''
		Display one fully formatted post
	'''
	def displayFullPost (self, post):
		postAuthors = post["account"]
		postClient = post["client"]
		postName = postAuthors[0]["name"]
		postThread = post["thread"]
		postID = post["id"]
		poster = postAuthors[0]["username"]
		posterDisplay = postName["display"]
		postContent = post["content"]

		createdUNIX = post["created_unix"]
		dateText = self.longDate(createdUNIX)
		postedDate = dateText[0]
		postedTime = dateText[1]

		if (posterDisplay == ""):
			posterFirst = postName["first_name"]
			posterLast = postName["last_name"]
			posterDisplay = posterFirst + " " + posterLast

		print ("@{0} ({1}) [{2}] {3} using {4}".format(poster, posterDisplay, postID, postedDate + " at " + postedTime, postClient["name"]))

		wrapped = textwrap.wrap(postContent["text"], 78, replace_whitespace=False)
		length = len(wrapped)

		for i in range(0, length):
			print (wrapped[i])

		print ("")
		print ("{0}: postThread = {1}".format(self.libName, postThread))
		print ("")

		if (postThread != False):
			replyTo = postThread["reply_to"]
			threadID = postThread["thread_id"]

			#	Get the post this is a reply to
			post = self.getPosts(replyTo)

			print ("{0}: Reply to post {1} in root thread {2}".format(self.libName, replyTo, threadID))

	'''
		Display a full stream of fully formatted posts
	'''
	def displayFullStream (self, stream):
		length = len(stream)

		for i in range(0, length):
			self.displayFullPost(stream[i])
			#print ("-------------------------------------------------------")

		print ("")

	'''
		Display a stream of the user's own posts
	'''
	def displayMyPostStream (self):
		#	Initialize stream
		stream = self.stream("Global", 9999999999, 100)
		length = len(stream)

		while (length > 0):
			for i in range(0, length):
				post = stream[i]
				postAuthors = post["account"]
				posterID = postAuthors[0]["id"]
				matchID = self.userData["id"]

				if (posterID == matchID):
					self.displayFullPost(post)

				unixTime = post["created_unix"]

			stream = self.stream("Global", unixTime, 100)
			length = len(stream)

	'''
		Display a single post in table format
	'''
	def displayTablePost (self, post):
		postID = post["id"]

		createdUNIX = post["created_unix"]
		dateText = self.shortDate(createdUNIX)
		createdDate = dateText[0]
		createdTime = dateText[1]

		publishUNIX = post["publish_unix"]
		dateText = self.shortDate(publishUNIX)
		publishDate = dateText[0]
		publishTime = dateText[1]

		postAuthors = post["account"]
		postThread = post["thread"]
		posterID = postAuthors[0]["id"]
		postName = postAuthors[0]["name"]
		poster = postAuthors[0]["username"]
		posterFL = postName["first_name"] + " " + postName["last_name"]
		posterDisplay = postName["display"]

		if (postThread == False):
			print ("@{:14} {:21} {:21} {:6}".format(poster, createdDate + " " + createdTime, publishDate + " " + publishTime, postID))
		else:
			print ("@{:14} {:21} {:21} {:6} {:6} {:7}".format(poster, createdDate + " " + createdTime, publishDate + " " + publishTime, postID, postThread["thread_id"], postThread["reply_to"]))

		return createdUNIX

	'''
		Display a full table of posts, with or without column headings
	'''
	def displayFullTable (self, stream, showHeaders=True):
		createdUNIX = 0
		length = len(stream)

		if showHeaders:
			print ("{:15} {:21} {:21} {:6} {:6} {:6}".format("@Author", "      Created", "     Published", "PostID", "Thread", "ReplyTo"))
			print ("{:15} {:21} {:21} {:6} {:6} {:6}".format("---------------", "-------------------", "-------------------", "------", "------", "-------"))

		#	Print data from each post
		for i in range(0, length):
			post = stream[i]
			createdUNIX = self.displayTablePost(post)

		return createdUNIX

	'''
		Display a threaded stream of posts using table format

		NOTE: This procedure is NOT in its final form. Do NOT
			use it!
	'''
	def displayThreadedStream (self, stream):
		thread = []
		threadList = []
		multipleReplies = False
		length = len(stream)

		print ("{0}: length(stream) = {1}\n".format(self.libName, length))

		for postNr in range(0, length):
			post = stream[postNr]
			postID = post["id"]
			postThread = post["thread"]

			print ("{0}: postNr = {1}, postID = {2}\n    postThread = {3}".format(self.libName, postNr, postID, postThread))

			if (postThread):
				threadID = postThread["thread_id"]
				replyTo = postThread["reply_to"]

				threadStream = self.thread(threadID, True)

				if (self.status == 200):
					if (threadID not in threadList):
						self.displayFullTable(threadStream, False)
						threadList.append(threadID)
				else:
					print ("{0}: Error {1}, There was a problem getting posts for thread {2}".format(self.libName, self.status, threadID))
			else:
				#	This post is not part of a thread
				self.displayTablePost(post)
