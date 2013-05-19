#!/usr/bin/env 

import sys


from datetime import datetime, date, time
import calendar


import re

import requests
from requests.auth import HTTPBasicAuth
import json

import config


current_day 	= datetime.now().strftime("%d")
current_month 	= datetime.now().strftime("%m")
current_year 	= datetime.now().strftime("%y")


last_day_in_month	= int(calendar.monthrange(int(current_year), int(current_month))[1])
days_left_in_month 	= last_day_in_month - int(current_day)

_deadline = "{}/{}/{} 23:59".format(last_day_in_month, current_month, current_year)


toggl_url = 'https://www.toggl.com/api/v6/time_entries.json?start_date=20{}-{}-{}T00%3A00%3A00%2B02%3A00&end_date=20{}-{}-{}T23%3A59%3A59%2B02%3A00'.format(current_year, current_month, 1, current_year, current_month, last_day_in_month)
headers = {'content-type': 'application/json'}

print "Connecting to Toggl, hang on!"
r = requests.get(toggl_url, headers=headers, auth=HTTPBasicAuth(API_TOKEN, 'api_token'))
time_entries = r.json()

total_seconds_tracked = 0
for entry in time_entries['data']:
	total_seconds_tracked += entry['duration']

achieved_hours = (total_seconds_tracked / 60.0) / 60
print achieved_hours


#salary 				= float(raw_input('Enter your Salary : '))

required_hours		= 172.0
minimum_hours 		= 172 - (0.1 * 172)


left_to_minimum		= minimum_hours - achieved_hours
left_to_required	= required_hours - achieved_hours
if achieved_hours >= minimum_hours :
	achieved_percentage = 1.0
else:
	achieved_percentage	= achieved_hours / required_hours

#earned_salary 		= achieved_percentage * salary

now 		= datetime.now()
deadline 	= datetime.strptime(_deadline, "%d/%m/%y %H:%M")

delta = deadline - now

minimum_work_hours_per_day = left_to_minimum / days_left_in_month
required_work_hours_per_day = left_to_required / days_left_in_month




print "Time left till dealine is : {}".format(delta)
print "You shold at least achieve {} hours and ideally {} hours".format(left_to_minimum, left_to_required)
print "This means you should work from {} to {} hours per day till the deadline".format(minimum_work_hours_per_day, required_work_hours_per_day)
print "So far you have achieved {} % of your target".format(achieved_percentage * 100)
#print "So far you have earned {} % of your salary which is {} LE".format('{0:.2f}'.format(achieved_percentage * 100), '{0:.2f}'.format(earned_salary))
