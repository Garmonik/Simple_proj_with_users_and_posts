import random

from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from facecontrol.models import CodeEmail
from social_media.helpfull import generate_password


def send_confirmation_email(request, user):
    six_digit_number = random.randint(100000, 999999)
    CodeEmail.objects.create(code=six_digit_number, email=user.email)
    current_site = get_current_site(request)
    subject = 'Confirm your account'
    message = render_to_string('email/confirmation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'code': six_digit_number,
    })
    # user.email_user(subject, message)


def send_password_recovery_email(request, user):
    password = generate_password()
    user.password = make_password(password)
    user.save()
    subject = 'Password Recovery'
    message = render_to_string('email/password_recovery.html', {
        'user': user,
        'password': password,
    })
    # user.email_user(subject, message)
