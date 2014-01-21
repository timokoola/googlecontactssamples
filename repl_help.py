from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run, run_flow, argparser
import gdata.contacts.data
import gdata.contacts.client

#...

#storage.put(credentials)
#...
#credentials = storage.get()

import argparse
import sys
import pprint


OAUTH_LABEL='OAuth '

#Transforms OAuth2 credentials to OAuth2 token.
class OAuthCred2Token(object):

    def __init__(self, token_string):
        self.token_string = token_string

    def modify_request(self, http_request):
        http_request.headers['Authorization'] = '%s%s' % (OAUTH_LABEL,
                                                          self.token_string)

    ModifyRequest = modify_request

def main(argv):
	parser = argparse.ArgumentParser(description=__doc__,
	        formatter_class=argparse.RawDescriptionHelpFormatter,
	        parents=[argparser])
	flags = parser.parse_args(argv)
	flow = flow_from_clientsecrets('client_secrets.json',
	#flow = run_flow('client_secrets.json',
	                              scope='https://www.google.com/m8/feeds',
	                              redirect_uri='http://example.com/auth_return')
	storage = Storage('a_credentials_file.json')
	credentials = run_flow(flow, storage, flags)
	gd_client = gdata.contacts.client.ContactsClient(source='contacts sample')
	token = OAuthCred2Token(credentials.access_token)
	gd_client.auth_token = token
	pp = pprint.PrettyPrinter(depth=6)
	contacts = gd_client.GetContacts()

if __name__ == '__main__':
	main(sys.argv[1:])