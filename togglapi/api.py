#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author Mosab Ibrahim <mosab.a.ibrahim@gmail.com>

import requests

from urllib.parse import urlencode
from requests.auth import HTTPBasicAuth


class TogglAPI(object):
    """A wrapper for Toggl Api"""

    def __init__(self, api_token, timezone):
        self.api_token = api_token
        self.timezone = timezone

    def _make_url(self, section='time_entries', params={}):
        """Constructs and returns an api url to call with the section of the API to be called
        and parameters defined by key/pair values in the paramas dict.
        Default section is "time_entries" which evaluates to "time_entries.json"

        >>> t = TogglAPI('_SECRET_TOGGLE_API_TOKEN_')
        >>> t._make_url(section='time_entries', params = {})
        'https://www.toggl.com/api/v8/time_entries'

        >>> t = TogglAPI('_SECRET_TOGGLE_API_TOKEN_')
        >>> t._make_url(section='time_entries', 
                        params = {'start_date': '2010-02-05T15:42:46+02:00', 'end_date': '2010-02-12T15:42:46+02:00'})
        'https://www.toggl.com/api/v8/time_entries?start_date=2010-02-05T15%3A42%3A46%2B02%3A00%2B02%3A00&end_date=2010-02-12T15%3A42%3A46%2B02%3A00%2B02%3A00'
        """

        url = 'https://www.toggl.com/api/v8/{}'.format(section)
        if len(params) > 0:
            url = url + '?{}'.format(urlencode(params))
        return url

    def _query(self, url, method):
        """Performs the actual call to Toggl API"""

        url = url
        headers = {'content-type': 'application/json'}

        if method == 'GET':
            return requests.get(url, headers=headers, auth=HTTPBasicAuth(self.api_token, 'api_token'))
        elif method == 'POST':
            return requests.post(url, headers=headers, auth=HTTPBasicAuth(self.api_token, 'api_token'))
        else:
            raise ValueError('Undefined HTTP method "{}"'.format(method))

    # Time Entry functions
    def get_time_entries(self, start_date='', end_date='', timezone=''):
        """Get Time Entries JSON object from Toggl within a given start_date and an end_date with a given timezone"""

        url = self._make_url(section='time_entries',
                             params={'start_date': start_date + self.timezone, 'end_date': end_date + self.timezone})
        r = self._query(url=url, method='GET')
        return r.json()

    def get_hours_tracked(self, start_date, end_date):
        """Count the total tracked hours within a given start_date and an end_date
        excluding any RUNNING real time tracked time entries
        """
        time_entries = self.get_time_entries(start_date=start_date.isoformat(), end_date=end_date.isoformat())

        if time_entries is None:
            return 0

        total_seconds_tracked = sum(max(entry['duration'], 0) for entry in time_entries)

        return (total_seconds_tracked / 60.0) / 60.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
