"""Stores the models used in the API."""

from django.db import models
from django.db.models import QuerySet


class MenuItem(models.Model):
    """Model for an item of a menu."""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    unit_price_p = models.PositiveIntegerField()
    vat_rate_percent = models.DecimalField(max_digits=5, decimal_places=2)


class Tab(models.Model):
    """Model for a tab."""

    class Status(models.TextChoices):
        """Statuses that a tab change have."""

        OPEN = "open", "Open"
        PAID = "paid", "Paid"

    id = models.AutoField(primary_key=True)
    table_number = models.PositiveIntegerField()
    covers = models.PositiveIntegerField()
    status = models.CharField(choices=Status.choices, default=Status.OPEN)
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    subtotal_p = models.PositiveIntegerField(default=0)
    service_charge_p = models.PositiveIntegerField(default=0)
    vat_total_p = models.PositiveIntegerField(default=0)
    total_p = models.PositiveIntegerField(default=0)

    def recalculate_totals(self) -> None:
        """Recalculate the totals of the tab."""
        self.items: QuerySet[TabItem]
        subtotal = sum(item.unit_price_p * item.qty for item in self.items.all())
        vat_total = sum(item.vat_p for item in self.items.all())
        self.subtotal_p = subtotal
        self.vat_total_p = vat_total
        self.service_charge_p = round(subtotal * 0.10)
        self.total_p = subtotal + vat_total + self.service_charge_p
        self.save()


class TabItem(models.Model):
    """Model for an item of a tab."""

    id = models.AutoField(primary_key=True)
    tab = models.ForeignKey(Tab, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    unit_price_p = models.PositiveIntegerField()
    vat_rate_percent = models.DecimalField(max_digits=5, decimal_places=2)
    vat_p = models.PositiveIntegerField()
    line_total_p = models.PositiveIntegerField()

    def save(self, *args, **kwargs) -> None:
        """Update pricing and totals of the tab item then save."""
        self.unit_price_p = self.menu_item.unit_price_p
        self.vat_rate_percent = self.menu_item.vat_rate_percent

        self.line_total_p = self.unit_price_p * self.qty

        self.vat_p = round(self.line_total_p * float(self.vat_rate_percent) / 100)

        super().save(*args, **kwargs)


class Payment(models.Model):
    """Model for a payment of a tab."""

    class Status(models.TextChoices):
        """Statuses that a payment can have."""

        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    id = models.AutoField(primary_key=True)
    tab = models.ForeignKey(Tab, on_delete=models.CASCADE, related_name="payments")
    client_secret = models.UUIDField()
    payment_intent_id = models.UUIDField()
    amount_p = models.PositiveIntegerField()
    status = models.CharField(choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
