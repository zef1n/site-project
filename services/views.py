from django.utils import timezone

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
            order_details = []  # Список для хранения информации о каждом товаре

            # Сохраняем данные пользователя и заказа
            order = form.save(commit=False)

            # Собираем данные обо всех товарах в корзине
            for item in cart:
                order.service = item['service']
                order.save()

                order_details.append(
                    f"🛠 Услуга: {item['service'].title} | Количество: {item['quantity']} | Сумма: {item['total_price']} руб."
                )

            # Формируем итоговое сообщение для Telegram
            message = (
                    f"🛒 <b>Новый заказ</b>\n\n"
                    f"👤 Имя: {order.customer_name}\n"
                    f"📧 Email: {order.customer_email}\n"
                    f"📞 Телефон: {order.phone_number}\n"
                    f"💬 Предпочитаемая соцсеть: {order.get_preferred_network_display()}\n"
                    f"📅 Дата: {order.created_at.strftime('%Y-%m-%d %H:%M')}\n\n"
                    f"📜 Товары:\n" + "\n".join(order_details) + "\n\n"
                                                                f"📜 Дополнительно: {order.additional_info if order.additional_info else 'Нет'}"
            )

            send_telegram_message(message)  # Отправка сообщения в Telegram

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


from django.shortcuts import render, get_object_or_404
from .models import Post

from django.shortcuts import render, get_object_or_404
from .models import Post
from django.utils import timezone
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_list(request, tag_slug=None):
    object_list = Post.objects.filter(published_date__lte=timezone.now())
    tag = None
    query = request.GET.get('q')

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    if query:
        object_list = object_list.filter(content__icontains=query) | object_list.filter(title__icontains=query)

    paginator = Paginator(object_list, 6)  # 6 постов на страницу
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'post_list.html', {'posts': posts, 'tag': tag, 'query': query})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'post_detail.html', {'post': post})
