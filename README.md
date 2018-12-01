nwapi-py
========

This is a small Python 3 API for interacting with some online booking systems,
and it just happens to work well with Nordic Wellness.

THIS IS NOT AN OFFICIAL OR SUPPORTED API. It might not even be working anymore
by the time you read this.

Example usage
-------------

You are encouraged to read the source for the full API (it's not very long)
but here's an example to get you up and running:

    from nwapi import NWApi
    session, userinfo = NWApi.login('myuser', 'mypassword')
    session.get_clubs()
    session.get_activities(clubsIds=[1])
