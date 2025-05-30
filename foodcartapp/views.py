import phonenumbers

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError
from rest_framework.serializers import Serializer
from rest_framework.serializers import CharField
from rest_framework import serializers

from django.http import JsonResponse
from django.templatetags.static import static

from .models import Product
from .models import Order, OrderItem, Product


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


class PhoneNumberField(serializers.CharField):
    def to_internal_value(self, data):
        if data == "":
            raise ValidationError("phonenumber: Это поле не может быть пустым.")

        try:
            parsed = phonenumbers.parse(data, "RU")
            if not phonenumbers.is_valid_number(parsed):
                raise ValidationError("phonenumber: Введен некорректный номер телефона.")
        except phonenumbers.NumberParseException:
            raise ValidationError("phonenumber: Неверный формат номера телефона.")


class ProductItemSerializer(serializers.Serializer):
    product = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)

    def validate_product(self, value):
        if not Product.objects.filter(id=value).exists():
            raise ValidationError(f'Недопустимый первичный ключ продукта "{value}"')


class ApplicationSerializer(Serializer):
    firstname = CharField()
    lastname = CharField()
    phonenumber = PhoneNumberField()
    address = CharField()
    products = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField(min_value=1)
        ),
        allow_empty=False
    )

    def validate_products(self, order):
        for item in order:
            serializer = ProductItemSerializer(data=item)
            serializer.is_valid(raise_exception=True)


def validate(order):
    serializer = ApplicationSerializer(data=order)
    serializer.is_valid(raise_exception=True)


@api_view(['POST'])
def register_order(request):
    order = request.data
    validate(order)

    create_order = Order.objects.create(
        first_name=order['firstname'],
        last_name=order.get('lastname', ''),
        phone_number=order['phonenumber'],
        address=order['address'],
    )

    for item in order['products']:
        product = Product.objects.get(pk=item['product'])
        OrderItem.objects.create(
            order=create_order,
            product=product,
            quantity=item['quantity']
        )
    return JsonResponse({})