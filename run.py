#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author Mosab Ibrahim <mosab.a.ibrahim@gmail.com>

import os
import sys
import config
import argparse
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

    progress_units = width - 10
    achieved_units = int(percentage * progress_units)
    remaining_units = int(progress_units - achieved_units)
    mark_pos = int(progress_units - tolerance * progress_units)

    progress_bar = "{}{}".format("=" * achieved_units, "-" * remaining_units)

    percentile_bar = hilite("{0:.2f}% ".format(percentage * 100), SUCCESS, True)
    if tolerance > 0:
        percentile_bar += "[{}]".format(progress_bar[0:mark_pos] + "|" + progress_bar[mark_pos + 1:])
    else:
        percentile_bar += "[{}]".format(progress_bar)

    return percentile_bar


ERROR = 0
SUCCESS = 1
WARNING = 2
def hilite(string, status=SUCCESS, bold=False):
    attr = []
    if status == SUCCESS:
        attr.append('32') # green
    elif status == ERROR:
        attr.append('31') # red
    elif status == WARNING:
        attr.append('33') # Brown/Orange
    if bold:
        attr.append('1')
    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)


def main(workspace_name=None, project_name=None, client_name=None, custom_left_days=None):

    w = workingtime.WorkingTime(config.WORKING_HOURS_PER_DAY, config.BUSINESS_DAYS, config.WEEK_DAYS)
    a = api.TogglAPI(config.API_TOKEN, config.TIMEZONE)
    t = target.Target()

    print("Hi")
    print("Checking Internet connectivity...")
    if not internet_on():
        print("OMG! There is no internet connection!")
        print("Good Bye Cruel World!")
        sys.exit()
    print("Internet seems fine!")
    print("\nTrying to connect to Toggl, hang on!\n")
    try:
        # filter to limit calculations to a perimeter (workspace, project, client)
        a.set_filter(project_name=project_name, workspace_name=workspace_name, client_name=client_name)

        # data from 1st of month
        t.achieved_hours = a.get_hours_tracked(start_date=w.month_start, end_date=w.now)
    except:
        print("OMG! Toggle request failed for some mysterious reason!")
        print("Good Bye Cruel World!")
        sys.exit()

    t.required_hours = w.required_hours_this_month
    t.tolerance = config.TOLERANCE_PERCENTAGE

    print("So far you have tracked :", hilite("{0:.2f} hours".format(t.achieved_hours), SUCCESS, True))

    if custom_left_days: # with --days cli argument
        business_days_left_count = custom_left_days
        days_left_count = custom_left_days
    else:
        business_days_left_count = w.business_days_left_count
        days_left_count = w.days_left_count

    normal_min_hours, crunch_min_hours = t.get_minimum_daily_hours(business_days_left_count, days_left_count)

    if custom_left_days:
        print(hilite("\nTotal days left till deadline : {} (custom)".format(custom_left_days), WARNING))
    else:
        print("\nBusiness days left till deadline : {}".format(business_days_left_count))
        print("Total days left till deadline : {}".format(days_left_count))

    print("\nThis month targets [Required (minimum)] : {} ({})".format(w.required_hours_this_month,
                                    w.required_hours_this_month - (w.required_hours_this_month * config.TOLERANCE_PERCENTAGE)))
    
    print(hilite("\nTo achieve the minimum:", WARNING, True))
    if custom_left_days:
        print("\n\tyou should log {0:.2f} hours every day".format(crunch_min_hours))
        print("\tleft is : {0:.2f} hours".format(
            (w.required_hours_this_month - (w.required_hours_this_month * config.TOLERANCE_PERCENTAGE)) - t.achieved_hours))
    else:
        print("\n\tyou should log {0:.2f} hours every business day".format(normal_min_hours))
        print("\tor log {0:.2f} hours every day".format(crunch_min_hours))
        print("\tleft is : {0:.2f} hours".format(
            (w.required_hours_this_month - (w.required_hours_this_month * config.TOLERANCE_PERCENTAGE)) - t.achieved_hours))

    normal_required_hours, crunch_required_hours = t.get_required_daily_hours(business_days_left_count, days_left_count)

    print(hilite("\nTo achieve the required:", SUCCESS, True))
    if custom_left_days:
        print("\n\tyou should log {0:.2f} hours every day".format(crunch_required_hours))
        print("\tleft is : {0:.2f} hours".format(w.required_hours_this_month - t.achieved_hours))
    else:
        print("\n\tyou should log {0:.2f} hours every business day".format(normal_required_hours))
        print("\tor log {0:.2f} hours every day".format(crunch_required_hours))
        print("\tleft is : {0:.2f} hours".format(w.required_hours_this_month - t.achieved_hours))

    print("\nHow your progress looks:")
    bar = percentile_bar(t.achieved_percentage, config.TOLERANCE_PERCENTAGE)
    print(bar)


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', "--workspace", help="filter by workspace's name")
    parser.add_argument('-p', "--project", help="filter by project's name")
    parser.add_argument('-c', "--client", help="filter by client's name")
    parser.add_argument('-d', "--days", help="remaining days (this month)", type=int)
    args = parser.parse_args()

    main(workspace_name=args.workspace, project_name=args.project, client_name=args.client, custom_left_days=args.days)
