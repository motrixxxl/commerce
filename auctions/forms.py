from django import forms
from django.utils.translation import ugettext

from .models import Currency, Category


class LotForm(forms.Form):
    currency_choices = []
    category_choices = []
    currencies = Currency.objects.all()
    for currency in currencies:
        currency_choices.append( (currency.id, currency.name) )

    categories = Category.objects.all()
    for category in categories:
        category_choices.append( (category.id, category.name) )

    title = forms.CharField(label='Lot Name', max_length=256)
    description = forms.CharField(widget=forms.Textarea)
    min_amount = forms.DecimalField(min_value=1, label='Starting price')
    currency = forms.ChoiceField(
        label='Currency',
        choices=currency_choices,
    )
    image = forms.CharField(max_length=256)
    category = forms.ChoiceField(
        label='Category',
        choices=category_choices,
    )
    state = forms.ChoiceField(
        label='State',
        choices=[ (0, 'inactive'), (1, 'active'), (2, 'closed') ],
    )

    field_order = ['title', 'category', 'image', 'description', 'min_amount', 'currency', 'state']

    labels = {
        'min_amount': 'Start Bid',
    }
