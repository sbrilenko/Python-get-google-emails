import httplib2

from oauth2client.client import AccessTokenCredentials
from apiclient.discovery import build


class EmailTools:

    def __init__(self, token, user):
        access_token_credentials = AccessTokenCredentials(token, '')
        self.user = user.email
        http = httplib2.Http()
        self.http = access_token_credentials.authorize(http)

    def get_emails(self, user_id, msg_id):
        service = build(serviceName='gmail', version='v1', http=self.http)
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        message_obj = {
            'snippet': message['snippet']
        }
        for head in message['payload']['headers']:
            if head['name'] in ('From', 'Subject','Reply-To', 'Date'):
                message_obj.update({ head['name']: head['value']})
        return message_obj

    def email_list(self):
        service = build(serviceName='gmail', version='v1', http=self.http)
        response = service.users().messages().list(userId=self.user, maxResults=100).execute()
        messages = response.get('messages', [])
        messages_ids = [message['id'] for message in messages]
        emails = [self.get_emails(user_id=self.user, msg_id=message_id
        ) for message_id in messages_ids]
        return emails
