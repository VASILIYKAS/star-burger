import phonenumbers

from rest_framework.decorators import api_view
from rest_framework.serializers import ValidationError
from rest_framework import serializers
from rest_framework.response import Response

from django.http import JsonResponse
from django.templatetags.static import static
from django.db import transaction

from geodata.utils import get_or_create_location
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
    products = OrderItemSerializer(many=True, source='items')

    class Meta:
        model = Order
        fields = ['id', 'firstname', 'lastname', 'phonenumber', 'address', 'products']

    def validate(self, data):
        if not data.get('items'):
            raise serializers.ValidationError({'products': 'Этот список не может быть пустым.'})
        return data


@api_view(['POST'])
@transaction.atomic
def register_order(request):
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    address = serializer.validated_data['address']

    try:
        order = Order.objects.create(
            firstname=serializer.validated_data['firstname'],
            lastname=serializer.validated_data['lastname'],
            phonenumber=serializer.validated_data['phonenumber'],
            address=serializer.validated_data['address'],
        )

        for item in serializer.validated_data['items']:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )

        get_or_create_location(address)
    except Exception as error:
        return Response({'error': str(error)}, status=400)

    output_serializer = OrderSerializer(order)
    return Response(output_serializer.data, status=201)