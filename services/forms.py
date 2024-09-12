from django import forms
from .models import Order
from .models import Profile

from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'telegram_username', 'additional_info']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'input input-bordered w-full', 'placeholder': 'Ваше ФИО'}),
            'customer_email': forms.EmailInput(
                attrs={'class': 'input input-bordered w-full', 'placeholder': 'Ваш email'}),
            'telegram_username': forms.TextInput(
                attrs={'class': 'input input-bordered w-full', 'placeholder': 'Ваш ник в telegram (@nickname)'}),
            'additional_info': forms.Textarea(
                attrs={'class': 'textarea textarea-bordered w-full', 'placeholder': 'Дополнительная информация'}),
        }
