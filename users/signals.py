import os

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from faker import Faker

from config.fake_data import create_users

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

fake = Faker()


@receiver(post_migrate)
def create_fake_users(sender, **kwargs):
    create_users()
    return True
