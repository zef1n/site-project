from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


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


class Order(models.Model):
    SOCIAL_NETWORK_CHOICES = [
        ('telegram', 'Telegram'),
        ('whatsapp', 'WhatsApp'),
        ('viber', 'Viber'),
        ('vk', 'ВКонтакте'),
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('other', 'Другое'),
    ]

    customer_name = models.CharField(max_length=255)  # Имя клиента
    customer_email = models.EmailField()  # Email клиента
    phone_number = models.CharField(max_length=20)  # Номер телефона
    preferred_network = models.CharField(max_length=20, choices=SOCIAL_NETWORK_CHOICES, default='telegram')  # Соцсеть
    additional_info = models.TextField(null=True, blank=True)  # Дополнительная информация от клиента
    service = models.ForeignKey('Service', on_delete=models.CASCADE)  # Выбранная услуга
    created_at = models.DateTimeField(default=timezone.now)  # Дата заказа
    paid = models.BooleanField(default=False)  # Статус оплаты

    def __str__(self):
        return f"Order by {self.customer_name} for {self.service.title}"


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    published_date = models.DateTimeField(default=timezone.now)
    tags = TaggableManager()  # Добавили теги
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = HTMLField()

    class Meta:
        ordering = ('-published_date',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('services:post_detail', args=[self.slug])


from django.urls import reverse


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post_list_by_tag', args=[self.slug])
