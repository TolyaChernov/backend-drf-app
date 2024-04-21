import os
import random

from django.utils import timezone
from faker import Faker

from links.models import Collection, Link
from users.models import CustomUser

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

fake = Faker()


def create_users(num_users=20):
    for _ in range(num_users):
        email = fake.email()
        password = fake.password()
        user = CustomUser.objects.create_user(email=email, password=password)
        print(f"Created user: {email}")
        create_collections(user)
        return


def create_collections(
    owner_collection, num_collections=10, num_links_per_collection=15
):
    CustomUser.objects.all()
    for _ in range(num_collections):
        collection = Collection.objects.create(
            title=fake.sentence(),
            description=fake.paragraph(),
            created_at=fake.date_time_between(
                start_date="-1y", end_date="now"),
            updated_at=timezone.now(),
            user=owner_collection,
        )
        print(f"Created collection: {collection.title}")
        create_links(collection, owner_collection, num_links_per_collection)


def create_links(collection, owner_link, num_links=15):
    for _ in range(num_links):
        link = Link.objects.create(
            title=fake.sentence(),
            description=fake.paragraph(),
            url=fake.url(),
            image=fake.image_url(),
            link_type=random.choice([choice[0] for choice in Link.LINK_TYPES]),
            created_at=fake.date_time_between(
                start_date="-1y", end_date="now"),
            updated_at=timezone.now(),
            user=owner_link,
        )
        link.collections.add(collection)
        print(f"Created link: {link.title}")
