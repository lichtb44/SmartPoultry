from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from core.models import TransactionRecord
from expenses.models import Expense
from revenue.models import Revenue


def _content_type_for(instance, using):
    return ContentType.objects.db_manager(using).get_for_model(
        instance,
        for_concrete_model=False,
    )


def _record_revenue_transaction(instance, action, using):
    TransactionRecord.objects.using(using).create(
        transaction_type='income',
        action=action,
        amount=instance.total_amount,
        description=instance.get_revenue_type_display(),
        transaction_date=instance.date,
        source_content_type=_content_type_for(instance, using),
        source_object_id=instance.pk,
        source_label=str(instance),
        notes=instance.notes,
        metadata={
            'revenue_type': instance.revenue_type,
            'quantity': str(instance.quantity),
            'unit': instance.unit,
            'price_per_unit': str(instance.price_per_unit),
            'flock_id': instance.flock_id,
        },
    )


def _record_expense_transaction(instance, action, using):
    TransactionRecord.objects.using(using).create(
        transaction_type='expense',
        action=action,
        amount=instance.amount,
        description=instance.description,
        transaction_date=instance.date,
        source_content_type=_content_type_for(instance, using),
        source_object_id=instance.pk,
        source_label=str(instance),
        notes=instance.notes,
        metadata={
            'expense_type': instance.expense_type,
            'category': instance.category,
        },
    )


@receiver(post_save, sender=Revenue, dispatch_uid='record_revenue_transaction_save')
def record_revenue_save(sender, instance, created, using, **kwargs):
    action = 'created' if created else 'updated'
    _record_revenue_transaction(instance, action, using)


@receiver(pre_delete, sender=Revenue, dispatch_uid='record_revenue_transaction_delete')
def record_revenue_delete(sender, instance, using, **kwargs):
    _record_revenue_transaction(instance, 'deleted', using)


@receiver(post_save, sender=Expense, dispatch_uid='record_expense_transaction_save')
def record_expense_save(sender, instance, created, using, **kwargs):
    action = 'created' if created else 'updated'
    _record_expense_transaction(instance, action, using)


@receiver(pre_delete, sender=Expense, dispatch_uid='record_expense_transaction_delete')
def record_expense_delete(sender, instance, using, **kwargs):
    _record_expense_transaction(instance, 'deleted', using)
