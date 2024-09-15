from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Service, Order, Post


# Регистрация модели Service
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'duration', 'created_at', 'display_image')  # Отображаем изображение
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'duration')
    ordering = ('-created_at',)

    # Метод для отображения миниатюры изображения
    def display_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return "-"

    display_image.short_description = 'Изображение'


# Регистрация модели Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'service', 'created_at', 'paid')  # Отображаемые поля в списке заказов
    list_filter = ('paid', 'created_at')  # Фильтры по оплате и дате
    search_fields = ('customer_name', 'customer_email')  # Поля для поиска
    readonly_fields = ('created_at',)  # Поля, которые нельзя изменять
    actions = ['mark_as_paid']  # Дополнительные действия для заказов

    # Действие для отметки заказа как оплаченного
    @admin.action(description='Отметить выбранные заказы как оплаченные')
    def mark_as_paid(self, request, queryset):
        queryset.update(paid=True)


from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'author')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)
    # filter_horizontal = ('tags',)
