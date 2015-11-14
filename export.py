import logging
import os
import sys
import urllib.parse
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

"""
MapMyRun workout export utility

Heavily drawn from https://developer.underarmour.com/docs/v71_OAuth_2_Demo
"""


def main():
    print('=======================')
    print('MapMyRun Export Utility')
    print('=======================\n')
    client_id = input('Enter the client id you will use for auth: ').strip()
    client_secret = input('Enter the client secret you will use for auth: ').strip()

    if not is_valid(client_id) or not is_valid(client_secret):
        print('\nMust provide a client id and client secret for auth! Exiting...')
        sys.exit(1)

    redirect_uri = 'http://localhost.mapmyapi.com:12345/callback'
    authorize_url = 'https://api.mapmyfitness.com/v7.1/oauth2/authorize/?' \
                    'client_id={0}&response_type=code&redirect_uri={1}'.format(client_id, redirect_uri)

    parsed_redirect_uri = urllib.parse.urlparse(redirect_uri)
    server_address = parsed_redirect_uri.hostname, parsed_redirect_uri.port

    print('server_address:', server_address)

    # NOTE: Don't go to the web browser just yet...
    webbrowser.open(authorize_url)

    # Start our web server. handle_request() will block until a request comes in.
    httpd = HTTPServer(server_address, AuthorizationHandler)
    print('Now waiting for the user to authorize the application...')
    httpd.handle_request()




def is_valid(some_str):
    return some_str is not None and len(some_str) > 0


class AuthorizationHandler(BaseHTTPRequestHandler):
    """
    Handler for redirect issued by the MapMyFitness authorize page.
    """
    def do_get(self):
        self.send_response(200, 'OK')
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.server.path = self.path


if __name__ == "__main__":
    main()
