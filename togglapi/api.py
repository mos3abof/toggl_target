#!/usr/bin/python
# -*- coding: utf-8 -*-
#@author Mosab Ahmad <mosab.ahmad@gmail.com>

import requests
import json
import traceback

from urllib import urlencode
from requests.auth import HTTPBasicAuth

class TogglAPI(object):
	"""A wrapper for Toggl Api"""

	def __init__(self, api_token):
		self.api_token = api_token

	def set_token_api(self, api_token = ''):
		self.api_token = api_token

	def make_url(self, section='time_entries', params = {}):
		"""Constructs and returns an api url to call with the section of the API to be called
		and parameters defined by key/pair values in the paramas dict.
		Default section is "time_entries" which evaluates to "time_entries.json"

		>>> t = TogglAPI('1971800d4d82861d8f2c1651fea4d212')
		>>> t.make_url(section='time_entries', params = {})
		'https://www.toggl.com/api/v6/time_entries'

		>>> t = TogglAPI('1971800d4d82861d8f2c1651fea4d212')
		>>> t.make_url(section='time_entries', params = {'start_date' : '2010-02-05T15:42:46+02:00', 'end_date' : '2010-02-12T15:42:46+02:00'})
		'https://www.toggl.com/api/v6/time_entries?start_date=2010-02-05T15%3A42%3A46%2B02%3A00&end_date=2010-02-12T15%3A42%3A46%2B02%3A00'
		"""

		url = 'https://www.toggl.com/api/v6/{}.json'.format(section)
		if len(params) > 0:
			url = url + '?{}'.format(urlencode(params))
		return url

	def internet_on(self):
		"""Checks if internet connection is on by connecting to Google"""
		try:
			r = requests.get('http://www.google.com', timeout=10)
			return True
		except requests.exceptions.ConnectionError:
			return False

	def query(self, url, method):
		url = url
		headers = {'content-type': 'application/json'}
		
		if method == 'GET':
			return requests.get(url, headers=headers, auth=HTTPBasicAuth(self.api_token, 'api_token'))
		elif method == 'POST':
			return requests.post(url, headers=headers, auth=HTTPBasicAuth(self.api_token, 'api_token'))
		else:
			raise ValueError('Undefined HTTP method "{}"'.format(method))

	## Time Entry functions
	def get_time_entries(self, start_date='', end_date=''):
		url = self.make_url(section = 'time_entries', params = {'start_date' : start_date, 'end_date': end_date})
		r = self.query(url = url, method = 'GET')
		return r.json()


	def get_hours_tracked(self, start_date='', end_date=''):
		total_seconds_tracked = 0

		time_entries = self.get_time_entries(start_date = start_date, end_date = end_date)

		for entry in time_entries['data']:
			total_seconds_tracked += entry['duration']

		return (total_seconds_tracked / 60.0) / 60.0



if __name__ == '__main__':
	import doctest
	doctest.testmod()