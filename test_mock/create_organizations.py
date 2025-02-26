from faker import Faker

from products.models import Organization


def create_fake_organizations():
    """
    Создание 10 организаций
    """
    fake = Faker()
    organizations = []
    for _ in range(10):
        org = Organization.objects.create(name=fake.company(), country=fake.country(), city=fake.city())
        organizations.append(org)
