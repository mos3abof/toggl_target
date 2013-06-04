#!/usr/bin/python
# -*- coding: utf-8 -*-
#@author Mosab Ahmad <mosab.ahmad@gmail.com>

from dateutil.rrule import *
from dateutil.parser import *
from dateutil.relativedelta import *
from datetime import datetime, date, time

class WorkingTime(object):
	"""Time and date calculations for working hours and days"""
	def __init__(self):
		self.daily_hours = 8

	def set_deadline(self):
		pass

	def set_daily_hours(self, daily_hours):
		self.daily_hours = daily_hours

	def get_now(self):
		return datetime.now()+relativedelta(microsecond=0)

	def get_month_start(self):
		today = self.get_now()
		return today+relativedelta(day=1, hour=0, minute=0, second=0, microsecond=0)

	def get_month_end(self):
		today = self.get_now()
		return today+relativedelta(day=31, hour=11, minute=59, second=59, microsecond=0)


	def get_total_business_days_count(self):
		firstday = self.get_month_start()
		lastday  = self.get_month_end()
		return len(list(rrule(DAILY, dtstart=firstday, until=lastday, byweekday=(SA, SU, MO, TU, WE))))

	def get_total_days_count(self):
		firstday = self.get_month_start()
		lastday  = self.get_month_end()
		return len(list(rrule(DAILY, dtstart=firstday, until=lastday, byweekday=(SA, SU, MO, TU, WE, TH, FR))))

	def get_business_days_left_count(self):
		today = self.get_now()
		lastday = self.get_month_end()
		return len(list(rrule(DAILY, dtstart=today, until=lastday, byweekday=(SA, SU, MO, TU, WE))))


	def get_days_left_count(self):
		today = self.get_now()
		lastday = self.get_month_end()
		return len(list(rrule(DAILY, dtstart=today, until=lastday, byweekday=(SA, SU, MO, TU, WE, TH, FR))))

	def get_business_days_elapsed_count(self):
		firstday = self.get_month_start()
		today = self.get_now()
		return len(list(rrule(DAILY, dtstart=firstday, until=today, byweekday=(SA, SU, MO, TU, WE))))


	def get_days_elapsed_count(self):
		firstday = self.get_month_start()
		today = self.get_now()
		return len(list(rrule(DAILY, dtstart=firstday, until=today, byweekday=(SA, SU, MO, TU, WE, TH, FR))))

	def get_datetime_iso(self, t):
		return t.isoformat()

	def get_now_iso(self):
		return self.get_datetime_iso(self.get_now())

	def get_month_start_iso(self):
		return self.get_datetime_iso(self.get_month_start())

	def get_month_end_iso(self):
		return self.get_datetime_iso(self.get_month_end())

	def get_required_hours_this_month(self):
		return self.get_total_business_days_count() * int(self.daily_hours)

if __name__ == '__main__':
	import doctest
	doctest.testmod()