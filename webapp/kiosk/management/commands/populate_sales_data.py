import random
from datetime import datetime, timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from kiosk.models import Product, Card, Cart, CartItem


class Command(BaseCommand):
    help = 'Populates the database with random sales data for testing (1 month, ~50 cards, 5-40 sales/day)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Number of days of sales data to generate (default: 30)',
        )
        parser.add_argument(
            '--cards',
            type=int,
            default=50,
            help='Number of unique cards to create (default: 50)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing carts, cart items, and cards before populating',
        )

    def handle(self, *args, **options):
        days = options['days']
        num_cards = options['cards']

        # Clear existing data if --clear flag is used
        if options['clear']:
            cart_items_count = CartItem.objects.all().count()
            carts_count = Cart.objects.all().count()
            cards_count = Card.objects.all().count()

            CartItem.objects.all().delete()
            Cart.objects.all().delete()
            Card.objects.all().delete()

            self.stdout.write(self.style.WARNING(
                f'Cleared {cart_items_count} cart items, {carts_count} carts, and {cards_count} cards'
            ))

        # Get all products
        products = list(Product.objects.filter(enabled=True))
        if not products:
            self.stdout.write(self.style.ERROR(
                'No products found! Run "python manage.py populate_products" first.'
            ))
            return

        self.stdout.write(f'Found {len(products)} products to use')

        # Create cards
        self.stdout.write(f'Creating {num_cards} cards...')
        cards = []
        for i in range(num_cards):
            # Generate random 8 or 14 character card numbers
            if random.random() < 0.5:
                card_number = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            else:
                card_number = ''.join([str(random.randint(0, 9)) for _ in range(14)])

            # Some cards get aliases
            alias = f'TestUser{i+1}' if random.random() < 0.3 else ''

            card = Card.objects.create(
                card_number=card_number,
                alias=alias,
                datetime_created=timezone.now() - timedelta(days=random.randint(30, 365))
            )
            cards.append(card)

        self.stdout.write(self.style.SUCCESS(f'Created {len(cards)} cards'))

        # Generate sales data for each day
        total_carts = 0
        total_items = 0

        for day_offset in range(days):
            # Calculate the date (going backwards from today)
            sale_date = timezone.now() - timedelta(days=days - day_offset - 1)

            # Random number of sales for this day (5-40)
            num_sales = random.randint(5, 40)

            for sale_num in range(num_sales):
                # Random card for this sale
                card = random.choice(cards)

                # Create random time during the day (business hours: 7am - 10pm)
                hour = random.randint(7, 21)
                minute = random.randint(0, 59)
                second = random.randint(0, 59)

                sale_datetime = sale_date.replace(hour=hour, minute=minute, second=second)

                # Create cart
                cart_obj = Cart.objects.create(
                    card=card,
                    completion_status='complete',
                    datetime_completed=sale_datetime
                )
                # Override the auto_now_add for datetime_created to be slightly before completion
                cart_obj.datetime_created = sale_datetime - timedelta(minutes=random.randint(1, 15))
                cart_obj.save()

                # Update card's last_scanned to this time
                if card.last_scanned is None or sale_datetime > card.last_scanned:
                    card.last_scanned = sale_datetime
                    card.save()

                # Add random number of items to cart (1-5 items)
                num_items = random.randint(1, 5)
                cart_products = random.choices(products, k=num_items)

                for product in cart_products:
                    CartItem.objects.create(
                        cart=cart_obj,
                        product=product,
                        price=product.price,
                        removed=False
                    )
                    total_items += 1

                total_carts += 1

            self.stdout.write(
                f'Day {day_offset + 1}/{days}: {sale_date.strftime("%Y-%m-%d")} - {num_sales} sales'
            )

        self.stdout.write(self.style.SUCCESS(
            f'\nSuccessfully created {total_carts} completed carts with {total_items} items!'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'Date range: {(timezone.now() - timedelta(days=days)).strftime("%Y-%m-%d")} to {timezone.now().strftime("%Y-%m-%d")}'
        ))
