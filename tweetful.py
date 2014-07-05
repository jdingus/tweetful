import authorization
import requests
import json
import logging
import argparse
import sys # Access argv variable
from urls import * # Location of endpoints for TwitterAPI
from collections import OrderedDict # Used in JSON printing
import urllib

# Set the log outtrend file, and the log level
logging.basicConfig(filename="output.log", level=logging.INFO)

def print_json_file(json_file):
	""" 
	Pass json_file as string and will pretty print json
	"""
	import pprint # alternative used to print unicode files

	with open(json_file) as json_file:
		json_data = json.load(json_file, object_pairs_hook=OrderedDict)

	print json.dumps(json_data, indent=2)

	print "\n"
	print "-----" * 4
	print "\n"

def tweet(tweet_text):
	""" Perform a tweet using TwitterAPI based on passed tweet_text """
	logging.info("Attempting to tweet '{}'".format(tweet_text))

	if len(tweet_text) > 140:
		print 'Tweets cannot be greater than 140 characters!'
		quit()
	
	oauth = authorization.authorize()
	url = TWEET_URL+"?status=" + urllib.quote(tweet_text)  #urllib.quote encode given text to url friendly
	response = requests.post(url, auth=oauth)
	response = response.json()

	with open('tweet.json', 'w') as outfile: # Save to file
		json.dump(response, outfile)

	return response,tweet_text

def get_trends(woeid):
	"""
	Get singular trends response from TwitterAPI and store to trends.json
	vars, woeid	
	Go here to look up a WOEID:
	http://woeid.rosselliot.co.nz/
	"""
	# Chicago, Cook County 			WOEID: 2379574
	# Indianapolis, Marion County 	WOEID: 2427032
	logging.info("Getting trends info from WOEID: '{}'".format(woeid))
	
	oauth = authorization.authorize()
	query = "?id="+str(woeid)
	url = TRENDS_URL+query
	response = requests.get(url, auth=oauth)
	# print response.encoding
	response = response.json()

	
	with open('trends.json', 'w') as outfile: # Save to file
		json.dump(response, outfile)

	""" Parse out the 'names' from response and return names[] """
	trends,location = parse_trends('trends.json')
	
	[x.encode('UTF-8','ignore') for x in trends]
	location = location.encode('utf-8','ignore')
	
	return woeid,trends,location

def parse_trends(json_file):
	""" Parse out the 'names' from response and return trends[] """
	logging.info("Parsing the JSON file: '{}'".format(json_file))
	trends = []
	with open(json_file) as json_file:
		json_data = json.load(json_file)

		for data in json_data:
			for item in json_data[0]['trends']:
				trend_name = item['name']
				trends.append(trend_name)
			location = json_data[0]['locations'][0]['name']
	return trends,location

def make_parser():
    """ Construct the command line parser """
    logging.info("Constructing parser")
    description = "TwitterAPI command line implementation, tweet or get trend by WOEID location"
    parser = argparse.ArgumentParser(description=description)

    subparsers = parser.add_subparsers(help="Available commands")

    # Subparser for the trend command
    logging.debug("Constructing trend subparser")
    trend_parser = subparsers.add_parser("trend", help="Get a twitter trend by WOEID location")
    trend_parser.add_argument("woeid"
    	, default=1, nargs="?", help="The WOEID of the location to query:"+ 
    	"     Go here to look up a WOEID: "+
	"http://woeid.rosselliot.co.nz/")
    trend_parser.set_defaults(command="trend")

        # Subparser for the tweet command
    logging.debug("Constructing tweet subparser")
    tweet_parser = subparsers.add_parser("tweet", help="Make a tweet from command line")
    tweet_parser.add_argument("tweet_text"
    	, default='', nargs="?", help="Text you want to tweet, max 140 characters!")
    tweet_parser.set_defaults(command="tweet")

    return parser

def main():
	""" Main function """
	# print_json_file('tweet.json')

	parser = make_parser()
	arguments = parser.parse_args(sys.argv[1:])
	arguments = vars(arguments)
	command = arguments.pop("command") # Identify which command sent from command line

	if command == 'tweet':
		response,tweet_text = tweet(**arguments)
		if len(response)==0:
			print "No text was passed to Tweet!"
		print response['user']['screen_name'] + ' Just tweeted: ' + tweet_text + '!'

	"""
	Trend Argument 

	woeid = 2379574 # Chicago
	woeid = 2427032 # Indy
	woeid = 2487889 # San Diego

	"""
	
	if command == 'trend':
		woeid, trends, location = get_trends(**arguments)
		print 'These are the latest twitter trends for {}'.format(location)
		# print "Returning Twitter trend info for: {}".format(location)
		print "*****" * 10
		i=1
		for trend in trends:
			trend.encode('utf-8','ignore')
			print "Trend #{} : {}".format(str(i),trend)
			i+=1


if __name__ == "__main__":
	main()



