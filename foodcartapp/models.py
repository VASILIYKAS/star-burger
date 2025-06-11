from django.db import models
from django.db.models import F, Sum
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50,
        db_index=True,
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
        db_index=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50,
        db_index=True,
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class OrderQuerySet(models.QuerySet):
    def total_cost(self):
        return self.annotate(
            total_cost=Sum(F('items__quantity') * F('items__product__price'))
        )


class Order(models.Model):
    firstname = models.CharField('Имя', max_length=255, db_index=True,)
    lastname = models.CharField('Фамилия', max_length=255)
    phonenumber = PhoneNumberField('Телефон', region='RU', db_index=True,)
    address = models.CharField('адрес', max_length=255, db_index=True,)
    created_at = models.DateTimeField(
        'Дата создания заказа',
        default=timezone.now,
        db_index=True
    )
    assembly_started_at = models.DateTimeField(
        'Дата начала сборки',
        blank=True,
        null=True,
        db_index=True
    )
    delivery_started_at = models.DateTimeField(
        'Дата начала доставки',
        blank=True,
        null=True,
        db_index=True
    )
    completed_at = models.DateTimeField(
        'Дата завершения',
        blank=True,
        null=True,
        db_index=True
    )

    STATUS_CHOICES = [
        ('accepted', 'Принят'),
        ('assembly', 'Сборка'),
        ('delivery', 'Доставка'),
        ('completed', 'Выполнен'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='accepted',
        verbose_name='Статус заказа',
        db_index=True,
    )

    PAYMENT_METHODS = [
        ('cash', 'Наличными'),
        ('card', 'Картой онлайн'),
        ('card_courier', 'Картой курьеру'),
    ]

    payment_method = models.CharField(
        'Способ оплаты',
        max_length=20,
        choices=PAYMENT_METHODS,
        default='card',
        db_index=True
    )

    comment = models.TextField('Комантарий', blank=True, null=True)

    restaurant = models.ForeignKey(
        Restaurant,
        verbose_name='Ресторан',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='orders'
    )

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.firstname} {self.lastname}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        verbose_name='Заказ',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        verbose_name='Товар',
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(
        'Количество',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )

    price = models.DecimalField(
        'цена',
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'элемент заказа'
        verbose_name_plural = 'элементы заказа'

    def __str__(self):
        return f'{self.product.name} - {self.quantity} шт.'