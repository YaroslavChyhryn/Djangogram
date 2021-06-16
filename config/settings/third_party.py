# easy-thumbnail
# todo play with thumbnail settings
THUMBNAIL_ALIASES = {
    'posts.Post.image': {
        'small': {'size': (256, 256)},
        'medium': {'size': (512, 512)},
        'large': {'size': (1024, 1024)},
    },
    'accounts.UserProfile.avatar': {
        'avatar_small': {'size': (64, 64)},
        'avatar_large': {'size': (256, 256)},
    },
}

# django-allauth
AUTH_USER_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_ADAPTER = 'accounts.adapter.MyAccountAdapter'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_EMAIL_VERIFICATION = False
SOCIALACCOUNT_QUERY_EMAIL = False
# crispy_forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

# django-allauth
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'github': {
        'SCOPE': [
            'user',
            'repo',
            'read:org',
        ],
    }
}