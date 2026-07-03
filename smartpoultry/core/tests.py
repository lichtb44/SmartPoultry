from datetime import date
from decimal import Decimal

from django.test import TestCase

from core.models import TransactionRecord
from expenses.models import Expense
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
