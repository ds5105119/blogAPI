Google SCOPE 응답

{
    "id": string,
    "email": string,
    "verified_email": boolean,
    "name": string,
    "given_name": string,
    "family_name": string,
    "picture": string,
    "locale": string,
}

```python
import os
import hashlib

from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import JsonResponse
import requests
from rest_framework import status


def google_login(request):
    """
    !!! Front-end로 이동 !!!

    Set authorization parameters and Redirect to Google's OAuth 2.0 server
    return
    https://github.com/pennersr/django-allauth/blob/main/allauth/socialaccount/providers/google/views.py
    :param request: httpRequest:
    """
    try:
        client_id = SOCIALACCOUNT_PROVIDERS['google']['APPS']['client_id']
        response_type = "code"

        # https://developers.google.com/people/api/rest/v1/people/get
        scope = SOCIALACCOUNT_PROVIDERS['google']['SCOPE']
        scope = [GOOGLE_PEOPLE_API_ENDPOINT + 'userinfo.' + i for i in scope]
        scope = '+'.join(scope)

        return redirect(
            f'https://accounts.google.com/o/oauth2/v2/accounts?'
            f'?scope={scope}'
            f'&response_type={response_type}'
            f'&redirect_uri={GOOGLE_CALLBACK_URI}'
            f'&client_id={client_id}'
        )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


def google_callback(request):
    """
    !!! Adapter 사용으로 필요없어짐 !!!
    
    Custom Google Login Callback View
    https://developers.google.com/identity/protocols/oauth2/native-app?hl=ko#obtainingaccesstokens
    :param request: httpResponse
    :return: JsonResponse
    """
    client_id = SOCIALACCOUNT_PROVIDERS['google']['client_id']
    secret = SOCIALACCOUNT_PROVIDERS['google']['secret']
    code = request.GET.get('code')
    state = hashlib.sha256(os.urandom(1024)).hexdigest()

    # ----- ISSUE TOKEN START ----- #
    token_response = requests.post(
        f'https://oauth2.googleapis.com/token?client_id={client_id}'
        f'&client_secret={secret}'
        f'&code={code}'
        f'&grant_type=authorization_code'
        f'&redirect_uri={GOOGLE_CALLBACK_URI}'
        f'&state={state}'
    )

    token_response_json = token_response.json()

    error = token_response_json.get("error")
    if error:
        raise ValueError(error)

    access_token = token_response_json.get('access_token')
    refresh_token = token_response_json.get('refresh_token')
    # ----- ISSUE TOKEN END ----- #

    # ----- ISSUE EMAIL, PROFILE IMAGE START ----- #
    tokeninfo_response = requests.get(f'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}')

    if tokeninfo_response.status_code != 200:
        return JsonResponse({'error': 'failed to get user information'}, status=status.HTTP_400_BAD_REQUEST)

    tokeninfo_response_json = tokeninfo_response.json()
    email = tokeninfo_response_json.get('email')
    picture = tokeninfo_response_json.get('picture')
    # ----- ISSUE EMAIL, PROFILE IMAGE END ----- #

    # ----- User Register START ----- #
    try:
        # Disable default login, only use social login
        user = User.objects.get(email=email)
        social_user = SocialAccount.objects.get(user=user)

        if social_user is None:
            return JsonResponse({'error': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'google':
            return JsonResponse({'error': 'already registered with other provider'}, status=status.HTTP_400_BAD_REQUEST)

        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{BASE_URL}accounts/google/login/finish/", data=data)

        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)

        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)

    except User.DoesNotExist:
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{BASE_URL}accounts/google/login/finish/", data=data)

        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)

        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)

```