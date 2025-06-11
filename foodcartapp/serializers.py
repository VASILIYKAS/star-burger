import phonenumbers

from django.core.exceptions import ValidationError
from geodata.utils import get_or_create_location
from rest_framework import serializers

from .models import Order, OrderItem, Product


class PhoneNumberField(serializers.CharField):
    def to_internal_value(self, phonenumber):
        if phonenumber == '':
            raise ValidationError('phonenumber: Это поле не может быть пустым.')

        try:
            parsed = phonenumbers.parse(phonenumber, 'RU')
            if not phonenumbers.is_valid_number(parsed):
                raise ValidationError('phonenumber: Введен некорректный номер телефона.')
        except phonenumbers.NumberParseException:
            raise ValidationError('phonenumber: Неверный формат номера телефона.')
        return phonenumber


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    phonenumber = PhoneNumberField()
    products = OrderItemSerializer(many=True, source='items', allow_empty=False)

    class Meta:
        model = Order
        fields = ['id', 'firstname', 'lastname', 'phonenumber', 'address', 'products']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(
                order=order,
                product=item_data['product'],
                quantity=item_data['quantity'],
                price=item_data['product'].price
            )

        get_or_create_location(validated_data['address'])
        return order