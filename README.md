# Task 12 Create basic application - DjangoGramm
Program like Instagram. The user can register on the website by email.After basic registration, the user will receive a confirmation of the continuation of registration. The email must have a unique link. The user goes by a link redirected to the profile page and add his full name, bio, and avatar. Next user can use DjangoGramm. He can post images, looks pictures of other users.Unauthorized guests cannot view the profile and pictures of users.
## List of used third party apps
1. allauth - Integrated set of Django applications addressing authentication, registration, account management as well as 3rd party (social) account authentication.
2. LoginRequiredMiddleware - All urls require login except registration and login.
3. easy_thumbnails - generation thumbnails for images
4. storages - Media and static storage on AWS S3
5. django_extensions - collection of custom extensions for the Django Framewor.
6. crispy_forms - helps to manage Django forms.
## Example of .env
```
DEBUG=**any or delete for DEBUG=False**
SECRET_KEY=**your secret key here**
DATABASE_URL=psql://urser:un-githubbedpassword@127.0.0.1:8458/database
AWS_ACCESS_KEY_ID=**AWS_ACCESS_KEY_ID**
AWS_SECRET_ACCESS_KEY=**AWS_SECRET_ACCESS_KEY**
AWS_STORAGE_BUCKET_NAME=**AWS_STORAGE_BUCKET_NAME**
EMAIL_HOST_USER=**EMAIL_HOST_USER**
EMAIL_HOST_PASSWORD=**EMAIL_HOST_PASSWORD**
DEFAULT_FROM_EMAIL=**DEFAULT_FROM_EMAIL**
USE_S3=TRUE
```

### Coverage report:
```bash
coverage report -i --omit="*venv\*","*tests\*","*migrations\*"
Name                   Stmts   Miss  Cover
------------------------------------------
__init__.py                0      0   100%
accounts\__init__.py       0      0   100%
accounts\adapter.py       12     12     0%
accounts\admin.py         11      4    64%
accounts\apps.py           4      0   100%
accounts\forms.py         13      6    54%
accounts\models.py        26      6    77%
accounts\urls.py           4      0   100%
accounts\views.py         46     33    28%
config\__init__.py         0      0   100%
config\asgi.py             4      4     0%
config\urls.py            10      4    60%
config\wsgi.py             4      4     0%
manage.py                 12      2    83%
posts\__init__.py          0      0   100%
posts\admin.py             5      0   100%
posts\apps.py              5      1    80%
posts\forms.py             6      0   100%
posts\models.py           25      8    68%
posts\urls.py              4      0   100%
posts\views.py            58     43    26%
------------------------------------------
TOTAL                    249    127    49%
```
## License
[MIT](https://choosealicense.com/licenses/mit/)
