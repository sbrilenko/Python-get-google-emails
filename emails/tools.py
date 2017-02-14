import httplib2

from oauth2client.client import AccessTokenCredentials
from apiclient.discovery import build


class EmailTools(object):

    def __init__(self, token, user):
        access_token_credentials = AccessTokenCredentials(token, '')
        self.user = user.email
        self.http = access_token_credentials.authorize(httplib2.Http())
        self.emails = []

    def batch_emails_callback(self, request_id, response, exception):
        if exception is not None:
            pass
        else:
            message_obj = {
                'snippet': response['snippet']
            }
            for head in response['payload']['headers']:
                if head['name'] in ('From', 'Subject','Reply-To', 'Date'):
                    message_obj.update({ head['name']: head['value']})
            self.emails.append(message_obj)

    def get_emails_list(self):
        service = build(serviceName='gmail', version='v1', http=self.http)
        service_users_messages = service.users().messages()
        response = service_users_messages.list(userId=self.user, maxResults=100).execute()
        messages = response.get('messages', [])
        batch = service.new_batch_http_request(callback=self.batch_emails_callback)
        for message in messages:
            batch.add(service_users_messages.get(userId=self.user, id=message['id']))

        batch.execute()
        return self.emails
