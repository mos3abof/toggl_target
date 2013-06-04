#!/usr/bin/python
# -*- coding: utf-8 -*-
#@author Mosab Ahmad <mosab.ahmad@gmail.com>

import sys
import config
import traceback

from togglapi import api
from toggltarget import target
from workingtime import workingtime

w = workingtime.WorkingTime()
a = api.TogglAPI(config.API_TOKEN)
t = target.Target()


t.set_required_hours(w.get_required_hours_this_month())
t.set_tolerance(config.TOLERANCE_PERCENTAGE)


print "Hi"
print "Checking Internet connectivity..."
if not a.internet_on():
	print "OMG! There is no internet connection!"
	print "Good Bye Cruel World!"
	sys.exit()
print "Internet seems fine!"
print "I am trying to connect to Toggl, hang on!"
try:
	tracked_hours = a.get_hours_tracked(start_date = str(w.get_month_start_iso()), end_date = str(w.get_now_iso()))
except:
	print "OMG! Toggle request failed for some mysterious reason!"
	print "Good Bye Cruel World!"
	print traceback.format_exc()
	sys.exit()

t.set_achieved_hours(tracked_hours)



left_to_minimum		= t.get_left_to_minimum()
left_to_required	= t.get_left_to_required()


achieved_percentage	= t.get_achieved_percentage()


print "So far you have tracked {} hours".format('{0:.2f}'.format(tracked_hours))
print "\nBusiness days left till deadline : {}".format(w.get_business_days_left_count())
print "Total days left till deadline : {}".format(w.get_days_left_count())
print "\nRquired working hours for this month : {}".format(w.get_required_hours_this_month())
print "\nTo achieve the minimum :\n\tyou should log {} hours every business day \n\tor log {} hours every day".format(
																			'{0:.2f}'.format(t.get_minimum_daily_hours(w.get_business_days_left_count(), w.get_days_left_count())[0]), 
																			'{0:.2f}'.format(t.get_minimum_daily_hours(w.get_business_days_left_count(), w.get_days_left_count())[1])
																		)
print "\nTo achieve the required :\n\tyou should log {} hours every business day \n\tor log {} hours every day".format(
																			'{0:.2f}'.format(t.get_required_daily_hours(w.get_business_days_left_count(), w.get_days_left_count())[0]), 
																			'{0:.2f}'.format(t.get_required_daily_hours(w.get_business_days_left_count(), w.get_days_left_count())[1])
																		)
print "\nSo far you have achieved {} % of your target".format('{0:.2f}'.format(achieved_percentage * 100))

