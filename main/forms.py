from django.forms import ModelForm
from main.models import Item

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ["name", "price", "description", "thumbnail", "category", "is_featured", "stock", "brand"]