#!/usr/bin/python
# -*- coding: utf-8 -*-
#@author Mosab Ahmad <mosab.ahmad@gmail.com>

import 	sys

from 	datetime import datetime, date, time
import 	calendar

import 	re

import 	requests
from 	requests.auth import HTTPBasicAuth
import 	json

import 	config

from togglapi import api
from toggltarget import target

current_day 	= datetime.now().strftime("%d")
current_month 	= datetime.now().strftime("%m")
current_year 	= datetime.now().strftime("%y")


last_day_in_month	= int(calendar.monthrange(int(current_year), int(current_month))[1])
days_left_in_month 	= last_day_in_month - int(current_day)

_deadline = "{}/{}/{} 23:59".format(last_day_in_month, current_month, current_year)


toggl_url = 'https://www.toggl.com/api/v6/time_entries.json?start_date=20{}-{}-{}T00%3A00%3A00%2B02%3A00&end_date=20{}-{}-{}T23%3A59%3A59%2B02%3A00'.format(current_year, current_month, 1, current_year, current_month, last_day_in_month)
headers = {'content-type': 'application/json'}

print "Hi"
print "I am trying to connect to Toggl, hang on!"
try:
	time_entries = requests.get(toggl_url, headers=headers, auth=HTTPBasicAuth(config.API_TOKEN, 'api_token')).json()
except requests.exceptions.ConnectionError:
	print "OMG! Either there is no internet connection, or Toggl is unavailable for some mysterious reason!"
	print "Good Bye Cruel World!"
	sys.exit()

total_seconds_tracked = 0
for entry in time_entries['data']:
	total_seconds_tracked += entry['duration']

achieved_hours = (total_seconds_tracked / 60.0) / 60


#salary 				= float(raw_input('Enter your Salary : '))

required_hours		= 173.0
tolerance			= 0.1
minimum_hours 		= required_hours - (tolerance * required_hours)


left_to_minimum		= minimum_hours - achieved_hours
left_to_required	= required_hours - achieved_hours

# Setting to 0 if passed
if achieved_hours >= minimum_hours :
	left_to_minimum		= 0
if achieved_hours > required_hours :
	left_to_required	= 0

achieved_percentage	= achieved_hours / required_hours

#earned_salary 		= achieved_percentage * salary

now 		= datetime.now()
deadline 	= datetime.strptime(_deadline, "%d/%m/%y %H:%M")

delta = deadline - now

minimum_work_hours_per_day = left_to_minimum / days_left_in_month
required_work_hours_per_day = left_to_required / days_left_in_month



print "So far you have tracked {} hours".format('{0:.2f}'.format(achieved_hours))
print "Time left till dealine is : {}".format(delta)
print "You should at least achieve {} hours and ideally {} hours".format(left_to_minimum, left_to_required)
print "This means you should work from {} to {} hours per day till the deadline".format(minimum_work_hours_per_day, required_work_hours_per_day)
print "So far you have achieved {} % of your target".format('{0:.2f}'.format(achieved_percentage * 100))
#print "So far you have earned {} % of your salary which is {} LE".format('{0:.2f}'.format(achieved_percentage * 100), '{0:.2f}'.format(earned_salary))
