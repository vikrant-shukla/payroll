# your_app/authentication.py
from django.contrib.auth.backends import ModelBackend

class LowercaseEmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None:
            email = kwargs.get('email')

        # Lowercase the email address
        if email is not None:
            email = email.lower()

        # Call the parent authenticate method
        return super().authenticate(request, email, password, **kwargs)
