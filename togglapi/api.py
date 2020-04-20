#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author Mosab Ibrahim <mosab.a.ibrahim@gmail.com>

import requests

from urllib.parse import urlencode
from requests.auth import HTTPBasicAuth

""" To access parent module """
import sys
sys.path.insert(0, '..')

from run import hilite, SUCCESS, ERROR, WARNING


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

        """
            -> the API can't filter by pid or wid ?! -> so it's done locally (below: doFilter())

            curl -v -u XXXXXXXXXXXXXXXXXXXXXXXXX:api_token \
            -X GET "https://www.toggl.com/api/v8/time_entries?start_date=2020-04-01T00%3A00%3A00%2B02%3A00&end_date=2020-04-20T14%3A27%3A31%2B02%3A00"
        """

        url = self._make_url(section='time_entries',
                             params={
                                        'start_date': start_date + self.timezone,
                                        'end_date': end_date + self.timezone
                                    })
        r = self._query(url=url, method='GET').json()
        ret = self.doFilter(r) # filter manually ...
        return ret

    def get_hours_tracked(self, start_date, end_date):
        """Count the total tracked hours within a given start_date and an end_date
        excluding any RUNNING real time tracked time entries
        """
        time_entries = self.get_time_entries(start_date=start_date.isoformat(), end_date=end_date.isoformat())

        print('Number of entries :', len(time_entries), "(max: 1000)\n")

        if time_entries is None:
            return 0

        total_seconds_tracked = sum(max(entry['duration'], 0) for entry in time_entries)

        return (total_seconds_tracked / 60.0) / 60.0

    def get_project_by_name(self, project_name):
        """Get project informations from %name% (CONTAINS)"""
        # Search in all workspaces
        url = self._make_url(section='workspaces')
        workspaces = self._query(url=url, method='GET').json()

        projects = []
        for w in workspaces: # search the matching project in all workspaces
            section = 'workspaces/'+str(w["id"])+'/projects'
            url = self._make_url(section=section)
            r = self._query(url=url, method='GET')
            try:
                projects = projects + r.json()
            except:
                pass # case when response = 'null' / no project ?

        match_projects = [p for p in projects if project_name in p['name']]
        if len(match_projects) > 1 or len(match_projects) == 0: # multiple <or> no match
            print(hilite('WARNING : Multiple matching project, or no project with name : ' + project_name + "\n", WARNING, True))
            return False
        return match_projects[0]

    def set_filter(self, project_name=None, workspace_name=None, client_name=None):
        """Find useful ids for the filter"""
        workspace_id = None
        project_id = None
        client_id = None
        client_project_ids = None

        # Search the project_id
        if project_name:
            project = self.get_project_by_name(project_name)
            if project != False:
                project_id = project['id']
        
        # Search the workspace_id
        if workspace_name:
            url = self._make_url(section='workspaces')
            workspaces = self._query(url=url, method='GET').json()
            workspace = [w for w in workspaces if workspace_name in w['name']]
            if len(workspace) == 1:
                workspace_id = workspace[0]['id']
        
        # Search the project_id(s) for this client
        if client_name:
            url = self._make_url(section='clients')
            clients = self._query(url=url, method='GET').json()
            client = [w for w in clients if client_name in w['name']]
            if len(client) == 1:
                client_id = client[0]['id']
                # find projects linked to a client
                section = 'clients/'+str(client_id)+'/projects'
                url = self._make_url(section=section)
                r = self._query(url=url, method='GET')
                client_projects = []
                try:
                    client_projects = client_projects + r.json()
                except:
                    pass # case when repsonse = 'null'
                client_project_ids = [p['id'] for p in client_projects]

        self.workspace_id = workspace_id
        self.project_id = project_id
        self.client_id = client_id
        self.client_project_ids = client_project_ids

    def doFilter(self, r):
        """Apply filter on entries"""
        ret = []
        if self.project_id:
            ret = [entry for entry in r if "pid" in entry and entry["pid"] == self.project_id]
        if self.workspace_id:
            ret = [entry for entry in r if "wid" in entry and entry["wid"] == self.workspace_id]
        if self.client_project_ids:
            ret = [entry for entry in r if "pid" in entry and entry["pid"] in self.client_project_ids]
        if not self.project_id and not self.workspace_id and not self.client_project_ids:
            ret = r # no filter
        return ret

if __name__ == '__main__':
    import doctest

    doctest.testmod()
