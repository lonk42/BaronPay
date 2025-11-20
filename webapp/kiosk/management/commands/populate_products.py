import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from kiosk.models import Product


class Command(BaseCommand):
    help = 'Populates the database with dummy junk food products for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing products before populating',
        )

    def handle(self, *args, **options):
        # Junk food names for random selection
        junk_food_names = [
            "Chips",
            "Soda Can",
            "Chocolate Bar",
            "Pie",
            "Noodles",
            "Poplers",
            "Chocolate Biscuit",
            "Pizza",
            "Energy Drink",
            "Sauce",
            "Museli Bar",
            "Bacon Strips",
            "An entire ham leg",
            "Fruit"
        ]

        # Discount text options for the 3 items that will have discounts
        discount_options = ["SALE!", "2 for 1", "50% OFF", "LIMITED"]

        # Clear existing products if --clear flag is used
        if options['clear']:
            count = Product.objects.all().count()
            Product.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Cleared {count} existing products'))

        # Create 12 products (one page worth: 3 rows x 4 columns)
        products_created = 0
        selected_names = random.sample(junk_food_names, min(12, len(junk_food_names)))

        # Select 3 random indices to have discount text
        discount_indices = set(random.sample(range(len(selected_names)), 3))

        for i, name in enumerate(selected_names):
            # Generate random price between $0.20 and $5.00, rounded to 10 cents
            price_cents = random.randint(2, 50) * 10  # 20 to 500 cents, in steps of 10
            price = Decimal(price_cents) / Decimal(100)

            # Only assign discount text to 3 products
            discount_text = random.choice(discount_options) if i in discount_indices else ""

            # Create the product
            product = Product.objects.create(
                name=name,
                price=price,
                enabled=True,
                notes=f"Dummy product for testing",
                discount_text=discount_text,
                thumbnail_file="chocolate_bar.jpg",
                ordering_priority=i * 10  # Spread them out: 0, 10, 20, ...
            )
            products_created += 1

            # Display created product info
            discount_display = f" [{discount_text}]" if discount_text else ""
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created: {name} - ${price}{discount_display}'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully created {products_created} dummy products!'
            )
        )
