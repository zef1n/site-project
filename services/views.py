from .forms import OrderForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Service
from .cart import Cart
import asyncio

import requests


# Главная страница
def index(request):
    return render(request, 'index.html')


def catalog(request):
    services = Service.objects.all()  # Получаем все услуги из базы данных
    return render(request, 'catalog.html', {'services': services})


def cart_add(request, service_id):
    cart = Cart(request)
    service = get_object_or_404(Service, id=service_id)
    cart.add(service=service)
    return redirect('services:cart_detail')


def cart_remove(request, service_id):
    cart = Cart(request)
    service = get_object_or_404(Service, id=service_id)
    cart.remove(service)
    return redirect('services:cart_detail')


def cart_detail(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Обработка каждого товара в корзине
            for item in cart:
                order = form.save(commit=False)
                order.service = item['service']  # Привязываем услугу из корзины к заказу
                order.save()

                # Формирование сообщения для Telegram
                message = f"🛒 <b>Новый заказ</b>\n\n" \
                          f"👤 Имя: {order.customer_name}\n" \
                          f"📧 Email: {order.customer_email}\n" \
                          f"🔗 Telegram: @{order.telegram_username}\n" \
                          f"🛠 Услуга: {item['service'].title}\n" \
                          f"💰 Стоимость: {item['total_price']} руб.\n" \
                          f"📅 Дата: {order.created_at.strftime('%Y-%m-%d %H:%M')}\n\n" \
                          f"📜 Дополнительно: {order.additional_info}"

                # Отправка сообщения в Telegram
                send_telegram_message(message)

            cart.clear()  # Очищаем корзину после оформления заказа
            return redirect('services:order_success')
    else:
        form = OrderForm()

    return render(request, 'cart_detail.html', {'cart': cart, 'form': form})


# Функция для отправки сообщения модератору
def send_telegram_message(message: str):
    bot_token = '7442945233:AAFcqTkImSRADz5IoZdK9zurLbyATDGopP0'
    chat_id = '-4509762134'  # ID чата модератора

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Проверяем на наличие ошибок HTTP
        print("Сообщение успешно отправлено")
    except requests.exceptions.HTTPError as err:
        print(f"Ошибка HTTP: {err}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


# Вызов асинхронной функции
def send_telegram_message_sync(message: str):
    asyncio.run(send_telegram_message(message))
