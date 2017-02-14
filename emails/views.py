# -*- encoding: utf-8 -*-
import httplib2
from apiclient import errors
from apiclient.discovery import build
from oauth2client.client import AccessTokenCredentials
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from rest_framework.renderers import JSONRenderer

def index(request):
    user = request.user
    if not hasattr(user, 'social_auth'):
        logout(request)
    return render(request, 'index.html')

def logout_user(request):
    logout(request)
    return redirect('emails:index')

def google_service(request):
    user = request.user
    if hasattr(user, 'social_auth'):
        social = user.social_auth.get(provider='google-oauth2')
        access_token = social.extra_data['access_token']
        access_token_credentials = AccessTokenCredentials(access_token, '')
        http = httplib2.Http()
        http = access_token_credentials.authorize(http)
        service = build(serviceName='gmail', version='v1', http=http)
        return service
    else: return

def email_list(service):
    response = service.users().messages().list(userId='me', maxResults=100).execute()
    messages = response.get('messages', [])
    messages_ids = [message['id'] for message in messages]
    emails = [get_emails(
        service=service, user_id='me', msg_id=message_id
        ) for message_id in messages_ids]
    return emails

def get_emails(service, user_id, msg_id):
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()
    message_obj = {
        'snippet': message['snippet']
    }
    for head in message['payload']['headers']:
        if head['name'] in ('From', 'Subject','Reply-To', 'Date'):
            message_obj.update({ head['name']: head['value']})
    return message_obj

class Emails(APIView):
    renderer_classes = (JSONRenderer,)

    def get(self, request):
        try:
            service = google_service(request)
            if service:
                emails = email_list(service)
                return Response(emails)
        except errors.HttpError, error:
            return Response('An error occurred: %s' % error)
        except:
            return Response([])
