from django import forms
from .models import Order
from .models import Profile


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'telegram_username', 'additional_info']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ваш email'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
            'additional_info': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Дополнительная информация'}),
        }
