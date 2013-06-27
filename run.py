#!/usr/bin/python
# -*- coding: utf-8 -*-
#@author Mosab Ahmad <mosab.ahmad@gmail.com>

import os
import sys
import config
import requests

from togglapi import api
from toggltarget import target
from workingtime import workingtime


def internet_on():
    """Checks if internet connection is on by connecting to Google"""
    try:
        requests.get('http://www.google.com', timeout=10)
        return True
    except requests.exceptions.ConnectionError:
        return False
    except:
        return False


def getTerminalSize():
    env = os.environ

    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            import struct
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            return
        return cr

    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)

    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

    return int(cr[1]), int(cr[0])


def percentile_bar(percentage, tolerance):
    (width, height) = getTerminalSize()

    # progress_units        = int((0.8 * width))
    progress_units        = width - 10
    achieved_units        = int(percentage * progress_units)
    remaining_units       = int(progress_units - achieved_units)
    minimum_mark_position = int(progress_units - tolerance * progress_units)

    progress_bar = "{}{}".format("=" * achieved_units, "-" * remaining_units)

    percentile_bar = "{0:.2f}% ".format(percentage * 100)
    if tolerance > 0:
        percentile_bar += "[{}]".format(progress_bar[0:minimum_mark_position] + "|" + progress_bar[minimum_mark_position+1:])
    else:
        percentile_bar += "[{}]".format(progress_bar)

    return percentile_bar


def main():
    w = workingtime.WorkingTime(config.WORKING_HOURS_PER_DAY, config.BUSINESS_DAYS, config.WEEK_DAYS)
    a = api.TogglAPI(config.API_TOKEN, config.TIMEZONE)
    t = target.Target()

    print "Hi"
    print "Checking Internet connectivity..."
    if not internet_on():
        print "OMG! There is no internet connection!"
        print "Good Bye Cruel World!"
        sys.exit()
    print "Internet seems fine!"
    print "\nTrying to connect to Toggl, hang on!\n"
    try:
        t.achieved_hours = a.get_hours_tracked(start_date=w.month_start, end_date=w.now)
    except:
        print "OMG! Toggle request failed for some mysterious reason!"
        print "Good Bye Cruel World!"
        sys.exit()

    t.required_hours = w.required_hours_this_month
    t.tolerance      = config.TOLERANCE_PERCENTAGE

    normal_min_hours, crunch_min_hours = t.get_minimum_daily_hours(w.business_days_left_count, w.days_left_count)

    print "So far you have tracked {0:.2f} hours".format(t.achieved_hours)
    print "\nBusiness days left till deadline : {}".format(w.business_days_left_count)
    print "Total days left till deadline : {}".format(w.days_left_count)
    print "\nThis month targets [Required (minimum)] : {} ({})".format(w.required_hours_this_month, w.required_hours_this_month - (w.required_hours_this_month * config.TOLERANCE_PERCENTAGE))
    print "\nTo achieve the minimum:\n\tyou should log {0:.2f} hours every business day".format(normal_min_hours)
    print "\tor log {0:.2f} hours every day".format(crunch_min_hours)
    print "\tleft is : {0:.2f}".format((w.required_hours_this_month - (w.required_hours_this_month * config.TOLERANCE_PERCENTAGE)) - t.achieved_hours)

    normal_required_hours, crunch_required_hours = t.get_required_daily_hours(w.business_days_left_count, w.days_left_count)

    print "\nTo achieve the required :\n\tyou should log {0:.2f} hours every business day".format(normal_required_hours)
    print "\tor log {0:.2f} hours every day".format(crunch_required_hours)
    print "\tleft is : {0:.2f}".format(w.required_hours_this_month - t.achieved_hours)
    print "\nSo far you have achieved:\n"
    bar = percentile_bar(t.achieved_percentage, config.TOLERANCE_PERCENTAGE)
    print bar

if __name__ == '__main__':
    main()
