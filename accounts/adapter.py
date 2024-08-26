from accounts.models import User
from accounts.utils import generate_handel

try:
    from allauth.utils import valid_email_or_none
    from allauth.account.adapter import DefaultAccountAdapter
    from allauth.account.adapter import get_adapter as get_account_adapter
    from allauth.account.utils import user_email, user_username
    from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
except ImportError:
    raise ImportError('allauth needs to be added to INSTALLED_APPS.')


class CustomAccountAdapter(DefaultAccountAdapter):
    pass


# https://docs.allauth.org/en/latest/account/advanced.html
class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user_data = sociallogin.account.extra_data

    def save_user(self, request, sociallogin, form=None):
        user = sociallogin.user
        user.set_unusable_password()
        if form:
            get_account_adapter().save_user(request, user, form)
        else:
            get_account_adapter().populate_username(request, user)
        sociallogin.save(request)
        return user

    def populate_user(self, request, sociallogin, data):
        extra_data = sociallogin.account.extra_data

        name = data.get("name") or extra_data.get("name")
        email = data.get("email") or extra_data.get("email")
        profile_image = extra_data.get("picture")
        handel = generate_handel()
        while User.objects.filter(handel=handel).exists():
            handel = generate_handel()

        user = sociallogin.user
        user.name = name or ""
        user_email(user, valid_email_or_none(email) or "")
        user.handel = handel
        return user
