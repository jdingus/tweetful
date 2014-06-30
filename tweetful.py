import authorization
import requests
from urls import TIMELINE_URL
# import json

def main():
	""" Main function """
	oauth = authorization.authorize()
	response = requests.get(TIMELINE_URL, auth=oauth)
	print response.json()


if __name__ == "__main__":
	main()
