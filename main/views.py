from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ItemForm
from main.models import Item

def show_main(request):
    item_list = Item.objects.all()
    context = {
        'app_name' : 'Strike Shop',
        'name': 'Angga Tri Setiawan',
        'class': 'PBP F',
        'item_list': item_list
    }

    return render(request, "main.html", context)

def create_item(request):
    form = ItemForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_item.html", context)

def show_item(request, id):
    item = get_object_or_404(Item, pk=id)
    item.increment_views()

    context = {
        'item': item
    }

    return render(request, "item_detail.html", context)

def show_xml(request):
    item_list = Item.objects.all()
    xml_data = serializers.serialize("xml", item_list)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    item_list = Item.objects.all()
    json_data = serializers.serialize("json", item_list)
    return HttpResponse(json_data, content_type="application/json")

def show_xml_by_id(request, item_id):
    try:
        item_list = Item.objects.filter(pk=item_id)
        xml_data = serializers.serialize("xml", item_list)
        return HttpResponse(xml_data, content_type="application/xml")
    except Item.DoesNotExist:
        return HttpResponse(status=404)

def show_json_by_id(request, item_id):
    try:
        item_list = Item.objects.get(pk=item_id)
        json_data = serializers.serialize("json", [item_list])
        return HttpResponse(json_data, content_type="application/json")
    except Item.DoesNotExist:
        return HttpResponse(status=404)

