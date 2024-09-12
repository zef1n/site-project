from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Модель для описания услуг
class Service(models.Model):
    title = models.CharField(max_length=255)  # Название услуги
    description = models.TextField()  # Описание услуги
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена услуги
    duration = models.CharField(max_length=100, null=True, blank=True)  # Продолжительность
    image = models.ImageField(upload_to='services/', null=True, blank=True)  # Изображение услуги (опционально)
    created_at = models.DateTimeField(default=timezone.now)  # Дата создания услуги

    def __str__(self):
        return self.title


# Модель для хранения заказов клиентов
from django.db import models
from django.contrib.auth.models import User



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                             blank=True)  # Связь с пользователем (если есть)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)  # Услуга, которую заказывают
    customer_name = models.CharField(max_length=255)  # Имя клиента
    customer_email = models.EmailField()  # Email клиента
    telegram_username = models.CharField(max_length=255, blank=True)  # Telegram ник клиента
    additional_info = models.TextField(blank=True)  # Дополнительная информация
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания заказа
    paid = models.BooleanField(default=False)  # Статус оплаты

    def __str__(self):
        return f"Order {self.id} by {self.customer_name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)  # Краткая информация о пользователе
    location = models.CharField(max_length=100, blank=True)  # Местоположение пользователя
    birth_date = models.DateField(null=True, blank=True)  # Дата рождения

    def __str__(self):
        return self.user.username


from django.db import models
from django.contrib.auth.models import User


class TelegramProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_id = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username
