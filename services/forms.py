from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'phone_number', 'preferred_network', 'additional_info']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'input input-bordered w-full', 'placeholder': 'Ваше ФИО'}),
            'customer_email': forms.EmailInput(attrs={'class': 'input input-bordered w-full', 'placeholder': 'Ваш email'}),
            'phone_number': forms.TextInput(attrs={'class': 'input input-bordered w-full', 'placeholder': 'Ваш номер телефона'}),
            'preferred_network': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'additional_info': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'placeholder': 'Дополнительная информация'}),
        }

