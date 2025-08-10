# Django JWT Authentication App

## Introduction

This app can handle user registration, login and logout with JSON Web Token authentication.

## Setting up

### Prerequisites

Before starting you have to install the required packages. They are listed inside the `requirements.txt` file.

### Integration

To integrate this tool to your project, you must copy the `auth_app` directory to the root directory of your project.

Then, inside the `settings.py` file of your project, make sure to add `'auth_app'` inside the `INSTALLED_APPS` list.

### CORS Configuration

To allow API calls for a front end framework, you must also configure CORS headers.

Inside the `settings.py`, add these lines:

```python
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [
    'http://localhost:4200',  # This is the address of your front end app
]
```

### Simple JWT Configuration

Inside the `settings.py` file of your project, add `'rest_framework_simplejwt'` and `'rest_framework_simplejwt.token_blacklist'` to the `INSTALLED_APPS`.

Then, at the end of the `settings.py` file, add these lines:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'],  # All views in your app will require authentication. You can comment this line if you want
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),  # The access token expires after 5 minutes (you might add this import: from datetime import timedelta)
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),    # The refresh token expires after 1 day
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

AUTH_USER_MODEL = "auth_app.User"
```

### URL Configuration

To finish, in the `urls.py` file of your project, add this path to the URL patterns:

```python
path('auth/', include('auth_app.urls')),
```

Then you are all set!

## Initialization

### Database Setup

Do the migrations first:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Run the Server

Then run the server:

```bash
python manage.py runserver
```

## Usage

### Configuration

Check `serializers.py` and `models.py` if you need to see or modify the required fields for registration.

### Authentication

- **Login**: Expects 3 fields: `email`, `username`, `password` and returns 2 tokens:
  - An access token that may be associated to prove the user authenticity
  - A refresh token needed to refresh the access token when it expires

- **Logout**: Will blacklist the access token, making it no longer usable. This will require the user to login once again to get new usable tokens.

### Examples

For examples of requests, see the `api.http` file.