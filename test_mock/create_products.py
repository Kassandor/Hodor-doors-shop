import os
import random

from faker import Faker

from products.models import Product, Organization


def create_fake_products():
    """
    Создание 100 товаров
    """
    fake = Faker()
    image_choices = [f for f in os.listdir('static/img') if f.endswith(('.png', '.jpg', '.jpeg'))]
    organizations = Organization.objects.all()
    # Создаем 100 товаров
    for _ in range(100):
        Product.objects.create(
            name=fake.word(),
            price=round(random.uniform(10, 1000), 2),
            img=random.choice(image_choices),
            organization=random.choice(organizations),
        )
