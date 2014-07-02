import authorization
import requests

import json

from urls import TIMELINE_URL
# import json

def main():
	""" Main function """
	oauth = authorization.authorize()
#	response = requests.get('https://api.twitter.com/1.1/trends/place.json?id=1', auth=oauth)
	# response = requests.get(TIMELINE_URL, auth=oauth)
#	new_response = response.json()

	
#	with open('data.txt', 'w') as outfile:
 # 		json.dump(new_response, outfile) # Save json to file for debugging

	with open("data.txt") as json_file:
    		json_data = json.load(json_file)
 	   
    	# print json_data[0].items()
    	print json_data[0][u'trends'][2]  #[u'name']
    	for name in json_data[0][u'trends'][2]:
    		print json_data[0][u'trends'][2][name]
    	# 	print json_data[0][u'trends'][item][u'name'] 




	# # for key in new_response:
	# # new_response[u'trends']
	# print new_response
	# # [0][u'trends'][u'urls']
	# print ''
	# # for o in new_response:
	# 	print ''
	# 	print '*******************************'
	# 	print ''
	# print new_response[0][u'locations']        #,o['favorite_count']
# Fort Wayne, Indiana (US-IN) WOEID: 2406008
# Fort Wayne, Indiana (US-IN) WOEID: 56559321	

if __name__ == "__main__":
	main()



