from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['last_name', 'first_name', 'surname',
            'iin', 'address', 'place_work', 'telephone_number', 'profession']