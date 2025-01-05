
from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl import fields
from .models import Product

class ProductDocument(Document):
    name = fields.TextField()
    description = fields.TextField()
    price = fields.FloatField()

    class Index:
        name = 'my_index'

    class Django:
        model = Product

