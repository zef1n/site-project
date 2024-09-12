from decimal import Decimal
from django.conf import settings
from .models import Service

class Cart:
    def __init__(self, request):
        """
        Инициализация корзины.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, service, quantity=1, update_quantity=False):
        """
        Добавить услугу в корзину или обновить её количество.
        """
        service_id = str(service.id)
        if service_id not in self.cart:
            self.cart[service_id] = {
                'quantity': 0,
                'price': str(service.price)
            }
        if update_quantity:
            self.cart[service_id]['quantity'] = quantity
        else:
            self.cart[service_id]['quantity'] += quantity
        self.save()

    def save(self):
        """
        Обновить сессию корзины.
        """
        self.session.modified = True

    def remove(self, service):
        """
        Удалить услугу из корзины.
        """
        service_id = str(service.id)
        if service_id in self.cart:
            del self.cart[service_id]
            self.save()

    def __iter__(self):
        """
        Пройти по товарам в корзине и получить данные из базы.
        """
        service_ids = self.cart.keys()
        services = Service.objects.filter(id__in=service_ids)
        cart = self.cart.copy()

        for service in services:
            cart[str(service.id)]['service'] = service

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Получить общую стоимость товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Очистить корзину.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()
