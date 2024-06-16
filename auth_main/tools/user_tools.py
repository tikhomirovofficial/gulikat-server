import uuid
import random
from django.contrib.auth.models import User
from lk.models import Profile
from settings.tools.atc import ATC

from settings.tools.telegram import (
    send_message_auth,
    # TelegramBot,
)

def get_uuid():
    return uuid.uuid4()


def set_user_code(user):
    code = random.randint(1010, 9090)
    user.set_password(f"{code}")
    user.save()
    atc = ATC()
    atc.send_message(user.username, f"{code}")
    send_message_auth(user.username, f"{code}")
    # th.start()
    # send_message_auth(user.username, code)
    return f"{code}"


def create_user(username):
    user = User.objects.create(
        username = username,
        password = get_uuid()
    )
    code = set_user_code(user)
    # user.set_password(code)
    profile = Profile.objects.create(
        user = user
    )