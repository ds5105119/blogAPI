from accounts.models import User, Profile, Follow

try:
    from rest_framework import serializers
    from dj_rest_auth.registration.serializers import *
    from django.utils.translation import gettext_lazy as _
    from dj_rest_auth.registration.serializers import RegisterSerializer
except ImportError:
    raise ImportError('django, django-rest-framework, dj-rest-accounts needs to be added to INSTALLED_APPS.')


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('follower', 'created_at')
        read_only_fields = ['follower', 'created_at']


class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('user', 'created_at')
        read_only_fields = ['user', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('handel',
                  'username',
                  'email',
                  'following',
                  'followers')

    def get_following(self, obj):
        return FollowingSerializer(obj.following.all(), many=True).data

    def get_followers(self, obj):
        return FollowerSerializer(obj.followers.all(), many=True).data


class UserIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('handel', )

    def validate(self, attrs):
        if 'handel' not in attrs:
            raise serializers.ValidationError({"error": "handel not provided"})
        if User.objects.filter(id=attrs['handel']).exists():
            raise serializers.ValidationError({"error": "This ID already exists."})
        return attrs


class CustomSocialLoginSerializer(SocialLoginSerializer):
    """
    dj_rest_auth.registration.serializers.SocialLoginSerializer.validate method is not compatible
    with get_scope of adapter in allauth version 0.62.0 and higher.
    Handling to use get_scope_from_request
    https://github.com/iMerica/dj-rest-auth/issues/639
    """
    def validate(self, attrs):
        try:
            return super().validate(attrs)
        except TypeError as e:
            return self.custom_validate(attrs)

    def custom_validate(self, attrs):
        view = self.context.get('view')
        request = self._get_request()

        if not view:
            raise serializers.ValidationError(
                _('View is not defined, pass it as a context variable'),
            )

        adapter_class = getattr(view, 'adapter_class', None)
        if not adapter_class:
            raise serializers.ValidationError(_('Define adapter_class in view'))

        adapter = adapter_class(request)
        app = adapter.get_provider().app

        # More info on code vs access_token
        # http://stackoverflow.com/questions/8666316/facebook-oauth-2-0-code-and-token

        access_token = attrs.get('access_token')
        code = attrs.get('code')
        # Case 1: We received the access_token
        if access_token:
            tokens_to_parse = {'access_token': access_token}
            token = access_token
            # For sign in with apple
            id_token = attrs.get('id_token')
            if id_token:
                tokens_to_parse['id_token'] = id_token

        # Case 2: We received the authorization code
        elif code:
            self.set_callback_url(view=view, adapter_class=adapter_class)
            self.client_class = getattr(view, 'client_class', None)

            if not self.client_class:
                raise serializers.ValidationError(
                    _('Define client_class in view'),
                )

            provider = adapter.get_provider()
            client = self.client_class(
                request,
                app.client_id,
                app.secret,
                adapter.access_token_method,
                adapter.access_token_url,
                self.callback_url,
                scope_delimiter=adapter.scope_delimiter,
                headers=adapter.headers,
                basic_auth=adapter.basic_auth,
            )
            try:
                token = client.get_access_token(code)
            except OAuth2Error as ex:
                raise serializers.ValidationError(
                    _(f'Failed to exchange code for access token, received: {ex}')
                ) from ex
            access_token = token['access_token']
            tokens_to_parse = {'access_token': access_token}

            # If available we add additional data to the dictionary
            for key in ['refresh_token', 'id_token', adapter.expires_in_key]:
                if key in token:
                    tokens_to_parse[key] = token[key]
        else:
            raise serializers.ValidationError(
                _('Incorrect input. access_token or code is required.'),
            )

        social_token = adapter.parse_token(tokens_to_parse)
        social_token.app = app

        try:
            if adapter.provider_id == 'google' and not code:
                login = self.get_social_login(adapter, app, social_token, response={'id_token': id_token})
            else:
                login = self.get_social_login(adapter, app, social_token, token)
            ret = complete_social_login(request, login)
        except HTTPError:
            raise serializers.ValidationError(_('Incorrect value'))

        if isinstance(ret, HttpResponseBadRequest):
            raise serializers.ValidationError(ret.content)

        if not login.is_existing:
            # We have an account already signed up in a different flow
            # with the same email address: raise an exception.
            # This needs to be handled in the frontend. We can not just
            # link up the accounts due to security constraints
            if allauth_account_settings.UNIQUE_EMAIL:
                # Do we have an account already with this email address?
                account_exists = get_user_model().objects.filter(
                    email=login.user.email,
                ).exists()
                if account_exists:
                    raise serializers.ValidationError(
                        _('User is already registered with this e-mail address.'),
                    )

            login.lookup()
            try:
                login.save(request, connect=True)
            except IntegrityError as ex:
                raise serializers.ValidationError(
                    _('User is already registered with this e-mail address.'),
                ) from ex
            self.post_signup(login, attrs)

        attrs['user'] = login.account.user

        return attrs
