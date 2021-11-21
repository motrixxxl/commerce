from django import forms


class LotForm(forms.Form):
    title = forms.CharField(label='Lot Name', max_length=100)
