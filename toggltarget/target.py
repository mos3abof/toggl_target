#!/usr/bin/python
# -*- coding: utf-8 -*-
#@author Mosab Ahmad <mosab.ahmad@gmail.com>

class Target(object):
	"""Caclulate the actual target achievments"""
	
	def __init__(self):
		super(Target, self).__init__()

	def set_achieved_hours(self, achieved_hours):
		self.achieved_hours = achieved_hours
	
	def set_required_hours(self, required_hours):
		self.required_hours = required_hours

	def set_tolerance(self, tolerance):
		self.tolerance = tolerance

	def get_minimum_hours(self):
		return self.required_hours - (self.tolerance * self.required_hours)

	def get_left_to_minimum(self):
		m = self.get_minimum_hours() - self.achieved_hours
		if m > 0 :
			return m
		else:
			return 0

	def get_left_to_required(self):
		m = self.required_hours - self.achieved_hours
		if m > 0 :
			return m
		else:
			return 0

	def get_achieved_percentage(self):
		return self.achieved_hours / self.required_hours

	def get_required_daily_hours(self, business_days, days):
		normal_hours = self.get_left_to_required() / business_days
		crunch_hours = self.get_left_to_required() / days
		return (normal_hours, crunch_hours)

	def get_minimum_daily_hours(self, business_days, days):
		normal_hours = self.get_left_to_minimum() / business_days
		crunch_hours = self.get_left_to_minimum() / days
		return (normal_hours, crunch_hours)




if __name__ == '__main__':
	import doctest
	doctest.testmod()