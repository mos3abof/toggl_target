#!/usr/bin/python
# -*- coding: utf-8 -*-
#@author Mosab Ahmad <mosab.ahmad@gmail.com>

from dateutil.rrule import rrule, SA, SU, MO, TU, WE, TH, FR, DAILY
from dateutil.relativedelta import relativedelta
from datetime import datetime

# TODO: Should we move these to config.py?
BUSINESS_DAYS = (SA, SU, MO, TU, WE)
WEEK_DAYS = (SA, SU, MO, TU, WE, TH, FR)

class WorkingTime(object):
	"""Time and date calculations for working hours and days"""
	def __init__(self, daily_hours):
		self.daily_hours = daily_hours

	@property
	def now(self):
		return datetime.now() + relativedelta(microsecond=0)

	@property
	def month_start(self):
		return self.now + relativedelta(day=1, hour=0, minute=0, second=0, microsecond=0)

	@property
	def month_end(self):
		return self.now + relativedelta(day=31, hour=11, minute=59, second=59, microsecond=0)

	@property
	def total_business_days_count(self):
		return rrule(DAILY, dtstart=self.month_start, until=self.month_end, byweekday=BUSINESS_DAYS).count()

	@property
	def total_days_count(self):
		return rrule(DAILY, dtstart=self.month_start, until=self.month_end, byweekday=WEEK_DAYS).count()

	@property
	def business_days_left_count(self):
		return rrule(DAILY, dtstart=self.now, until=self.month_end, byweekday=BUSINESS_DAYS).count()

	@property
	def days_left_count(self):
		return rrule(DAILY, dtstart=self.now, until=self.month_end, byweekday=WEEK_DAYS).count()

	@property
	def business_days_elapsed_count(self):
		return rrule(DAILY, dtstart=self.month_start, until=self.now, byweekday=BUSINESS_DAYS).count()


	@property
	def days_elapsed_count(self):
		firstday = self.month_start
		today = self.now
		return rrule(DAILY, dtstart=firstday, until=today, byweekday=WEEK_DAYS).count()

	@property
	def required_hours_this_month(self):
		return self.total_business_days_count * self.daily_hours

if __name__ == '__main__':
	import doctest
	doctest.testmod()
