import requests

USERAGENT='okhttp/3.6.0'
APIURL='https://umbrella.nordicwellness.se/api'

class NWSession(object):
    def __init__(self, apiurl, session):
        self._apiurl = apiurl
        self._session = session
    def _get(self, path, params=None):
        r = self._session.get(self._apiurl + path, params=params)
        r.raise_for_status()
        return r.json()
    def _post(self, path):
        r = self._session.post(self._apiurl + path, json={})
        r.raise_for_status()
        return r.json()
    def _delete(self, path):
        r = self._session.delete(self._apiurl + path)
        r.raise_for_status()
        return r.json()
    def get_user(self):
        r = self._get('/user')
        return r['data']
    def get_clubs(self):
        r = self._get('/clubs')
        return r['data']
    def get_activities(self, clubIds=[], groupActivityProductIds=[], instructorIds=[], all=False):
        params={}
        if clubIds:
            params['clubs[]'] = ','.join(str(id) for id in clubIds)
        if groupActivityProductIds:
            params['groupActivityProducts[]'] = ','.join(str(id) for id in groupActivityProductIds)
        if instructorIds:
            params['instructors[]'] = ','.join(str(id) for id in instructorIds)
        if not (params or all):
            return [] # Avoid downloading a huge amount of data unless it's explicitly requested
        r = self._get('/activities', params=params)
        return r['data']
    def get_group_activity_products(self):
        r = self._get('/group-activity-products')
        return r['data']
    def get_instructors(self):
        r = self._get('/instructors')
        return r['data']
    def add_favorite(self, activityId):
        r = self._post('/user/favorite/' + str(activityId))
        return r['message']
    def remove_favorite(self, activityId):
        r = self._delete('/user/favorite/' + str(activityId))
        return r['message']
    def book_activity(self, activityId):
        r = self._post('/activities/' + str(activityId) + '/book')
        return r['message']
    def unbook_activity(self, activityId, brpBookingId):
        r = self._delete('/activities/' + str(activityId) + '/book/' + str(brpBookingId))
        return r['message']

class NWApi(object):
    @staticmethod
    def login(email, password, apiurl=APIURL, userAgent=USERAGENT):
        s = requests.Session()
        s.headers.update({'Accept': 'application/json', 'User-Agent': userAgent})
        r = s.post(apiurl + '/user/auth', json={'email': email, 'password': password})
        r.raise_for_status()
        info = r.json()
        token = info['data']['token']
        user = info['data']['user']
        s.headers.update({'Authorization': 'Bearer ' + token})
        return NWSession(apiurl, s), user
