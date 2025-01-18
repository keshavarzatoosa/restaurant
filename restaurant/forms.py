from django import forms
from .models import Menu, Branch, Order


class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['branch'].queryset = Branch.active.all()


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['branch'].queryset = Branch.active.all()