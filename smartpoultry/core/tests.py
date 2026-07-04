from datetime import date
from decimal import Decimal
import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from core.models import RoosterAgeEstimate, TransactionRecord
from expenses.models import Expense
from inventory.models import Inventory
from revenue.models import Revenue


class TransactionRecordTests(TestCase):
    def test_revenue_creates_transaction_record(self):
        revenue = Revenue.objects.create(
            revenue_type='eggs',
            quantity=Decimal('12'),
            unit='tray',
            price_per_unit=Decimal('180'),
            date=date(2026, 7, 4),
            notes='Morning sale',
        )

        transaction = TransactionRecord.objects.get(source_object_id=revenue.pk)

        self.assertEqual(transaction.transaction_type, 'income')
        self.assertEqual(transaction.action, 'created')
        self.assertEqual(transaction.amount, revenue.total_amount)
        self.assertEqual(transaction.transaction_date, revenue.date)

    def test_expense_creates_transaction_record(self):
        expense = Expense.objects.create(
            expense_type='feed',
            description='Layer feed',
            amount=Decimal('1250.00'),
            date=date(2026, 7, 4),
            category='supplies',
        )

        transaction = TransactionRecord.objects.get(source_object_id=expense.pk)

        self.assertEqual(transaction.transaction_type, 'expense')
        self.assertEqual(transaction.action, 'created')
        self.assertEqual(transaction.amount, expense.amount)
        self.assertEqual(transaction.description, expense.description)

    def test_inventory_create_creates_matching_expense(self):
        item = Inventory.objects.create(
            item_type='feed',
            name='Chicken Feeds',
            quantity=Decimal('10'),
            unit='kg',
            cost_per_unit=Decimal('125.00'),
        )

        expense = Expense.objects.get(description='Inventory purchase: Chicken Feeds')

        self.assertEqual(expense.expense_type, item.item_type)
        self.assertEqual(expense.amount, Decimal('1250.00'))
        self.assertEqual(expense.date, item.date_added)
        self.assertEqual(expense.category, 'inventory')


class RoosterAgeEstimatorTests(TestCase):
    def setUp(self):
        self.media_root = tempfile.mkdtemp()
        self.override = override_settings(MEDIA_ROOT=self.media_root)
        self.override.enable()
        self.user = get_user_model().objects.create_user(
            username='tester',
            password='password123',
        )
        self.client.force_login(self.user)

    def tearDown(self):
        self.override.disable()
        shutil.rmtree(self.media_root, ignore_errors=True)

    def test_saves_only_uploaded_rooster_photos(self):
        photo = SimpleUploadedFile(
            'rooster.jpg',
            b'fake image bytes',
            content_type='image/jpeg',
        )

        response = self.client.post(reverse('rooster_age_estimator'), {
            'photos': [photo],
            'spur_visibility': ['clear', 'clear'],
            'spur_length': ['short', 'long'],
            'spur_thickness': ['thin', 'thick'],
            'spur_point_shape': ['rounded', 'pointed'],
            'spur_curvature': ['straight', 'curved'],
            'secondary_clues': ['', 'extra blank card'],
        })

        self.assertEqual(response.status_code, 200)
        estimates = RoosterAgeEstimate.objects.filter(user=self.user)
        self.assertEqual(estimates.count(), 1)
        self.assertEqual(estimates.first().photo_name, 'rooster.jpg')
        self.assertTrue(estimates.first().photo)
