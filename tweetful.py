import authorization
import requests
import json
import logging
import argparse
import sys # Access argv variable
from urls import * # Location of endpoints for TwitterAPI
from collections import OrderedDict # Used in JSON printing

# Set the log output file, and the log level
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

def tweet(tw_text):
	pass
	""" Perform a tweet using TwitterAPI based on passed tw_text """
	logging.info("Attempting to tweet '{}'".format(tw_text))

def get_trends(woeid):
	"""
	Get singular trends response from TwitterAPI and store to trends.json
	vars, woeid	
	Go here to look up a WOEID:
	http://woeid.rosselliot.co.nz/
	"""
	# Chicago, Cook County 			WOEID: 2379574
	# Indianapolis, Marion County 	WOEID: 2427032
	
	oauth = authorization.authorize()
	query = "?id="+str(woeid)
	url = TRENDS_URL+query
	response = requests.get(url, auth=oauth)
	response = response.json()
	
	with open('trends.json', 'w') as outfile: # Save to file
		json.dump(response, outfile)

	""" Parse out the 'names' from response and return names[] """
	trends,location = parse_trends('trends.json')

	return woeid,trends,location

def parse_trends(json_file):
	""" Parse out the 'names' from response and return trends[] """
	trends = []
	with open(json_file) as json_file:
		json_data = json.load(json_file)

		for data in json_data:
			for item in json_data[0]['trends']:
				trend_name = item['name']
				trends.append(trend_name)
			location = json_data[0]['locations'][0]['name']
	return trends,location


def main():
	""" Main function """

	woeid = 2379574 # Chicago
	# woeid = 2427032 # Indy
	woeid,trends,location = get_trends(woeid)
	print_json_file('trends.json')
	print woeid
	print location


	"""
	Steps:
		1.) Construct make_parser() >> -tweet , -trends
		2.) Get Trends from Twitter by WOEID#
			> If one item passed will just return that item
			> If multiple WOEID's pass will return both and compare
			> Store resulting data to trends.json
		3.) Perform status update, aka tweet to my user account
		4.) Make sure to do commits along the way and use error logging
	"""

if __name__ == "__main__":
	main()



