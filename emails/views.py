# -*- encoding: utf-8 -*-
from apiclient import errors
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from rest_framework.renderers import JSONRenderer

from .tools import EmailTools

def index(request):
    user = request.user
    if not hasattr(user, 'social_auth'):
        logout(request)
    return render(request, 'index.html')

def logout_user(request):
    logout(request)
    return redirect('emails:index')

class Emails(APIView):
    renderer_classes = (JSONRenderer,)

    def get(self, request):
        user = request.user
        social = user.social_auth.get(provider='google-oauth2')
        access_token = social.extra_data['access_token']
        print(access_token)
        email_tools = EmailTools(access_token, user)
        print(email_tools)
        print(EmailTools)
        try:
            emails = email_tools.get_emails_list()
            return Response(emails)
        except errors.HttpError, error:
            return Response('An error occurred: %s' % error)
        except Exception as e:
            raise e
            return Response([])
