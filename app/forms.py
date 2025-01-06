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



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'complete']
        widgets = {
            'complete': forms.CheckboxInput(attrs={'style': 'width: 15px; height: 15px;'})
        }

