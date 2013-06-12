#!/usr/bin/python
# -*- coding: utf-8 -*-
#@author Mosab Ahmad <mosab.ahmad@gmail.com>


class Target(object):
    """Calculate the actual target achievments"""

    def __init__(self):
        super(Target, self).__init__()

    @property
    def minimum_hours(self):
        return self.required_hours - (self.tolerance * self.required_hours)

    @property
    def left_to_minimum(self):
        m = self.minimum_hours - self.achieved_hours
        return max(m, 0)

    @property
    def left_to_required(self):
        m = self.required_hours - self.achieved_hours
        return max(m, 0)

    @property
    def achieved_percentage(self):
        return self.achieved_hours / self.required_hours

    def get_required_daily_hours(self, business_days, days):
        normal_hours = self.left_to_required / business_days
        crunch_hours = self.left_to_required / days
        return (normal_hours, crunch_hours)

    def get_minimum_daily_hours(self, business_days, days):
        normal_hours = self.left_to_minimum / business_days
        crunch_hours = self.left_to_minimum / days
        return (normal_hours, crunch_hours)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
