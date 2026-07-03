from django.db import migrations


def backfill_transaction_records(apps, schema_editor):
    TransactionRecord = apps.get_model('core', 'TransactionRecord')
    Revenue = apps.get_model('revenue', 'Revenue')
    Expense = apps.get_model('expenses', 'Expense')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    revenue_content_type, _ = ContentType.objects.using(schema_editor.connection.alias).get_or_create(
        app_label='revenue',
        model='revenue',
    )
    expense_content_type, _ = ContentType.objects.using(schema_editor.connection.alias).get_or_create(
        app_label='expenses',
        model='expense',
    )

    for revenue in Revenue.objects.using(schema_editor.connection.alias).all():
        exists = TransactionRecord.objects.using(schema_editor.connection.alias).filter(
            source_content_type=revenue_content_type,
            source_object_id=revenue.pk,
            action='created',
        ).exists()
        if exists:
            continue

        TransactionRecord.objects.using(schema_editor.connection.alias).create(
            transaction_type='income',
            action='created',
            amount=revenue.total_amount,
            description=revenue.revenue_type,
            transaction_date=revenue.date,
            source_content_type=revenue_content_type,
            source_object_id=revenue.pk,
            source_label=str(revenue),
            notes=revenue.notes,
            metadata={
                'revenue_type': revenue.revenue_type,
                'quantity': str(revenue.quantity),
                'unit': revenue.unit,
                'price_per_unit': str(revenue.price_per_unit),
                'flock_id': revenue.flock_id,
            },
        )

    for expense in Expense.objects.using(schema_editor.connection.alias).all():
        exists = TransactionRecord.objects.using(schema_editor.connection.alias).filter(
            source_content_type=expense_content_type,
            source_object_id=expense.pk,
            action='created',
        ).exists()
        if exists:
            continue

        TransactionRecord.objects.using(schema_editor.connection.alias).create(
            transaction_type='expense',
            action='created',
            amount=expense.amount,
            description=expense.description,
            transaction_date=expense.date,
            source_content_type=expense_content_type,
            source_object_id=expense.pk,
            source_label=str(expense),
            notes=expense.notes,
            metadata={
                'expense_type': expense.expense_type,
                'category': expense.category,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ('revenue', '0001_initial'),
        ('expenses', '0001_initial'),
        ('core', '0004_transactionrecord'),
    ]

    operations = [
        migrations.RunPython(backfill_transaction_records, migrations.RunPython.noop),
    ]
