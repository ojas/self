#!/usr/bin/env python

from __future__ import print_function
import webbrowser
import BaseHTTPServer
from pocket import Pocket
import os

TEMP_SERVER = ('127.0.0.1', 27888)
POCKET_CONSUMER_KEY = '18137-0cc8336b0b4416b26bab9f50'
IMGUR_CLIENT_ID = 'e0fec1517f55162'
IMGUR_SECRET = '69dd7a346509d3c47969395cd22b43d70dc66a7a'
TOKEN_FILE = '.pocket_token'

BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
TOKEN_FILE = os.path.join(BASE_DIR, '.pocket_token')

def get_access_token():
    class WebRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/done': 
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write("<html><script>window.close()</script></html>")
            else:
                self.send_error(404)

    redirect_uri = 'http://%s:%s/done' % (TEMP_SERVER[0], TEMP_SERVER[1])

    request_token = Pocket.get_request_token(consumer_key=POCKET_CONSUMER_KEY, redirect_uri=redirect_uri)

    # URL to redirect user to, to authorize your app
    auth_url = Pocket.get_auth_url(code=request_token, redirect_uri=redirect_uri)

    webbrowser.open(auth_url)

    server = BaseHTTPServer.HTTPServer(TEMP_SERVER, WebRequestHandler)
    server.handle_request()

    user_credentials = Pocket.get_credentials(consumer_key=POCKET_CONSUMER_KEY, code=request_token)
    access_token = user_credentials['access_token']
    return access_token

def get_imgur_token():
    url = 'https://api.imgur.com/oauth2/authorize?client_id=%s&response_type=token' % (IMGUR_CLIENT_ID,)
    print(url)

#get_imgur_token()
#exit()

if __name__ == "__main__":
    token = None
    if os.path.isfile(TOKEN_FILE):
        with open (TOKEN_FILE, 'r') as f:
            token = f.read()

    if token is None:
        token = get_access_token()
        with open (TOKEN_FILE, 'w') as f:
            f.write(token)

    pocket = Pocket(POCKET_CONSUMER_KEY, token)
    """
     u'96090721': {u'excerpt': u'Tells the story of Sofia (Angie Cepeda), a Colombian college student struggling with immigration issues in LA, who accepts a $50,000 offer to rent her body and soul and become a surrogate mother to a wealthy couple.',
                             u'favorite': u'0',
                             u'given_title': u'Love for Rent (2005) - IMDb',
                             u'given_url': u'http://www.imdb.com/title/tt0386603/',
                             u'has_image': u'1',
                             u'has_video': u'0',
                             u'is_article': u'1',
                             u'is_index': u'0',
                             u'item_id': u'96090721',
                             u'resolved_id': u'96090721',
                             u'resolved_title': u'Love for Rent (2005)',
                             u'resolved_url': u'http://www.imdb.com/title/tt0386603/',
                             u'sort_id': 6,
                             u'status': u'0',
                             u'time_added': u'1409164463',
                             u'time_favorited': u'0',
                             u'time_read': u'0',
                             u'time_updated': u'1409164472',
                             u'word_count': u'38'}},

    """

    from pprint import pprint

    resp, meta = pocket.get(state='all', contentType='image')
    # resp, meta = pocket.get(tag='to-watch')
    with open(os.path.join(BASE_DIR, 'Images.md'), 'w') as f:
        print('# Images', file=f)
        print('', file=f)
        for id, item in resp['list'].items():
            s = '![%s](%s)' % (item.get('given_title'), item.get('given_url'))
    #        pprint(item)
    #        s = u'- [%s](%s) - %s' % (item.get('resolved_title', item['given_title']), item.get('resolved_url', item['given_url']), item.get('excerpt', ''))
            print(s.encode('utf-8'), file=f)
            print('', file=f)
    #        f.write()
    #        print 

    #pprint(resp)
    #exit()

    resp, meta = pocket.get(tag='to-watch')
    with open(os.path.join(BASE_DIR, 'Movies.md'), 'w') as f:
        print('# Movies', file=f)
        print('', file=f)
        for id, item in resp['list'].items():
    #        pprint(item)
            s = u'- [%s](%s) - %s' % (item.get('resolved_title', item['given_title']), item.get('resolved_url', item['given_url']), item.get('excerpt', ''))
            print(s.encode('utf-8'), file=f)
    #        f.write()
    #        print 

    # pprint(resp)
    # print 'I have a token %s' % token

