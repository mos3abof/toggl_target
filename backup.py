#!/usr/bin/env python
# encoding: utf8

import hashlib
import json
import os
import re
from datetime import datetime, timedelta

from togglapi import api

from config import API_TOKEN, TIMEZONE

START_MONTH = '2015-03'


def get_month_start(time):
    return time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def get_month_end(time):
    month_start = get_month_start(time)
    next_month_start = (month_start + timedelta(days=31)).replace(day=1)
    return next_month_start - timedelta(seconds=1)


def dump(dump_dir, year, month, pretty_json=False, verbose=False):
    time = datetime(year=year, month=month, day=1)
    month_start = get_month_start(time)
    month_end = get_month_end(time)
    month = '%d-%02d' % (year, month)
    if verbose:
        print month + ':',
        print month_start.isoformat(), 'to', month_end.isoformat(), '...'
    toggl = api.TogglAPI(API_TOKEN, TIMEZONE)
    data = toggl.get_time_entries(month_start.isoformat(), month_end.isoformat())
    if pretty_json:
        content = json.dumps(data, sort_keys=True, indent=1,
                             ensure_ascii=False, separators=(',', ': '))
        content = content.encode('utf8')
    else:
        content = json.dumps(data)
    if not os.path.exists(dump_dir):
        os.makedirs(dump_dir)
    filename = os.path.join(dump_dir, '%s.json' % month)

    def md5(string):
        return hashlib.md5(string).digest()

    if os.path.exists(filename) and md5(content) == md5(open(filename).read()):
        if verbose:
            print filename, 'not changed.'
    else:
        file(filename, 'w').write(content)
        if verbose:
            print filename, 'saved.'
    return data


def backup(backup_dir, start_month, pretty_json=False, verbose=False):
    time = datetime.now()
    while True:
        month = '%d-%02d' % (time.year, time.month)
        if month < start_month:
            break
        dump(backup_dir, time.year, time.month, pretty_json=pretty_json,
             verbose=verbose)
        prev_month = (time - timedelta(days=31)).replace(day=1)
        time = prev_month

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('backup_dir')
    parser.add_argument('-v', '--verbose', help='output verbosity',
                        action='store_true')
    parser.add_argument('-p', '--pretty-json',
                        help='save pretty printed JSON, read and diff friendly',
                        action='store_true')
    parser.add_argument('-m', '--start_month', default=START_MONTH,
                        help='backup from START_MONTH, default %r' % START_MONTH)
    args = parser.parse_args()
    backup(args.backup_dir, start_month=args.start_month,
           pretty_json=args.pretty_json, verbose=args.verbose)
