from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView
from astro_site import settings
from services.views import index, catalog, cart_detail, cart_add, cart_remove

app_name = 'services'

urlpatterns = [
    path('', index, name='index'),  # Главная страница
    path('catalog/', catalog, name='catalog'),  # Каталог услуг
    path('cart/', cart_detail, name='cart_detail'),  # Страница корзины
    path('cart/add/<int:service_id>/', cart_add, name='cart_add'),  # Добавление товара в корзину
    path('cart/remove/<int:service_id>/', cart_remove, name='cart_remove'),  # Удаление товара из корзины
    path('order_success/', TemplateView.as_view(template_name='order_success.html'), name='order_success'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
