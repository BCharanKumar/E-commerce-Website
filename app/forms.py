from app.models import *
from django import forms


class ProductSearchForm(forms.Form):
    search_query = forms.CharField(max_length=255, required=False, label='Search Products')

    def search(self):
        search_query = self.cleaned_data['search_query']
        if search_query:
            return Product.objects.filter(name__icontains=search_query)
        else:
            return Product.objects.all()

