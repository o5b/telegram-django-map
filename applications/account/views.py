# import requests
# import json
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.serializers import TokenVerifySerializer

from django.forms import models as model_forms
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

import pprint

from django.http import HttpResponse

from . import forms

User = get_user_model()


def get_tokens(request):
    access = ''
    refresh = ''

    if request.method == 'GET':
        # получаем JWT токены из параметров запроса
        access = request.GET.get('access')
        print(f'******* def get_tokens(request): access:**{access}**')
        refresh = request.GET.get('refresh')
        print(f'******* def get_tokens(request): refresh:**{refresh}**')

    if not access or not refresh:
        if hasattr(request, 'headers') and request.headers:

            # получаем JWT токены из Cookie
            if 'Cookie' in request.headers and request.headers['Cookie']:
                cookie_list = request.headers['Cookie'].split()
                for cookie in cookie_list:
                    print(f'******  cookie: {cookie}')
                    if cookie[-1] == ';':
                        cookie = cookie[:-1]
                    if 'refreshToken=' in cookie:
                        refresh = cookie.split('=')[1]
                        print(f'***** cookie refresh: {refresh}')
                    if 'accessToken=' in cookie:
                        access = cookie.split('=')[1]
                        print(f'***** cookie access: {access}')

            # получаем access токен из Token Bearer Authorization
            if not access and 'Authorization' in request.headers and request.headers['Authorization']:
                authorization_list = request.headers['Authorization'].split()
                if len(authorization_list) == 2:
                    if authorization_list[0] == 'Bearer':
                        access = authorization_list[1]
                        print(f'***** Authorization access: {access}')

    return access, refresh



def user_settings_page(request, pk=None, id=None):
    print('******* user_settings_page *******')
    print('***** request: ', dir(request))
    print('***** request.headers: ', request.headers)
    user = {}
    access = ''
    refresh = ''
    access_token = ''
    refresh_token = ''
    user_form = {}
    form_save_result = ''
    user_markers = []

    access, refresh = get_tokens(request)

    if access:
        try:
            access_token_obj = AccessToken(access)
            user = User.objects.get(id=access_token_obj.payload["user_id"])
        except Exception as e:
            print(f'Error get user from access token. Msg: {e}')

    if refresh:
        try:
            refresh_token_obj = RefreshToken(token=refresh)
            print('******* refresh_token_obj: ', refresh_token_obj)
            refresh_token = str(refresh_token_obj)
            access_token = str(refresh_token_obj.access_token)
            if not user:
                access_token_obj = AccessToken(str(refresh_token_obj.access_token))
                user = User.objects.get(id=access_token_obj.payload["user_id"])
        except Exception as e:
            print(f'Error get user from refresh token. Msg: {e}')
            refresh = ''

    if user and not refresh:
        refresh_token_obj = RefreshToken.for_user(user)
        refresh_token = str(refresh_token_obj)
        access_token = str(refresh_token_obj.access_token)

    if request.method == 'POST':
        print(f'********** POST request.user.is_authenticated: {request.user.is_authenticated}')
        print(f'********** POST request.user: {request.user}')
        print(f'******* request.POST:**{request.POST}')
        if user:
            user_form = forms.UserForm(instance=user, data=request.POST)
            if user_form.is_valid():
                user_form.save()
                form_save_result = _('User data saved successfully.')

    if user:
        user_form = forms.UserForm(instance=user)
        # print('******* dir: ', dir(user))
        # print(user.markers.filter(status='published'))
        print('***** user zoom: ', user.map_zoom)
        user_markers = [marker for marker in user.markers.filter(status='published')]
        pprint.pprint(user_markers[1].photo.url)
    else:
        user_form = forms.UserForm()

    print(f'******* user:**{user}**')
    print(f'******* dir user: {dir(user)}')
    print(f'********** request.user.is_authenticated: {request.user.is_authenticated}')

    # print('********* user form: ', user_form)

    return render(
        request,
        'account/user_settings_page.html',
        {
            'form_save_result': form_save_result,
            'user': user,
            'user_form': user_form,
            'refresh_token': refresh_token,
            'access_token': access_token,
            'user_markers': user_markers,
        },
    )


# def user_settings_page(request, pk=None, id=None):
#     print('******* user_settings_page *******')
#     print('***** request: ', dir(request))
#     print('***** request.headers: ', request.headers)
#     user = {}
#     access = ''
#     refresh = ''
#     access_token = ''
#     refresh_token = ''
#     user_form = {}
#     result = ''

#     # if request.user.is_authenticated:
#     #     try:
#     #         user = request.user
#     #     except Exception as e:
#     #         print(f'Error get user from request.user. Msg: {e}')

#     # if not user and not access and not refresh:
#     if not access and not refresh:
#         if hasattr(request, 'headers') and request.headers:

#             # получаем JWT токены из Cookie
#             if 'Cookie' in request.headers and request.headers['Cookie']:
#                 cookie_list = request.headers['Cookie'].split()
#                 for cookie in cookie_list:
#                     print(f'******  cookie: {cookie}')
#                     if cookie[-1] == ';':
#                         cookie = cookie[:-1]
#                     if 'refreshToken=' in cookie:
#                         refresh = cookie.split('=')[1]
#                         print(f'***** cookie refresh: {refresh}')
#                     if 'accessToken=' in cookie:
#                         access = cookie.split('=')[1]
#                         print(f'***** cookie access: {access}')

#             # получаем access токен из Token Bearer Authorization
#             if not access and 'Authorization' in request.headers and request.headers['Authorization']:
#                 authorization_list = request.headers['Authorization'].split()
#                 if len(authorization_list) == 2:
#                     if authorization_list[0] == 'Bearer':
#                         access = authorization_list[1]
#                         print(f'***** Authorization access: {access}')

#     if access:
#         try:
#             access_token_obj = AccessToken(access)
#             user = User.objects.get(id=access_token_obj.payload["user_id"])
#         except Exception as e:
#             print(f'Error get user from access token. Msg: {e}')

#     if refresh:
#         try:
#             refresh_token_obj = RefreshToken(token=refresh)
#             print('******* refresh_token_obj: ', refresh_token_obj)
#             refresh_token = str(refresh_token_obj)
#             access_token = str(refresh_token_obj.access_token)
#             if not user:
#                 access_token_obj = AccessToken(str(refresh_token_obj.access_token))
#                 user = User.objects.get(id=access_token_obj.payload["user_id"])
#         except Exception as e:
#             print(f'Error get user from refresh token. Msg: {e}')
#             refresh = ''

#     if user and not refresh:
#         refresh_token_obj = RefreshToken.for_user(user)
#         refresh_token = str(refresh_token_obj)
#         access_token = str(refresh_token_obj.access_token)

#     if request.method == 'POST':
#         print(f'******* POST user:**{user}**')
#         print(f'********** POST request.user.is_authenticated: {request.user.is_authenticated}')
#         print(f'********** POST request.user: {request.user}')
#         print(f'******* POST user:**{request.POST}')
#         if user:
#             user_form = forms.UserForm(instance=user, data=request.POST)
#             if user_form.is_valid():
#                 user_form.save()
#                 # return HttpResponse('Form save success!')
#                 result = 'Form save success!'

#     if user:
#         user_form = forms.UserForm(instance=user)
#     else:
#         user_form = forms.UserForm()

#     print(f'******* user:**{user}**')
#     print(f'********** request.user.is_authenticated: {request.user.is_authenticated}')

#     # print('********* user form: ', user_form)

#     return render(
#         request,
#         'account/user_settings_page.html',
#         {
#             'result': result,
#             'user': user,
#             'user_form': user_form,
#             'refresh_token': refresh_token,
#             'access_token': access_token,
#         },
#     )



# class DashboardView(TemplateView):
#     template_name = 'account/dashboard.html'
#     UserForm = model_forms.modelform_factory(
#         User, fields=[
#             'username',
#             'telegram_id',
#             'telegram_username',
#             'telegram_language',
#             'is_bot',
#         ])

#     def get_initial(self):
#         if self.request.user.is_authenticated:
#             return {
#                 'username': self.request.user.username or '',
#                 'telegram_id': self.request.user.telegram_id or '',
#                 'telegram_username': self.request.user.telegram_username or '',
#                 'telegram_language': self.request.user.telegram_language or '',
#                 'is_bot': self.request.user.is_bot or '',
#             }
#         return {}

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # client_form = self.ClientForm(instance=self.request.user)
#         # client_form.fields['phone'].widget.attrs['data-mask'] = '+0 (000) 000-00-00'
#         context['user_form'] = self.UserForm(instance=self.request.user)
#         # context['refresh_token'] = refresh_token
#         return context

#     def post(self, *args, **kwargs):
#         user_form = self.UserForm(self.request.POST, instance=self.request.user)

#         if user_form.is_valid():
#             user_form.save()

#         return self.render_to_response(self.get_context_data())
