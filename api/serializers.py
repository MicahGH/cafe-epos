"""Stores the serializers for the models used in the API."""

from rest_framework import serializers

from api.models import MenuItem, Payment, Tab, TabItem


class MenuItemRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for retrieving the data of an existing menu item."""

    class Meta:
        """Metadata."""

        model = MenuItem
        fields = "__all__"


class TabItemCreateSerializer(serializers.ModelSerializer):
    """Serializer for adding a new tab item to a tab."""

    class Meta:
        """Metadata."""

        model = TabItem
        fields = ["menu_item", "qty"]


class TabItemRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for retrieving the data of an existing tab item."""

    name = serializers.CharField(source="menu_item.name", read_only=True)

    class Meta:
        """Metadata."""

        model = TabItem
        fields = [
            "name",
            "qty",
            "unit_price_p",
            "vat_rate_percent",
            "vat_p",
            "line_total_p",
        ]


class TabCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new tab."""

    class Meta:
        """Metadata."""

        model = Tab
        fields = ["table_number", "covers"]


class TabRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for retrieving the data of an existing tab."""

    items = TabItemRetrieveSerializer(many=True, read_only=True)

    class Meta:
        """Metadata."""

        model = Tab
        fields = [
            "id",
            "table_number",
            "covers",
            "status",
            "items",
            "subtotal_p",
            "service_charge_p",
            "vat_total_p",
            "total_p",
        ]


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for the payment."""

    class Meta:
        """Metadata."""

        model = Payment
        fields = [
            "id",
            "payment_intent_id",
            "client_secret",
            "status",
            "amount_p",
            "created_at",
        ]
        read_only_fields = fields
